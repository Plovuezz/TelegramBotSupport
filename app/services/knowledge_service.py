from __future__ import annotations

import re
import string
from dataclasses import dataclass
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


@dataclass
class KnowledgeChunk:
    source: str
    content: str


def load_knowledge() -> List[KnowledgeChunk]:
    chunks = []

    if not KNOWLEDGE_DIR.exists():
        return chunks

    for path in KNOWLEDGE_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")


        raw_chunks = text.split("\n\n")

        for block in raw_chunks:
            block = block.strip()
            if not block:
                continue
            chunks.append(KnowledgeChunk(source=path.name, content=block))

    return chunks


KNOWLEDGE_CHUNKS: List[KnowledgeChunk] = load_knowledge()


def find_relevant_chunks(query: str, max_chunks: int = 3) -> List[KnowledgeChunk]:

    query = query.lower()

    for ch in string.punctuation:
        query = query.replace(ch, " ")
    query_words = [w for w in query.split() if len(w) > 2]

    scored: list[tuple[int, KnowledgeChunk]] = []

    for chunk in KNOWLEDGE_CHUNKS:
        score = 0
        text = chunk.content.lower()

        for word in query_words:
            if word in text:
                score += 1

        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored[:max_chunks]]


def get_knowledge(query: str, max_chunks: int = 3) -> str:

    chunks = find_relevant_chunks(query, max_chunks=max_chunks)

    if not chunks:
        return ""

    parts = []
    for chunk in chunks:
        parts.append(f"[{chunk.source}]\n{chunk.content}")

    return "\n\n".join(parts)
