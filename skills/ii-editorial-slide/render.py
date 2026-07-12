#!/usr/bin/env python3
"""II Editorial Slide renderer — HTML → PNG @2x via Playwright."""
from __future__ import annotations
import argparse
import http.server
import socketserver
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright


def serve_static(directory: str, port: int):
    """Запускаем http-сервер на статике в фоне."""
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=directory, **kw)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def render(html_path: Path, out_path: Path | None = None, port: int = 8766, scale: int = 2):
    html_path = html_path.resolve()
    if out_path is None:
        out_path = html_path.with_suffix(".png")
    out_path = out_path.resolve()

    # Корнем поднимаем родителя posts/, чтобы относительные пути типа ../assets/ работали
    root = html_path.parent.parent if html_path.parent.name == "posts" else html_path.parent
    rel = html_path.relative_to(root)
    httpd = serve_static(str(root), port)
    try:
        url = f"http://127.0.0.1:{port}/{rel.as_posix()}"
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=scale)
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2500)
            box = page.evaluate(
                "() => { const s = document.querySelector('.slide'); const r = s.getBoundingClientRect(); return {x:r.x, y:r.y, width:r.width, height:r.height}; }"
            )
            page.screenshot(path=str(out_path), full_page=False, clip=box)
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    return out_path


def main():
    ap = argparse.ArgumentParser(description="II Editorial Slide renderer")
    ap.add_argument("html", help="Путь к HTML-файлу слайда")
    ap.add_argument("--output", "-o", help="Путь PNG-выхода (по умолчанию рядом с HTML)")
    ap.add_argument("--port", type=int, default=8766)
    ap.add_argument("--scale", type=int, default=2)
    args = ap.parse_args()
    out = render(Path(args.html), Path(args.output) if args.output else None, args.port, args.scale)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
