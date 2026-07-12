#!/usr/bin/env python3
"""
II Channel Carousel Generator — 9-слайдовая IG-карусель по словарю канала И_И_.

Шаблоны слайдов:
  cover    — обложка с большим заголовком и подзаголовком
  formula  — формула A × B × C × ...
  flow     — горизонтальный поток с иконками и стрелками
  listing  — вертикальный список терминов с подписями
  quote    — большой текст-цитата
  diagram  — структурная схема (упрощённая)
  finale   — финальный слайд с большим утверждением

Использование (как библиотека):
    from build_carousel import build_glossary_carousel
    build_glossary_carousel(output_dir="./out")

Размер слайда: 1080×1080.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Палитра и константы
# ---------------------------------------------------------------------------

M_PAPER = (248, 245, 237)
M_INK = (26, 23, 20)
M_RED = (232, 74, 56)
M_MUTED = (138, 133, 122)
M_LINE_LIGHT = (200, 195, 185)

CANVAS_SIZE = (1080, 1080)
SLIDE_NUM_BOX = (50, 1020, 110, 1040)

# Пути к шрифтам
HOME_FONTS = Path.home() / "Library" / "Fonts"
LOCAL_FONTS = Path(__file__).parent / "fonts"

FONT_PATHS = {
    "display": [
        LOCAL_FONTS / "PlayfairDisplay.ttf",
        HOME_FONTS / "PlayfairDisplay.ttf",
    ],
    "sans": [
        HOME_FONTS / "InterTight.ttf",
        HOME_FONTS / "Inter-VariableFont_opsz,wght.ttf",
    ],
    "mono": [
        HOME_FONTS / "JetBrainsMono.ttf",
    ],
}


def load_font(role: str, size: int, weight: int = 400) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS[role]:
        if path.exists():
            try:
                font = ImageFont.truetype(str(path), size)
                try:
                    font.set_variation_by_axes([weight])
                except Exception:
                    pass
                return font
            except Exception:
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Общие элементы слайдов
# ---------------------------------------------------------------------------


def header_label(draw: ImageDraw.ImageDraw, size: int = 28) -> None:
    """Лейбл «И_И_» в верхнем левом углу — общая шапка всех слайдов."""
    font = load_font("mono", size)
    draw.text((50, 45), "И_И_", font=font, fill=M_INK)


def slide_number(draw: ImageDraw.ImageDraw, n: int) -> None:
    """Маленький номер слайда в нижнем левом углу."""
    font = load_font("mono", 18)
    draw.text((50, 1020), f"{n:02d}", font=font, fill=M_MUTED)
    # тонкая линия слева от номера
    draw.line([(86, 1029), (140, 1029)], fill=M_MUTED, width=1)


def section_title(draw: ImageDraw.ImageDraw, text: str, y: int = 110) -> None:
    """Крупный моноширинный заголовок раздела — caps."""
    font = load_font("mono", 36)
    draw.text((50, y), text.upper(), font=font, fill=M_INK, spacing=2)
    # подчёркивание-ниточка
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    tw = bbox[2] - bbox[0]
    # маленький красный крест в правом верхнем для декора
    cx, cy = 1010, 70
    draw.line([(cx - 8, cy), (cx + 8, cy)], fill=M_RED, width=2)
    draw.line([(cx, cy - 8), (cx, cy + 8)], fill=M_RED, width=2)


def paper_noise(img: Image.Image) -> None:
    """Лёгкое бумажное зерно."""
    import random

    rng = random.Random(11)
    px = img.load()
    w, h = img.size
    for _ in range(int(w * h * 0.002)):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        r, g, b = px[x, y][:3]
        d = rng.randint(0, 5)
        px[x, y] = (max(0, r - d), max(0, g - d), max(0, b - d))


def new_canvas() -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", CANVAS_SIZE, M_PAPER)
    draw = ImageDraw.Draw(img)
    return img, draw


def finalize(img: Image.Image, n: int) -> Image.Image:
    draw = ImageDraw.Draw(img)
    header_label(draw)
    slide_number(draw, n)
    paper_noise(img)
    return img


# ---------------------------------------------------------------------------
# Шаблоны слайдов
# ---------------------------------------------------------------------------


def slide_cover(title_lines: List[str], description: str, n: int) -> Image.Image:
    """Обложка карусели — большой заголовок и описание."""
    img, draw = new_canvas()

    # большой заголовок Playfair (или display fallback)
    font_title = load_font("display", 130, weight=900)
    y = 200
    for line in title_lines:
        draw.text((50, y), line, font=font_title, fill=M_INK)
        bbox = draw.textbbox((0, 0), line, font=font_title)
        y += (bbox[3] - bbox[1]) + 15

    # описание
    font_body = load_font("sans", 28, weight=500)
    y += 30
    for line in description.split("\n"):
        draw.text((50, y), line, font=font_body, fill=M_INK)
        y += 38

    # декор: круг с диагональю (стрела)
    cx, cy, r = 800, 380, 220
    for ring_r in (r, r - 60, r - 120, r - 180):
        draw.ellipse(
            [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
            outline=M_LINE_LIGHT,
            width=1,
        )
    # центр-крест
    draw.line([(cx - 12, cy), (cx + 12, cy)], fill=M_RED, width=2)
    draw.line([(cx, cy - 12), (cx, cy + 12)], fill=M_RED, width=2)
    # стрелка через круг
    draw_arrow(draw, (cx + 200, cy + 200), (cx - 220, cy - 220), color=M_RED, width=3)

    return finalize(img, n)


def slide_formula(title: str, formula_parts: List[str], n: int) -> Image.Image:
    """Слайд с формулой: A × B × C."""
    img, draw = new_canvas()
    section_title(draw, title)

    # подпись формулы
    font_label = load_font("sans", 32, weight=500)
    draw.text((50, 380), "AI-ready — рабочая формула готовности:", font=font_label, fill=M_INK)

    # сами блоки формулы
    font_block = load_font("mono", 38)
    block_w = 220
    block_h = 90
    gap = 50
    total_w = len(formula_parts) * block_w + (len(formula_parts) - 1) * gap
    x = (CANVAS_SIZE[0] - total_w) // 2
    y = 500
    for i, part in enumerate(formula_parts):
        bx = x + i * (block_w + gap)
        draw.rectangle([bx, y, bx + block_w, y + block_h], outline=M_INK, width=2)
        # центрируем текст
        bb = draw.textbbox((0, 0), part.upper(), font=font_block)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        draw.text(
            (bx + (block_w - tw) // 2, y + (block_h - th) // 2 - 5),
            part.upper(),
            font=font_block,
            fill=M_INK,
        )
        # знак × между блоками
        if i < len(formula_parts) - 1:
            mult_x = bx + block_w + gap // 2
            mult_y = y + block_h // 2
            f_mult = load_font("display", 48, weight=900)
            mb = draw.textbbox((0, 0), "×", font=f_mult)
            mw = mb[2] - mb[0]
            mh = mb[3] - mb[1]
            draw.text(
                (mult_x - mw // 2, mult_y - mh // 2 - 5),
                "×",
                font=f_mult,
                fill=M_INK,
            )

    # маленький красный квадрат-точка снизу справа
    draw.rectangle([970, 700, 990, 720], fill=M_RED)

    return finalize(img, n)


def slide_flow(title: str, subtitle_lines: List[Tuple[str, List[str]]], n: int) -> Image.Image:
    """Слайд с горизонтальным потоком: 2 строки по 4 шага.
    subtitle_lines: [(подпись_сверху, [шаг1, шаг2, шаг3, шаг4]), ...]
    """
    img, draw = new_canvas()
    section_title(draw, title)

    font_label = load_font("sans", 26, weight=600)
    font_step = load_font("mono", 22)

    # дополнительный заголовок справа сверху — пунктирная вертикальная сетка точек
    for i in range(5):
        for j in range(5):
            draw.ellipse(
                [950 + i * 14, 100 + j * 14, 952 + i * 14, 102 + j * 14],
                fill=M_LINE_LIGHT,
            )

    y = 250
    for label, steps in subtitle_lines:
        # лейбл
        draw.text((50, y), label, font=font_label, fill=M_RED)
        y += 50
        # 4 кружка-шага с подписями
        step_count = len(steps)
        circle_d = 90
        gap = 80
        total_w = step_count * circle_d + (step_count - 1) * gap
        x_start = (CANVAS_SIZE[0] - total_w) // 2
        for i, step in enumerate(steps):
            cx = x_start + i * (circle_d + gap) + circle_d // 2
            cy = y + circle_d // 2
            draw.ellipse([cx - circle_d // 2, cy - circle_d // 2, cx + circle_d // 2, cy + circle_d // 2], outline=M_INK, width=2)
            # подпись под кружком
            bb = draw.textbbox((0, 0), step, font=font_step)
            tw = bb[2] - bb[0]
            draw.text((cx - tw // 2, cy + circle_d // 2 + 12), step, font=font_step, fill=M_INK)
            # стрелка между кружками
            if i < step_count - 1:
                arrow_start = (cx + circle_d // 2 + 5, cy)
                arrow_end = (cx + circle_d // 2 + gap - 5, cy)
                draw.line([arrow_start, arrow_end], fill=M_INK, width=1)
                # наконечник
                draw.polygon(
                    [
                        arrow_end,
                        (arrow_end[0] - 8, arrow_end[1] - 5),
                        (arrow_end[0] - 8, arrow_end[1] + 5),
                    ],
                    fill=M_INK,
                )
        y += circle_d + 100

    return finalize(img, n)


def slide_listing(title: str, items: List[Tuple[str, str]], n: int) -> Image.Image:
    """Список терминов с иконкой-плейсхолдером и подписью.
    items: [(термин, краткое описание из 2-3 строк)]
    Максимум 4-5 элементов на слайд.
    """
    img, draw = new_canvas()
    section_title(draw, title)

    font_term = load_font("mono", 22)
    font_desc = load_font("sans", 18, weight=400)

    y = 220
    icon_size = 60
    row_h = 140
    for term, desc in items:
        # иконка-плейсхолдер (квадрат с иконкой внутри)
        draw.rectangle([50, y, 50 + icon_size, y + icon_size], outline=M_INK, width=2)
        # схематическая иконка (буква-инициал)
        f_icon = load_font("mono", 26)
        ib = draw.textbbox((0, 0), term[0].upper(), font=f_icon)
        iw = ib[2] - ib[0]
        ih = ib[3] - ib[1]
        draw.text(
            (50 + (icon_size - iw) // 2, y + (icon_size - ih) // 2 - 3),
            term[0].upper(),
            font=f_icon,
            fill=M_INK,
        )
        # термин
        draw.text((130, y), term.upper(), font=font_term, fill=M_INK)
        # описание (многострочное)
        desc_lines = wrap_text(desc, font_desc, max_width=900)
        dy = y + 32
        for line in desc_lines[:3]:  # максимум 3 строки описания
            draw.text((130, dy), line, font=font_desc, fill=M_INK)
            dy += 24

        y += row_h

    return finalize(img, n)


def slide_quote(text_lines: List[str], n: int, accent_line: int = 0) -> Image.Image:
    """Финальный слайд с большой цитатой."""
    img, draw = new_canvas()
    font = load_font("display", 60, weight=700)

    y = 350
    for i, line in enumerate(text_lines):
        color = M_INK
        draw.text((50, y), line, font=font, fill=color)
        bb = draw.textbbox((0, 0), line, font=font)
        y += (bb[3] - bb[1]) + 20

    # декор — ступени или диагональ внизу справа
    draw_steps_decoration(draw, anchor=(700, 750))

    return finalize(img, n)


def slide_diagram(title: str, n: int) -> Image.Image:
    """Слайд со схемой потоков 'как всё связано'."""
    img, draw = new_canvas()
    section_title(draw, title)

    font_box = load_font("mono", 16)

    def box(label: str, x: int, y: int, w: int = 200, h: int = 60, color=M_INK):
        draw.rectangle([x, y, x + w, y + h], outline=color, width=2)
        bb = draw.textbbox((0, 0), label.upper(), font=font_box)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 3), label.upper(), font=font_box, fill=color)
        return (x, y, x + w, y + h)

    # центр — Vault (память системы)
    vault = box("Vault\n(память)", 440, 600, w=200, h=80, color=M_RED)

    # левая колонка
    sig = box("Входящий сигнал", 100, 250)
    tun = box("Туннелирование", 100, 360)
    home = box("Дом приземления", 100, 470)
    skill = box("Скилл / Рельса", 100, 580)

    # правая колонка
    art = box("Артефакт (do)", 800, 250)
    qa = box("Проверка (QA-агент)", 800, 360)
    ret = box("Возврат как сигнал", 800, 470)

    # стрелки сверху вниз слева
    def arrow_between(a, b, color=M_INK):
        x1 = (a[0] + a[2]) // 2
        y1 = a[3]
        x2 = (b[0] + b[2]) // 2
        y2 = b[1]
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
        draw.polygon(
            [(x2, y2), (x2 - 5, y2 - 8), (x2 + 5, y2 - 8)], fill=color
        )

    arrow_between(sig, tun)
    arrow_between(tun, home)
    arrow_between(home, skill)
    arrow_between(art, qa, color=M_RED)
    arrow_between(qa, ret, color=M_RED)

    # центральные стрелки в Vault и из Vault
    # skill → vault
    draw.line([(300, 640), (440, 640)], fill=M_INK, width=1)
    # vault → art
    draw.line([(640, 640), (800, 290)], fill=M_INK, width=1)
    # ret → vault (закрытие петли)
    draw.line([(900, 530), (540, 600)], fill=M_RED, width=1, joint="curve")

    return finalize(img, n)


# ---------------------------------------------------------------------------
# Утилиты
# ---------------------------------------------------------------------------


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    """Простой word wrap."""
    words = text.split()
    lines: List[str] = []
    current: List[str] = []
    for w in words:
        test = " ".join(current + [w])
        bb = font.getbbox(test)
        if bb[2] - bb[0] <= max_width:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_arrow(draw, start, end, color=M_RED, width=2, head=18):
    draw.line([start, end], fill=color, width=width)
    dx, dy = end[0] - start[0], end[1] - start[1]
    angle = math.atan2(dy, dx)
    a1 = angle + math.radians(155)
    a2 = angle - math.radians(155)
    p1 = (end[0] + head * math.cos(a1), end[1] + head * math.sin(a1))
    p2 = (end[0] + head * math.cos(a2), end[1] + head * math.sin(a2))
    draw.polygon([end, p1, p2], fill=color)


def draw_steps_decoration(draw, anchor):
    """Декор: схематические ступени снизу справа."""
    x, y = anchor
    for i in range(5):
        sw = 50
        sh = 30
        x0 = x + i * sw // 2
        y0 = y - i * sh
        draw.rectangle([x0, y0, x0 + sw, y0 + sh], outline=M_LINE_LIGHT, width=1)


# ---------------------------------------------------------------------------
# Сборка карусели по словарю
# ---------------------------------------------------------------------------


def build_glossary_carousel(output_dir: str = "./glossary_carousel") -> List[str]:
    out = Path(output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    paths: List[str] = []

    # Слайд 01 — обложка
    img = slide_cover(
        title_lines=["Словарь", "канала"],
        description=(
            "В канале будут постепенно\n"
            "набираться спец-термины.\n"
            "Часть слов я ввёл сам,\n"
            "часть забрал из внешних источников\n"
            "и закрепил у нас. Собираю полный\n"
            "список, чтобы после не возвращаться."
        ),
        n=1,
    )
    p = out / "01_cover.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 02 — концептуальная рамка (формула)
    img = slide_formula(
        title="Концептуальная рамка",
        formula_parts=["Эффект", "Готовность", "Внедряемость"],
        n=2,
    )
    p = out / "02_formula.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 03 — контуры системы (flow)
    img = slide_flow(
        title="Контуры системы",
        subtitle_lines=[
            ("ДУМАЙ — контур работы со знанием", ["collect", "organize", "review", "do"]),
            ("ДЕЛАЙ — контур работы с артефактом", ["plan", "do", "check", "act"]),
        ],
        n=3,
    )
    p = out / "03_flow.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 04 — объекты ИИ-системы
    img = slide_listing(
        title="Объекты ИИ-системы",
        items=[
            ("Vault", "хранилище md-файлов с wikilink-разметкой; у нас в связке Codex → Obsidian → Google Drive"),
            ("Плагин", "внешний коннектор к комбайну: Notion, Drive, MCP-интеграции"),
            ("Скилл", "исполняемый артефакт методологии с триггерами, шагами, проверками и выходами"),
            ("Рельса", "сквозной производственный маршрут с входом, шагами, набором скиллов и артефактами"),
            ("Проходчик", "автоматический крон-оператор, сканирует Vault по расписанию"),
        ],
        n=4,
    )
    p = out / "04_listing_objects.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 05 — операции и места
    img = slide_listing(
        title="Операции и места",
        items=[
            ("Туннелирование", "разнесение входящего сигнала по нескольким местам приземления, термин из BPMN"),
            ("Handoff", "передача задачи или контекста от одного исполнителя к другому, точка потери смысла"),
            ("Дом приземления", "конкретное место в Vault, куда сигнал относится по правилам разнесения"),
            ("Контрольная вышка", "образ управленческой роли собственника внутри собственной ИИ-системы"),
        ],
        n=5,
    )
    p = out / "05_listing_ops.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 06 — качество ИИ-внедрения
    img = slide_listing(
        title="Качество ИИ-внедрения",
        items=[
            ("HITL (Human in the Loop)", "человек как центр системы; владелец смысла, постановщик задачи, держатель решения"),
            ("Когнитивная стратегия", "алгоритм рассуждения, который человек способен интерпретировать и улучшить"),
            ("Скафолдинг", "поддерживающие леса вокруг сотрудника; полезны, опасны без когнитивной стратегии"),
        ],
        n=6,
    )
    p = out / "06_listing_quality.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 07 — о системе коротко
    img = slide_quote(
        text_lines=[
            "Цель — не рост.",
            "Цель — система,",
            "которая его создаёт.",
        ],
        n=7,
    )
    p = out / "07_quote_system.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 08 — как всё связано (diagram)
    img = slide_diagram(title="Как всё связано", n=8)
    p = out / "08_diagram.png"
    img.save(p)
    paths.append(str(p))

    # Слайд 09 — финал
    img = slide_quote(
        text_lines=[
            "Рост — не цель.",
            "Цель — система,",
            "которая его создаёт.",
        ],
        n=9,
    )
    p = out / "09_finale.png"
    img.save(p)
    paths.append(str(p))

    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="./glossary_carousel")
    parser.add_argument("--only", type=int, default=0, help="Сгенерировать только N-й слайд (1-9)")
    args = parser.parse_args()

    paths = build_glossary_carousel(output_dir=args.output)
    if args.only:
        print(paths[args.only - 1])
    else:
        for p in paths:
            print(p)
