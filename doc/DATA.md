# Данные и назначение репозитория

Документ описывает, **какие данные** использует учебный RAG, **откуда** они взяты и **что именно** попадает в индекс.

**Автор:** Силин Иван Андреевич

---

## Назначение репозитория

**Для кого:** студенты и начинающие разработчики, которые учатся строить RAG с нуля.

**Что демонстрирует:**

- полный offline-pipeline: сырые данные → документы → чанки → TF-IDF индекс → поиск → demo-ответ;
- ответ **только по найденным фрагментам** с указанием источника (`doc_id`, score);
- явный **отказ**, если релевантного контекста нет;
- Streamlit UI для интерактивной проверки на реальном корпусе из 1500 отзывов.

**Границы MVP:**

- поиск по **словам** (TF-IDF), не embeddings и не LLM;
- demo-режим без внешних API;
- корпус: **1500 отзывов** → **1597 чанков** после нарезки;
- не production-система, а **учебный RAG** на открытых данных Amazon.

---

## Источники данных

| Источник | Файл в проекте | Комментарий |
|----------|----------------|-------------|
| [Amazon Electronics Reviews (Kaggle)](https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products) | `data/raw/1429_1.csv` | Сырой CSV (~41k строк). **Не коммитится** — см. `.gitignore`. |
| Подготовленный корпус | `data/raw/datasets.json` | 1500 записей: `id`, `name` (заголовок отзыва), `text`. **Коммитится**. |
| Скрипт подготовки | `data/raw/extract.py` | Извлекает `reviews.title`, `reviews.text` → первые 1500 валидных отзывов |

**Лицензия:** открытые данные с Kaggle; уточняйте условия на странице датасета при скачивании.

**Дата подготовки:** июнь 2026.

---

## Что индексируем

| Поле / артефакт | Индексируется? | Где используется |
|-----------------|:--------------:|------------------|
| `text` из `datasets.json` | **Да** | TF-IDF матрица, поиск, demo-ответ |
| `name` (заголовок отзыва) | Нет (метаданные) | UI, источники — подпись документа |
| `doc_id` | Нет (метаданные) | UI, источники — идентификатор записи |
| `source_file` | Нет | `documents.jsonl`, трассировка происхождения |

**Pipeline:**

```
1429_1.csv → extract.py → datasets.json → documents.jsonl → chunks.jsonl → vectorizer.pkl + matrix.npz
```

- **Чанки:** нарезка по абзацам, max 400 символов, overlap 50 (`app/chunker.py`).
- **Поиск:** cosine similarity по TF-IDF векторам (`app/retriever.py`).
- **Индекс:** 1597 чанков × 3081 признак (после `build_index.py`).

---

## Что не индексируем

| Не индексируется | Причина |
|------------------|---------|
| `data/raw/1429_1.csv` | Сырой CSV — только для локальной подготовки `datasets.json` |
| `reviews.rating`, `brand`, `categories` и др. | MVP работает с текстом отзывов, не с табличными полями |
| Kaggle API | Не используется в runtime |
| Секреты, API-ключи | Demo-режим без внешних LLM |
| `data/processed/*.jsonl` | Промежуточные артефакты, генерируются скриптами |
| `data/index/*` | Индекс пересобирается командой `build_index.py` |

---

## Состав корпуса

1500 отзывов на продукт **Amazon Fire HD 8 Tablet** (английский язык).

Типичные темы в отзывах:

| Тема | Примеры слов в тексте |
|------|----------------------|
| Prime / контент | Prime Members, movies, download |
| Дети / parental controls | kids, children, age, content |
| Чтение / e-reader | reading, books, Kindle |
| Батарея | battery life |
| Цена / value | great value, price |

**Рабочие demo-запросы в UI:**

- «Prime Members tablet movies content» → ответ с score > 0.15
- «battery life fire tablet» → отзывы про battery
- «quantum physics relativity» → **отказ** (negative-case)

---

## Как обновить данные

1. Скачать `1429_1.csv` с Kaggle в `data/raw/`.
2. Запустить: `python data/raw/extract.py` (или адаптировать лимит в скрипте).
3. Пересобрать индекс: `uv run python scripts/build_index.py`

---

## Связанные документы

- [00_project_idea.md](00_project_idea.md) — идея проекта
- [vision.md](vision.md) — стек и границы MVP
- [tasklist.md](tasklist.md) — итерационный план
