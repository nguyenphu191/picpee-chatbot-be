"""
Adapter cho Vector Store (hỗ trợ pgvector và Qdrant skeleton).
"""

from typing import Any, List, Optional
from sqlalchemy import text
from app.db.base import SessionLocal
from app.db.models import Chunk
import numpy as np

class VectorStore:
    def __init__(self, store_type: str, url: str, collection: str):
        self.store_type = store_type
        self.url = url
        self.collection = collection

    async def upsert_document_chunks(
        self,
        document_id: str,
        embeddings: List[List[float]],
        metadatas: List[dict],
    ) -> None:
        """
        Lưu vector cho các chunk của 1 tài liệu vào Postgres (pgvector).
        """
        if self.store_type == "pgvector":
            db = SessionLocal()
            try:
                for i, emb in enumerate(embeddings):
                    # Cập nhật embedding cho chunk đã có (dựa trên document_id và chunk_index)
                    # Giả sử metadata có chunk_index
                    chunk_idx = metadatas[i].get("chunk_index")
                    db.query(Chunk).filter(
                        Chunk.document_id == document_id, 
                        Chunk.chunk_index == chunk_idx
                    ).update({"embedding": emb})
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
        else:
            raise NotImplementedError(
                f"upsert_document_chunks chưa được triển khai cho {self.store_type}"
            )

    async def query_similar_chunks(
        self,
        query_vector: List[float],
        top_k: int,
        document_ids: Optional[List[str]] = None,
    ) -> List[Any]:
        """
        Truy vấn các chunk tương tự bằng pgvector.
        """
        if self.store_type == "pgvector":
            db = SessionLocal()
            try:
                # Sử dụng toán tử <=> cho cosine distance trong pgvector
                query = db.query(Chunk).order_by(Chunk.embedding.cosine_distance(query_vector)).limit(top_k)
                
                if document_ids:
                    query = query.filter(Chunk.document_id.in_(document_ids))
                
                results = query.all()
                return results
            finally:
                db.close()
        else:
            raise NotImplementedError(
                f"query_similar_chunks chưa được triển khai cho {self.store_type}"
            )
