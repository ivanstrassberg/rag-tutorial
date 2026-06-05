# Vision — техническое видение проекта

> Отправная точка для разработки.  
> Идея продукта: [00_project_idea.md](00_project_idea.md)

**Учебный RAG** на отзывах Amazon Fire HD 8 (1500 записей): локально, просто, с ответом и источниками.

---

## 1. Технологии

Минимальный стек — только то, без чего MVP не работает.

| Слой | Выбор | Комментарий |
|------|-------|-------------|
| Язык | **Python 3.10+** | — |
| Окружение | **uv** + `.venv` | venv через uv; локально, не коммитим |
| UI | **Streamlit** | Один entry point, видны чанки, scores и источники |
| Поиск | **TF-IDF + cosine similarity** (`scikit-learn`) | Без torch и тяжёлых моделей; ищет по совпадению слов, не по «смыслу» |
| Индекс | **Локальные файлы** (`data/index/`) | `vectorizer.pkl` + `matrix.npz` + `chunks.jsonl` — без ChromaDB и без сервера |
| LLM | **Только demo-режим** | Ответ из найденных чанков по правилам system prompt; внешний API не используем |
| Данные | **Amazon Reviews (Kaggle)** → `data/raw/datasets.json` | 1500 отзывов; в RAG идёт текст, не CSV |
| Тесты | **pytest** | 3–5 тестов: chunking, retrieval, источники |
| Зависимости | **`pyproject.toml`** + uv | `uv sync`; без pip/poetry/conda |

### Данные с Kaggle (как устроено)

1. Скачиваем `1429_1.csv` (Amazon Consumer Reviews).
2. Скрипт `data/raw/extract.py` извлекает заголовок и текст отзыва.
3. Сохраняем 1500 записей в `datasets.json` (без Kaggle API в runtime).
4. CSV **не индексируем** — только текст для RAG.

### Ограничение TF-IDF (осознанно)

Поиск по ключевым словам: синонимы и перефразировки могут не находиться. Для учебного MVP это приемлемо — pipeline тот же, что и с embeddings.

### Не используем в MVP

ChromaDB, sentence-transformers, torch, LangChain / LlamaIndex, FastAPI, Docker, reranking, hybrid search, OpenAI, Kaggle API, pandas для анализа CSV, pip/poetry/conda (используем **uv**).

### Окружение (как запускать)

```bash
uv venv          # создать .venv
uv sync          # установить зависимости из pyproject.toml
```

---
