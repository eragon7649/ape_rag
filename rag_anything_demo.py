import asyncio
import os
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
import base64

# ==============================================================================
# BƯỚC 1: Cấu hình API và Tệp
# Thay thế giá trị dưới đây
# ==============================================================================
# Lưu ý: Sử dụng environment variable để bảo mật API key
API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
BASE_URL = None # Có thể để None nếu dùng API mặc định của OpenAI

# Đường dẫn đến tài liệu của anh (PDF, DOCX, v.v.)
# ĐẢM BẢO TỆP NÀY CÓ SẴN TRONG THƯ MỤC CỦA ANH
FILE_TO_PROCESS = "report.pdf" 
OUTPUT_DIRECTORY = "./rag_output_storage"

# ==============================================================================
# BƯỚC 2: Định nghĩa các hàm mô hình (LLM, VLM, Embedding)
# ==============================================================================

# Hàm dùng cho các tác vụ LLM (chỉ văn bản)
def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
    """Sử dụng gpt-4o-mini cho các tác vụ văn bản."""
    return openai_complete_if_cache(
        "gpt-4o-mini",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=API_KEY,
        base_url=BASE_URL,
        **kwargs
    )

# Hàm dùng cho các tác vụ VLM (Vision Language Model)
def vision_model_func(prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs):
    """Sử dụng gpt-4o cho các tác vụ đa phương tiện (văn bản + hình ảnh)."""
    if messages:
        return openai_complete_if_cache(
            "gpt-4o",
            "",
            messages=messages,
            api_key=API_KEY,
            base_url=BASE_URL,
            **kwargs
        )
    elif image_data:
        # Tạo messages từ image_data và prompt
        image_url_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        user_content = [{"type": "text", "text": prompt}, image_url_content]
        
        system_message = [{"role": "system", "content": system_prompt}] if system_prompt else []
        user_message = [{"role": "user", "content": user_content}]
        
        return openai_complete_if_cache(
            "gpt-4o",
            "",
            messages=system_message + user_message,
            api_key=API_KEY,
            base_url=BASE_URL,
            **kwargs
        )
    else:
        return llm_model_func(prompt, system_prompt, history_messages, **kwargs)

# Hàm dùng cho Embedding
def embedding_func(texts):
    """Sử dụng text-embedding-3-large cho embedding."""
    return openai_embed(texts, model="text-embedding-3-large", api_key=API_KEY, base_url=BASE_URL)

# ==============================================================================
# BƯỚC 3: Khởi tạo RAGAnything
# ==============================================================================

# Tạo wrapper cho embedding function
embedding_func_wrapper = EmbeddingFunc(
    embedding_dim=3072,  # text-embedding-3-large có 3072 dimensions
    max_token_size=8192,
    func=embedding_func,
)

# Cấu hình RAGAnything
config = RAGAnythingConfig(
    working_dir=OUTPUT_DIRECTORY,
    parser="mineru",  # Sử dụng MinerU parser
    parse_method="auto",  # Tự động chọn phương pháp parse tốt nhất
    enable_image_processing=True,  # Bật xử lý hình ảnh
    enable_table_processing=True,  # Bật xử lý bảng
    enable_equation_processing=True,  # Bật xử lý công thức toán học
)

# Khởi tạo RAGAnything
rag = RAGAnything(
    config=config,
    llm_model_func=llm_model_func,
    vision_model_func=vision_model_func,
    embedding_func=embedding_func_wrapper,
)

# ==============================================================================
# BƯỚC 4: Xử lý tài liệu và truy vấn
# ==============================================================================

async def main():
    """Hàm chính để xử lý tài liệu và thực hiện truy vấn."""
    
    print("🚀 Bắt đầu xử lý tài liệu...")
    
    # Xử lý tài liệu (parsing và indexing)
    await rag.process_document_complete(
        file_path=FILE_TO_PROCESS,
        output_dir=os.path.join(OUTPUT_DIRECTORY, "parsed_docs"),
        parse_method="auto"
    )
    
    print("✅ Hoàn tất xử lý tài liệu!")
    
    # Thực hiện truy vấn
    query = "Hãy tóm tắt nội dung chính của tài liệu này."
    
    print(f"🔍 Thực hiện truy vấn: {query}")
    
    result = await rag.aquery(
        query,
        mode="hybrid",  # Kết hợp vector search và graph search
        user_prompt="Bạn là một chuyên gia phân tích tài liệu. Hãy trả lời dựa trên nội dung được cung cấp.",
        vlm_enhanced=True,  # Sử dụng VLM để xử lý hình ảnh
        top_k=20,  # Lấy top 20 chunks liên quan nhất
        enable_rerank=False  # Tắt rerank để tăng tốc độ
    )
    
    print("📄 Kết quả truy vấn:")
    print(result)
    
    return result

if __name__ == "__main__":
    # Kiểm tra API key
    if API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        print("❌ Vui lòng thiết lập biến môi trường OPENAI_API_KEY hoặc thay thế API_KEY trong code!")
        print("💡 Cách thiết lập: export OPENAI_API_KEY='your-api-key-here'")
        exit(1)
    
    # Chạy chương trình chính
    asyncio.run(main())
