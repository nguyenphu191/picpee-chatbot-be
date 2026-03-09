from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .chat import ChatSource

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    sources: Optional[List[ChatSource]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: str
    title: Optional[str] = None
    created_at: datetime
    last_message: Optional[str] = None

    class Config:
        from_attributes = True

class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse]
