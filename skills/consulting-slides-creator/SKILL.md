---
name: "consulting-slides"
description: "|"
---

# Consulting Slides Creator (Paper Planes)

Генерация консалтинговых слайдументов в PPTX. Единый генератор, 38 типов слайдов.

## Генератор

```bash
cd ~/.claude/skills/consulting-slides-creator && python3 -m src.generator \
  --config /path/to/config.json \
  --output /path/to/slide.pptx
```

Форматы входа: одиночный JSON `{"type": "scqa", ...}`, массив `[{...}, {...}]`, обёртка `{"slides": [...]}`, несколько файлов через CLI.

## Каталог типов

| Задача | Типы |
|--------|------|
| Графики, KPI | chart, data, waterfall |
| Стратегия | sankey, treemap, matrix, funnel, swot |
| SCQA | scqa |
| Процессы | chevron_process, flow_blocks, mermaid |
| Списки | numbered_list |
| Комбо | chart_table, multi_table, table_sidebar |
| RASCI | rasci |
| Roadmap | roadmap_swimlane |
| Stage-gate | stage_gate |
| Do/Don't | do_dont |
| Сегменты | segment_matrix |
| KPI-строки | goals_rows |
| Brand pyramid | brand_pyramid |
| Mechanism | mechanism_card |
| Титульный | title_dark |
| Executive summary | exec_summary |
| Next steps | next_steps |
| AS IS → TO BE | from_to |
| Сравнение | comparison |
| Issue tree | issue_tree |
| Цитата | quote |
| Пирамида Минто | pyramid |
| Процесс | process_detail |

> ⛔ `divider` ЗАПРЕЩЁН (обучение Балахнина 21.03.2026)

## Критические правила

### Плотность контента
Слайдументы ≠ презентации. Плотные аналитические документы, читаются без спикера.
- Таблицы: 15-30 строк, 4-8 буллетов в ячейке, шрифт 8-10pt
- Боковые блоки (facts): заполнение 80%+ высоты
- Если не помещается — [1/2], [2/2] в заголовке, не обрезать

### Цвета Paper Planes
- **#FF5850** (коралловый) — акцент
- **#000000** — основной текст
- **#374151 / #6B7280 / #E5E7EB** — вторичный, фоны
- Светофор (зелёный/жёлтый/красный) — ТОЛЬКО для RAG-статусов, приоритетов, стрелок динамики

### Action Titles
Каждый слайд — вывод, не описание. «Выручка выросла на 15% за счёт B2B» — не «Динамика выручки».

### Установка зависимостей
```bash
cd ~/.claude/skills/consulting-slides-creator && uv pip install -r requirements.txt
```

## References (Load при необходимости)

| Файл | Содержание |
|------|-----------|
| `references/json_examples_analytical.md` | JSON-примеры для всех 18 аналитических типов |
| `references/json_examples_structural.md` | JSON-примеры для 20 структурных типов |
| `references/content_formatting.md` | Правила форматирования текста, таблиц, фактов |
| `references/slide_type_algorithm.md` | Алгоритм выбора типа слайда |
| `references/visual_diversity.md` | Принцип визуального разнообразия |
| `references/data_extraction.md` | Извлечение данных для графиков |
| `references/quality_checklist.md` | QA checklist + предотвращение ошибок |
| `references/workflow.md` | Workflow для Claude: от контента к PPTX |
| `references/consulting_principles.md` | Консалтинговые элементы и принципы |
| `references/self_learning_log.md` | Лог ошибок из реальных проектов |
| `references/structural_layouts.md` | Детальные спецификации структурных layout'ов |

## Workflow (краткий)

1. **Анализ контента** → определить тип слайда (Load: `references/slide_type_algorithm.md`)
2. **Составить JSON** → по примерам (Load: `references/json_examples_analytical.md` или `references/json_examples_structural.md`)
3. **Генерация** → `python3 -m src.generator --config config.json --output slide.pptx`
4. **QA** → проверить action title, плотность, цвета (Load: `references/quality_checklist.md`)
5. **Итерация** → если есть проблемы, исправить JSON и перегенерировать

## Модульная структура кода

```
src/
├── core/           — constants, shapes, text_blocks, charts, typography, grid, qa, styles
├── layouts/
│   ├── __init__.py — реестр layout'ов + auto-discovery + build_slide()
│   ├── analytical/ — 18 модулей
│   └── structural/ — 20 модулей
└── generator.py    — единый CLI entry point
```

## MANUAL MIGRATION REQUIRED

Review unsupported Claude skill fields manually: `**Paper Planes Consulting Slides Generator**`.
