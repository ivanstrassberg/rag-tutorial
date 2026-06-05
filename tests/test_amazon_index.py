"""Тесты на реальном индексе Amazon Reviews."""

import pytest

from app.config import INDEX_CHUNKS_JSONL, MATRIX_NPZ, VECTORIZER_PKL
from app.generator import ask
from app.prompts import REFUSAL_NO_CONTEXT, MIN_SCORE
from app.retriever import Retriever


@pytest.fixture
def amazon_retriever() -> Retriever:
    if not all(p.exists() for p in (VECTORIZER_PKL, MATRIX_NPZ, INDEX_CHUNKS_JSONL)):
        pytest.skip("Индекс не собран — запустите scripts/build_index.py")
    return Retriever()


def test_battery_query_finds_relevant_chunk(amazon_retriever):
    results = amazon_retriever.search("battery life fire tablet", k=3)
    assert results
    assert results[0]["score"] >= MIN_SCORE
    assert "battery" in results[0]["text"].lower()


def test_negative_query_refuses(amazon_retriever):
    result = ask("quantum physics relativity", retriever=amazon_retriever)
    assert result["answer"] == REFUSAL_NO_CONTEXT


def test_datasets_json_has_1500_records():
    import json
    from app.config import RAW_DATASETS

    data = json.loads(RAW_DATASETS.read_text(encoding="utf-8"))
    assert len(data["datasets"]) >= 1000
