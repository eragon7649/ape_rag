# INCREMENTAL_PROCESSING_GUIDE.md

# Hướng dẫn sử dụng RAG Meeting Processor với Incremental Processing

## 🚀 Tính năng mới

### 1. Incremental Processing
- ✅ Chỉ xử lý file mới hoặc đã thay đổi
- ✅ Theo dõi trạng thái xử lý của từng file
- ✅ Tránh xử lý lại file không cần thiết
- ✅ Tiết kiệm thời gian và API calls

### 2. Giao diện Web với 2 Menu
- 📁 **Upload & Process**: Upload và xử lý file mới
- 📊 **View Reports**: Xem báo cáo của file đã xử lý

## 📋 Cài đặt

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình API Key
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

## 🎯 Cách sử dụng

### 1. Chạy giao diện Web (Khuyến nghị)
```bash
streamlit run test_interface.py
```

### 2. Chạy incremental processing từ command line
```bash
python run_incremental_processor.py
```

### 3. Chạy xử lý toàn bộ (cách cũ)
```bash
python run_processor.py
```

## 🔧 Giao diện Web

### Menu 1: Upload & Process
1. **Upload file**: Drag & drop hoặc click để chọn file
2. **Cấu hình**: Chọn các tùy chọn xử lý
3. **Process**: Click để xử lý file
4. **Status**: Xem trạng thái xử lý của tất cả files

### Menu 2: View Reports
1. **Chọn document**: Chọn file từ danh sách
2. **Xem output files**: Danh sách các file đã tạo
3. **Preview content**: Xem nội dung của từng file

## 📊 File Tracking System

### Cách hoạt động:
- File tracking được lưu trong `rag_storage/file_tracking.json`
- Theo dõi hash, thời gian sửa đổi của từng file
- Đánh dấu trạng thái xử lý (processed/failed/pending)

### Cấu trúc tracking:
```json
{
  "version": "1.0",
  "created_at": "2025-01-27T...",
  "files": {
    "document.pdf": {
      "path": "/path/to/document.pdf",
      "size": 1234567,
      "modified_time": 1640995200,
      "hash": "abc123...",
      "processed": true,
      "processed_at": "2025-01-27T...",
      "processing_result": {...}
    }
  }
}
```

## 🔄 Incremental Processing Logic

### 1. Scan Directory
- Quét thư mục `documents/`
- So sánh với dữ liệu tracking
- Xác định file cần xử lý

### 2. File Classification
- **New files**: File chưa có trong tracking
- **Changed files**: Hash hoặc modified_time khác
- **Unchanged files**: Không có thay đổi
- **Removed files**: File đã bị xóa

### 3. Processing
- Chỉ xử lý file mới/changed
- Cập nhật tracking sau khi xử lý
- Tạo output files

## 📁 Output Files

Mỗi file được xử lý sẽ tạo ra các output:
- `SUMMARY_filename.docx` - Tài liệu Word tóm tắt
- `COMPREHENSIVE_filename.txt` - Báo cáo toàn diện
- `DATA_filename.json` - Dữ liệu JSON
- `RAW_CONTENT_filename.txt` - Nội dung gốc
- `SUMMARY_filename.txt` - Báo cáo tóm tắt

## 🛠️ Troubleshooting

### 1. Reset File Tracking
```python
from src.core.rag_processor import MeetingProcessor
processor = MeetingProcessor()
processor.reset_file_tracking()  # Reset tất cả
processor.reset_file_tracking("filename.pdf")  # Reset file cụ thể
```

### 2. Kiểm tra trạng thái
```python
status = processor.get_processing_status()
print(f"Total: {status['total_files']}")
print(f"Processed: {status['processed_files']}")
print(f"Failed: {status['failed_files']}")
```

### 3. Xem chi tiết file
```python
status = processor.get_processing_status()
for filename, detail in status['files_detail'].items():
    print(f"{filename}: {detail['status']}")
```

## 🎨 Giao diện Features

### Upload Menu:
- ✅ Drag & drop file upload
- ✅ File type validation
- ✅ Processing options configuration
- ✅ Real-time processing status
- ✅ File processing history

### Report Menu:
- ✅ Document selection dropdown
- ✅ Output files listing
- ✅ File type identification
- ✅ Content preview
- ✅ File metadata display

## 🔍 Advanced Usage

### 1. Custom Processing Options
```python
# Trong giao diện web, có thể tùy chỉnh:
- Enable VLM Enhanced (for images)
- Enable Table Processing
- Enable Equation Processing
- Query Mode (hybrid/vector/graph)
- Top K Results
```

### 2. Batch Processing
```python
# Xử lý nhiều file cùng lúc
result = await processor.process_incremental(DOCUMENTS_DIR)
```

### 3. Error Handling
- Tự động retry với backoff
- Fallback methods cho parsing
- Detailed error reporting

## 📈 Performance Benefits

### Incremental Processing:
- ⚡ **Nhanh hơn**: Chỉ xử lý file thay đổi
- 💰 **Tiết kiệm**: Ít API calls hơn
- 🔄 **Hiệu quả**: Không xử lý lại file cũ
- 📊 **Theo dõi**: Biết chính xác file nào đã xử lý

### Web Interface:
- 🎯 **Dễ dùng**: Giao diện trực quan
- 📱 **Responsive**: Hoạt động trên mọi thiết bị
- 🔍 **Tìm kiếm**: Dễ dàng tìm và xem reports
- 📈 **Real-time**: Cập nhật trạng thái real-time

## 🚀 Next Steps

1. **Cross-document linking**: Liên kết kiến thức giữa các file
2. **Advanced search**: Tìm kiếm trong tất cả documents
3. **Analytics dashboard**: Thống kê và phân tích
4. **API endpoints**: REST API cho integration
5. **Multi-user support**: Hỗ trợ nhiều người dùng

## 📞 Support

Nếu gặp vấn đề, hãy kiểm tra:
1. API key đã được thiết lập chưa
2. File có format được hỗ trợ không
3. Dung lượng file có quá lớn không
4. Logs trong console để debug
