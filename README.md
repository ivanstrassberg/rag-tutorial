# RAG Tutorial

Учебный RAG на текстовых описаниях: TF-IDF + demo-ответ с источниками.  
Pipeline: данные → чанки → индекс → поиск → ответ.

**Документы разработки:** [doc/tasklist.md](doc/tasklist.md) · **Данные:** [doc/DATA.md](doc/DATA.md) · **Домашнее задание:** [homework/README.md](homework/README.md) · **Слайды:** [Seminar_Big_data.pdf](Seminar_Big_data.pdf) · **Kaggle:** [Consumer Complaint Database](https://www.kaggle.com/datasets/datasnaek/consumer-complaint-database)

## Требования

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Быстрый старт

```bash
# 1. Окружение
uv venv
uv sync

# 2. Сборка индекса (ingest + chunk + TF-IDF)
uv run python scripts/build_index.py

# 3. Запуск UI
uv run streamlit run app/main.py
```

Откройте в браузере: http://localhost:8501

## Demo-вопросы

В sidebar приложения или в поле ввода:

| Вопрос | Ожидание |
|--------|----------|
| **Ипотека - закрытие ипотечной сделки** | ответ, doc_id=2, score > 0.4 |
| Какие переменные в датасете про безработицу? | отказ (нет таких данных) |
| За какой период данные об инфляции? | отказ |
| Как приготовить борщ? | отказ |

Другие рабочие запросы: `студенческий кредит`, `Capital One`, `Wells Fargo закрытие счёта`.

## Проверка из консоли

```bash
# Тесты
uv run pytest tests/ -v

# Поиск (итерация 5)
uv run python scripts/check_retrieval.py

# Demo-ответ (итерация 6)
uv run python scripts/check_generator.py
```

## Структура проекта

```
rag-tutorial/
├── app/
│   ├── config.py       # пути, top_k, размер чанка
│   ├── chunker.py      # нарезка текста
│   ├── retriever.py    # TF-IDF + cosine top-k
│   ├── generator.py    # demo-ответ
│   ├── prompts.py      # правила и отказы
│   └── main.py         # Streamlit UI
├── scripts/
│   ├── ingest.py
│   ├── build_index.py
│   ├── check_retrieval.py
│   └── check_generator.py
├── data/
│   ├── raw/datasets.json
│   ├── processed/      # documents.jsonl, chunks.jsonl (генерируются)
│   └── index/          # vectorizer.pkl, matrix.npz (генерируются)
├── tests/
└── doc/
```

## Пересборка индекса

После изменения `data/raw/datasets.json`:

```bash
uv run python scripts/build_index.py
```

## Ограничения MVP

- Поиск по **словам** (TF-IDF), не по смыслу — синонимы могут не находиться.
- Demo-режим: ответ из найденных чанков, без внешней LLM.
- Индексируется только текст описаний, CSV не используется.

## Контакты
Подписывайтесь на канал: @Marat_notes
