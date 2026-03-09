"""
Adapter embedding hỗ trợ Google Gemini và các provider khác.
"""

from typing import List
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()

class EmbeddingClient:
    def __init__(self, provider: str, model_name: str, api_key: str):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        
        if self.provider == "google":
            genai.configure(api_key=self.api_key)

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Tạo embedding cho nhiều đoạn text bằng Google Gemini.
        """
        if self.provider == "google":
            # Gemini text-embedding-004
            result = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type="retrieval_document"
            )
            return result['embedding']
        else:
            raise NotImplementedError(
                f"embed_texts chưa được triển khai cho provider {self.provider}"
            )

    async def embed_query(self, text: str) -> List[float]:
        """
        Tạo embedding cho 1 câu hỏi.
        """
        if self.provider == "google":
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        
        vectors = await self.embed_texts([text])
        return vectors[0]
