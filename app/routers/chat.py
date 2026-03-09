import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db.models import Conversation, Message, User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag import answer_question
from app.services.deps import get_optional_current_user

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_with_bot(
    payload: ChatRequest, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> ChatResponse:
    """
    Endpoint chính để frontend gọi chatbot.
    Nếu user đã login, lưu history vào DB.
    """

    try:
        answer, sources = await answer_question(
            question=payload.question,
            document_ids=payload.document_ids,
            language=payload.language or "vi",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý: {str(e)}")

    # Xử lý lưu history nếu user đã đăng nhập
    conversation_id = payload.conversation_id
    if current_user:
        # Nếu chưa có conversation_id, tạo mới
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            new_conv = Conversation(
                id=conversation_id,
                user_id=current_user.id,
                title=payload.question[:50] + "..." if len(payload.question) > 50 else payload.question
            )
            db.add(new_conv)
        
        # Lưu tin nhắn của user
        user_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role="user",
            content=payload.question
        )
        db.add(user_msg)
        
        # Lưu tin nhắn của assistant
        assistant_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            sources=[s.dict() for s in sources] if sources else None
        )
        db.add(assistant_msg)
        
        db.commit()

    return ChatResponse(
        answer=answer,
        sources=sources,
        conversation_id=conversation_id
    )
