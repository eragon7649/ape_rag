# src/core/config.py

import os

# --- 1. CẤU HÌNH API (Môi trường an toàn hơn) ---
# Đảm bảo các biến môi trường này được thiết lập trước khi chạy
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", None)

# --- 2. CẤU HÌNH ĐƯỜNG DẪN HỆ THỐNG ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
RAG_STORAGE_DIR = os.path.join(BASE_DIR, "rag_storage")

# --- 3. CẤU HÌNH MÔ HÌNH RAG ---
LLM_MODEL = "gpt-4o-mini"
VLM_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 3072

# Cấu hình RAGAnything
from raganything import RAGAnythingConfig

RAG_CONFIG = RAGAnythingConfig(
    working_dir=RAG_STORAGE_DIR,
    parser="mineru",
    parse_method="auto",
    enable_image_processing=True,
    enable_table_processing=True,
    enable_equation_processing=True,
)
