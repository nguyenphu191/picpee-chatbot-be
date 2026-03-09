import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ChunkData:
    document_id: str
    page: Optional[int]
    chunk_index: int
    text: str

def split_text_by_headings(text: str, max_chars: int, overlap: int) -> List[str]:
    """
    Tách text theo các đầu mục (I., II., 1., 2., a., b., ... ở đầu dòng)
    Nếu một mục quá dài so với max_chars, tiếp tục tách theo đoạn văn hoặc câu với overlap.
    """
    heading_pattern = r'(?=\n\s*(?:[IVX]+\.|[0-9]+\.|[a-z]\.)\s+)'
    parts_by_heading = re.split(heading_pattern, "\n" + text)
    
    chunks = []
    for part in parts_by_heading:
        part = part.strip()
        if not part:
            continue
            
        if len(part) <= max_chars:
            chunks.append(part)
        else:
            # Nếu mục này quá dài, tách tiếp bằng đoạn văn hoặc câu và áp dụng overlap
            paragraphs = re.split(r'\n+', part)
            current_chunk = ""
            
            for p in paragraphs:
                p = p.strip()
                if not p:
                    continue
                
                # Nếu thêm đoạn mới vào vẫn chưa quá giới hạn
                if len(current_chunk) + len(p) + 1 <= max_chars:
                    current_chunk += ("\n" if current_chunk else "") + p
                else:
                    # Nếu đã có nội dung trong current_chunk, đẩy vào list chunks
                    if current_chunk:
                        chunks.append(current_chunk)
                        # Tính toán overlap: Lấy phần cuối của current_chunk để bắt đầu chunk mới
                        # Đảm bảo không lấy quá độ dài của chính đoạn vừa rồi
                        overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                        current_chunk = overlap_text + "\n" + p
                    else:
                        # Trường hợp Paragraph bản thân nó đã quá dài ( > max_chars )
                        # Tách theo câu (.)
                        sentences = re.split(r'(?<=\.)\s+', p)
                        for s in sentences:
                            if len(current_chunk) + len(s) + 1 <= max_chars:
                                current_chunk += (" " if current_chunk else "") + s
                            else:
                                if current_chunk:
                                    chunks.append(current_chunk)
                                    overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                                    current_chunk = overlap_text + " " + s
                                else:
                                    # Nếu 1 câu quá dài, cắt cứng (biện pháp cuối)
                                    for i in range(0, len(s), max_chars - overlap):
                                        c = s[i:i + max_chars]
                                        chunks.append(c)
                                    current_chunk = "" # Sau khi cắt cứng câu siêu dài, reset
            
            if current_chunk:
                chunks.append(current_chunk)
                
    return chunks

def chunk_text(
    document_id: str,
    pages_text: List[str],
    max_chars: int = 512,
    overlap: int = 100, # Bật overlap 100 ký tự
) -> List[ChunkData]:
    """
    Chia text theo trang sử dụng thuật toán phân tách theo đầu mục và đoạn văn, hỗ trợ overlap.
    """
    chunks: List[ChunkData] = []
    chunk_index = 0

    for page_num, page_text in enumerate(pages_text, start=1):
        text = page_text or ""
        
        # Gọi hàm tách với tham số overlap
        text_chunks = split_text_by_headings(text, max_chars, overlap)
        
        for c_text in text_chunks:
            if not c_text.strip():
                continue
                
            chunks.append(
                ChunkData(
                    document_id=document_id,
                    page=page_num,
                    chunk_index=chunk_index,
                    text=c_text.strip(),
                )
            )
            chunk_index += 1

    return chunks

