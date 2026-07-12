#!/usr/bin/env python3
"""
II Channel Cover Generator — PP.MEDIA / Paper Planes.

Генератор обложек для канала И_И_. Палитра — Балахнин (paper / ink / red / muted),
типографика — серифный Playfair Display + Inter Tight + JetBrains Mono.

CLI:
    python3 build.py \\
      --title "И_И_." \\
      --slogans "и <r>ИИ</r>, и человек" "и скорость, и качество" "и технологии, и риск" \\
      --format tg \\
      --diagram on \\
      --output cover.png
"""

from __future__ import annotations

import argparse
import os
import random
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ============================================================================
# КОНСТАНТЫ
# ============================================================================

# Палитра канала И_И_ (HEX → RGB)
M_PAPER = (239, 235, 231)   # #EFEBE7 — фон
M_RED = (214, 34, 25)       # #D62219 — акцент
M_MUTED = (184, 179, 173)   # #B8B3AD — линии, тонкие обводки
M_INK = (26, 23, 20)        # #1A1714 — основной текст
M_PAPER_DIM = (231, 226, 220)  # вторичный фон

# Размеры под форматы
FORMATS = {
    "tg": (1280, 720),
    "ig_portrait": (1080, 1350),
    "ig_square": (1080, 1080),
}

# Шрифты — пути с fallback
SKILL_DIR = Path(__file__).parent
USER_FONTS = Path.home() / "Library" / "Fonts"
LOCAL_FONTS = SKILL_DIR / "fonts"

FONT_CANDIDATES = {
    "display": [
        USER_FONTS / "Unbounded.ttf",
    ],
    "sans": [
        USER_FONTS / "InterTight.ttf",
        USER_FONTS / "Inter-VariableFont_opsz,wght.ttf",
    ],
    "mono": [
        USER_FONTS / "JetBrainsMono.ttf",
    ],
}


def resolve_font(role: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    """Подбираем шрифт по роли с fallback. Variable fonts — задаём axes если можно."""
    for candidate in FONT_CANDIDATES[role]:
        if candidate.exists():
            try:
                font = ImageFont.truetype(str(candidate), size)
                if weight is not None:
                    try:
                        # Для variable fonts
                        font.set_variation_by_axes([weight])
                    except Exception:
                        pass
                return font
            except Exception:
                continue
    # последний резерв — дефолтный bitmap-шрифт PIL
    return ImageFont.load_default()


# ============================================================================
# ПАРСИНГ СЛОГАНОВ
# ============================================================================

# инлайн-маркер <r>текст</r> для красного акцента
RED_TAG = re.compile(r"<r>(.+?)</r>")


def parse_slogan(text: str) -> list[tuple[str, tuple[int, int, int]]]:
    """Разбиваем слоган на (фрагмент, цвет). <r>X</r> = M_RED."""
    chunks = []
    pos = 0
    for m in RED_TAG.finditer(text):
        if m.start() > pos:
            chunks.append((text[pos:m.start()], M_INK))
        chunks.append((m.group(1), M_RED))
        pos = m.end()
    if pos < len(text):
        chunks.append((text[pos:], M_INK))
    return chunks


# ============================================================================
# ЭЛЕМЕНТЫ КОМПОЗИЦИИ
# ============================================================================

def draw_paper_noise(img: Image.Image, intensity: float = 0.04) -> None:
    """Лёгкое бумажное зерно — пиксельный шум поверх paper-фона."""
    if intensity <= 0:
        return
    w, h = img.size
    # просто рисуем редкие тёмные точки
    px = img.load()
    rng = random.Random(42)
    for _ in range(int(w * h * intensity * 0.05)):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        r, g, b = px[x, y][:3]
        d = rng.randint(0, 6)
        px[x, y] = (max(0, r - d), max(0, g - d), max(0, b - d))


def draw_blueprint_circles(
    draw: ImageDraw.ImageDraw,
    canvas_size: tuple[int, int],
    seed: int = 7,
) -> None:
    """Несколько лёгких пунктирных окружностей — blueprint-подложка."""
    w, h = canvas_size
    rng = random.Random(seed)
    # центр чуть выше середины
    cx, cy = w // 2, int(h * 0.42)
    # три окружности разных радиусов
    radii = [int(min(w, h) * f) for f in (0.32, 0.42, 0.52)]
    for r in radii:
        draw_dashed_circle(draw, (cx, cy), r, color=M_MUTED, width=1, dash=(6, 8))
    # пара мелких крестиков-перекрестий
    for _ in range(5):
        x = rng.randint(int(w * 0.1), int(w * 0.9))
        y = rng.randint(int(h * 0.1), int(h * 0.9))
        s = 6
        draw.line([(x - s, y), (x + s, y)], fill=M_MUTED, width=1)
        draw.line([(x, y - s), (x, y + s)], fill=M_MUTED, width=1)


def draw_dashed_circle(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    radius: int,
    color: tuple[int, int, int],
    width: int = 1,
    dash: tuple[int, int] = (6, 6),
) -> None:
    """Пунктирная окружность через дугу-сегменты."""
    import math

    cx, cy = center
    bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
    circumference = 2 * math.pi * radius
    if circumference <= 0:
        return
    dash_on, dash_off = dash
    step = dash_on + dash_off
    n = max(1, int(circumference / step))
    deg_per_dash = 360 / n
    on_fraction = dash_on / step
    for i in range(n):
        start = i * deg_per_dash
        end = start + deg_per_dash * on_fraction
        draw.arc(bbox, start, end, fill=color, width=width)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int] = M_RED,
    width: int = 2,
    head: int = 22,
) -> None:
    """Тонкая стрелка с маленьким наконечником."""
    import math

    draw.line([start, end], fill=color, width=width)
    # наконечник
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    a1 = angle + math.radians(155)
    a2 = angle - math.radians(155)
    p1 = (end[0] + head * math.cos(a1), end[1] + head * math.sin(a1))
    p2 = (end[0] + head * math.cos(a2), end[1] + head * math.sin(a2))
    draw.polygon([end, p1, p2], fill=color)


def draw_paperplane_icon(
    draw: ImageDraw.ImageDraw,
    anchor: tuple[int, int],
    size: int = 28,
    color: tuple[int, int, int] = M_RED,
) -> None:
    """Иконка бумажного самолётика — простая контурная фигура."""
    x, y = anchor
    s = size
    # треугольная форма с диагональной линией внутри
    pts = [(x, y + s // 2), (x + s, y), (x + int(s * 0.55), y + s // 2), (x + s, y + s)]
    draw.line(pts, fill=color, width=2, joint="curve")
    # внутренний штрих
    draw.line([(x + int(s * 0.55), y + s // 2), (x + int(s * 0.85), y + int(s * 0.25))], fill=color, width=2)


def draw_header(
    draw: ImageDraw.ImageDraw,
    canvas_size: tuple[int, int],
    mono_size: int = 16,
) -> None:
    """Шапка: PP.MEDIA. слева, PAPER PLANES + paperplane справа."""
    w, h = canvas_size
    margin = int(min(w, h) * 0.035)
    mono = resolve_font("mono", mono_size)
    # левая метка
    draw.text((margin, margin), "PP.MEDIA.", font=mono, fill=M_INK)
    # правая метка
    label = "PAPER PLANES"
    bbox = draw.textbbox((0, 0), label, font=mono)
    label_w = bbox[2] - bbox[0]
    plane_offset = 12
    plane_size = int(mono_size * 1.4)
    label_x = w - margin - label_w - plane_offset - plane_size
    draw.text((label_x, margin), label, font=mono, fill=M_INK)
    # paperplane справа от текста
    draw_paperplane_icon(
        draw,
        (label_x + label_w + plane_offset, margin - 2),
        size=plane_size,
        color=M_RED,
    )


def draw_red_block(
    img: Image.Image,
    position: str = "bottom_left",
    margin_factor: float = 0.06,
    size_factor: float = 0.09,
) -> None:
    """Квадратный красный блок-акцент."""
    w, h = img.size
    side = int(min(w, h) * size_factor)
    margin = int(min(w, h) * margin_factor)
    overlay = Image.new("RGBA", (side, side), M_RED + (255,))
    if position == "bottom_left":
        pos = (margin, h - margin - side)
    elif position == "top_left":
        pos = (margin, margin)
    elif position == "top_right":
        pos = (w - margin - side, margin)
    else:  # bottom_right
        pos = (w - margin - side, h - margin - side)
    img.paste(overlay, pos, overlay)


def _draw_title_wrapped(
    draw: ImageDraw.ImageDraw,
    canvas_size: Tuple[int, int],
    title: str,
) -> Tuple[int, int, int, int]:
    """Многословный заголовок-фраза: перенос по словам + подгонка под ширину.

    Левое выравнивание по полю PP.MEDIA. Playfair Display Black, M_INK.
    Используется для длинных тайтлов («Экспертные продажи 2.0»), где
    буквенно-подчёркивательный рендер «И_И_.» не подходит.
    """
    w, h = canvas_size
    margin = int(w * 0.045)
    maxw = w - margin - int(w * 0.10)  # правое поле под стрелку/диаграмму
    words = title.split()

    size = int(min(w, h) * 0.205)
    lines: List[str] = []
    line_h = 0
    total_h = 0
    while size > 46:
        font = resolve_font("display", size, weight=900)
        lines = []
        cur = ""
        for word in words:
            t = (cur + " " + word).strip()
            if draw.textlength(t, font=font) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        widest = max(draw.textlength(ln, font=font) for ln in lines)
        line_h = int(size * 1.04)
        total_h = line_h * len(lines)
        if widest <= maxw and total_h <= int(h * 0.5) and len(lines) <= 3:
            break
        size -= 4

    font = resolve_font("display", size, weight=900)
    top = int(h * 0.30) - total_h // 2
    y = top
    right = margin
    for ln in lines:
        draw.text((margin, y), ln, font=font, fill=M_INK)
        right = max(right, margin + int(draw.textlength(ln, font=font)))
        y += line_h
    return (margin, top, right, y)


def draw_title(
    draw: ImageDraw.ImageDraw,
    canvas_size: Tuple[int, int],
    title: str,
    size_factor: float = 0.34,
) -> Tuple[int, int, int, int]:
    """Главный заголовок Playfair Display Black.

    Парсит формат «И_И_.» как: буква + подчёркивание (рисуется линией) ...
    плюс финальная точка → красный квадрат.
    """
    w, h = canvas_size
    # многословная фраза → отдельный рендер с переносом
    if " " in title.strip():
        return _draw_title_wrapped(draw, canvas_size, title.strip())
    font_size = int(min(w, h) * size_factor)
    font = resolve_font("display", font_size, weight=900)

    # парсим title: убираем финальную точку, разбираем буквы и подчёркивания
    has_dot = title.endswith(".")
    body = title[:-1] if has_dot else title

    # разбиваем на пары (letter, underscore_count)
    parts: List[Tuple[str, int]] = []
    i = 0
    while i < len(body):
        if body[i] == "_":
            i += 1
            continue
        letter = body[i]
        i += 1
        underscores = 0
        while i < len(body) and body[i] == "_":
            underscores += 1
            i += 1
        parts.append((letter, underscores))

    # измеряем буквы и считаем общую ширину
    letter_widths: List[int] = []
    max_h = 0
    max_descent = 0  # глубина под базовой линией
    for letter, _ in parts:
        bb = draw.textbbox((0, 0), letter, font=font)
        letter_widths.append(bb[2] - bb[0])
        max_h = max(max_h, bb[3] - bb[1])

    # ширина подчёркивания = ширина буквы × 0.85
    gap_after_letter = int(font_size * 0.04)
    underscore_gap = int(font_size * 0.06)

    # total width
    total_w = 0
    for idx, (letter, n_under) in enumerate(parts):
        total_w += letter_widths[idx]
        if n_under > 0:
            total_w += gap_after_letter + int(letter_widths[idx] * 0.85) + (n_under - 1) * underscore_gap
        if idx < len(parts) - 1:
            total_w += int(font_size * 0.04)  # отступ между буквами

    # рисуем
    start_x = (w - total_w) // 2 - int(min(w, h) * 0.04)
    y = int(h * 0.32) - max_h // 2
    underscore_thickness = max(4, int(font_size * 0.05))
    underscore_y = y + max_h + int(font_size * 0.04)
    underscore_width = lambda lw: int(lw * 0.85)  # noqa: E731

    cx = start_x
    last_underscore_end_x = None
    for idx, (letter, n_under) in enumerate(parts):
        draw.text((cx, y), letter, font=font, fill=M_INK)
        letter_w = letter_widths[idx]
        cursor_after_letter = cx + letter_w
        # подчёркивания после буквы
        if n_under > 0:
            u_start_x = cursor_after_letter + gap_after_letter
            u_w = underscore_width(letter_w)
            for k in range(n_under):
                ux0 = u_start_x + k * (u_w + underscore_gap)
                draw.rectangle(
                    [ux0, underscore_y, ux0 + u_w, underscore_y + underscore_thickness],
                    fill=M_INK,
                )
                last_underscore_end_x = ux0 + u_w
            cursor_after_letter = u_start_x + n_under * u_w + (n_under - 1) * underscore_gap
        cx = cursor_after_letter + int(font_size * 0.04)

    # красный квадрат-точка справа от последнего подчёркивания
    if has_dot:
        dot_side = int(font_size * 0.085)
        dot_x = (last_underscore_end_x or cx) + int(font_size * 0.05)
        dot_y = underscore_y + underscore_thickness // 2 - dot_side // 2
        draw.rectangle(
            [dot_x, dot_y, dot_x + dot_side, dot_y + dot_side],
            fill=M_RED,
        )
        bbox_right = dot_x + dot_side
    else:
        bbox_right = (last_underscore_end_x or cx)

    return (start_x, y, bbox_right, underscore_y + underscore_thickness)


def draw_slogans(
    draw: ImageDraw.ImageDraw,
    canvas_size: Tuple[int, int],
    title_bbox: Tuple[int, int, int, int],
    slogans: List[str],
    size_factor: float = 0.038,
) -> None:
    """Подзаголовки под главным заголовком. Поддержка <r>X</r> для красного."""
    w, h = canvas_size
    font_size = int(min(w, h) * size_factor)
    font = resolve_font("sans", font_size, weight=500)
    # выравниваем слоганы по левому краю заголовка, со смещением правее
    x = title_bbox[0] + int(min(w, h) * 0.02)
    # отступ под заголовком — большой, чтобы не наезжать на хвосты букв и подчёркивания
    y = title_bbox[3] + int(h * 0.08)
    line_height = int(font_size * 1.4)
    for line in slogans:
        chunks = parse_slogan(line)
        cx = x
        for txt, color in chunks:
            draw.text((cx, y), txt, font=font, fill=color)
            bbox = draw.textbbox((0, 0), txt, font=font)
            cx += bbox[2] - bbox[0]
        y += line_height


def draw_diagram(
    draw: ImageDraw.ImageDraw,
    canvas_size: tuple[int, int],
    anchor: str = "bottom_right",
) -> None:
    """Блок-схема СИСТЕМА — ЛЮДИ — ДАННЫЕ — ИИ в углу."""
    w, h = canvas_size
    size = int(min(w, h) * 0.28)
    margin = int(min(w, h) * 0.05)
    if anchor == "bottom_right":
        x0 = w - margin - size
        y0 = h - margin - int(size * 0.55) - int(min(w, h) * 0.04)
    else:
        x0 = margin
        y0 = h - margin - int(size * 0.55)

    # рамка
    frame_w = size
    frame_h = int(size * 0.55)
    draw.rectangle([x0, y0, x0 + frame_w, y0 + frame_h], outline=M_INK, width=1)

    # ячейки СИСТЕМА (топ-лево) и ДАННЫЕ (низ-лево)
    cell_w = int(frame_w * 0.32)
    cell_h = int(frame_h * 0.32)
    pad = int(frame_h * 0.1)
    font_size = int(min(w, h) * 0.018)
    font = resolve_font("sans", font_size, weight=600)

    cell1 = (x0 + pad, y0 + pad, x0 + pad + cell_w, y0 + pad + cell_h)
    cell2 = (x0 + pad, y0 + pad + cell_h + pad, x0 + pad + cell_w, y0 + pad + 2 * cell_h + pad)
    draw.rectangle(cell1, outline=M_INK, width=1)
    draw.rectangle(cell2, outline=M_INK, width=1)
    _center_text(draw, cell1, "СИСТЕМА", font, M_INK)
    _center_text(draw, cell2, "ДАННЫЕ", font, M_INK)

    # ЛЮДИ — справа сверху без рамки или с тонкой рамкой
    cell3 = (x0 + pad + cell_w + pad, y0 + pad, x0 + pad + 2 * cell_w + pad, y0 + pad + cell_h)
    draw.rectangle(cell3, outline=M_INK, width=1)
    _center_text(draw, cell3, "ЛЮДИ", font, M_INK)

    # ИИ — красным справа снизу, без рамки
    ii_x = x0 + pad + 2 * cell_w + 2 * pad
    ii_y = y0 + pad + cell_h + pad + cell_h // 2 - font_size // 2
    draw.text((ii_x, ii_y), "ИИ", font=font, fill=M_RED)

    # соединительные линии (тонкие)
    # СИСТЕМА → ЛЮДИ
    draw.line([(cell1[2], (cell1[1] + cell1[3]) // 2), (cell3[0], (cell3[1] + cell3[3]) // 2)], fill=M_INK, width=1)
    # СИСТЕМА → ДАННЫЕ (вниз)
    draw.line([((cell1[0] + cell1[2]) // 2, cell1[3]), ((cell2[0] + cell2[2]) // 2, cell2[1])], fill=M_RED, width=1)
    # ЛЮДИ → ИИ
    draw.line([(cell3[2], (cell3[1] + cell3[3]) // 2), (ii_x - 4, (cell3[1] + cell3[3]) // 2)], fill=M_RED, width=1)
    # ДАННЫЕ → ИИ (через низ)
    draw.line([(cell2[2], (cell2[1] + cell2[3]) // 2), (ii_x - 4, (cell2[1] + cell2[3]) // 2)], fill=M_RED, width=1)

    # подпись «И_И_.» снизу
    cap_font = resolve_font("mono", int(font_size * 0.85))
    draw.text((x0, y0 + frame_h + 6), "И_И_.", font=cap_font, fill=M_INK)


def _center_text(
    draw: ImageDraw.ImageDraw,
    bbox: tuple[int, int, int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    color: tuple[int, int, int],
) -> None:
    tb = draw.textbbox((0, 0), text, font=font)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    cx = (bbox[0] + bbox[2]) // 2 - tw // 2
    cy = (bbox[1] + bbox[3]) // 2 - th // 2
    draw.text((cx, cy), text, font=font, fill=color)


def insert_photo_fragment(
    canvas: Image.Image,
    photo_path: str,
    crop_factor: float = 0.32,
    anchor: str = "bottom_left",
) -> None:
    """Вставка монохромного фрагмента архитектурной фотографии."""
    if not photo_path or not Path(photo_path).exists():
        return
    photo = Image.open(photo_path).convert("L")  # ч/б
    w, h = canvas.size
    side = int(min(w, h) * crop_factor)
    photo.thumbnail((side, side), Image.LANCZOS)
    pw, ph = photo.size
    photo_rgb = Image.merge("RGB", [photo] * 3)
    margin = int(min(w, h) * 0.0)
    if anchor == "bottom_left":
        pos = (margin, h - margin - ph)
    elif anchor == "bottom_right":
        pos = (w - margin - pw, h - margin - ph)
    else:
        pos = (margin, margin)
    canvas.paste(photo_rgb, pos)


# ============================================================================
# ГЛАВНАЯ СБОРКА
# ============================================================================

def build_cover(
    title: str = "И_И_.",
    slogans: list[str] | None = None,
    fmt: str = "tg",
    diagram: bool = True,
    photo: str | None = None,
    arrow: bool = True,
    output: str = "cover.png",
    seed: int = 7,
    background: str | None = None,
    overlay: str = "none",  # none / light / dark / split
    overlay_alpha: int = 140,
) -> str:
    if fmt not in FORMATS:
        raise ValueError(f"Unknown format: {fmt}. Available: {list(FORMATS)}")
    if slogans is None:
        slogans = [
            "и <r>ИИ</r>, и человек",
            "и скорость, и качество",
            "и технологии, и риск",
        ]

    w, h = FORMATS[fmt]

    # фон: либо чистый paper, либо AI-картинка (cover-fit)
    if background and Path(background).exists():
        bg = Image.open(background).convert("RGB")
        # cover-fit с центрированием
        bg_ratio = bg.width / bg.height
        target_ratio = w / h
        if bg_ratio > target_ratio:
            new_w = int(bg.height * target_ratio)
            left = (bg.width - new_w) // 2
            bg = bg.crop((left, 0, left + new_w, bg.height))
        else:
            new_h = int(bg.width / target_ratio)
            top = (bg.height - new_h) // 2
            bg = bg.crop((0, top, bg.width, top + new_h))
        canvas = bg.resize((w, h), Image.LANCZOS)

        # overlay для читаемости текста
        if overlay == "light":
            ov = Image.new("RGBA", (w, h), M_PAPER + (overlay_alpha,))
            canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
        elif overlay == "dark":
            ov = Image.new("RGBA", (w, h), M_INK + (overlay_alpha,))
            canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
        elif overlay == "split":
            # светлый сверху (под типографику), без оверлея снизу
            ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ov_draw = ImageDraw.Draw(ov)
            ov_draw.rectangle([0, 0, w, h // 2], fill=M_PAPER + (overlay_alpha,))
            canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
    else:
        canvas = Image.new("RGB", (w, h), M_PAPER)

    draw = ImageDraw.Draw(canvas)

    # 1. blueprint-подложка только если нет AI-фона
    if not background:
        draw_blueprint_circles(draw, (w, h), seed=seed)

    # 2. фотовставка (опц.) — раньше блока, чтобы блок мог лечь поверх
    if photo:
        insert_photo_fragment(canvas, photo, crop_factor=0.32, anchor="bottom_left")
        draw = ImageDraw.Draw(canvas)

    # 3. красный блок-акцент — крупнее в нижнем левом углу
    draw_red_block(canvas, position="bottom_left", margin_factor=0.04, size_factor=0.13)
    draw = ImageDraw.Draw(canvas)

    # 4. красная диагональная стрелка — проходит выше заголовка, не пересекает основной текст
    if arrow:
        draw_arrow(
            draw,
            start=(int(w * 0.18), int(h * 0.50)),
            end=(int(w * 0.94), int(h * 0.16)),
            color=M_RED,
            width=2,
            head=18,
        )

    # 5. шапка PP.MEDIA. + PAPER PLANES
    draw_header(draw, (w, h), mono_size=max(14, int(min(w, h) * 0.022)))

    # 6. главный заголовок
    size_factor = {"tg": 0.26, "ig_portrait": 0.30, "ig_square": 0.30}.get(fmt, 0.26)
    title_bbox = draw_title(draw, (w, h), title, size_factor=size_factor)

    # 7. слоганы
    draw_slogans(draw, (w, h), title_bbox, slogans, size_factor=0.034)

    # 8. диаграмма
    if diagram:
        draw_diagram(draw, (w, h), anchor="bottom_right")

    # 9. бумажное зерно
    draw_paper_noise(canvas, intensity=0.04)

    out_path = Path(output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "PNG", optimize=True)
    return str(out_path)


# ============================================================================
# CLI
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="II Channel Cover Generator (PP.MEDIA)")
    parser.add_argument("--title", default="И_И_.", help="Главный заголовок")
    parser.add_argument(
        "--slogans",
        nargs="*",
        default=None,
        help='Подзаголовки. Используй <r>X</r> для красного акцента',
    )
    parser.add_argument("--format", default="tg", choices=list(FORMATS.keys()))
    parser.add_argument("--diagram", default="on", choices=["on", "off"])
    parser.add_argument("--no-arrow", action="store_true")
    parser.add_argument("--photo", default=None)
    parser.add_argument("--output", default="cover.png")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--background", default=None, help="Путь к AI-фону (PNG/JPG)")
    parser.add_argument("--overlay", default="none", choices=["none", "light", "dark", "split"],
                        help="Полупрозрачный слой над AI-фоном для читаемости текста")
    parser.add_argument("--overlay-alpha", type=int, default=140, help="0-255")
    args = parser.parse_args()

    path = build_cover(
        title=args.title,
        slogans=args.slogans,
        fmt=args.format,
        diagram=(args.diagram == "on"),
        photo=args.photo,
        arrow=not args.no_arrow,
        output=args.output,
        seed=args.seed,
        background=args.background,
        overlay=args.overlay,
        overlay_alpha=args.overlay_alpha,
    )
    print(f"Cover saved: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
