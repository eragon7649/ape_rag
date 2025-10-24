# RAG Meeting Processor

Hệ thống xử lý biên bản cuộc họp tự động sử dụng RAG-Anything để trích xuất thông tin quan trọng từ các tài liệu đa phương tiện (PDF, hình ảnh, văn bản viết tay).

## Tính năng chính

- 🔍 **Xử lý đa phương tiện**: Hỗ trợ PDF, hình ảnh, văn bản viết tay
- 🤖 **AI-Powered**: Sử dụng GPT-4o và GPT-4o-mini cho xử lý thông minh
- 📊 **Trích xuất có cấu trúc**: Chuyển đổi biên bản thành JSON có cấu trúc
- 📄 **Đầu ra đa dạng**: Tạo tài liệu Word, ghi vào cơ sở dữ liệu
- ⚡ **Tốc độ cao**: Xử lý dưới 1 phút/biên bản

## Cấu trúc dự án

```
rag-meeting-processor/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Cấu hình hệ thống và API keys
│   │   ├── rag_processor.py      # Logic xử lý RAG chính
│   │   └── output_formatter.py   # Chuyển đổi JSON sang Word/DB
│   ├── data/
│   │   └── extraction_prompts.py # Prompt templates cho trích xuất
│   └── main.py                   # Điểm khởi chạy hệ thống
├── documents/                    # Thư mục chứa tài liệu đầu vào
├── output/                       # Thư mục chứa kết quả đầu ra
├── rag_storage/                  # Lưu trữ Vector DB/Knowledge Graph
├── requirements.txt              # Dependencies
└── README.md                     # Tài liệu này
```

## Cài đặt

### Cách 1: Tự động (Khuyến nghị)

```bash
python setup.py
```

### Cách 2: Thủ công

#### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

#### 2. Cấu hình API Keys

Thiết lập các biến môi trường:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export OPENAI_BASE_URL="your_openai_base_url"  # Tùy chọn
```

#### 3. Cài đặt LibreOffice (cho xử lý tài liệu Office)

- **macOS**: `brew install --cask libreoffice`
- **Ubuntu**: `sudo apt-get install libreoffice`
- **Windows**: Tải từ [LibreOffice.org](https://www.libreoffice.org/)

## Sử dụng

### 1. Chuẩn bị tài liệu

Đặt các tệp biên bản cuộc họp vào thư mục `documents/`:
- `meeting_123_scan.pdf`
- `meeting_124_handwritten.jpg`
- `meeting_125_notes.docx`

### 2. Chạy hệ thống

```bash
# Từ thư mục gốc của dự án
python run_processor.py
```

Hoặc:

```bash
# Chạy trực tiếp từ thư mục src
cd src
python main.py
```

### 3. Kết quả

Hệ thống sẽ tự động:
1. Xử lý và lập chỉ mục tài liệu
2. Trích xuất thông tin quan trọng
3. Tạo tài liệu Word tóm tắt
4. Ghi dữ liệu vào cơ sở dữ liệu (mô phỏng)

Kết quả được lưu trong thư mục `output/`:
- `SUMMARY_meeting_123_scan.docx`
- `SUMMARY_meeting_124_handwritten.docx`

## Cấu hình

### Mô hình AI

Có thể tùy chỉnh trong `src/core/config.py`:

```python
LLM_MODEL = "gpt-4o-mini"        # Mô hình xử lý văn bản
VLM_MODEL = "gpt-4o"             # Mô hình xử lý hình ảnh
EMBEDDING_MODEL = "text-embedding-3-large"  # Mô hình embedding
```

### Schema trích xuất

Tùy chỉnh cấu trúc dữ liệu trong `src/data/extraction_prompts.py`:

```python
JSON_SCHEMA_TEMPLATE = """
{
    "meeting_title": "string",
    "date": "string", 
    "participants": "array of strings",
    "summary": "string",
    "decisions": [...],
    "action_items_count": "integer"
}
"""
```

## API Reference

### MeetingProcessor

Lớp chính xử lý tài liệu và trích xuất thông tin.

```python
processor = MeetingProcessor(api_key="your_key", base_url="your_url")
result = await processor.process_document_and_extract("path/to/document.pdf")
```

### OutputFormatter

Lớp chuyển đổi dữ liệu JSON thành các định dạng đầu ra.

```python
formatter = OutputFormatter("output_directory")
formatter.to_word_document(data, "filename")
formatter.to_database(data)
```

## Troubleshooting

### Lỗi thường gặp

1. **"API Key not found"**
   - Đảm bảo đã thiết lập biến môi trường `OPENAI_API_KEY`

2. **"LibreOffice not found"**
   - Cài đặt LibreOffice và đảm bảo có trong PATH

3. **"JSON Parsing Failed"**
   - Kiểm tra prompt template và cấu trúc dữ liệu đầu ra

### Logs và Debug

Hệ thống in ra các thông báo chi tiết trong quá trình xử lý:
- ✅ Thành công
- ❌ Lỗi
- 🚀 Bắt đầu xử lý
- 📥 Ghi dữ liệu

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.
