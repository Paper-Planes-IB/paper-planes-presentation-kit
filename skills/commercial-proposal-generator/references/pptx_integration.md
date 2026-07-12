## 6. ИНТЕГРАЦИЯ С PPTX-ГЕНЕРАТОРОМ

### Маппинг секций → slide types

При генерации PPTX использовать consulting-slides-creator.
Для каждой секции подобрать оптимальный slide type:

**Аналитический генератор** (generate_slide.py):
- `scqa` — для контекста (SCQA)
- `chart` — для данных с графиками
- `numbered_list` — для целей / рекомендаций
- `chevron_process` — для подхода / методологии
- `from_to` — для результатов (AS IS → TO BE)
- `flow_blocks` — для процессных схем
- `comparison` — для сценариев

**Структурный генератор** (generator_structural.py):
- `title_dark` — титульный слайд
- ~~`divider`~~ — ⛔ ЗАПРЕЩЁН
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

### Генерация JSON-конфигов

Для каждого слайда формировать JSON по схеме consulting-slides-creator:
```json
{
  "type": "<slide_type>",
  "title": "Action Title — вывод в 3-5 слов (тест Маккинзи: только заголовки = история)",
  "subtitle": "Контекстная строка (опционально)",
  "sources": "Источник данных",
  "takeaway": "Ключевой инсайт (опционально)",
  ...type-specific fields
}
```

**Правила для titles:**
- Action title = вывод/заключение в **3-5 слов**, а не название темы
- Тест Маккинзи: при чтении только заголовков подряд — связная история
- Без стоп-листа
- На русском языке

**Правила структуры (SOSTAC):**
КП следует логике SOSTAC: Situation → Objectives → Strategy → Tactics → Action → Control.
Каждый слайд — SCQA: S=факты, C=почему важно (самый важный элемент), Q=инструментарий, A=action title.

**Storyboard обязателен:** перед генерацией PPTX согласовать с пользователем последовательность слайдов и action titles. Без storyboard генерация запрещена.

---

