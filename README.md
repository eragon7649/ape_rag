# APE RAG - Hệ Thống Xử Lý Tài Liệu Thông Minh

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Tổng Quan

APE RAG (Advanced Processing Engine - Retrieval-Augmented Generation) là hệ thống AI tiên tiến được thiết kế để tự động hóa việc xử lý, phân tích và trích xuất thông tin từ tài liệu cuộc họp và các văn bản doanh nghiệp. Hệ thống sử dụng công nghệ RAG (Retrieval-Augmented Generation) kết hợp với các mô hình AI mới nhất để tạo ra nội dung có cấu trúc và dễ hiểu.

## ✨ Tính Năng Chính

### 🔄 Xử Lý Đa Định Dạng
- **PDF**: OCR viết tay, trích xuất bảng biểu, phân tích layout
- **DOCX**: Bảo toàn định dạng, trích xuất đoạn văn và bảng
- **TXT**: Hỗ trợ nhiều encoding (UTF-8, Latin-1, CP1252)
- **HTML/Markdown**: Làm sạch nội dung và trích xuất text

### 🧠 Trích Xuất Thông Minh
- **Entity Recognition**: Người, tổ chức, ngày tháng, quyết định
- **Structured Data**: Tiêu đề, bảng biểu, danh sách, thông tin cuộc họp
- **Metadata Analysis**: Phát hiện loại tài liệu, ngôn ngữ, từ khóa
- **Relationship Mapping**: Mối quan hệ giữa các thực thể

### 📝 Tạo Nội Dung Tự Động
- **Tóm tắt thông minh**: Cấu trúc rõ ràng với thông tin chính
- **Nội dung đầy đủ**: Chi tiết toàn diện với định dạng chuẩn
- **Template-based**: Sử dụng template tùy chỉnh cho từng loại tài liệu
- **Multi-language**: Hỗ trợ tiếng Việt và tiếng Anh

### 🚀 Tính Năng Nâng Cao
- **Incremental Processing**: Chỉ xử lý file mới hoặc đã thay đổi
- **Error Handling**: Retry với exponential backoff (3 lần thử)
- **Real-time Status**: Cập nhật trạng thái xử lý trực tiếp
- **File Tracking**: Phát hiện thay đổi dựa trên hash MD5

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Layer   │    │ Processing Layer │    │  AI Models      │
│                 │    │                  │    │                 │
│ • PDF/DOCX/TXT  │───▶│ • RAGAnything    │───▶│ • GPT-4o-mini   │
│ • File Upload   │    │ • LightRAG       │    │ • GPT-4o (VLM)  │
│ • Validation    │    │ • Document Parser│    │ • Embeddings    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Storage Layer  │    │  Output Layer    │    │  Interface      │
│                 │    │                  │    │                 │
│ • Vector DB     │◀───│ • Summary.txt    │◀───│ • Streamlit UI  │
│ • JSON Storage  │    │ • Full_Content   │    │ • Real-time     │
│ • File System   │    │ • Error Reports  │    │ • Progress      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Công Nghệ Sử Dụng

### AI/ML Framework
- **OpenAI GPT-4o-mini**: Xử lý văn bản và tạo nội dung
- **OpenAI GPT-4o**: Xử lý hình ảnh và OCR
- **text-embedding-3-large**: Vector embeddings (3072 dimensions)
- **RAGAnything**: Engine xử lý tài liệu chính
- **LightRAG**: Xây dựng knowledge graph

### Backend Technologies
- **Python 3.13**: Ngôn ngữ lập trình chính
- **asyncio**: Xử lý bất đồng bộ
- **Pydantic**: Validation dữ liệu
- **BeautifulSoup4 + lxml**: Xử lý HTML/XML
- **python-docx**: Xử lý file Microsoft Word
- **hashlib**: Phát hiện thay đổi file (MD5)

### Frontend & Interface
- **Streamlit**: Giao diện web trực quan
- **Custom CSS**: Thiết kế chuyên nghiệp
- **File Upload/Download**: Giao diện kéo thả
- **Progress Tracking**: Hiển thị tiến trình real-time

### Storage & Infrastructure
- **Vector Database**: Lưu trữ chunks và embeddings
- **JSON Storage**: Metadata, cache, file tracking
- **File System**: Tài liệu đã parse, hình ảnh, layout
- **Incremental System**: Hệ thống theo dõi thay đổi

## 📊 Hiệu Suất & Yêu Cầu Hệ Thống

### Thời Gian Xử Lý (Ước tính)
- **PDF (10-20 trang)**: 20-45 giây
- **DOCX (5-15 trang)**: 15-30 giây  
- **TXT (1-5 trang)**: 5-15 giây
- **HTML/MD (1-10 trang)**: 10-25 giây



## 🚀 Cài Đặt & Sử Dụng

### 1. Cài Đặt Dependencies

```bash
# Clone repository
git clone <repository-url>
cd ape_rag

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu Hình Environment

```bash
# Tạo file .env
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
echo "OPENAI_BASE_URL=https://api.openai.com/v1" >> .env
```

### 3. Chạy Hệ Thống

```bash
# Chạy xử lý tài liệu
python src/main.py

# Chạy giao diện web
streamlit run test_interface.py

# Chạy xử lý incremental
python run_incremental_processor.py
```

## 📁 Cấu Trúc Dự Án

```
ape_rag/
├── src/                          # Source code chính
│   ├── core/                     # Core modules
│   │   ├── config.py            # Cấu hình hệ thống
│   │   ├── rag_processor.py     # RAG processing engine
│   │   ├── document_parser.py   # Document parsing
│   │   ├── content_extractor.py # Content extraction
│   │   ├── incremental_processor.py # Incremental processing
│   │   └── error_handler.py     # Error handling
│   ├── data/                    # Data và prompts
│   │   └── extraction_prompts.py
│   └── main.py                  # Entry point
├── documents/                   # Thư mục input
├── output/                      # Thư mục output
├── rag_storage/                 # RAG storage
├── test_interface.py           # Streamlit interface
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## 🔄 Quy Trình Xử Lý

### 1. Upload & Validation (1-2s)
- Upload file qua giao diện web
- Kiểm tra định dạng và kích thước
- Phát hiện encoding và thông tin file

### 2. Document Parsing (5-15s)
- **PDF**: Sử dụng MinerU với multiple methods
- **DOCX**: python-docx extraction
- **TXT**: Multi-encoding fallback
- **HTML**: BeautifulSoup cleaning

### 3. AI Analysis (10-30s)
- Chunking và vectorization
- Entity extraction (8 structured queries)
- Metadata analysis và language detection
- Relationship mapping

### 4. Content Generation (5-15s)
- Tạo summary với template
- Tạo full content có cấu trúc
- Error handling với retry
- Quality assurance

### 5. Output & Storage (1-3s)
- Tạo file Summary.txt và Full_Content.txt
- Lưu trữ vector và metadata
- Cập nhật tracking status
- Sẵn sàng download

## 📈 Ví Dụ Kết Quả

### Input: Biên bản cuộc họp PDF
```
Biên bản cuộc họp ngày 27/10/2025
Tham gia: Ông Nguyễn Văn A, Bà Trần Thị B, Ông Lê Văn C
Nội dung: Đánh giá kết quả quý III, lên kế hoạch quý IV
```

### Output: Summary.txt
```
### THÔNG TIN CHÍNH
- Tiêu đề: Biên Bản Cuộc Họp
- Ngày: 09h00, ngày 27 tháng 10 năm 2025
- Người liên quan: Ông Nguyễn Văn A, Bà Trần Thị B, Ông Lê Văn C

### NỘI DUNG QUAN TRỌNG
- Đánh giá kết quả hoạt động kinh doanh quý III/2025
- Thảo luận kế hoạch sản xuất – kinh doanh quý IV/2025
- Quyết định: Thực hiện chương trình cải tiến quy trình nội bộ

### HÀNH ĐỘNG CẦN THỰC HIỆN
- Phòng Kinh doanh: Hoàn thiện kế hoạch doanh số trước 05/11/2025
- Phòng Kế toán: Lập dự toán chi phí cho từng bộ phận
- Phòng Sản xuất: Đề xuất danh mục đầu tư thiết bị trước 10/11/2025
```

## 🔧 Cấu Hình Nâng Cao

### Tùy Chỉnh Models
```python
# src/core/config.py
LLM_MODEL = "gpt-4o-mini"           # Text processing
VLM_MODEL = "gpt-4o"                # Vision processing  
EMBEDDING_MODEL = "text-embedding-3-large"  # Embeddings
EMBEDDING_DIM = 3072                # Vector dimensions
```

### Tùy Chỉnh Prompts
```python
# src/data/extraction_prompts.py
SUMMARY_TEMPLATE = """
# Custom summary template
...
"""
```

**APE RAG** - Tự động hóa xử lý tài liệu với AI tiên tiến 🚀
