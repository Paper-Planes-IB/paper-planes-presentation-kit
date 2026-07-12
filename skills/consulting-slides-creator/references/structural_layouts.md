# SEVENCOM Generator - Complete Structural Layouts Reference

**Document**: Comprehensive JSON schema for all 20 layout types in `src/layouts/structural/`
**Version**: Paper Planes Consulting, March 2026
**Invocation**: `python3 src/generator.py --config config.json --output output.pptx`

---

## ARCHITECTURAL OVERVIEW

### Key Design Principles

1. **Shape-Based Tables**: Uses PowerPoint shape rectangles, not native PPTX tables
2. **Content/Sidebar Split**: Standard 63/37 layout (`L_W` / `R_W`)
3. **Adaptive Typography**: `calc_size()` dynamically adjusts font 6.5–9.0pt based on content
4. **Accent Bars**: Coral left bars (0.025") on primary cells
5. **Color Consistency**: Fixed palette (CORAL, GRAY_*, CORAL_LIGHT, etc.)

### Dimensions

| Constant | Value | Purpose |
|----------|-------|---------|
| SLIDE_W | 13.333" | Full width |
| SLIDE_H | 7.5" | Full height |
| MG | 0.25" | Standard margin |
| L_W | ~7.5" | Left column (63% of available) |
| R_W | ~5.3" | Right sidebar (37% of available) |
| SB_GAP | 0.05" | Gap between left/right |
| TITLE_H | 0.38" | Title strip height |
| HDR_H | 0.18" | Column header height |
| SB_HDR_H | 0.20" | Sidebar header height |

### Color Palette

| Name | Hex RGB | Usage |
|------|---------|-------|
| CORAL | #FF5850 | Primary accent, headers, highlights |
| GRAY_DARK | #374151 | Headers, bold text |
| GRAY_MED | #6B7280 | Secondary text |
| GRAY_LIGHT | #E5E7EB | Light backgrounds, alternating rows |
| CORAL_LIGHT | #FFEBEA | Soft accent backgrounds |
| CORAL_MID | #FFC8C5 | Medium coral tint |
| CELL_ALT_BG | #FAFAFD | Alternating row background |
| WHITE | #FFFFFF | Default background |

### Adaptive Font Sizing

```python
# calc_size(w_in, h_in, chars, n_items=0, target=0.87, lo=6.5, hi=9.0)
# Returns: (font_size_pt, line_spacing_pt)
TARGET_FILL = 0.87  # % of box to fill
MIN_PT = 6.5        # Minimum font size
MAX_PT = 9.0        # Maximum font size
```

### Sidebar Format (Reusable)

```json
{
  "title": "КЛЮЧЕВЫЕ МЕТРИКИ",
  "items": [
    {
      "label": "Метрика",
      "value": "123 млн"  // OR array ["bullet1", "bullet2"]
    },
    {
      "label": "КПЭ",
      "text": "Описание"     // Alternative to "value"
    }
  ]
}
```

---

## LAYOUT 1: TABLE_SIDEBAR

**Type**: `table_sidebar`

**Purpose**: Tabular data presentation with left 63% content area and right 37% information sidebar. Supports flexible column widths, row highlighting, and alternating row colors.

### JSON Schema

```json
{
  "type": "table_sidebar",
  "title": "Сравнение показателей",
  "sources": "Источник: аналитический отчет",

  "table": {
    "headers": ["ПАРАМЕТР", "ОПИСАНИЕ", "ЗНАЧЕНИЕ"],
    "col_widths": [0.18, 0.40, 0.42],
    "rows": [
      {
        "cells": ["Выручка", "Годовая выручка", "2.5 млрд"]
      },
      {
        "cells": ["EBITDA", "Операционная маржа", "34%"],
        "highlight": false
      },
      {
        "cells": ["Прибыль", "Чистая прибыль", "1.2 млрд"],
        "highlight": true
      }
    ],
    "highlight_col": -1,
    "first_col_bold": true
  },

  "sidebar": {
    "title": "КЛЮЧЕВЫЕ ДАННЫЕ",
    "items": [
      {
        "label": "Рыночная капитализация",
        "value": "45 млрд руб"
      },
      {
        "label": "Основные рынки",
        "value": ["Россия", "Казахстан", "Беларусь"]
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "table_sidebar" |
| title | string | No | Slide title (11pt bold) |
| sources | string | No | Source attribution (6.5pt gray) |
| table.headers | array | Yes | Column header labels |
| table.col_widths | array | No | Fractional widths (default: auto) |
| table.rows | array | Yes | Row data; each row is dict with `cells` array |
| table.rows[].cells | array | Yes | Cell content (strings) |
| table.rows[].highlight | bool | No | True = coral_light background |
| table.highlight_col | int | No | Column index to highlight (-1 = none) |
| table.first_col_bold | bool | No | Bold first column (default: true) |
| sidebar | object | No | Standard sidebar structure |

### Realistic Russian Example

```json
{
  "type": "table_sidebar",
  "title": "Анализ рынка консалтинговых услуг",
  "sources": "McKinsey Global Survey 2025",
  "table": {
    "headers": ["Сегмент", "2023", "2024", "CAGR"],
    "col_widths": [0.25, 0.25, 0.25, 0.25],
    "rows": [
      {
        "cells": ["Стратегия", "12 млн", "14 млн", "17%"]
      },
      {
        "cells": ["Операции", "8 млн", "9.2 млн", "8%"],
        "highlight": false
      },
      {
        "cells": ["Технология", "15 млн", "18 млн", "20%"],
        "highlight": true
      }
    ]
  },
  "sidebar": {
    "title": "КОНТЕКСТ",
    "items": [
      {
        "label": "Регионы фокуса",
        "value": ["Москва", "Санкт-Петербург", "Екатеринбург"]
      },
      {
        "label": "Целевой сегмент",
        "value": "Enterprise & Mid-Market"
      }
    ]
  }
}
```

### Special Behavior

- **Column Width Auto**: If `col_widths` omitted, defaults to [0.18, 0.82] for 2 columns
- **Row Coloring**: Alternates CELL_ALT_BG (light) and WHITE (odd rows)
- **Highlight Override**: If `highlight: true`, uses CORAL_LIGHT
- **First Column**: Always has left coral accent bar

---

## LAYOUT 2: FROM_TO

**Type**: `from_to`

**Purpose**: Horizontal transformation showing AS IS → TO BE states side-by-side with chevron arrows. No vertical accent bars. Flexible number of paired rows.

### JSON Schema

```json
{
  "type": "from_to",
  "title": "Переход к новой модели",
  "sources": "Стратегический план 2025",

  "as_is": {
    "header": "ТЕКУЩЕЕ СОСТОЯНИЕ",
    "items": [
      "Ручные процессы",
      "Отсутствие автоматизации",
      "Низкая скорость обработки"
    ]
  },

  "to_be": {
    "header": "ЦЕЛЕВОЕ СОСТОЯНИЕ",
    "items": [
      "Полная автоматизация RPA",
      "Цифровые рабочие процессы",
      "Обработка за 24 часа"
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "from_to" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| as_is | object \| array | Yes | Current state; header + items |
| as_is.header | string | No | Column label (default: "СЕЙЧАС") |
| as_is.items | array | Yes | Bullet items (strings) |
| to_be | object \| array | Yes | Target state |
| to_be.header | string | No | Column label (default: "РЕШЕНИЕ") |
| to_be.items | array | Yes | Bullet items |

### Realistic Russian Example

```json
{
  "type": "from_to",
  "title": "Трансформация управления кадрами",
  "as_is": {
    "header": "СЕЙЧАС (AS IS)",
    "items": [
      "HR-процессы в Excel и бумаге",
      "Отсутствие единой БД кандидатов",
      "Рекрутмент 3-4 месяца"
    ]
  },
  "to_be": {
    "header": "БУДУЩЕЕ (TO BE)",
    "items": [
      "Интегрированная HRIS система",
      "АИ-поддержанный поиск талантов",
      "Рекрутмент за 2 недели"
    ]
  }
}
```

### Special Behavior

- **Chevron Gap**: 0.22" divider between columns visually separates left/right
- **Header Bars**: Left = GRAY_MED, right = CORAL
- **No Sidebar**: Right 37% remains empty (full width content area)
- **Bullet Items**: Rendered with coral bullets (▪)

---

## LAYOUT 3: COMPARISON

**Type**: `comparison`

**Purpose**: Criteria-based decision comparison with 2+ options (usually A vs B), verdict column (✓), and top/bottom dual sidebars for context and mitigations.

### JSON Schema

```json
{
  "type": "comparison",
  "title": "Сравнение вариантов решения",
  "sources": "Анализ альтернатив",

  "comparison": {
    "col_a_header": "РЕШЕНИЕ А",
    "col_b_header": "РЕШЕНИЕ B",
    "rows": [
      {
        "criterion": "Стоимость реализации",
        "option_a": "120 млн руб",
        "option_b": "180 млн руб",
        "winner": "a"
      },
      {
        "criterion": "Время внедрения",
        "option_a": "6 месяцев",
        "option_b": "4 месяца",
        "winner": "b"
      },
      {
        "criterion": "Масштабируемость",
        "option_a": "Средняя",
        "option_b": "Высокая",
        "winner": "b"
      }
    ]
  },

  "sidebar_top": {
    "title": "КОНТЕКСТ",
    "quotes": [
      {
        "text": "Нужно сбалансировать цену и качество",
        "ref": "Stakeholder interview"
      }
    ]
  },

  "sidebar_bottom": {
    "title": "ВОЗМОЖНОСТИ",
    "items": [
      {
        "label": "Гибридный подход",
        "value": "Комбинировать A+B"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "comparison" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| comparison.col_a_header | string | No | Column A label (default: "ВАРИАНТ A") |
| comparison.col_b_header | string | No | Column B label (default: "ВАРИАНТ B") |
| comparison.rows | array | Yes | Criteria rows |
| comparison.rows[].criterion | string | Yes | Evaluation criteria |
| comparison.rows[].option_a | string | Yes | Option A text |
| comparison.rows[].option_b | string | Yes | Option B text |
| comparison.rows[].winner | string | No | "a" or "b" (marks winner) |
| sidebar_top | object | No | Context sidebar (quotes, italics) |
| sidebar_bottom | object | No | Mitigations sidebar (arrows) |

### Realistic Russian Example

```json
{
  "type": "comparison",
  "title": "Выбор платформы ERP: SAP vs Oracle",
  "comparison": {
    "col_a_header": "SAP S/4HANA",
    "col_b_header": "Oracle Cloud",
    "rows": [
      {
        "criterion": "Соответствие МСФО",
        "option_a": "Встроенная поддержка",
        "option_b": "Требуется доработка",
        "winner": "a"
      },
      {
        "criterion": "Облачная архитектура",
        "option_a": "SAP Cloud",
        "option_b": "Нативная облачная",
        "winner": "b"
      },
      {
        "criterion": "Экосистема партнёров в РФ",
        "option_a": "Обширная",
        "option_b": "Растущая",
        "winner": "a"
      },
      {
        "criterion": "Стоимость владения (5 лет)",
        "option_a": "2.5 млрд руб",
        "option_b": "1.8 млрд руб",
        "winner": "b"
      }
    ]
  },
  "sidebar_top": {
    "title": "КРИТИЧЕСКИЕ ФАКТОРЫ",
    "quotes": [
      {
        "text": "Срок внедрения < 12 месяцев критичен для бюджета",
        "ref": "CFO"
      }
    ]
  }
}
```

### Special Behavior

- **Dual Sidebars**: Top sidebar uses quotes (italics, gray); bottom uses arrows (→ prefix)
- **Verdict Column**: Center-aligned ✓ symbol; color based on winner
- **Score Bar**: Bottom bar shows count "РЕШЕНИЕ B 2:2 SAP S/4HANA"
- **Row Coloring**: Alternates CELL_ALT_BG and WHITE
- **Winner Highlighting**: Losing option gets GRAY_LIGHT background

---

## LAYOUT 4: PROCESS_DETAIL

**Type**: `process_detail`

**Purpose**: Detailed process workflow with AS IS multi-column table, TO BE improvement section, and rich header/footer metadata. Suitable for operational processes, decision gates, etc.

### JSON Schema

```json
{
  "type": "process_detail",
  "title": "Процесс утверждения капитальных расходов",
  "sources": "Finance Operations Manual v2.3",

  "header": {
    "id": "GATE-03",
    "name": "Отпуск средств",
    "stage": "Stage 3",
    "duration": "2-4 недели"
  },

  "as_is_label": "AS IS — существующий процесс",

  "steps": [
    {
      "step_id": "3.1",
      "step_name": "Проверка бюджета",
      "responsible": "Финансовый контроллер",
      "content": "Проверка наличия бюджета на счёте",
      "duration": "1 день"
    },
    {
      "step_id": "3.2",
      "step_name": "Согласование с руководством",
      "responsible": "CFO",
      "content": "Финальное утверждение",
      "duration": "3 дня"
    }
  ],

  "to_be": [
    "Автоматизация проверки бюджета через систему",
    "Email-уведомления вместо ручного звонка",
    "Параллельное согласование с CFO и COO"
  ]
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "process_detail" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| header.id | string | No | Gate/phase ID (11pt, bold, white) |
| header.name | string | No | Gate name (9pt, bold) |
| header.stage | string | No | Stage label (7pt) |
| header.duration | string | No | Duration estimate (7pt, coral_mid) |
| as_is_label | string | No | AS IS label (default shown) |
| steps | array | Yes | Process steps |
| steps[].step_id | string | Yes | Step ID/number |
| steps[].step_name | string | Yes | Step title |
| steps[].responsible | string | Yes | Responsible party |
| steps[].content | string | Yes | Step description |
| steps[].duration | string | No | Time estimate |
| to_be | array | No | Improvements (bullets) |

### Realistic Russian Example

```json
{
  "type": "process_detail",
  "title": "Управление контрактами для поставщиков",
  "header": {
    "id": "PROC-CONT",
    "name": "Управление жизненным циклом контракта",
    "stage": "Этап 2: Согласование",
    "duration": "15-20 дней"
  },
  "steps": [
    {
      "step_id": "2.1",
      "step_name": "Подготовка проекта контракта",
      "responsible": "Procurement Manager",
      "content": "Разработка на основе шаблона с учётом специфики",
      "duration": "3 дня"
    },
    {
      "step_id": "2.2",
      "step_name": "Согласование с юристом",
      "responsible": "Legal Counsel",
      "content": "Проверка условий и рисков",
      "duration": "5 дней"
    },
    {
      "step_id": "2.3",
      "step_name": "Отправка поставщику",
      "responsible": "Procurement Manager",
      "content": "Email с комментариями и запросом обратной связи",
      "duration": "1 день"
    }
  ],
  "to_be": [
    "Использование Docusign для электронной подписи",
    "Интеграция с системой CMS для отслеживания версий",
    "Автоматическая отправка напоминаний через 5 дней ожидания"
  ]
}
```

### Special Behavior

- **Header Bar**: Full-width CORAL with mixed font sizes
- **Column Headers**: Small headers (0.16") for 4 fixed columns
- **Row Heights**: Auto-split remaining height by step count
- **Accent Bar**: Left coral bar on each step row
- **TO BE Section**: Optional light coral background with bullets

---

## LAYOUT 5: RASCI

**Type**: `rasci`

**Purpose**: RASCI matrix (Responsible, Accountable, Supportive, Consulted, Informed) for governance/organizational design. Supports both flat gate lists and full role/activity mappings. Color-coded cells: R=blue, A=coral, S=green, C=yellow, I=gray.

### JSON Schema

```json
{
  "type": "rasci",
  "title": "RASCI матрица управления проектом",
  "sources": "Project Charter",

  "departments": [
    {
      "id": "pm",
      "name": "Project Office"
    },
    {
      "id": "dev",
      "name": "Development"
    },
    {
      "id": "ops",
      "name": "Operations"
    },
    {
      "id": "qa",
      "name": "QA"
    }
  ],

  "gates": [
    {
      "gate_id": "G1",
      "activities": "Инициация проекта",
      "roles": {
        "pm": "A",
        "dev": "C",
        "ops": "I",
        "qa": "I"
      },
      "note": "Базовое планирование"
    },
    {
      "gate_id": "G2",
      "activities": "Разработка решения",
      "roles": {
        "pm": "S",
        "dev": "R",
        "ops": "C",
        "qa": "C"
      },
      "note": ""
    }
  ],

  "legend": {
    "R": "Ответственный (выполняет работу)",
    "A": "Подотчётный (принимает решение)",
    "S": "Поддерживающий (помогает)",
    "C": "Консультируемый (участвует в решении)",
    "I": "Информируемый (на курсе)"
  },

  "synthesis": [
    "Управление требованиями ведёт PM",
    "Development отвечает за качество кода",
    "Operations готовит окружение"
  ]
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "rasci" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| departments | array | Yes | Column definitions |
| departments[].id | string | Yes | Unique dept ID (used in roles map) |
| departments[].name | string | Yes | Display name |
| gates | array | Yes | Row definitions |
| gates[].gate_id | string | Yes | Row label (e.g., "G1", "Phase 1") |
| gates[].activities | string | No | Activity description |
| gates[].roles | object | Yes | Map {dept_id: code} where code ∈ {R,A,S,C,I} |
| gates[].note | string | No | Additional notes |
| legend | object | No | Code descriptions (custom or default) |
| synthesis | array | No | Bottom summary bullets |

### Realistic Russian Example

```json
{
  "type": "rasci",
  "title": "RASCI матрица: Цифровая трансформация",
  "departments": [
    {
      "id": "cdo",
      "name": "Chief Digital Officer"
    },
    {
      "id": "engineering",
      "name": "Инженерия"
    },
    {
      "id": "business",
      "name": "Бизнес-единица"
    },
    {
      "id": "hr",
      "name": "HR & Org Dev"
    }
  ],
  "gates": [
    {
      "gate_id": "Диагностика",
      "activities": "Оценка текущего состояния IT",
      "roles": {
        "cdo": "A",
        "engineering": "R",
        "business": "C",
        "hr": "I"
      },
      "note": "3-недельный аудит"
    },
    {
      "gate_id": "Дизайн",
      "activities": "Разработка стратегии цифровизации",
      "roles": {
        "cdo": "R",
        "engineering": "C",
        "business": "S",
        "hr": "C"
      },
      "note": "Вовлечение сценариев потребления"
    },
    {
      "gate_id": "Рилиз",
      "activities": "Запуск платформы и обучение",
      "roles": {
        "cdo": "S",
        "engineering": "R",
        "business": "A",
        "hr": "R"
      },
      "note": "Параллельные инициативы обучения"
    }
  ],
  "legend": {
    "R": "Ответственный (исполняет)",
    "A": "Подотчётный (решает)",
    "S": "Поддерживает",
    "C": "Консультируется",
    "I": "Информируется"
  },
  "synthesis": [
    "CDO управляет стратегией; Engineering владеет разработкой",
    "Business и HR интегрированы на всех этапах",
    "3-месячный итеративный цикл внедрения"
  ]
}
```

### Color Map (Fixed)

| Code | Background | Text | Meaning |
|------|-----------|------|---------|
| R | Blue #3B82F6 | White | Ответственный |
| A | Coral #FF5850 | White | Подотчётный |
| S | Green #10B981 | White | Поддерживающий |
| C | Yellow #F59E0B | White | Консультируемый |
| I | Gray #D1D5DB | Dark | Информируемый |

### Special Behavior

- **Flexible Columns**: Supports 3–8 departments
- **Activities Column**: Optional; if present, adds description column
- **Legend Bar**: Top colored bar shows all codes with definitions
- **Synthesis Section**: Optional bottom bar with key takeaways
- **Matrix Data Format**: Two supported structures (Format A: nested in gates; Format B: separate matrix array)

---

## LAYOUT 6: STAGE_GATE

**Type**: `stage_gate`

**Purpose**: Project timeline with stages/phases displayed as vertical columns. Each stage shows header (numbered), bullet items, and duration label. Useful for roadmaps, project phasing, milestone tracking.

### JSON Schema

```json
{
  "type": "stage_gate",
  "title": "Фазы внедрения системы",
  "sources": "Project Schedule v3.2",

  "stages": [
    {
      "id": "stage_1",
      "name": "Диагностика",
      "items": [
        "Оценка текущего состояния",
        "Интервью с ключевыми лицами",
        "Подготовка отчёта"
      ],
      "duration": "4 недели",
      "color": "coral"
    },
    {
      "id": "stage_2",
      "name": "Дизайн решения",
      "items": [
        "Определение требований",
        "Архитектурные решения",
        "План внедрения"
      ],
      "duration": "6 недель",
      "color": "coral_light"
    },
    {
      "id": "stage_3",
      "name": "Внедрение",
      "items": [
        "Разработка и тестирование",
        "Обучение команд",
        "Go-live"
      ],
      "duration": "8 недель",
      "color": "gray"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "stage_gate" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| stages | array | Yes | Stage columns |
| stages[].id | string | No | Unique stage identifier |
| stages[].name | string | Yes | Stage display name |
| stages[].items | array | Yes | Bullet items (shown as coral bullets) |
| stages[].duration | string | No | Duration label (6pt, bottom) |
| stages[].color | string | No | "coral", "gray", or "coral_light" (default) |

### Realistic Russian Example

```json
{
  "type": "stage_gate",
  "title": "Временная шкала трансформации закупок",
  "sources": "Procurement Transformation Roadmap Q1-Q4 2025",
  "stages": [
    {
      "name": "Оценка (Assess)",
      "items": [
        "Анализ текущих процессов",
        "Интервью с участниками",
        "Выявление болевых точек"
      ],
      "duration": "3 недели",
      "color": "coral"
    },
    {
      "name": "Дизайн (Design)",
      "items": [
        "Целевые процессы",
        "Требования к системе",
        "План обучения"
      ],
      "duration": "5 недель",
      "color": "coral_light"
    },
    {
      "name": "Разработка (Build)",
      "items": [
        "Конфигурация SAP",
        "Интеграции",
        "Тестирование UAT"
      ],
      "duration": "12 недель",
      "color": "coral_light"
    },
    {
      "name": "Запуск (Launch)",
      "items": [
        "Go-live support",
        "Обучение пользователей",
        "Стабилизация"
      ],
      "duration": "4 недели",
      "color": "gray"
    }
  ]
}
```

### Special Behavior

- **Equal-Width Columns**: Stages split remaining width evenly
- **Column Color Mapping**: "coral" (CORAL, white text), "gray" (GRAY_DARK, white), "coral_light" (default, gray text)
- **Numbered Headers**: Displays as "1", "2", "3", etc. (not raw ID)
- **Bottom Duration Bar**: GRAY_LIGHT background with duration text

---

## LAYOUT 7: BRAND_PYRAMID

**Type**: `brand_pyramid`

**Purpose**: RDB (Reason to believe, Differentiator, Benefit) or similar 3-tier brand/value pyramid with full-width stacked boxes. Each component shows letter + name + subtitle + content. Bottom unifying message bar.

### JSON Schema

```json
{
  "type": "brand_pyramid",
  "title": "Модель ценности платформы",
  "sources": "Brand Strategy 2025",

  "components": [
    {
      "letter": "R",
      "name": "Технологическое лидерство",
      "subtitle": "Reason to Believe",
      "content": "Запатентованная технология машинного обучения, прошедшая 5 лет разработки и доказавшая эффективность на 500+ компаниях"
    },
    {
      "letter": "D",
      "name": "Встроенная аналитика",
      "subtitle": "Дифференциатор",
      "content": "Уникальное сочетание предиктивной аналитики с интуитивным интерфейсом, позволяющее даже неспециалистам принимать данные-обоснованные решения"
    },
    {
      "letter": "B",
      "name": "ROI за 6 месяцев",
      "subtitle": "Выгода",
      "content": "Средняя окупаемость инвестиций 340% в год, что даёт возможность перераспределить средства на стратегические инициативы"
    }
  ],

  "unifying_message": "Мы помогаем организациям превращать данные в конкурентное преимущество"
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "brand_pyramid" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| components | array | Yes | 1–3 boxes (R, D, B or custom) |
| components[].letter | string | Yes | Large letter (16pt, coral) |
| components[].name | string | Yes | Bold title (9pt) |
| components[].subtitle | string | No | Smaller subtitle (6pt, gray_med) |
| components[].content | string | Yes | Main text (adaptive, 6.5–7.0pt) |
| unifying_message | string | Yes | Bottom CORAL bar message (8pt, bold) |

### Realistic Russian Example

```json
{
  "type": "brand_pyramid",
  "title": "Цена предложения сервиса облачных вычислений",
  "components": [
    {
      "letter": "R",
      "name": "Надежность 99.99%",
      "subtitle": "Причина верить",
      "content": "Сертифицированная инфраструктура ISO 27001 с географически распределёнными дата-центрами в РФ и СНГ, гарантирующая непрерывность"
    },
    {
      "letter": "D",
      "name": "Гибкая тарификация",
      "subtitle": "Дифференциатор",
      "content": "Pay-as-you-go модель с приостановкой услуг без штрафов, позволяющая стартапам масштабироваться без переплаты за запас мощности"
    },
    {
      "letter": "B",
      "name": "Экономия 40% на IT",
      "subtitle": "Выгода",
      "content": "Переход в облако исключает CapEx, сокращает IT-штат на 30% и позволяет сфокусироваться на инновациях вместо управления оборудованием"
    }
  ],
  "unifying_message": "Облачные вычисления, которые понимают ваш бизнес"
}
```

### Special Behavior

- **3-Component Max**: Only first 3 components render (fixed RDB structure)
- **Box Gaps**: 0.02" spacing between boxes
- **Color Scheme**:
  - R box: CORAL_LIGHT with coral accent bar
  - D box: WHITE with coral accent bar
  - B box: CELL_ALT_BG with coral accent bar
- **Bottom Bar**: Full-width CORAL with centered white bold text

---

## LAYOUT 8: MECHANISM_CARD

**Type**: `mechanism_card`

**Purpose**: Big3-style mechanism card showing metric KPIs, process steps, conditions/constraints, and optional sidebar. Modular design for detailed deep-dives.

### JSON Schema

```json
{
  "type": "mechanism_card",
  "title": "Механизм повышения производительности",
  "sources": "Операционный анализ",

  "metrics": [
    {
      "value": "+25%",
      "label": "Прирост производительности"
    },
    {
      "value": "-15 дн",
      "label": "Сокращение цикла"
    },
    {
      "value": "2.5x",
      "label": "ROI"
    }
  ],

  "process_steps": [
    "Автоматизация повторяющихся задач через RPA",
    "Перераспределение ресурсов на высокоценные операции",
    "Мониторинг эффективности KPI в реальном времени"
  ],

  "conditions": [
    "Требуется участие IT-команды для конфигурации",
    "Смена процессов требует переподготовки (2 недели)",
    "Совместимость с текущими системами (SAP, Oracle)"
  ],

  "sidebar": {
    "title": "МЕТРИКИ УСПЕХА",
    "items": [
      {
        "label": "Целевой EBITDA",
        "value": "35%"
      },
      {
        "label": "Инвестиции",
        "value": "18 млн руб"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "mechanism_card" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| metrics | array | No | 2–3 KPI tiles (value + label) |
| metrics[].value | string | Yes | Large metric (14pt, coral, bold) |
| metrics[].label | string | Yes | Metric label (6pt, gray) |
| process_steps | array | No | Bullet items (ПРОЦЕСС section) |
| conditions | array | No | Bullet items (УСЛОВИЯ И ОГРАНИЧЕНИЯ section) |
| sidebar | object | No | Standard sidebar structure |

### Realistic Russian Example

```json
{
  "type": "mechanism_card",
  "title": "Механизм улучшения NPS у клиентов",
  "metrics": [
    {
      "value": "+15 пт",
      "label": "Улучшение NPS"
    },
    {
      "value": "-20%",
      "label": "Чёрн интернет-обращений"
    },
    {
      "value": "+40%",
      "label": "Repeat rate"
    }
  ],
  "process_steps": [
    "Создание комплексной программы лояльности с уровнями",
    "Внедрение system обратной связи на каждом touchpoint",
    "Автоматизация целевых предложений по истории покупок",
    "Обучение сотрудников культуре customer obsession"
  ],
  "conditions": [
    "Требуется инвестиция в CRM-систему (~12 млн)",
    "Изменение процессов обслуживания у 150+ сотрудников",
    "Зависимость от качества данных в системе"
  ],
  "sidebar": {
    "title": "КЛЮЧЕВЫЕ СОБЫТИЯ",
    "items": [
      {
        "label": "Фаза 1 (квартал I)",
        "value": ["Обучение персонала", "Внедрение CRM"]
      },
      {
        "label": "Фаза 2 (квартал II)",
        "value": "Запуск программы лояльности"
      }
    ]
  }
}
```

### Special Behavior

- **Metric Tiles**: Top section; auto-split width if 2–3 metrics
- **Process Section**: Gray_dark header, white background with coral bullets
- **Conditions Section**: Gray_med header, light alt background
- **Sidebar**: Right 37% (optional)
- **Spacing**: 0.04" gap between sections

---

## LAYOUT 9: ROADMAP_SWIMLANE

**Type**: `roadmap_swimlane`

**Purpose**: Multi-horizon roadmap with swimlanes for strategic initiatives. Horizons (H1, H2, H3) map to time periods; initiatives placed within swimlanes. Configurable timeline sections (0-3mo, 3-6mo, 6-12mo).

### JSON Schema

```json
{
  "type": "roadmap_swimlane",
  "title": "Цифровая трансформация: 3-летная дорожная карта",
  "sources": "Digital Strategy 2025-2027",

  "timeline_sections": [
    {
      "label": "2025 H1",
      "color": "coral"
    },
    {
      "label": "2025 H2",
      "color": "coral_light"
    },
    {
      "label": "2026+",
      "color": "gray_light"
    }
  ],

  "horizons": [
    {
      "name": "Горизонт 1: Core",
      "subtitle": "Стабилизировать текущие операции",
      "initiatives": [
        "Миграция ERP в облако",
        "RPA для финансовых процессов"
      ]
    },
    {
      "name": "Горизонт 2: Grow",
      "subtitle": "Новые возможности для бизнеса",
      "initiatives": [
        "Аналитическая платформа",
        "Мобильное приложение"
      ]
    },
    {
      "name": "Горизонт 3: Transform",
      "subtitle": "Долгосрочные трансформационные инициативы",
      "initiatives": [
        "AI-driven customer service",
        "Blockchain для supply chain"
      ]
    }
  ],

  "summary": "Трёхлетная инвестиция 150 млн руб с ожидаемой ROI 320% к концу 2027 года"
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "roadmap_swimlane" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| timeline_sections | array | No | Custom time periods (default: 0-3m, 3-6m, 6-12m) |
| timeline_sections[].label | string | Yes | Period label (e.g., "Q1 2025") |
| timeline_sections[].color | string | Yes | "coral", "coral_light", "coral_mid", "gray_light", etc. |
| horizons | array | Yes | 1–3 swimlane definitions |
| horizons[].name | string | Yes | Horizon title (e.g., "H1: Core") |
| horizons[].subtitle | string | No | Horizon description |
| horizons[].initiatives | array | Yes | Initiative names (rendered as boxes) |
| summary | string | No | Bottom bar summary text |

### Realistic Russian Example

```json
{
  "type": "roadmap_swimlane",
  "title": "Стратегия внедрения аналитики в гос. учреждение",
  "timeline_sections": [
    {
      "label": "2025 (Быстрые победы)",
      "color": "coral"
    },
    {
      "label": "2026 (Расширение)",
      "color": "coral_light"
    },
    {
      "label": "2027+ (Трансформация)",
      "color": "gray_light"
    }
  ],
  "horizons": [
    {
      "name": "Фаза 1: Фундамент",
      "subtitle": "Подготовка инфраструктуры и данных",
      "initiatives": [
        "Data governance framework",
        "Миграция на современный DWH",
        "Обучение аналитиков"
      ]
    },
    {
      "name": "Фаза 2: Автоматизация",
      "subtitle": "Масштабирование аналитики по организации",
      "initiatives": [
        "Dashboards для руководства",
        "RPA для отчётности",
        "Интеграция ведомственных систем"
      ]
    },
    {
      "name": "Фаза 3: Предиктивность",
      "subtitle": "Перейти к предиктивной аналитике",
      "initiatives": [
        "AI-модели прогнозирования",
        "Персонализированные insights",
        "Автоматические рекомендации"
      ]
    }
  ],
  "summary": "Инвестиция в аналитику позволит улучшить эффективность на 25% и снизить затраты на 40 млн рублей в год"
}
```

### Special Behavior

- **Timeline Header**: Top colored strips for each time period
- **Swimlane Layout**: Left label column + content areas
- **Initiative Boxes**: CORAL_LIGHT background with coral accent bars
- **Default Periods**: If no timeline_sections, uses 0-3mo, 3-6mo, 6-12mo with CORAL, CORAL_LIGHT, GRAY_LIGHT
- **Empty Swimlanes**: Render as blank bordered areas

---

## LAYOUT 10: TITLE_DARK

**Type**: `title_dark`

**Purpose**: Full-slide title cover slide with dark background (GRAY_DARK), large left-aligned title, subtitle (coral), date/company info, optional governing thought on right, and vertical coral accent bar at 42% x-position.

### JSON Schema

```json
{
  "type": "title_dark",

  "title": "Трансформация операций: Путь к экспоненциальному росту",
  "subtitle": "Стратегический план 2025-2027",
  "date": "Февраль 2025",
  "company": "Paper Planes Consulting",

  "governing_thought": "В мире VUCA только организации, которые быстро адаптируются и экспериментируют, останутся конкурентоспособны. Операционная трансформация должна быть инвестицией в агилитет и инновационность, а не только в эффективность."
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "title_dark" |
| title | string | Yes | Main title (28pt, bold, white, left) |
| subtitle | string | No | Subtitle (14pt, coral, left) |
| date | string | No | Date text (9pt, white, bottom-left) |
| company | string | No | Company name (9pt, white, bottom-left) |
| governing_thought | string | No | Right side italics (11pt, white, italic) |

### Realistic Russian Example

```json
{
  "type": "title_dark",
  "title": "Переход на Agile: Путь к быстрым поставкам",
  "subtitle": "Инициатива трансформации IT-подразделения",
  "date": "Март 2025",
  "company": "Сбербанк CIB",
  "governing_thought": "Agile — это не просто методология разработки, это философия управления и культурное изменение, требующее переподготовки 70% персонала и переопределения KPI на результаты вместо активностей."
}
```

### Special Behavior

- **Dark Background**: Full-slide GRAY_DARK
- **Left Layout**: Title (40%), subtitle below
- **Vertical Accent**: Full-height coral bar at X=42%
- **Right Section**: Optional governing thought (58% of width, right-aligned)
- **Bottom-Right Logo**: Small coral square placeholder (0.25" × 0.25")
- **No Title/Source Bars**: Standalone cover slide

---

## LAYOUT 11: EXEC_SUMMARY

**Type**: `exec_summary`

**Purpose**: Executive summary with up to 4 numbered insight cards in 2×2 grid. Each card shows number, heading, bullet text, and optional bottom conclusion bar for key takeaway.

### JSON Schema

```json
{
  "type": "exec_summary",
  "title": "Ключевые выводы анализа",
  "sources": "Comprehensive Market Study",

  "insights": [
    {
      "number": "01",
      "heading": "Рост рынка ускоряется",
      "text": [
        "CAGR 2020-2025 достиг 23%",
        "Ожидается 35% роста в 2026 году",
        "Новые сегменты открываются в B2B2C"
      ]
    },
    {
      "number": "02",
      "heading": "Конкуренция интенсифицируется",
      "text": "15 новых игроков вошли на рынок в последние 2 года; консолидация неизбежна в ближайшие 3 года"
    },
    {
      "number": "03",
      "heading": "Потребитель меняет поведение",
      "text": [
        "Переход на омниканальный шопинг (70%)",
        "Ожидания к персонализации растут",
        "Sustainability становится критичным фактором"
      ]
    },
    {
      "number": "04",
      "heading": "Инвестиции в технологию критичны",
      "text": "Компании, инвестирующие в AI/ML, выигрывают в скорости вывода продуктов на 40%"
    }
  ],

  "conclusion": "Три года окна возможности для позиционирования как лидер; требуется немедленные инвестиции в технологию и таланты"
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "exec_summary" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| insights | array | Yes | 1–4 cards |
| insights[].number | string | No | Card number (default: 01, 02, etc.) |
| insights[].heading | string | Yes | Card title (9pt, bold) |
| insights[].text | string \| array | Yes | Body text or bullets |
| conclusion | string | Yes | Bottom bar text (8pt, gray_dark, left) |

### Realistic Russian Example

```json
{
  "type": "exec_summary",
  "title": "Итоги диагностики: Быстрые выводы",
  "sources": "15-дневная диагностика Feb 2025",
  "insights": [
    {
      "number": "1",
      "heading": "Процессы морально устарели",
      "text": [
        "Среднее время обработки платежа: 5 дней (vs. 1 день в лучших компаниях)",
        "Отсутствие автоматизации: 70% операций ручные",
        "Потеря документов: ежегодно 50+ юридических инцидентов"
      ]
    },
    {
      "number": "2",
      "heading": "Технологический стек фрагментирован",
      "text": "15 несвязанных систем; данные дублируются и расходятся; отсутствует единая source-of-truth для управления"
    },
    {
      "number": "3",
      "heading": "Талант выходит из организации",
      "text": [
        "Текучесть IT-специалистов: 35% в год",
        "Зарплаты ниже рынка на 20-30%",
        "Отсутствие карьерного развития и инструментов работы"
      ]
    },
    {
      "number": "4",
      "heading": "Окно возможности: 18 месяцев",
      "text": "Конкуренты уже внедряют AI-решения; задержка на 18 месяцев может стоить 100+ млн в потерянной выручке"
    }
  ],
  "conclusion": "Срочно требуется: (1) Выбор целевой архитектуры, (2) Инвестиция в переподготовку, (3) Быстрые победы для мотивации команды"
}
```

### Special Behavior

- **2×2 Grid**: Cards split horizontally/vertically with 0.02" gaps
- **Card Colors**: WHITE background with coral accent bar on left
- **Adaptive Fonts**: Text auto-sizes to fit card
- **Bullet Support**: If `text` is array, renders as bullets with coral markers
- **Bottom Conclusion**: CORAL_LIGHT bar with 0.35" height, coral accent bar

---

## LAYOUT 12: DIVIDER

**Type**: `divider`

**Purpose**: Track divider slide with dark background (GRAY_DARK) separating presentation sections. Shows large track number (coral, 36pt), track name (white, 18pt), governing thought (italic, 10pt), left coral accent bar, and bottom coral bar.

### JSON Schema

```json
{
  "type": "divider",

  "track_number": "ТРЕК 2",
  "track_name": "Операционная эффективность",

  "governing_thought": "Операционная совершенство — это не единовременный проект, а культурный сдвиг. Требуется постоянное внимание к процессам, инвестиции в инструменты и расширение прав и возможностей сотрудников как авторов улучшений."
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "divider" |
| track_number | string | Yes | Track label (36pt, coral, bold, centered) |
| track_name | string | Yes | Track title (18pt, white, centered) |
| governing_thought | string | Yes | Philosophy/context (10pt, white, italic, centered) |

### Realistic Russian Example

```json
{
  "type": "divider",
  "track_number": "ТРЕК 3",
  "track_name": "Цифровые возможности и данные",
  "governing_thought": "Данные — новая нефть, но они полезны только в руках организаций, которые могут их быстро интерпретировать и действовать. Инвестиции в аналитику, AI и культуру data-driven принятия решений — это конкурентное преимущество следующего десятилетия."
}
```

### Special Behavior

- **Full Dark Background**: GRAY_DARK fill
- **Left Accent**: 0.06" coral vertical bar (full height)
- **Centered Layout**: Track number, name, thought — все центрированы
- **Bottom Bar**: 0.04" coral horizontal bar (full width)
- **No Title/Source**: Standalone divider
- **Typical Position**: Between major presentation sections

---

## LAYOUT 13: NEXT_STEPS

**Type**: `next_steps`

**Purpose**: Call-to-action slide with up to 4 phase columns (typically: Immediate, Short-term, Medium-term, Long-term) showing action items as bullets. Bottom coral bar for the "Ask" or recommendation.

### JSON Schema

```json
{
  "type": "next_steps",
  "title": "Рекомендуемые шаги",
  "sources": "Consulting recommendations",

  "phases": [
    {
      "name": "Неделя 1-2",
      "items": [
        "Утвердить steering committee",
        "Назначить project manager",
        "Провести kick-off с командой"
      ]
    },
    {
      "name": "Месяц 1-2",
      "items": [
        "Завершить detailed assessment",
        "Разработать бизнес-кейс",
        "Определить целевые состояния"
      ]
    },
    {
      "name": "Месяц 2-6",
      "items": [
        "Выбрать технологического партнёра",
        "Запустить пилот на одном процессе",
        "Измерить quick wins"
      ]
    }
  ],

  "ask": "Примите решение по инвестициям к концу марта 2025; ожидаемая ROI составит 250% в течение 2 лет"
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "next_steps" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| phases | array | Yes | 2–4 phase columns |
| phases[].name | string | Yes | Phase label (7pt, bold, white header) |
| phases[].items | array | Yes | Action bullets (coral-marked) |
| ask | string | Yes | Call-to-action (8pt, bold, white, CORAL bg) |

### Realistic Russian Example

```json
{
  "type": "next_steps",
  "title": "План действий: Следующие 90 дней",
  "phases": [
    {
      "name": "Неделя 1-2: Подготовка",
      "items": [
        "Создать cross-functional team (PM, Engineering, Product)",
        "Утвердить budget и timeline",
        "Определить success metrics"
      ]
    },
    {
      "name": "Неделя 3-4: Дизайн",
      "items": [
        "Провести workshops с users",
        "Разработать требования",
        "Создать mock-ups и прототипы"
      ]
    },
    {
      "name": "Месяц 2: MVP разработка",
      "items": [
        "Sprint-планирование с Agile team",
        "Разработка core features",
        "Parallel: обучение support team"
      ]
    },
    {
      "name": "Месяц 3: Go-Live",
      "items": [
        "Тестирование в production-like окружении",
        "Подготовка launch communications",
        "Запуск с поддержкой и мониторингом"
      ]
    }
  ],
  "ask": "Инвестиция 45 млн руб; ожидаемая выручка 120 млн руб в первый год; примите решение к 15 февраля"
}
```

### Special Behavior

- **Equal-Width Columns**: Phases split remaining width evenly
- **Phase Headers**: GRAY_DARK background, white 7pt bold text
- **Content Background**: WHITE with coral accent bars
- **Bottom Ask Bar**: Full-width CORAL, white 8pt bold left-aligned text
- **Flexible Columns**: 2–4 phases supported

---

## LAYOUT 14: MATRIX_2X2

**Type**: `matrix_2x2`

**Purpose**: 2×2 (or custom) quadrant framework for positioning, prioritization, risk assessment, etc. Four quadrants with label + name + description; axis labels (X: low↔high, Y: low↔high); optional right sidebar.

### JSON Schema

```json
{
  "type": "matrix_2x2",
  "title": "Матрица приоритизации инициатив",
  "sources": "Strategic planning workshop",

  "x_axis": {
    "label": "Сложность внедрения",
    "low": "Низкая",
    "high": "Высокая"
  },

  "y_axis": {
    "label": "Бизнес-влияние",
    "low": "Низкое",
    "high": "Высокое"
  },

  "quadrants": [
    {
      "position": "top_right",
      "label": "1",
      "name": "Quick Wins",
      "description": "Высокое влияние, низкая сложность — реализовать в первую очередь",
      "color": "coral"
    },
    {
      "position": "top_left",
      "label": "2",
      "name": "Strategic",
      "description": "Высокое влияние, высокая сложность — требует планирования",
      "color": "coral_light"
    },
    {
      "position": "bottom_right",
      "label": "3",
      "name": "Fill-ins",
      "description": "Низкое влияние, низкая сложность — делать если есть ресурсы",
      "color": "gray_light"
    },
    {
      "position": "bottom_left",
      "label": "4",
      "name": "Avoid",
      "description": "Низкое влияние, высокая сложность — отложить или отклонить",
      "color": "white"
    }
  ],

  "sidebar": {
    "title": "МЕТОДОЛОГИЯ",
    "items": [
      {
        "label": "Влияние",
        "value": "Бизнес-выгода в млн руб"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "matrix_2x2" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| x_axis.label | string | No | X-axis name |
| x_axis.low | string | No | Low end label |
| x_axis.high | string | No | High end label |
| y_axis.label | string | No | Y-axis name |
| y_axis.low | string | No | Low end label |
| y_axis.high | string | No | High end label |
| quadrants | array | Yes | 4 quadrant definitions |
| quadrants[].position | string | Yes | "top_left", "top_right", "bottom_left", "bottom_right" |
| quadrants[].label | string | Yes | Quadrant number/label (10pt, coral) |
| quadrants[].name | string | No | Quadrant name (6.5pt, bold) |
| quadrants[].description | string | No | Quadrant description (6pt) |
| quadrants[].color | string | Yes | "coral", "coral_light", "gray_light", "white" |
| sidebar | object | No | Optional right sidebar |

### Realistic Russian Example

```json
{
  "type": "matrix_2x2",
  "title": "Портфель компетенций: Инвестиции и развитие",
  "x_axis": {
    "label": "Текущая силь",
    "low": "Слабая",
    "high": "Сильная"
  },
  "y_axis": {
    "label": "Важность для стратегии",
    "low": "Низкая",
    "high": "Критичная"
  },
  "quadrants": [
    {
      "position": "top_right",
      "label": "A",
      "name": "Защитить & расширить",
      "description": "Лидирующие компетенции; вложить в опыт и инновации",
      "color": "coral"
    },
    {
      "position": "top_left",
      "label": "B",
      "name": "Срочно развивать",
      "description": "Стратегически важно, но слабо развито; требует программа обучения",
      "color": "coral_light"
    },
    {
      "position": "bottom_right",
      "label": "C",
      "name": "Поддерживать",
      "description": "Не критично, но у нас сильно; использовать для доходов",
      "color": "gray_light"
    },
    {
      "position": "bottom_left",
      "label": "D",
      "name": "Аутсорс или отказ",
      "description": "Низкая важность и слабость; передать третьим лицам",
      "color": "white"
    }
  ],
  "sidebar": {
    "title": "ПРИМЕРЫ КОМПЕТЕНЦИЙ",
    "items": [
      {
        "label": "A (Защитить)",
        "value": ["Risk management", "Financial planning"]
      },
      {
        "label": "B (Развивать)",
        "value": ["Data science", "Cloud architecture"]
      }
    ]
  }
}
```

### Special Behavior

- **2×2 Grid**: Fixed 2×2 layout; gaps = 0.02"
- **Axis Labels**: Left and bottom; endpoints (low/high) labeled
- **Quadrant Colors**: Mapped by color name string
- **Accent Bars**: Left coral bars on each quadrant
- **No Sidebar**: Right 37% empty if sidebar omitted

---

## LAYOUT 15: DO_DONT

**Type**: `do_dont`

**Purpose**: Two-column comparison: DO (green, checkmarks) vs DON'T (red/coral, X marks). Each column has header and continuous bullet list. Useful for guidelines, best practices, anti-patterns.

### JSON Schema

```json
{
  "type": "do_dont",
  "title": "Лучшие практики работы с данными",
  "sources": "Data governance guidelines",

  "do_header": "ДЕЛАЕМ ✓",
  "dont_header": "НЕ ДЕЛАЕМ ✗",

  "items": [
    {
      "do": "Документировать источник данных и метаданные",
      "dont": "Использовать данные без понимания их происхождения"
    },
    {
      "do": "Проводить регулярные аудиты качества данных",
      "dont": "Доверять данным без проверки точности"
    },
    {
      "do": "Ограничить доступ по принципу наименьших привилегий",
      "dont": "Давать всем доступ ко всем данным"
    },
    {
      "do": "Архивировать исторические данные по расписанию",
      "dont": "Хранить всё в production системе"
    }
  ],

  "sidebar": {
    "title": "КРИТИЧЕСКИЕ ОБЛАСТИ",
    "items": [
      {
        "label": "Персональные данные",
        "value": "GDPR/CCPA compliance"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "do_dont" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| do_header | string | No | DO column header (default: "ДЕЛАЕМ") |
| dont_header | string | No | DON'T column header (default: "НЕ ДЕЛАЕМ") |
| items | array | Yes | Row pairs |
| items[].do | string | Yes | DO column text |
| items[].dont | string | Yes | DON'T column text |
| sidebar | object | No | Optional right sidebar |

### Realistic Russian Example

```json
{
  "type": "do_dont",
  "title": "Правила успешной реализации инициатив",
  "do_header": "ДЕЛАЕМ ✓",
  "dont_header": "НЕ ДЕЛАЕМ ✗",
  "items": [
    {
      "do": "Четко определить границы и scope проекта",
      "dont": "Начать без четкого плана; менять scope в процессе"
    },
    {
      "do": "Установить измеримые KPI в самом начале",
      "dont": "Определять успех в конце проекта"
    },
    {
      "do": "Регулярно общаться со stakeholders еженедельно",
      "dont": "Общаться только при проблемах"
    },
    {
      "do": "Управлять рисками проактивно",
      "dont": "Реагировать на проблемы после их возникновения"
    },
    {
      "do": "Праздновать quick wins и отмечать успехи команды",
      "dont": "Сосредотачиваться только на том, что осталось сделать"
    }
  ],
  "sidebar": {
    "title": "ЧАСТЫЕ ОШИБКИ",
    "items": [
      {
        "label": "Переоценка ресурсов",
        "value": "Всегда добавьте 30% к плану"
      },
      {
        "label": "Недообщение",
        "value": "Общайтесь чаще, чем кажется нужно"
      }
    ]
  }
}
```

### Special Behavior

- **Two Columns**: Equal width, 0.03" gap
- **Header Bars**: DO = light green (RGBColor(220, 252, 231)) with dark green text; DON'T = coral_light with coral text
- **Checkmarks/X Marks**: Inline with each bullet (✓ for DO, ✗ for DON'T)
- **Continuous Lists**: Single textbox per column; no row division
- **Colors**: Green = #16A34A (do), Red = #FF5850 (dont)

---

## LAYOUT 16: SEGMENT_MATRIX

**Type**: `segment_matrix`

**Purpose**: 3×N matrix with traffic-light color coding (green/yellow/red/gray) for segment status, KPI tracking, or portfolio review. Each cell has label, name, and text. Supports custom column/row headers.

### JSON Schema

```json
{
  "type": "segment_matrix",
  "title": "Портфель рынков: Стратегический обзор",
  "sources": "Market assessment Q4 2024",

  "x_headers": ["Россия", "Казахстан", "Беларусь"],
  "y_headers": ["Рост", "Прибыль", "Риск"],

  "cells": [
    {
      "row": 0,
      "col": 0,
      "label": "↑25%",
      "name": "Сегмент растет",
      "text": "CAGR выше ожиданий",
      "color": "green"
    },
    {
      "row": 0,
      "col": 1,
      "label": "↑18%",
      "name": "Умеренный рост",
      "text": "Ниже плана на 5%",
      "color": "yellow"
    },
    {
      "row": 1,
      "col": 0,
      "label": "32%",
      "name": "Здоровая маржа",
      "text": "На уровне плана",
      "color": "green"
    },
    {
      "row": 2,
      "col": 0,
      "label": "3",
      "name": "Средний риск",
      "text": "Регуляторные изменения",
      "color": "yellow"
    }
  ],

  "sidebar": {
    "title": "СТАТУС-КВО",
    "items": [
      {
        "label": "Зеленые рынки",
        "value": "3 из 9 сегментов"
      },
      {
        "label": "Красные флаги",
        "value": "Беларусь: санкции"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "segment_matrix" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| x_headers | array | Yes | Column headers |
| y_headers | array | Yes | Row headers |
| cells | array | Yes | Cell configurations |
| cells[].row | int | Yes | 0-indexed row |
| cells[].col | int | Yes | 0-indexed column |
| cells[].label | string | Yes | Big label (large, color-coded) |
| cells[].name | string | No | Cell name (6.5pt, bold) |
| cells[].text | string | No | Description (6pt) |
| cells[].color | string | Yes | "green", "yellow", "red", "gray" |
| sidebar | object | No | Optional right sidebar |

### Realistic Russian Example

```json
{
  "type": "segment_matrix",
  "title": "Портфель продуктов: Жизненный цикл и инвестиции",
  "x_headers": ["Карточки", "Кредиты", "Инвестиции", "Страхование"],
  "y_headers": ["Выручка рост", "Маржинальность", "Затраты на операции"],
  "cells": [
    {
      "row": 0,
      "col": 0,
      "label": "+35%",
      "name": "Карточки растут",
      "text": "Вовлечение новых каналов",
      "color": "green"
    },
    {
      "row": 0,
      "col": 1,
      "label": "+8%",
      "name": "Кредиты стабильны",
      "text": "Конкуренция растёт",
      "color": "yellow"
    },
    {
      "row": 0,
      "col": 2,
      "label": "-5%",
      "name": "Инвестиции падают",
      "text": "Отток в конкурентов",
      "color": "red"
    },
    {
      "row": 1,
      "col": 0,
      "label": "38%",
      "name": "Здоровая маржа",
      "text": "Оптимизация комиссий",
      "color": "green"
    },
    {
      "row": 1,
      "col": 1,
      "label": "22%",
      "name": "Сжимающаяся маржа",
      "text": "Требуется реструктуризация",
      "color": "yellow"
    },
    {
      "row": 2,
      "col": 0,
      "label": "12%",
      "name": "Оптимизированы",
      "text": "RPA внедрена на 60%",
      "color": "green"
    },
    {
      "row": 2,
      "col": 3,
      "label": "18%",
      "name": "Остаётся ручная работа",
      "text": "Неправильное распределение ресурсов",
      "color": "red"
    }
  ],
  "sidebar": {
    "title": "ПРИОРИТЕТЫ",
    "items": [
      {
        "label": "Ближайшие 90 дней",
        "value": ["Спасать инвестиции", "Оптимизировать затраты страховки"]
      },
      {
        "label": "Долгоterm",
        "value": "Трансформировать кредитный портфель"
      }
    ]
  }
}
```

### Color Map (Traffic Light)

| Color | Background | Border | Label | Meaning |
|-------|-----------|--------|-------|---------|
| green | RGBColor(209, 250, 229) | RGBColor(16, 185, 129) | RGBColor(5, 150, 105) | Healthy |
| yellow | RGBColor(254, 243, 199) | RGBColor(245, 158, 11) | RGBColor(180, 83, 9) | Caution |
| red | RGBColor(254, 226, 226) | RGBColor(239, 68, 68) | RGBColor(185, 28, 28) | Alert |
| gray | GRAY_LIGHT | GRAY_BORDER | GRAY_MED | No data |

### Special Behavior

- **Dynamic Grid**: N × M matrix; no fixed size limit
- **Traffic Light Coloring**: Auto-applied per cell color string
- **Empty Cells**: Render as white with light gray border
- **Thicker Borders**: 1.0pt vs standard 0.3pt (more visual emphasis)
- **Adaptive Font**: Label size increases with text length

---

## LAYOUT 17: GOALS_ROWS

**Type**: `goals_rows`

**Purpose**: Numbered goals/objectives with big left number cell (CORAL) and right text cell (heading + description + optional target KPI). One goal per row; supports unlimited rows.

### JSON Schema

```json
{
  "type": "goals_rows",
  "title": "Стратегические цели на 2025-2026",
  "sources": "Strategic plan FY2025",

  "goals": [
    {
      "number": "01",
      "heading": "Увеличить выручку на 30%",
      "text": "Вывести 3 новых продукта на рынок, расширить присутствие в 5 регионах",
      "target": "Целевой доход: 3.5 млрд руб (vs. 2.7 млрд в 2024)"
    },
    {
      "number": "02",
      "heading": "Улучшить NPS на 15 пунктов",
      "text": "Трансформировать customer journey, внедрить AI-поддержку в contact center",
      "target": "Целевой NPS: 65+ (текущий 50)"
    },
    {
      "number": "03",
      "heading": "Снизить операционные затраты на 20%",
      "text": "Автоматизировать 80% ручных процессов через RPA, оптимизировать организационную структуру",
      "target": "Экономия: 400 млн руб в год"
    },
    {
      "number": "04",
      "heading": "Удержать ключевых талантов (текучесть < 10%)",
      "text": "Внедрить программу лидерства, повысить зарплаты на 15%, создать карьерные пути",
      "target": "Текучесть сейчас 18% → целевая 8%"
    }
  ],

  "sidebar": {
    "title": "КРИТЕРИИ УСПЕХА",
    "items": [
      {
        "label": "OKR фокус",
        "value": "2-3 цели за квартал"
      },
      {
        "label": "Review цикл",
        "value": "Еженедельно с Executive team"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | Yes | "goals_rows" |
| title | string | No | Slide title |
| sources | string | No | Source attribution |
| goals | array | Yes | Goal rows |
| goals[].number | string | No | Goal number (default: 01, 02, etc.; 22pt, bold, white) |
| goals[].heading | string | Yes | Goal title (9pt, bold, dark) |
| goals[].text | string | Yes | Description/approach |
| goals[].target | string | No | Target KPI or metric (coral, bold) |
| sidebar | object | No | Optional right sidebar |

### Realistic Russian Example

```json
{
  "type": "goals_rows",
  "title": "Цели трансформации: Следующие 24 месяца",
  "goals": [
    {
      "number": "1",
      "heading": "Цифровая зрелость Level 3",
      "text": "Переход с Legacy систем на облачную архитектуру, внедрение API-first подхода, Data mesh для аналитики",
      "target": "IT budget: 200 млн руб; ROI: 280% к 2027"
    },
    {
      "number": "2",
      "heading": "Культура инноваций и экспериментирования",
      "text": "Запуск Innovation lab, выделение 10% времени на side projects, награды за эксперименты (успех и неудачи)",
      "target": "50+ инициатив, 8+ внутренних стартапов"
    },
    {
      "number": "3",
      "heading": "Лидерство в sustainability",
      "text": "Углеродная нейтральность к 2030, переход на 100% возобновляемые источники, ESG интеграция в бизнес-решения",
      "target": "Сокращение выбросов на 50% к 2026"
    }
  ],
  "sidebar": {
    "title": "УПРАВЛЕНИЕ ПРОГРЕССОМ",
    "items": [
      {
        "label": "Quarterly reviews",
        "value": "Board-level review"
      },
      {
        "label": "Compensation tied to",
        "value": "OKR achievement (40%)"
      }
    ]
  }
}
```

### Special Behavior

- **Number Cells**: CORAL background, white text, 22pt bold, no borders
- **Text Cells**: WHITE or alternating CORAL_LIGHT background; accent bar on left
- **Alternating Rows**: CORAL_LIGHT for even indices; WHITE for odd
- **Gap Between Rows**: 0.008" (minimal spacing)
- **Target Highlight**: Coral color, slightly larger (bold, +0.5pt)
- **No Max Rows**: Supports unlimited goals

---

## LAYOUT DISPATCHER

All 17 layouts are registered in the `LAYOUTS` dictionary:

```python
LAYOUTS = {
    'table_sidebar': build_table_sidebar,      # 1
    'from_to': build_from_to,                  # 2
    'comparison': build_comparison,            # 3
    'process_detail': build_process_detail,    # 4
    'rasci': build_rasci,                      # 5
    'stage_gate': build_stage_gate,            # 6
    'brand_pyramid': build_brand_pyramid,      # 7
    'mechanism_card': build_mechanism_card,    # 8
    'roadmap_swimlane': build_roadmap_swimlane,# 9
    'title_dark': build_title_dark,            # 10
    'exec_summary': build_exec_summary,        # 11
    'divider': build_divider,                  # 12
    'next_steps': build_next_steps,            # 13
    'matrix_2x2': build_matrix_2x2,            # 14
    'do_dont': build_do_dont,                  # 15
    'segment_matrix': build_segment_matrix,    # 16
    'goals_rows': build_goals_rows,            # 17
}
```

---

## INVOCATION EXAMPLE

```bash
python3 generator_structural.py base_structural.pptx config.json --output output.pptx
```

Where `config.json` contains:

```json
[
  {
    "type": "title_dark",
    "title": "Трансформация операций",
    "subtitle": "Путь к миру",
    "date": "Февраль 2025",
    "company": "Acme Corp"
  },
  {
    "type": "table_sidebar",
    "title": "Текущее состояние",
    "table": {
      "headers": ["Метрика", "Текущее", "Целевое"],
      "rows": [
        {"cells": ["Выручка", "100 млн", "150 млн"]},
        {"cells": ["Маржа", "20%", "35%"]}
      ]
    }
  },
  {
    "type": "divider",
    "track_number": "ТРЕК 1",
    "track_name": "Стратегия",
    "governing_thought": "Правильная стратегия требует смелости"
  }
]
```

---

## KEY DESIGN PATTERNS

1. **Consistent Spacing**: 0.25" margins, 0.05" sidebar gap
2. **Adaptive Typography**: font-size scales with content; always readable
3. **Color Hierarchy**: CORAL for action/primary, GRAY_DARK for structure, GRAY_MED for secondary
4. **Accent Bars**: Left 0.025" coral bars on primary cells for visual flow
5. **Sidebar Reuse**: Standard 37% right sidebar used across 8+ layouts
6. **Grid Flexibility**: Most layouts support variable columns/rows
7. **Dark Dividers**: Title_dark and divider use full GRAY_DARK background for section breaks

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Text too small | Reduce content length or increase cell height |
| Text overflow | Lower font sizes in config or shorten strings |
| Sidebar empty | Provide `sidebar` object or omit key entirely |
| Colors not matching | Check color names (must match CORAL, GRAY_DARK, etc.) |
| RASCI codes undefined | Add custom `color_map` or use default R/A/S/C/I |
| Row heights uneven | Rows auto-split; ensure all rows have data |

---

---

## 18. ISSUE TREE (decision_tree, solution_tree)

**Type**: `issue_tree` | **Category**: structural | **Aliases**: `decision_tree`, `solution_tree`

McKinsey-style hierarchical L→R tree with bracket connectors. Root question at left, branches spreading right through sub-questions, hypotheses, and evidence.

### JSON Schema

```json
{
  "type": "issue_tree",
  "title": "Action title — вывод в заголовок",
  "root": {
    "text": "Корневой вопрос / проблема",
    "children": [
      {
        "text": "Ветка уровня 1",
        "children": [
          {"text": "Лист уровня 2"},
          {"text": "Лист уровня 2"}
        ]
      },
      {
        "text": "Ветка уровня 1",
        "children": [
          {"text": "Лист уровня 2"},
          {"text": "Лист уровня 2"}
        ]
      }
    ]
  },
  "sources": "Источник данных"
}
```

### Design Specs

| Element | Spec |
|---------|------|
| Max depth | 5 levels (0-indexed: root = level 0) |
| Root column | Slightly wider (+0.15") for 3+ levels |
| Column gap | 0.22" (bracket connectors drawn here) |
| Node height | Capped at 0.70", min 0.22" |
| Vertical gap | 0.04" between sibling nodes |
| Root BG | CORAL, text WHITE, bold, center-aligned |
| Level 1 BG | CORAL_LIGHT, text GRAY_DARK |
| Level 2 BG | CELL_ALT_BG (#F9FAFB), text GRAY_DARK |
| Level 3+ BG | WHITE, border GRAY_BORDER |
| Font size | Root: 7–9pt adaptive; children: 6–7.5pt adaptive |
| Connectors | Bracket style: horizontal→vertical→horizontal, GRAY_BORDER, 0.75pt |

### Vertical Space Allocation

Space allocated proportional to leaf count: if a branch has 3 leaves and its sibling has 2, they get 60%/40% of available height respectively.

### When to Use

- MECE decomposition of a problem
- Decision trees (if/then logic)
- Hypothesis-driven analysis (McKinsey style)
- Factor analysis: "why" breakdowns

---

## 19. QUOTE (interview, testimonial)

**Type**: `quote` | **Category**: structural | **Aliases**: `interview`, `testimonial`

BCG-style minimal quote slide with decorative quotation mark, attribution bar, and optional context line.

### JSON Schema

```json
{
  "type": "quote",
  "title": "Action title",
  "quote": "Текст цитаты — полная фраза респондента.",
  "attribution": "Имя / должность",
  "role": "Компания / контекст роли",
  "context": "Когда/где получена цитата (опционально)",
  "sources": "Источник данных"
}
```

### Field Aliases

| Canonical | Alias |
|-----------|-------|
| `quote` | `text` |
| `attribution` | `author` |

### Design Specs

| Element | Spec |
|---------|------|
| Quote BG | CORAL_LIGHT box, full content width |
| Left accent | Coral accent bar (0.025") |
| Decorative mark | Unicode `"` (opening curly), 42pt CORAL bold |
| Quote text | Italic, GRAY_DARK, left-aligned |
| Attribution bar | Full-width CORAL bar: `— Name, Role` in WHITE, 8pt bold |
| Context line | Italic, 6.5pt, GRAY_MED (optional) |

### Adaptive Font Sizing

| Quote length | Font size |
|-------------|-----------|
| < 60 chars | 16pt |
| < 100 chars | 14pt |
| < 160 chars | 12pt |
| < 250 chars | 10pt |
| < 400 chars | 9pt |
| 400+ chars | 8pt |

### When to Use

- Customer voice / voice of the customer
- Interview excerpts (depth interviews, CustDev)
- Expert opinions with attribution
- Testimonials for case studies

---

## 20. PYRAMID (minto_pyramid, argument_pyramid)

**Type**: `pyramid` | **Category**: structural | **Aliases**: `minto_pyramid`, `argument_pyramid`

Minto Pyramid Principle: stacked centered tiers from recommendation (top) through arguments to evidence (bottom). Different from `brand_pyramid` which uses vertical letter-coded boxes.

### JSON Schema

```json
{
  "type": "pyramid",
  "title": "Action title",
  "tiers": [
    {
      "label": "РЕКОМЕНДАЦИЯ",
      "text": "Тезис — главный вывод"
    },
    {
      "label": "АРГУМЕНТЫ",
      "text": "Аргумент 1 | Аргумент 2 | Аргумент 3"
    },
    {
      "label": "ДОКАЗАТЕЛЬСТВА",
      "text": "Факт 1 | Факт 2 | Факт 3"
    }
  ],
  "sources": "Источник данных"
}
```

### Design Specs

| Element | Spec |
|---------|------|
| Max tiers | 4 |
| Tier gap | 0.03" |
| Width interpolation | Top tier: 35% of AVAIL_W → bottom tier: 100% of AVAIL_W |
| Centering | Each tier centered horizontally |
| Tier 0 (top) | CORAL bg, WHITE text, bold |
| Tier 1 | CORAL_LIGHT bg, GRAY_DARK text |
| Tier 2 | CELL_ALT_BG (#F9FAFB), GRAY_DARK text |
| Tier 3 | WHITE bg, GRAY_BORDER border |
| Label | Uppercase, smaller font (6-7pt), CORAL for tier 0 / GRAY_MED for others |
| Text | Larger font (7-9pt adaptive), below label |
| Separator | Pipe `|` in text → visually separates sub-arguments |

### Width Formula

```
w_frac = 0.35 + 0.65 * tier_index / (n_tiers - 1)
tier_width = AVAIL_W * w_frac
```

### When to Use

- Recommendation with supporting arguments (McKinsey Minto)
- MECE argument structure
- "Why should we do X?" slide
- Thesis → evidence hierarchy

### Difference from brand_pyramid

| | `pyramid` | `brand_pyramid` |
|--|-----------|----------------|
| Direction | Top-down stacked tiers | Bottom-up vertical boxes |
| Purpose | Minto argument structure | Brand/EVP architecture |
| Visual | Triangle shape (narrow top → wide bottom) | Equal-width lettered tiers |
| Data | `tiers: [{label, text}]` | `tiers: [{letter, label, items}]` |

---

**Version 1.1** | Paper Planes Consulting | Mar 2026
