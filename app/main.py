from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.base import engine
from app.db.models import Base
from app.routers import chat as chat_router
from app.routers import documents as doc_router
from app.routers import auth as auth_router
from app.routers import history as history_router


settings = get_settings()

app = FastAPI(
    title="Chatbot RAG Backend",
    description="Backend FastAPI cho chatbot RAG phục vụ trang web chỉnh sửa ảnh",
    version="0.1.0",
)

# CORS cho frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    """
    Tạo bảng DB lần đầu nếu chưa có (đơn giản cho prototype).
    Nếu bạn muốn chuẩn production, có thể chuyển sang Alembic migrations sau.
    """

    Base.metadata.create_all(bind=engine)


# Đăng ký routers chính
app.include_router(doc_router.router, prefix="/documents", tags=["documents"])
app.include_router(chat_router.router, prefix="/chat", tags=["chat"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(history_router.router, prefix="/history", tags=["history"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

