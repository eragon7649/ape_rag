# src/core/output_formatter.py

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from typing import Dict, Any, List
import os
import json
from datetime import datetime

class OutputFormatter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def create_summary_txt(self, extracted_data: Dict[str, Any], file_name: str):
        """Tạo file TXT tóm tắt ngắn gọn"""
        # Lấy nội dung đã được AI xử lý
        summary_content = extracted_data.get('summary_content', '')
        raw_content = extracted_data.get('raw_content', '')
        
        # Nếu không có summary_content từ AI, tạo tóm tắt đơn giản từ raw_content
        if not summary_content and raw_content:
            summary_content = self._create_simple_summary(raw_content)
        
        content = f"""
========================================
BẢN TÓM TẮT: {file_name}
========================================
Thời gian xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Loại file: {extracted_data.get('file_info', {}).get('format', 'Unknown')}

========================================
NỘI DUNG TÓM TẮT:
========================================

{summary_content}

========================================
THÔNG TIN FILE:
========================================
- Tên file gốc: {extracted_data.get('file_info', {}).get('name', 'N/A')}
- Kích thước: {extracted_data.get('file_info', {}).get('size_mb', 0):.2f} MB
- Thời gian xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        output_path = os.path.join(self.output_dir, f"SUMMARY_{file_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Đã tạo file tóm tắt tại: {output_path}")
        return output_path

    def create_full_content_txt(self, extracted_data: Dict[str, Any], file_name: str):
        """Tạo file TXT chứa toàn bộ nội dung"""
        # Lấy nội dung đầy đủ từ AI hoặc raw content
        full_content = extracted_data.get('full_content', '')
        raw_content = extracted_data.get('raw_content', '')
        
        # Nếu không có full_content từ AI, sử dụng raw_content
        if not full_content and raw_content:
            full_content = raw_content
        
        content = f"""
========================================
NỘI DUNG ĐẦY ĐỦ: {file_name}
========================================
Thời gian xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Loại file: {extracted_data.get('file_info', {}).get('format', 'Unknown')}

========================================
THÔNG TIN FILE:
========================================
- Tên file gốc: {extracted_data.get('file_info', {}).get('name', 'N/A')}
- Kích thước: {extracted_data.get('file_info', {}).get('size_mb', 0):.2f} MB
- Đường dẫn: {extracted_data.get('file_info', {}).get('path', 'N/A')}
- Thời gian tạo: {extracted_data.get('file_info', {}).get('created', 'N/A')}
- Thời gian sửa đổi: {extracted_data.get('file_info', {}).get('modified', 'N/A')}

========================================
NỘI DUNG CHI TIẾT:
========================================

{full_content}

========================================
THÔNG TIN XỬ LÝ:
========================================
- Thời gian xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Trạng thái: Hoàn thành
- Chất lượng: {'Tốt' if full_content else 'Cần kiểm tra'}
"""
        
        output_path = os.path.join(self.output_dir, f"FULL_CONTENT_{file_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Đã tạo file nội dung đầy đủ tại: {output_path}")
        return output_path

    def _create_simple_summary(self, raw_content: str) -> str:
        """Tạo tóm tắt đơn giản từ raw content"""
        # Lấy 500 ký tự đầu và cuối
        if len(raw_content) <= 1000:
            return raw_content
        
        first_part = raw_content[:500]
        last_part = raw_content[-500:]
        
        return f"""
{first_part}

... (nội dung ở giữa đã được rút gọn) ...

{last_part}

Lưu ý: Đây là tóm tắt tự động. Để xem nội dung đầy đủ, vui lòng tham khảo file FULL_CONTENT.
"""

