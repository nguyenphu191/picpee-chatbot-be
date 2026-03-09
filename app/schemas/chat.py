from typing import List, Optional

from pydantic import BaseModel


class ChatSource(BaseModel):
    document_id: Optional[str] = None
    page: Optional[int] = None
    chunk_index: Optional[int] = None
    snippet: Optional[str] = None


class ChatRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None
    language: Optional[str] = "vi"
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatSource] = []
    conversation_id: Optional[str] = None

