## Примеры JSON конфигов

### SCQA слайд
```json
{
  "type": "scqa",
  "title": "Action Title — главный вывод",
  "columns": [
    {
      "header": "Action title левой колонки",
      "content": [
        {"text": "Факт с цифрой", "bold": true, "size": 11},
        {"text": "Развёрнутое объяснение", "bullet": true, "size": 10}
      ]
    },
    {
      "header": "Action title центральной",
      "content": [
        {"text": "Проблема", "bold": true, "coral": true},
        {"text": "Детали", "bullet": true}
      ]
    },
    {
      "header": "Рекомендации",
      "content": [
        {"text": "① Действие 1", "bold": true},
        {"text": "Детали", "bullet": true},
        {"text": "Ожидаемый эффект", "bold": true, "coral": true}
      ],
      "highlight": true
    }
  ],
  "sources": "Источник 1, Источник 2"
}
```

### Таблица с Harvey Balls и RAG
```json
{
  "type": "table",
  "title": "Конкуренты отстают по 3 из 5 параметров",
  "table_data": [
    ["Критерий", "Мы", "Конкурент X", "Конкурент Y"],
    ["NPS", "HB:50", "HB:75", "HB:25"],
    ["Приложение", "RAG:red", "RAG:green", "RAG:yellow"],
    ["Лояльность", "RAG:green", "RAG:yellow", "RAG:red"]
  ],
  "col_widths": [3, 2.5, 2.5, 2.5],
  "notes": ["NPS: ◔ 25% ◑ 50% ◕ 75%"],
  "sources": "Бенчмаркинг Q1 2026"
}
```

### Таблица с highlights и trend-индикаторами
```json
{
  "type": "table",
  "title": "Два продукта показывают устойчивый рост, TDR требует внимания",
  "table_data": [
    ["Продукт", "Выручка Q1", "Выручка Q2", "Динамика", "Маржа"],
    ["TDR Platform", "45.2M₽", "52.8M₽", "trend:up:+17%", "64%"],
    ["SOC Service", "28.5M₽", "34.2M₽", "trend:up:+20%", "74%"],
    ["Consulting", "18.3M₽", "17.1M₽", "trend:down:-7%", "48%"],
    ["Legacy", "12.0M₽", "12.0M₽", "trend:flat:0%", "35%"]
  ],
  "highlights": {
    "columns": [3],
    "cells": [[3, 4]]
  },
  "sources": "Финансовый отчёт Q2 2026"
}
```

**Формат trend**: `"trend:up:+15%"` → ↑ +15% (зелёный), `"trend:down:-8%"` → ↓ −8% (красный), `"trend:flat:0%"` → → 0% (серый).

**Формат highlights**: `columns` — выделить колонки coral_light, `rows` — строки, `cells` — отдельные ячейки [row, col].

### Универсальный параметр `takeaway`

Любой слайд может иметь takeaway box — коралловая рамка с ключевым выводом над источниками:
```json
{
  "type": "chart",
  "title": "Выручка восстановится к Q4",
  "chart_type": "column",
  "categories": ["Q1", "Q2", "Q3", "Q4"],
  "series": [{"name": "Выручка", "values": [100, 85, 95, 110]}],
  "takeaway": "Ключевой вывод: рост на 30% к Q4 потребует инвестиций в маркетинг 15M₽",
  "sources": "Финансовая модель v3.2"
}
```

### График с фактами
```json
{
  "type": "chart",
  "title": "Выручка восстановится к Q4",
  "chart_type": "column",
  "categories": ["Q1", "Q2", "Q3", "Q4"],
  "series": [
    {"name": "Выручка", "values": [100, 85, 95, 110]}
  ],
  "facts": [
    {"text": "Драйверы роста:", "bold": true},
    {"text": "Сокращение доставки до 2 дней", "bullet": true}
  ],
  "sources": "Финансовая модель v3.2"
}
```

### Большая метрика
```json
{
  "type": "data",
  "title": "Падение выручки на 15% требует срочных мер",
  "metric_value": "−15%",
  "metric_label": "падение выручки Q2 vs Q1",
  "trend": "down",
  "facts": [
    {"text": "Основная причина — логистика", "bold": true}
  ],
  "sources": "Финансовый отчёт Q2 2026"
}
```

### Waterfall (мостовая диаграмма)
```json
{
  "type": "waterfall",
  "title": "Рост выручки на 15M обеспечен тремя факторами",
  "subtitle": "Декомпозиция изменения выручки Q1→Q2, млн ₽",
  "items": [
    {"label": "Выручка Q1", "value": 100, "type": "total"},
    {"label": "Новые клиенты", "value": 20, "type": "relative"},
    {"label": "Рост среднего чека", "value": 8, "type": "relative"},
    {"label": "Отток клиентов", "value": -13, "type": "relative"},
    {"label": "Выручка Q2", "value": 115, "type": "total"}
  ],
  "facts": [
    {"text": "Драйверы роста:", "bold": true},
    {"text": "Маркетинговая кампания дала +20M новых клиентов", "bullet": true},
    {"text": "Программа лояльности увеличила чек на 8%", "bullet": true}
  ],
  "sources": "Финансовый отчёт Q2 2026, CRM-аналитика"
}
```

### 2x2 Matrix (BCG, Risk-Impact)
```json
{
  "type": "matrix",
  "title": "3 из 5 продуктов требуют стратегических решений",
  "subtitle": "BCG-матрица портфеля продуктов",
  "quadrants": ["Звёзды", "Вопросы", "Собаки", "Дойные коровы"],
  "x_axis": "Доля рынка",
  "y_axis": "Рост рынка",
  "items": [
    {"label": "Продукт A", "x": 0.8, "y": 0.7, "size": 40},
    {"label": "Продукт B", "x": 0.3, "y": 0.8, "size": 25},
    {"label": "Продукт C", "x": 0.7, "y": 0.3, "size": 50},
    {"label": "Продукт D", "x": 0.2, "y": 0.2, "size": 15},
    {"label": "Продукт E", "x": 0.6, "y": 0.9, "size": 30}
  ],
  "sources": "Анализ рынка Q1 2026, внутренняя аналитика"
}
```

### Sankey (диаграмма потоков)
```json
{
  "type": "sankey",
  "title": "40% лидов теряется на этапе квалификации",
  "subtitle": "Воронка продаж, количество лидов",
  "nodes": [
    "Входящие лиды",
    "Квалифицированные",
    "Презентация",
    "Предложение",
    "Сделка",
    "Отказ (квалификация)",
    "Отказ (презентация)",
    "Отказ (предложение)"
  ],
  "links": [
    {"source": 0, "target": 1, "value": 600},
    {"source": 0, "target": 5, "value": 400},
    {"source": 1, "target": 2, "value": 450},
    {"source": 1, "target": 6, "value": 150},
    {"source": 2, "target": 3, "value": 300},
    {"source": 2, "target": 7, "value": 150},
    {"source": 3, "target": 4, "value": 200}
  ],
  "sources": "CRM-аналитика Q1 2026"
}
```

### Treemap (иерархическая структура)
```json
{
  "type": "treemap",
  "title": "70% выручки генерируют 2 категории из 5",
  "subtitle": "Структура выручки по категориям продуктов",
  "value_suffix": "M₽",
  "data": [
    {"label": "Всего", "parent": "", "value": 0},
    {"label": "Электроника", "parent": "Всего", "value": 0},
    {"label": "Смартфоны", "parent": "Электроника", "value": 45},
    {"label": "Ноутбуки", "parent": "Электроника", "value": 25},
    {"label": "Одежда", "parent": "Всего", "value": 0},
    {"label": "Мужская", "parent": "Одежда", "value": 15},
    {"label": "Женская", "parent": "Одежда", "value": 10},
    {"label": "Прочее", "parent": "Всего", "value": 5}
  ],
  "sources": "Финансовый отчёт 2025"
}
```

### From-To (трансформация AS IS → TO BE)
```json
{
  "type": "from_to",
  "title": "Трансформация TTM требует изменения 5 ключевых процессов",
  "subtitle": "От последовательного к параллельному выполнению",
  "from_label": "AS IS (6 мес.)",
  "to_label": "TO BE (2 мес.)",
  "from_state": [
    {"text": "Последовательное выполнение", "bold": true},
    {"text": "Каждый этап ждёт предыдущий", "bullet": true},
    {"text": "Аналитика после испытаний", "bold": true, "space_before": 10},
    {"text": "+4-6 недель к сроку", "bullet": true},
    {"text": "Обучение после прихода товара", "bold": true, "space_before": 10},
    {"text": "+2-3 недели ожидания", "bullet": true}
  ],
  "to_state": [
    {"text": "Параллельное выполнение", "bold": true},
    {"text": "Процессы запускаются одновременно", "bullet": true},
    {"text": "Аналитика сразу после ввоза", "bold": true, "space_before": 10},
    {"text": "−6 недель экономии", "bullet": true},
    {"text": "Обучение параллельно с доставкой", "bold": true, "space_before": 10},
    {"text": "−3 недели экономии", "bullet": true}
  ],
  "sources": "Gap-анализ TTM, best practices Henry Schein / Dentsply Sirona"
}
```

### Funnel (воронка конверсии)
```json
{
  "type": "funnel",
  "title": "Воронка вывода нового продукта показывает 3 критичных барьера",
  "subtitle": "Анализ конверсии по этапам TTM",
  "stages": [
    {
      "name": "Идентификация",
      "value": 100,
      "conversion": "100%",
      "details": "Все потенциальные продукты"
    },
    {
      "name": "Анализ рынка",
      "value": 65,
      "conversion": "65%",
      "details": "−35% отсеяно по ёмкости рынка"
    },
    {
      "name": "Испытания",
      "value": 40,
      "conversion": "62%",
      "details": "−25% не прошли сертификацию"
    },
    {
      "name": "Пилот",
      "value": 20,
      "conversion": "50%",
      "details": "−20% низкая конверсия в продажи"
    },
    {
      "name": "Масштабирование",
      "value": 8,
      "conversion": "40%",
      "details": "−12% проблемы с логистикой"
    }
  ],
  "sources": "Данные отдела развития 2024-2025, n=47 продуктов"
}
```

### Mermaid (flowchart, sequence, gantt)
```json
{
  "type": "mermaid",
  "title": "Процесс обработки заказа занимает 5 дней",
  "subtitle": "Текущий бизнес-процесс",
  "mermaid_code": "flowchart LR\n    A[Заказ] --> B{Наличие}\n    B -->|Есть| C[Сборка]\n    B -->|Нет| D[Закупка]\n    D --> C\n    C --> E[Доставка]\n    E --> F[Клиент]",
  "facts": [
    {"text": "Узкие места:", "bold": true},
    {"text": "Закупка добавляет 3 дня к сроку", "bullet": true, "coral": true},
    {"text": "Сборка — единственный склад в Москве", "bullet": true}
  ],
  "sources": "Интервью с операционным директором"
}
```

**Примеры Mermaid-кода:**

Flowchart:
```
flowchart TD
    A[Начало] --> B{Решение}
    B -->|Да| C[Действие 1]
    B -->|Нет| D[Действие 2]
    C --> E[Конец]
    D --> E
```

Sequence diagram:
```
sequenceDiagram
    Клиент->>Сервер: Запрос
    Сервер->>БД: Query
    БД-->>Сервер: Данные
    Сервер-->>Клиент: Ответ
```

Gantt chart:
```
gantt
    title Таймлайн проекта
    dateFormat YYYY-MM-DD
    section Фаза 1
    Анализ :a1, 2024-01-01, 30d
    Дизайн :a2, after a1, 20d
    section Фаза 2
    Разработка :b1, after a2, 45d
```

### SWOT-анализ
```json
{
  "type": "swot",
  "title": "Компания X обладает сильными позициями, но требует развития партнёрской сети",
  "subtitle": "SWOT-анализ конкурентной позиции",
  "strengths": [
    {"text": "Технологическое лидерство", "bold": true, "size": 9},
    {"text": "Собственная платформа с ML-моделями, превосходящая аналоги на 40%", "bullet": true, "size": 9},
    {"text": "Финансовая устойчивость", "bold": true, "size": 9, "space_before": 6},
    {"text": "Поддержка холдинга обеспечивает стабильное R&D", "bullet": true, "size": 9}
  ],
  "weaknesses": [
    {"text": "Ограниченная дистрибуция", "bold": true, "size": 9},
    {"text": "Партнёрская сеть 45 компаний vs 200+ у лидеров", "bullet": true, "size": 9}
  ],
  "opportunities": [
    {"text": "Рост рынка на 20% CAGR к 2027", "bold": true, "size": 9},
    {"text": "Импортозамещение создаёт спрос", "bullet": true, "size": 9}
  ],
  "threats": [
    {"text": "Агрессивная конкуренция", "bold": true, "size": 9},
    {"text": "Positive Technologies инвестирует 5 млрд ₽/год в маркетинг", "bullet": true, "size": 9}
  ],
  "sources": "Анализ рынка 2025, интервью с руководством"
}
```

### Блоки со связями (flow_blocks)
```json
{
  "type": "flow_blocks",
  "title": "Ключевые точки взаимодействия требуют автоматизации",
  "subtitle": "Процесс работы с клиентом",
  "blocks": [
    {
      "header": "Product Owner",
      "color": "coral",
      "content": [
        {"text": "Управление бэклогом", "bold": true, "size": 9},
        {"text": "Приоритизация по ICE-скорингу", "bullet": true, "size": 9},
        {"text": "Связь с Pre-sell", "bold": true, "size": 9, "space_before": 6},
        {"text": "Передача требований в roadmap", "bullet": true, "size": 9}
      ]
    },
    {
      "header": "Pre-sell",
      "color": "gray",
      "content": [
        {"text": "Квалификация лидов", "bold": true, "size": 9},
        {"text": "BANT-скоринг, конверсия 65%", "bullet": true, "size": 9}
      ]
    },
    {
      "header": "Сервис-менеджеры",
      "color": "green",
      "content": [
        {"text": "Онбординг за 14 дней (SLA)", "bold": true, "size": 9},
        {"text": "NPS 72, CSAT 4.2/5.0", "bullet": true, "size": 9}
      ]
    }
  ],
  "sources": "CRM Salesforce, Customer Success дашборд"
}
```

### Шевронный процесс (chevron_process)
```json
{
  "type": "chevron_process",
  "title": "Внедрение займёт 4 этапа и 6 месяцев от анализа до масштабирования",
  "subtitle": "Дорожная карта трансформации TTM",
  "stages": [
    {"name": "Анализ", "description": "Аудит текущих процессов и определение точек потерь", "metric": "2 мес."},
    {"name": "Пилот", "description": "Запуск на 3 категориях товаров", "metric": "1.5 мес."},
    {"name": "Оптимизация", "description": "Доработка на основе результатов пилота", "metric": "1 мес."},
    {"name": "Масштабирование", "description": "Распространение на все категории", "metric": "1.5 мес."}
  ],
  "facts": [
    {"text": "Ожидаемые результаты:", "bold": true},
    {"text": "Сокращение TTM с 6 до 2 месяцев", "bullet": true},
    {"text": "Экономия 12M₽ в год на логистике", "bullet": true},
    {"text": "Рост SKU в активном ассортименте на 40%", "bullet": true, "coral": true}
  ],
  "sources": "Стратегическая сессия, best practices Henry Schein"
}
```

### Пронумерованный список (numbered_list)
```json
{
  "type": "numbered_list",
  "title": "6 приоритетных действий для сокращения TTM до 2 месяцев",
  "subtitle": "Рекомендации по итогам стратегической сессии",
  "items": [
    {"number": 1, "title": "Параллельный запуск процессов", "description": "Совместить анализ рынка, сертификацию и обучение — экономия 6 недель"},
    {"number": 2, "title": "Цифровой каталог продуктов", "description": "Внедрить PIM-систему для автоматизации описаний и характеристик товаров"},
    {"number": 3, "title": "Партнёрская программа обучения", "description": "Запустить онлайн-платформу для дилеров с сертификацией до прихода товара"},
    {"number": 4, "title": "KPI-дашборд TTM", "description": "Еженедельный мониторинг сроков по каждому этапу pipeline"},
    {"number": 5, "title": "Экспресс-сертификация", "description": "Заключить договор с лабораторией на ускоренное тестирование (5 дней вместо 21)"},
    {"number": 6, "title": "Логистический хаб в регионах", "description": "Открыть 3 промежуточных склада для сокращения Last Mile с 7 до 2 дней"}
  ],
  "sources": "Стратегическая сессия, gap-анализ TTM"
}
```

### График + таблица (chart_table)
```json
{
  "type": "chart_table",
  "title": "Рост выручки обеспечен новыми клиентами, но средний чек снижается",
  "subtitle": "Динамика показателей Q1-Q4 2025",
  "layout": "left-right",
  "chart_config": {
    "type": "column",
    "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": [{"name": "Выручка, млн ₽", "values": [42, 48, 55, 62]}]
  },
  "table_data": [
    ["Показатель", "Q1", "Q2", "Q3", "Q4"],
    ["Новые клиенты", "12", "15", "18", "22"],
    ["Средний чек, тыс. ₽", "3 500", "3 200", "3 055", "2 818"],
    ["Конверсия, %", "18%", "21%", "19%", "23%"]
  ],
  "sources": "CRM Salesforce, финансовый отчёт 2025"
}
```

### Несколько таблиц (multi_table)
```json
{
  "type": "multi_table",
  "title": "Все три продукта показали рост, но маржинальность TDR требует внимания",
  "subtitle": "Финансовые показатели Q1 2026",
  "layout": "horizontal",
  "tables": [
    {
      "header": "TDR Platform",
      "data": [
        ["Метрика", "Q4", "Q1", "Δ"],
        ["Выручка, млн ₽", "45.2", "52.8", "+17%"],
        ["Маржа", "68%", "64%", "-4пп"],
        ["Клиенты", "42", "51", "+21%"]
      ]
    },
    {
      "header": "SOC as a Service",
      "data": [
        ["Метрика", "Q4", "Q1", "Δ"],
        ["Выручка, млн ₽", "28.5", "34.2", "+20%"],
        ["Маржа", "72%", "74%", "+2пп"],
        ["Клиенты", "18", "24", "+33%"]
      ]
    },
    {
      "header": "Consulting",
      "data": [
        ["Метрика", "Q4", "Q1", "Δ"],
        ["Выручка, млн ₽", "18.3", "21.0", "+15%"],
        ["Маржа", "45%", "48%", "+3пп"],
        ["Проекты", "12", "15", "+25%"]
      ]
    }
  ],
  "sources": "1С:ERP, финансовый отчёт Q1 2026"
}
```

