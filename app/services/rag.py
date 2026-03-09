"""
Dịch vụ RAG hỗ trợ đa provider: Google Gemini và Groq.
"""

import time
from typing import List, Optional
from app.config import get_settings
from app.db.vector_store import VectorStore
from app.schemas.chat import ChatSource
from app.services.embedding import EmbeddingClient

settings = get_settings()

# Embedding client (dùng Gemini, key riêng)
embedding_client = EmbeddingClient(
    provider=settings.embedding_provider,
    model_name=settings.embedding_model_name,
    api_key=settings.embedding_api_key,
)

vector_store = VectorStore(
    store_type=settings.vector_db_type,
    url=settings.vector_db_url,
    collection=settings.vector_db_collection,
)


def _call_llm(prompt: str) -> str:
    """Gọi LLM theo provider đã cấu hình, có retry tự động."""
    
    if settings.llm_provider == "groq":
        from groq import Groq
        client = Groq(api_key=settings.llm_api_key)
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=settings.llm_model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    wait_time = 10 * (attempt + 1)
                    print(f"Rate limit hit, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e

    elif settings.llm_provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=settings.llm_api_key)
        for attempt in range(3):
            try:
                model = genai.GenerativeModel(settings.llm_model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    wait_time = 30 * (attempt + 1)
                    print(f"Rate limit hit, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
    
    raise ValueError(f"LLM Provider '{settings.llm_provider}' chưa được hỗ trợ.")


async def answer_question(
    question: str, document_ids: Optional[List[str]] = None, language: str = "vi"
) -> tuple[str, List[ChatSource]]:
    """Thực hiện quy trình RAG."""

    # 1. Embedding cho câu hỏi
    query_vector = await embedding_client.embed_query(question)

    # 2. Tìm chunks tương tự
    similar_chunks = await vector_store.query_similar_chunks(
        query_vector=query_vector,
        top_k=settings.rag_top_k,
        document_ids=document_ids,
    )

    # 3. Tổng hợp context
    if similar_chunks:
        context_text = "\n\n".join(
            [f"Source {i+1}:\n{chunk.text}" for i, chunk in enumerate(similar_chunks)]
        )
    else:
        context_text = "(Không tìm thấy tài liệu liên quan)"

    # 4. Gọi LLM
    prompt = f"""Bạn là một trợ lý ảo thông minh cho trang web chỉnh sửa ảnh PicPee.
Hãy trả lời câu hỏi dựa trên Context bên dưới.
Nếu Context không có thông tin, hãy nói thật là bạn không biết.

Câu hỏi: {question}

Context:
{context_text}

Trả lời bằng ngôn ngữ: {language}"""

    answer = _call_llm(prompt)

    # 5. Nguồn tài liệu
    sources = [
        ChatSource(
            document_id=chunk.document_id,
            page=chunk.page,
            snippet=chunk.text[:200],
        )
        for chunk in similar_chunks
    ]

    return answer, sources
