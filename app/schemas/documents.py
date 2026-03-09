from typing import List, Optional

from pydantic import BaseModel


class DocumentDetailResponse(BaseModel):
    id: str
    name: str
    status: str
    page_count: Optional[int] = 0
    chunk_count: Optional[int] = 0


class DocumentListResponse(BaseModel):
    items: List[DocumentDetailResponse]


class ChunkResponse(BaseModel):
    id: str
    document_id: str
    page: Optional[int] = None
    chunk_index: int
    text: str


class ChunkUpdateRequest(BaseModel):
    text: str

