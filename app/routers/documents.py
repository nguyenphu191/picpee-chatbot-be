from typing import List, Optional
import os
import uuid
import shutil
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.base import get_db
from app.db.models import Document, Chunk
from app.db.vector_store import VectorStore
from app.schemas.documents import (
    ChunkResponse,
    DocumentDetailResponse,
    DocumentListResponse,
    ChunkUpdateRequest,
)
from app.services.text_extraction import extract_text_from_pdf
from app.services.chunking import chunk_text
from app.services.embedding import EmbeddingClient
from app.services.deps import get_current_admin_user, User

router = APIRouter()
settings = get_settings()

# Khởi tạo clients
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

@router.post("/upload", response_model=DocumentDetailResponse)
async def upload_document(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF")

    doc_id = str(uuid.uuid4())
    filename = file.filename
    
    # 1. Lưu file vào storage
    os.makedirs(settings.documents_storage_path, exist_ok=True)
    file_path = os.path.join(settings.documents_storage_path, f"{doc_id}.pdf")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Lưu metadata vào DB ban đầu
    db_doc = Document(
        id=doc_id,
        name=filename,
        file_path=file_path,
        status="PROCESSING"
    )
    db.add(db_doc)
    db.commit()

    try:
        # 3. Trích xuất text
        pages_text = extract_text_from_pdf(file_path)
        
        # 4. Chia nhỏ (Chunking)
        chunks_data = chunk_text(
            document_id=doc_id,
            pages_text=pages_text,
            max_chars=settings.max_chunk_size,
            overlap=settings.chunk_overlap
        )
        
        # 5. Lưu chunks vào DB (không có embedding trước)
        db_chunks = []
        for c in chunks_data:
            chunk_id = str(uuid.uuid4())
            db_chunk = Chunk(
                id=chunk_id,
                document_id=doc_id,
                page=c.page,
                chunk_index=c.chunk_index,
                text=c.text
            )
            db_chunks.append(db_chunk)
            db.add(db_chunk)
        
        db.commit()

        # 6. Tạo embedding và update vào DB + VectorStore (pgvector)
        texts = [c.text for c in chunks_data]
        embeddings = await embedding_client.embed_texts(texts)
        
        # Cập nhật embedding cho từng chunk trong DB (pgvector)
        for i, db_chunk in enumerate(db_chunks):
            db_chunk.embedding = embeddings[i]
        
        # 7. Cập nhật trạng thái hoàn tất
        db_doc.status = "READY"
        db_doc.page_count = len(pages_text)
        db_doc.chunk_count = len(db_chunks)
        db.commit()

    except Exception as e:
        db_doc.status = "ERROR"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý tài liệu: {str(e)}")

    return DocumentDetailResponse(
        id=db_doc.id,
        name=db_doc.name,
        status=db_doc.status,
        page_count=db_doc.page_count,
        chunk_count=db_doc.chunk_count,
    )

@router.get("/", response_model=DocumentListResponse)
async def list_documents(db: Session = Depends(get_db)) -> DocumentListResponse:
    documents = db.query(Document).order_by(Document.created_at.desc()).all()
    items = [
        DocumentDetailResponse(
            id=d.id,
            name=d.name,
            status=d.status,
            page_count=d.page_count,
            chunk_count=d.chunk_count,
        ) for d in documents
    ]
    return DocumentListResponse(items=items)

@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document_detail(document_id: str, db: Session = Depends(get_db)) -> DocumentDetailResponse:
    d = db.query(Document).filter(Document.id == document_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    return DocumentDetailResponse(
        id=d.id,
        name=d.name,
        status=d.status,
        page_count=d.page_count,
        chunk_count=d.chunk_count,
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    
    # 1. Xóa file vật lý
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception as e:
            print(f"Lỗi khi xóa file {doc.file_path}: {e}")
            
    # 2. Xóa các chunk liên quan (cascade)
    db.query(Chunk).filter(Chunk.document_id == document_id).delete()
    
    # 3. Xóa document
    db.delete(doc)
    db.commit()
    
    return {"message": "Đã xóa tài liệu và các chunk liên quan"}

@router.get("/{document_id}/chunks", response_model=List[ChunkResponse])
async def list_document_chunks(document_id: str, db: Session = Depends(get_db)) -> List[ChunkResponse]:
    chunks = db.query(Chunk).filter(Chunk.document_id == document_id).order_by(Chunk.chunk_index).all()
    return [
        ChunkResponse(
            id=c.id,
            document_id=c.document_id,
            page=c.page,
            chunk_index=c.chunk_index,
            text=c.text,
        ) for c in chunks
    ]

@router.put("/chunks/{chunk_id}", response_model=ChunkResponse)
async def update_chunk(
    chunk_id: str, 
    payload: ChunkUpdateRequest, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
) -> ChunkResponse:
    chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Không tìm thấy chunk")
    
    # 1. Cập nhật text
    chunk.text = payload.text
    
    # 2. Cập nhật embedding cho text mới
    try:
        embedding = await embedding_client.embed_query(payload.text)
        chunk.embedding = embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo embedding mới: {str(e)}")
        
    db.commit()
    
    return ChunkResponse(
        id=chunk.id,
        document_id=chunk.document_id,
        page=chunk.page,
        chunk_index=chunk.chunk_index,
        text=chunk.text,
    )

@router.delete("/chunks/{chunk_id}")
async def delete_chunk(
    chunk_id: str, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
    if not chunk:
        raise HTTPException(status_code=404, detail="Không tìm thấy chunk")
        
    db.delete(chunk)
    db.commit()
    
    return {"message": "Đã xóa chunk"}
