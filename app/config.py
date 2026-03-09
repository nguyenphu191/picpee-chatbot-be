from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


# Tự động load biến môi trường từ file .env (nếu tồn tại)
load_dotenv()


class Settings(BaseSettings):
    # LLM sinh câu trả lời
    llm_provider: str = Field("groq", env="LLM_PROVIDER")
    llm_api_key: str = Field("", env="LLM_API_KEY")
    llm_model_name: str = Field("llama-3.1-8b-instant", env="LLM_MODEL_NAME")

    # Embedding
    embedding_provider: str = Field("google", env="EMBEDDING_PROVIDER")
    embedding_api_key: str = Field("", env="EMBEDDING_API_KEY")
    embedding_model_name: str = Field(
        "models/gemini-embedding-001", env="EMBEDDING_MODEL_NAME"
    )

    # Database metadata (documents, chunks, ...)
    # Ví dụ PostgreSQL: postgresql+psycopg2://user:password@localhost:5432/chatbot_rag
    db_url: str = Field(
        "postgresql+psycopg2://user:password@localhost:5432/chatbot_rag",
        env="DB_URL",
    )

    # Vector DB (Qdrant, FAISS, ...)
    vector_db_type: str = Field("qdrant", env="VECTOR_DB_TYPE")
    vector_db_url: str = Field("http://localhost:6333", env="VECTOR_DB_URL")
    vector_db_collection: str = Field(
        "documents_embeddings", env="VECTOR_DB_COLLECTION"
    )

    # Lưu trữ file PDF
    documents_storage_path: str = Field(
        "./storage/documents", env="DOCUMENTS_STORAGE_PATH"
    )

    # CORS
    allowed_origins: str = Field("http://localhost:3000", env="ALLOWED_ORIGINS")

    # Tham số RAG
    max_chunk_size: int = Field(1000, env="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(150, env="CHUNK_OVERLAP")
    rag_top_k: int = Field(5, env="RAG_TOP_K")

    # Security
    secret_key: str = Field("your-super-secret-key-change-it-in-prod", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(60 * 24 * 7, env="ACCESS_TOKEN_EXPIRE_MINUTES") # 7 days
    default_admin_password: str = Field("admin123", env="DEFAULT_ADMIN_PASSWORD")

    class Config:
        case_sensitive = False

    def allowed_origins_list(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """
    Hàm dùng để lấy config (được cache), dùng trong toàn bộ app:

    from app.config import get_settings
    settings = get_settings()
    """

    return Settings()

