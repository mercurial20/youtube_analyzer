import math
import os
from typing import List

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"  # ~1M токенов контекст

# Оставим чуть для контекста и системных промптов
MAX_CHUNK_TOKENS = 900_000


def count_tokens(text: str) -> int:
    """Считает токены текста для выбранной модели через API."""
    resp = client.models.count_tokens(
        model=MODEL,
        contents=text,
    )
    if resp.total_tokens:
        return resp.total_tokens
    return 0


def split_text_by_tokens(text: str, max_tokens: int = MAX_CHUNK_TOKENS) -> List[str]:
    """
    Делит текст на чанки по max_tokens токенов (приблизительно).
    Чтобы не делать 100500 запросов к count_tokens, считаем токены
    для всего текста 1 раз, оцениваем количество чанков и режем по словам.
    """
    total_tokens = count_tokens(text)

    # Если влезает целиком не режем вообще
    if total_tokens <= max_tokens:
        return [text]

    # Сколько чанков примерно нужно
    n_chunks = math.ceil(total_tokens / max_tokens)

    words = text.split()
    total_words = len(words)

    # Примерное количество слов в чанке
    words_per_chunk = math.ceil(total_words / n_chunks)

    chunks: List[str] = []
    for i in range(0, total_words, words_per_chunk):
        chunk_words = words[i : i + words_per_chunk]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)

    return chunks


def _summarize_chunk(
    chunk: str, idx: int | None = None, total: int | None = None
) -> str:
    """Суммаризация одного чанка."""
    prefix = ""
    if idx is not None and total is not None:
        prefix = f"Это часть {idx} из {total} транскрипта длинного видео.\n\n"

    prompt = (
        prefix + "Ниже фрагмент транскрипта видео.\n"
        "Сделай краткий, но информативный конспект: основные идеи и важные детали.\n\n"
        + chunk
    )

    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    if not resp.text:
        return "Ошибка в клиенте google-genai"
    return resp.text


def summarize_long_text(
    full_text: str, max_chunk_tokens: int = MAX_CHUNK_TOKENS
) -> str:
    """
    Map-Reduce суммаризация:
    - режем текст на крупные чанки (до ~900k токенов)
    - для каждого чанка получаем локальный конспект
    - из конспектов делаем финальный конспект.
    """
    chunks = split_text_by_tokens(full_text, max_tokens=max_chunk_tokens)

    # Если влезло в один чанк просто один запрос
    if len(chunks) == 1:
        return _summarize_chunk(chunks[0])

    # Map: конспект по каждой части
    partial_summaries: List[str] = []
    total = len(chunks)
    for i, chunk in enumerate(chunks, start=1):
        summary = _summarize_chunk(chunk, idx=i, total=total)
        partial_summaries.append(summary)

    merged = "\n\n".join(
        f"Часть {i + 1}:\n{s}" for i, s in enumerate(partial_summaries)
    )

    final_prompt = (
        "Ниже конспекты отдельных частей длинного видео.\n"
        "Сделай один связный, структурированный итог всего видео в формате md.\n\n"
        f"{merged}"
    )

    final_resp = client.models.generate_content(
        model=MODEL,
        contents=final_prompt,
    )

    if not final_resp.text:
        return "Ошибка в клиенте google-genai"
    return final_resp.text
