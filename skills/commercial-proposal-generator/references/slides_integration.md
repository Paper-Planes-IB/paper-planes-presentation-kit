# Интеграция с PPTX-генератором и Gamma App

## PPTX: маппинг секций КП → slide types

При генерации PPTX использовать consulting-slides-creator (src/generator.py).

### Аналитические layout'ы
- `scqa` — контекст (SCQA)
- `chart` — данные с графиками
- `numbered_list` — цели / рекомендации
- `chevron_process` — подход / методология
- `from_to` — результаты (AS IS → TO BE)
- `flow_blocks` — процессные схемы
- `comparison` — сценарии

### Структурные layout'ы
- `title_dark` — титульный слайд
- `table_sidebar` — детали этапов (контент + метрики)
- `roadmap_swimlane` — overview этапов
- `stage_gate` — вертикальные фазы проекта
- `goals_rows` — цели / KPI
- `next_steps` — следующие шаги
- `exec_summary` — executive summary
- `do_dont` — границы ответственности
- `segment_matrix` — риски / допущения
- `process_detail` — детальные процессы
- `mechanism_card` — примеры артефактов
- ~~`divider`~~ — ЗАПРЕЩЕН

## JSON-конфигурация слайда

```json
{
  "type": "<slide_type>",
  "title": "Action Title — вывод в 3-5 слов",
  "subtitle": "Контекстная строка (опционально)",
  "sources": "Источник данных",
  "takeaway": "Ключевой инсайт (опционально)"
}
```

### Правила для titles
- Action title = вывод/заключение в 3-5 слов, а не название темы
- Тест Маккинзи: при чтении только заголовков подряд — связная история
- Без стоп-листа
- На русском языке

### Правила структуры (SOSTAC)
КП следует логике SOSTAC: Situation → Objectives → Strategy → Tactics → Action → Control.
Каждый слайд — SCQA: S=факты, C=почему важно (самый важный элемент), Q=инструментарий, A=action title.

**Storyboard обязателен:** перед генерацией PPTX согласовать с пользователем последовательность слайдов и action titles. Без storyboard генерация запрещена.

---

## Gamma App (опционально)

### Когда использовать
Перед каждым КП уточнять у пользователя: нужен ли вывод в Gamma App (помимо PPTX).

### Темы
- `5q01qcw7y3qkipj` — **PP** (дефолт для КП)
- `3diyqvfnznzfqny` — LeanCore Black
- `tvxxd8j2z6s6qtg` — LeanCore Blue
- `zq8hoyxygc5bve6` — LeanCore White

### Gamma API v1.0
**Endpoint:** `POST https://public-api.gamma.app/v1.0/generations`
**Auth:** `X-API-KEY: sk-gamma-xxxxxxxxxx` (файл `~/.gamma_api_key`)

Ключевые параметры:
- `inputText` — markdown (до 100K токенов)
- `textMode` — `"preserve"` / `"condense"` / `"generate"`
- `format` — `"presentation"`
- `numCards` — 1-60 (Pro) / 1-75 (Ultra)
- `cardSplit` — `"inputTextBreaks"` (разбивка по `---`)
- `exportAs` — `"pdf"` или `"pptx"`
- `themeId` — ID темы
- `textOptions.language` — `"ru"`

**Кредиты:** ~3-4 за карточку + 2-20 за изображение.

### Скрипт: gamma_export.py

```bash
# Список тем
python gamma_export.py --list-themes

# Генерация
python gamma_export.py --file kp_content.md --title "КП для «Клиент»"

# С экспортом
python gamma_export.py --file kp_content.md --title "КП" --export pptx --theme abc123
```

```python
from gamma_export import create_gamma_presentation
result = create_gamma_presentation(
    content=kp_markdown,
    title="КП для «Клиент»",
    theme_id="abc123",
    export_as="pptx",
    num_cards=12,
)
print(result["gammaUrl"])
```

### Подготовка контента для Gamma
1. Каждая секция КП = один card (разделять через `---`)
2. Заголовки секций = `## Заголовок`
3. textMode = `"preserve"`
4. additionalInstructions: «Corporate consulting style. Minimal text. Data-driven visuals. No stock photos. Use icons and diagrams. Russian language for all text.»

### Настройка API-ключа
```bash
echo "sk-gamma-YOUR_KEY" > ~/.gamma_api_key
# или: export GAMMA_API_KEY="sk-gamma-YOUR_KEY"
# Ключ: https://gamma.app/settings/developer (Pro+ подписка)
```
