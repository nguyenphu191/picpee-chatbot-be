import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.base import get_db
from app.db.models import Conversation, Message, User
from app.schemas.history import ConversationResponse, ConversationDetailResponse
from app.services.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ConversationResponse])
async def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Lấy danh sách các cuộc hội thoại của người dùng hiện tại"""
    conversations = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .order_by(desc(Conversation.created_at))\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    # Enrich with last message snippet if wanted
    results = []
    for conv in conversations:
        last_msg = db.query(Message)\
            .filter(Message.conversation_id == conv.id)\
            .order_by(desc(Message.created_at))\
            .first()
        
        results.append({
            "id": conv.id,
            "title": conv.title or (last_msg.content[:50] + "..." if last_msg else "Hội thoại mới"),
            "created_at": conv.created_at,
            "last_message": last_msg.content if last_msg else None
        })
        
    return results

@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Chi tiết một cuộc hội thoại bao gồm các tin nhắn"""
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Không tìm thấy hội thoại")
        
    messages = db.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at)\
        .all()
        
    return {
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at,
        "messages": messages
    }

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Xóa một cuộc hội thoại và tất cả tin nhắn liên quan"""
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Không tìm thấy hội thoại")
        
    # Delete messages first (or let DB handle cascade if configured, but let's be explicit)
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    db.delete(conv)
    db.commit()
    
    return {"message": "Đã xóa hội thoại thành công"}

@router.delete("/")
async def clear_all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Xóa toàn bộ lịch sử của người dùng hiện tại"""
    # Find all conv IDs for this user
    conv_ids = [c.id for c in db.query(Conversation.id).filter(Conversation.user_id == current_user.id).all()]
    
    if conv_ids:
        db.query(Message).filter(Message.conversation_id.in_(conv_ids)).delete(synchronize_session=False)
        db.query(Conversation).filter(Conversation.user_id == current_user.id).delete(synchronize_session=False)
        db.commit()
        
    return {"message": "Đã xóa toàn bộ lịch sử thành công"}
