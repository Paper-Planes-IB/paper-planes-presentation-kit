#!/usr/bin/env bash
# make_pdf.sh — HTML-методичка Paper Planes → печатный A4-PDF через Chrome headless.
#
# Использование:
#   bash make_pdf.sh "путь/к/methodika.html" "путь/к/methodika_печать.pdf"
#
# Зачем именно так:
#   --print-to-pdf-no-header / --no-pdf-header-footer  — убирают URL и дату по краям листа
#   --virtual-time-budget=8000                          — даёт Google Fonts (Oswald, Inter Tight,
#                                                          JetBrains Mono, Unbounded) догрузиться,
#                                                          иначе PDF рендерится дефолтным шрифтом.
#                                                          ТРЕБУЕТСЯ интернет при рендере.
#   --no-pdf-header-footer — новый флаг Chrome; старый --print-to-pdf-no-header оставлен для
#                            совместимости, лишним не будет.
#
# После генерации скрипт печатает число страниц (быстрый sanity-check «не 23 ли»).

set -euo pipefail

HTML="${1:?Укажи путь к HTML: make_pdf.sh input.html output.pdf}"
PDF="${2:?Укажи путь к выходному PDF: make_pdf.sh input.html output.pdf}"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ ! -x "$CHROME" ]]; then
  echo "✗ Chrome не найден по пути: $CHROME" >&2
  echo "  Поправь переменную CHROME в скрипте." >&2
  exit 1
fi

if [[ ! -f "$HTML" ]]; then
  echo "✗ HTML не найден: $HTML" >&2
  exit 1
fi

# Абсолютный путь для file:// (Chrome не любит относительные)
HTML_ABS="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"

echo "→ Рендерю $HTML_ABS"
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --hide-scrollbars \
  --print-to-pdf="$PDF" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  --virtual-time-budget=8000 \
  "file://$HTML_ABS" 2>/dev/null

if [[ ! -f "$PDF" ]]; then
  echo "✗ PDF не создан. Проверь, что Chrome закрыт другими headless-сессиями." >&2
  exit 1
fi

# Число страниц: пробуем mdls (macOS), потом pdfinfo, иначе грубо по /Type /Page
PAGES=""
if command -v mdls >/dev/null 2>&1; then
  PAGES="$(mdls -name kMDItemNumberOfPages -raw "$PDF" 2>/dev/null || true)"
fi
if [[ -z "$PAGES" || "$PAGES" == "(null)" ]] && command -v pdfinfo >/dev/null 2>&1; then
  PAGES="$(pdfinfo "$PDF" 2>/dev/null | awk '/^Pages:/ {print $2}')"
fi
# Последний резерв (работает и в /tmp, где Spotlight не индексирует): считаем /Type /Page
if [[ -z "$PAGES" || "$PAGES" == "(null)" ]]; then
  PAGES="$(grep -a -c '/Type[[:space:]]*/Page[^s]' "$PDF" 2>/dev/null || true)"
  [[ "$PAGES" == "0" ]] && PAGES=""
fi

SIZE="$(du -h "$PDF" | cut -f1)"
echo "✓ Готово: $PDF  ($SIZE${PAGES:+, ${PAGES} стр.})"
echo "  Проверка 1-й страницы:  sips -s format png \"$PDF\" --out /tmp/check.png"
