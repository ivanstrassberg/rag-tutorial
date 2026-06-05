# Submission

## Ссылка на репозиторий с заданием

- Repo URL: https://github.com/ivanstrassberg/rag-tutorial

## Автор

- ФИО / ник: Силин Иван Андреевич / ivanstrassberg

## Комментарий

- Реализован полный RAG-pipeline: ingest → chunking → TF-IDF index → retrieval → demo-answer → Streamlit UI.
- Данные: 1500 отзывов Amazon Fire HD 8 из Kaggle Electronics Reviews (`1429_1.csv`), подготовлены скриптом `data/raw/extract.py` → `datasets.json`.
- Индекс: 1500 документов, 1597 чанков.
- Demo: 3 рабочих вопроса (Prime/kids/battery) + 1 negative (`quantum physics relativity`) с отказом.
- Улучшения: описаны в `homework/STUDENT_IMPROVEMENTS.md` (embeddings + ChromaDB).
