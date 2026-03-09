import sys
import os
from sqlalchemy import text

# Thêm thư mục gốc vào path để import được app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import engine
from app.db.models import Base

def init_db():
    print("🚀 Đang khởi tạo Database trên Supabase...")

    with engine.connect() as conn:
        # 1. Bật extension pgvector (nếu chưa có)
        print("🔧 Đang bật extension pgvector...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
        print("✅ Đã bật pgvector.")

    # 3. Tạo lại các bảng theo model mới nhất
    print("🏗️ Đang tạo các bảng (documents, chunks)...")
    Base.metadata.create_all(bind=engine)
    print("✅ Đã tạo bảng thành công.")

    # 4. Tạo tài khoản ADMIN mặc định (nếu chưa có)
    from app.db.base import SessionLocal
    from app.db.models import User
    from app.services.auth import get_password_hash
    from app.config import get_settings
    import uuid

    settings = get_settings()
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.role == "ADMIN").first()
        if not admin_user:
            print("👤 Đang tạo tài khoản ADMIN mặc định...")
            new_admin = User(
                id=str(uuid.uuid4()),
                username="admin",
                hashed_password=get_password_hash(settings.default_admin_password),
                role="ADMIN"
            )
            db.add(new_admin)
            db.commit()
            print(f"✅ Đã tạo tài khoản ADMIN (username: admin, password: {settings.default_admin_password})")
        else:
            print("ℹ️ Tài khoản ADMIN đã tồn tại.")
    finally:
        db.close()

    print("\n🎉 Chúc mừng! Database đã được setup hoàn tất cho toàn dự án.")

if __name__ == "__main__":
    init_db()
