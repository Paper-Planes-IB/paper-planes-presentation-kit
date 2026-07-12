## 7. GAMMA APP (опционально)

### 7.1. Когда использовать
Перед каждым КП уточнять у пользователя:
1. Нужен ли вывод в Gamma App (помимо PPTX)
2. Какая тема — по умолчанию используется **PP** (`5q01qcw7y3qkipj`) — кастомная тема Paper Planes
3. API-ключ уже настроен в `~/.gamma_api_key`

Доступные кастомные темы:
- `5q01qcw7y3qkipj` — **PP** (дефолт для КП)
- `3diyqvfnznzfqny` — LeanCore Black
- `tvxxd8j2z6s6qtg` — LeanCore Blue
- `zq8hoyxygc5bve6` — LeanCore White

### 7.2. Gamma API v1.0 (GA с 05.11.2025)

**Endpoint:** `POST https://public-api.gamma.app/v1.0/generations`
**Auth:** `X-API-KEY: sk-gamma-xxxxxxxxxx`
**Доступ:** Pro / Ultra / Teams / Business

Ключевые параметры:
- `inputText` — содержимое КП в markdown (до 100K токенов)
- `textMode` — `"preserve"` (сохранить структуру) / `"condense"` / `"generate"`
- `format` — `"presentation"` (по умолчанию)
- `numCards` — количество слайдов (1-60 для Pro, 1-75 для Ultra)
- `cardSplit` — `"inputTextBreaks"` (разбивка по `---` в тексте)
- `exportAs` — `"pdf"` или `"pptx"` (авто-экспорт)
- `themeId` — ID темы из `GET /v1.0/themes`
- `additionalInstructions` — доп. инструкции по стилю (до 2000 символов)
- `textOptions.language` — `"ru"` для русского

**Кредиты:** ~3-4 за карточку + 2-20 за изображение. Пример: 10 карт + 5 картинок ≈ 40-50 кредитов.

### 7.3. Скрипт интеграции

Файл: `gamma_export.py`

**CLI-использование:**
```bash
# Список тем
python gamma_export.py --list-themes
python gamma_export.py --list-themes --query "minimal"

# Генерация из файла
python gamma_export.py --file kp_content.md --title "КП для «Клиент»"

# С авто-экспортом в PPTX
python gamma_export.py --file kp_content.md --title "КП" --export pptx

# С конкретной темой
python gamma_export.py --file kp_content.md --title "КП" --theme abc123
```

**Программный вызов из Python:**
```python
from gamma_export import create_gamma_presentation

result = create_gamma_presentation(
    content=kp_markdown,
    title="КП для «Клиент»",
    theme_id="abc123",       # опционально
    export_as="pptx",        # опционально
    num_cards=12,             # опционально
    additional_instructions="Use dark corporate style, minimal text per card",
)
print(result["gammaUrl"])    # → https://gamma.app/docs/xxxxxxxx
print(result["credits"])     # → {"deducted": 45, "remaining": 2955}
```

### 7.4. Подготовка контента для Gamma

При генерации контента для Gamma (в дополнение к PPTX):
1. Каждая секция КП = один card (разделять через `---`)
2. Заголовки секций = `## Заголовок`
3. textMode = `"preserve"` — Gamma сохранит нашу структуру
4. Добавить `additionalInstructions`:
   - «Corporate consulting style. Minimal text. Data-driven visuals.»
   - «No stock photos. Use icons and diagrams.»
   - «Russian language for all text.»

### 7.5. Настройка API-ключа

```bash
# Вариант 1: файл (рекомендуется)
echo "sk-gamma-YOUR_KEY" > ~/.gamma_api_key

# Вариант 2: переменная окружения
export GAMMA_API_KEY="sk-gamma-YOUR_KEY"

# Получить ключ: https://gamma.app/settings/developer
# Требуется: подписка Pro ($10/мес) или выше
```

---

