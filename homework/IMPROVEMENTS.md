# Улучшения MVP

Выбраны 2 направления из [IMPROVEMENTS.md](IMPROVEMENTS.md).

## 1) Embeddings вместо TF-IDF

**Зачем:** отзывы часто перефразируют одну мысль разными словами («long battery» vs «battery lasts all day»). TF-IDF не найдёт синонимы; sentence-transformers дадут поиск по смыслу.

**Какие файлы менять:**
- `scripts/build_index.py` — считать эмбеддинги вместо TF-IDF fit
- `app/retriever.py` — cosine similarity по dense-векторам
- `data/index/` — хранить `embeddings.npy` вместо `matrix.npz`

**Как проверить:** запрос «how long does the charge last» должен находить отзывы про battery life даже без точного совпадения слов.

## 2) Векторная база (ChromaDB)

**Зачем:** при масштабировании с 1500 до 40k+ отзывов файловый индекс (`vectorizer.pkl` + `matrix.npz`) станет медленным и неудобным для обновления.

**Какие файлы менять:**
- `scripts/build_index.py` — upsert в ChromaDB collection
- `app/retriever.py` — query через ChromaDB API
- `app/config.py` — путь к persistent store

**Как проверить:** время поиска top-k на 40k чанках < 100ms; добавление нового отзыва без полной пересборки матрицы.
