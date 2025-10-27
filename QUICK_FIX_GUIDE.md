# 🚀 Quick Fix Guide - RAG Meeting Processor

## ✅ **Vấn đề đã được khắc phục!**

Lỗi **"No LightRAG instance available"** đã được giải quyết thành công.

## 🎯 **Cách sử dụng:**

### **Cách 1: Sử dụng Script Tự động (Khuyến nghị)**
```bash
# Chạy script với menu tương tác
./run_commands.sh
```

### **Cách 2: Chạy từng lệnh riêng lẻ**

#### **1. Kích hoạt Virtual Environment:**
```bash
source .venv/bin/activate
```

#### **2. Thiết lập API Key:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

#### **3. Chạy Web Interface:**
```bash
streamlit run test_interface.py
```
**→ Truy cập: http://localhost:8501**

#### **4. Chạy Incremental Processing:**
```bash
python run_incremental_processor.py
```

#### **5. Chạy Demo:**
```bash
python demo_incremental.py
```

## 🔧 **Các lệnh hữu ích:**

### **Kiểm tra trạng thái hệ thống:**
```bash
python test_fix.py
```

### **Kiểm tra processing status:**
```bash
python -c "
import sys; sys.path.insert(0, 'src')
from core.rag_processor import MeetingProcessor
processor = MeetingProcessor()
status = processor.get_processing_status()
print(f'Total: {status[\"total_files\"]}')
print(f'Processed: {status[\"processed_files\"]}')
print(f'Failed: {status[\"failed_files\"]}')
"
```

### **Reset file tracking:**
```bash
python -c "
import sys; sys.path.insert(0, 'src')
from core.rag_processor import MeetingProcessor
processor = MeetingProcessor()
processor.reset_file_tracking()
print('✅ Reset completed')
"
```

## 📋 **Tính năng chính:**

### **🌐 Web Interface (`test_interface.py`):**
- **Menu 1 - Upload & Process**: Upload file và xử lý
- **Menu 2 - View Reports**: Xem reports của file đã xử lý
- **Real-time processing status**
- **File content preview**

### **🔄 Incremental Processing (`run_incremental_processor.py`):**
- Chỉ xử lý file mới/thay đổi
- Tự động generate outputs
- Production-ready

### **🧪 Demo Script (`demo_incremental.py`):**
- Hiển thị cách incremental processing hoạt động
- Detailed logging
- Educational purpose

## 🎉 **Kết quả:**

✅ **Tất cả dependencies đã được cài đặt**  
✅ **Virtual environment đã được tạo**  
✅ **RAGAnything và LightRAG hoạt động bình thường**  
✅ **API Key đã được thiết lập**  
✅ **Streamlit web interface chạy thành công**  
✅ **Incremental processing system hoạt động**  

## 🚀 **Bước tiếp theo:**

1. **Chạy web interface**: `./run_commands.sh` → chọn option 1
2. **Upload file test**: Sử dụng menu Upload & Process
3. **Xem reports**: Sử dụng menu View Reports
4. **Test incremental**: Upload file mới và xem hệ thống chỉ xử lý file đó

**Hệ thống đã sẵn sàng để sử dụng!** 🎯
