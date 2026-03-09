from pathlib import Path
from typing import List

import pdfplumber


def extract_text_from_pdf(file_path: str) -> List[str]:
    """
    Trích xuất text theo từng trang từ file PDF.

    Hiện tại dùng pdfplumber, đủ tốt cho đa số tài liệu đơn giản.
    Trả về: danh sách chuỗi, mỗi phần tử là text của 1 trang.
    """

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file PDF: {file_path}")

    pages_text: List[str] = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages_text.append(text)

    return pages_text

