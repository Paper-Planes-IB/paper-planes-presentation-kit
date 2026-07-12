---
name: "commercial-proposal-generator"
description: "|"
---

# Commercial Proposal Generator

Скилл для создания КП консалтинговых проектов Paper Planes.
Принимает входные данные любой полноты, дозапрашивает недостающее, генерирует КП.

## Workflow

```
0. Прочитать PP Knowledge Base: Notes/Work/PP Knowledge Base.md
   Подтянуть: кейсы (секция 8), бюджет (секция 7), методологии (секция 4), артефакты (секция 6)
1. Принять бриф -> распарсить -> классифицировать тип проекта
2. Проверить минимальный вход -> дозапросить недостающее
3. Сформировать структуру КП -> показать пользователю для подтверждения
4. Написать контент секций (правила: references/quality_checklist.md)
5. Прогнать по Quality Scoring (6 вопросов, цель 100%)
6. Уточнить формат выхода (PPTX / Gamma / оба)
7. PPTX: storyboard -> JSON-конфиги -> consulting-slides-creator
8. Gamma (если выбран): gamma_export.py с темой PP
```

## Минимальный вход (без этого КП не пишется)

- Конкретная управленческая проблема (не тема)
- Горизонт проекта (сроки)
- Тип решения (стратегия / аналитика / оргмодель / продажи)
- Ожидаемый уровень конкретики

Расширенный бриф (4 блока: контекст, цель, ограничения, формат): `references/client_brief.md`

## Ключевые правила

1. **Пирамида Минто**: вывод, затем логика, затем детали
2. **SCQA**: каждая секция = Situation + Complication + Question + Answer
3. **Action titles**: вывод в 3-5 слов (тест Маккинзи: заголовки подряд = связная история)
4. **Результат != процесс**: формулировать как изменение состояния
5. **Количественные обязательства**: N интервью, M конкурентов, охват %
6. **Стоимость из состава работ**: обоснована трудозатратами, не декларативна
7. **Стоп-лист**: уникальный, революционный, комплексный подход, повышение эффективности (без метрики)
8. **divider запрещен** (обучение Балахнина 21.03.2026)
9. **Storyboard обязателен**: перед PPTX согласовать слайды и titles с пользователем
10. **SOSTAC**: Situation -> Objectives -> Strategy -> Tactics -> Action -> Control

## Knowledge Hub

При подготовке КП проверять прошлые предложения для переиспользования:
- `Notes/Work/PP Knowledge Base.md` — кейсы, методологии, ценообразование
- `references/gold-standard-patterns.md` — паттерны из 56 реальных КП PP
- `references/pp-methodology-notion.md` — описания методологий
- Notion: поиск по клиенту/отрасли для контекста прошлых проектов
- Vault: `Notes/Work/` — заметки по прошлым проектам, approach notes

Цель: не писать с нуля то, что уже отработано. Адаптировать проверенные блоки под нового клиента.

## References

| Файл | Содержание |
|------|-----------|
| `references/proposal_templates.md` | Структура КП, скелет секций, типы проектов, Gold Standard |
| `references/pricing_examples.md` | Ценообразование, бюджетные ориентиры, scope |
| `references/client_brief.md` | Опросник брифа, минимальный/расширенный вход |
| `references/slides_integration.md` | Маппинг секций -> slide types, Gamma API, JSON-конфиги |
| `references/quality_checklist.md` | Чеклист качества, scoring, тон и стиль, стоп-лист |
| `references/gold-standard-patterns.md` | Паттерны из 56 реальных КП Paper Planes |
| `references/pp-methodology-notion.md` | Описания методологий PP |
| `references/brief-template.md` | Шаблон брифа |
| `references/tone-and-language.md` | Справочник формулировок |

## MANUAL MIGRATION REQUIRED

Review unsupported Claude skill fields manually: `MANDATORY TRIGGERS`, `Выход`, `Гибридный режим`, `Опционально`.
