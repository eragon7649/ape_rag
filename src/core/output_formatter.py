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

    def to_word_document(self, data: Dict[str, Any], file_name: str):
        """Chuyển dữ liệu JSON thành tài liệu Word (.docx)."""
        doc = Document()
        
        doc.add_heading('Biên Bản Tóm Tắt Cuộc Họp (AI Generated)', 0)
        
        doc.add_paragraph(f"Tên Cuộc Họp: {data.get('meeting_title', 'N/A')}")
        doc.add_paragraph(f"Ngày: {data.get('date', 'N/A')}")
        doc.add_paragraph(f"Người Tham Gia: {', '.join(data.get('participants', []))}")
        
        doc.add_heading('Quyết Định và Mục Hành Động', level=1)
        
        decisions = data.get('decisions', [])
        if decisions:
            for item in decisions:
                doc.add_paragraph(
                    f"Quyết Định #{item['decision_id']}: {item['description']}\n"
                    f" - Người chịu trách nhiệm: {item['responsible_person']}\n"
                    f" - Deadline: {item['due_date']}"
                )
        else:
            doc.add_paragraph("Không có quyết định chính thức nào được trích xuất.")
            
        output_path = os.path.join(self.output_dir, f"{file_name}.docx")
        doc.save(output_path)
        print(f"✅ Đã tạo tệp Word thành công tại: {output_path}")
        return output_path

    def to_database(self, data: Dict[str, Any]):
        """Mẫu logic để ghi dữ liệu vào cơ sở dữ liệu (ví dụ: PostgreSQL)"""
        # Trong thực tế, cần sử dụng thư viện kết nối DB như psycopg2 hoặc SQLAlchemy ORM.
        print("\n--- GHI VÀO CƠ SỞ DỮ LIỆU ---")
        print(f"📥 Kết nối đến DB và ghi dữ liệu có cấu trúc cho: {data.get('meeting_title', 'N/A')}")
        # Logic SQL INSERT/UPDATE sẽ được đặt ở đây
        print("✅ Ghi CSDL thành công (Logic mô phỏng).")

    def to_raw_content_txt(self, raw_content: str, file_name: str):
        """Xuất toàn bộ nội dung gốc của tài liệu thành file TXT"""
        # Tạo header cho file
        header = f"""
========================================
NỘI DUNG GỐC CỦA TÀI LIỆU: {file_name}
========================================
Thời gian xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Trạng thái: Đã đọc thành công
Loại dữ liệu: Nội dung gốc từ tài liệu

========================================
NỘI DUNG:
========================================

"""
        
        # Kết hợp header và nội dung
        full_content = header + raw_content
        
        # Lưu file TXT
        output_path = os.path.join(self.output_dir, f"RAW_CONTENT_{file_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✅ Đã tạo file nội dung gốc tại: {output_path}")
        return output_path

    def to_comprehensive_txt(self, extracted_data: Dict[str, Any], file_name: str):
        """Tạo file TXT toàn diện với nhiều thông tin"""
        content = f"""
========================================
BÁO CÁO TOÀN DIỆN: {file_name}
========================================
Thời gian xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Trạng thái: Đã xử lý thành công

========================================
1. THÔNG TIN FILE
========================================
- Tên file: {extracted_data.get('file_info', {}).get('name', 'N/A')}
- Kích thước: {extracted_data.get('file_info', {}).get('size', 'N/A')} bytes
- Format: {extracted_data.get('file_info', {}).get('format', 'N/A')}
- Encoding: {extracted_data.get('file_info', {}).get('encoding', 'N/A')}
- Thời gian tạo: {extracted_data.get('file_info', {}).get('created', 'N/A')}
- Thời gian sửa đổi: {extracted_data.get('file_info', {}).get('modified', 'N/A')}

========================================
2. NỘI DUNG GỐC
========================================
{extracted_data.get('raw_content', 'Không có nội dung')}

========================================
3. NỘI DUNG CÓ CẤU TRÚC
========================================
{self._format_structured_content(extracted_data.get('structured_content', {}))}

========================================
4. METADATA
========================================
{self._format_metadata(extracted_data.get('metadata', {}))}

========================================
5. THÔNG TIN ĐẶC BIỆT (PDF)
========================================
{self._format_pdf_specific(extracted_data.get('pdf_specific', {}))}

========================================
6. THÔNG TIN XỬ LÝ
========================================
- Thời gian trích xuất: {extracted_data.get('extraction_timestamp', 'N/A')}
- Trạng thái: Hoàn thành
- Chất lượng: {'Tốt' if extracted_data.get('raw_content') else 'Cần kiểm tra'}
"""
        
        output_path = os.path.join(self.output_dir, f"COMPREHENSIVE_{file_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Đã tạo file báo cáo toàn diện tại: {output_path}")
        return output_path

    def to_json_output(self, extracted_data: Dict[str, Any], file_name: str):
        """Tạo file JSON với dữ liệu đầy đủ"""
        # Làm sạch dữ liệu để có thể serialize
        clean_data = self._clean_data_for_json(extracted_data)
        
        output_path = os.path.join(self.output_dir, f"DATA_{file_name}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã tạo file JSON tại: {output_path}")
        return output_path

    def to_summary_report(self, extracted_data: Dict[str, Any], file_name: str):
        """Tạo báo cáo tóm tắt ngắn gọn"""
        file_info = extracted_data.get('file_info', {})
        structured_content = extracted_data.get('structured_content', {})
        
        content = f"""
BÁO CÁO TÓM TẮT: {file_name}
========================================
📁 File: {file_info.get('name', 'N/A')} ({file_info.get('size_mb', 0)}MB)
📅 Xử lý: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 NỘI DUNG CHÍNH:
{self._extract_main_content(structured_content)}

🎯 THÔNG TIN QUAN TRỌNG:
{self._extract_key_info(structured_content)}

📊 THỐNG KÊ:
- Số tiêu đề: {len(structured_content.get('headings', '').split('\n')) if structured_content.get('headings') else 0}
- Số bảng: {len(structured_content.get('tables', '').split('\n')) if structured_content.get('tables') else 0}
- Số quyết định: {len(structured_content.get('decisions', '').split('\n')) if structured_content.get('decisions') else 0}
"""
        
        output_path = os.path.join(self.output_dir, f"SUMMARY_{file_name}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Đã tạo báo cáo tóm tắt tại: {output_path}")
        return output_path

    def _format_structured_content(self, structured_content: Dict[str, Any]) -> str:
        """Format nội dung có cấu trúc"""
        if not structured_content:
            return "Không có nội dung có cấu trúc"
        
        formatted = ""
        for key, value in structured_content.items():
            if value and value != "Error: ...":
                formatted += f"\n--- {key.upper()} ---\n"
                formatted += str(value)[:500] + ("..." if len(str(value)) > 500 else "")
                formatted += "\n"
        
        return formatted or "Không có dữ liệu có cấu trúc"

    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata"""
        if not metadata:
            return "Không có metadata"
        
        formatted = ""
        for key, value in metadata.items():
            if isinstance(value, (str, int, float)):
                formatted += f"- {key}: {value}\n"
            elif isinstance(value, list):
                formatted += f"- {key}: {', '.join(map(str, value))}\n"
            else:
                formatted += f"- {key}: {str(value)[:100]}...\n"
        
        return formatted or "Không có metadata"

    def _format_pdf_specific(self, pdf_specific: Dict[str, Any]) -> str:
        """Format thông tin đặc biệt của PDF"""
        if not pdf_specific:
            return "Không phải file PDF hoặc không có thông tin đặc biệt"
        
        formatted = ""
        if pdf_specific.get('parsed_files'):
            formatted += f"Files đã parse: {', '.join(pdf_specific['parsed_files'])}\n"
        
        if pdf_specific.get('images'):
            formatted += f"Images: {', '.join(pdf_specific['images'])}\n"
        
        if pdf_specific.get('tables'):
            formatted += f"Tables: {', '.join(pdf_specific['tables'])}\n"
        
        return formatted or "Không có thông tin đặc biệt"

    def _clean_data_for_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Làm sạch dữ liệu để có thể serialize thành JSON"""
        def clean_value(value):
            if isinstance(value, (str, int, float, bool, type(None))):
                return value
            elif isinstance(value, dict):
                return {k: clean_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [clean_value(item) for item in value]
            else:
                return str(value)
        
        return clean_value(data)

    def _extract_main_content(self, structured_content: Dict[str, Any]) -> str:
        """Trích xuất nội dung chính"""
        main_parts = []
        
        if structured_content.get('meeting_info'):
            main_parts.append(f"Thông tin cuộc họp: {structured_content['meeting_info'][:200]}...")
        
        if structured_content.get('headings'):
            main_parts.append(f"Tiêu đề: {structured_content['headings'][:200]}...")
        
        if structured_content.get('decisions'):
            main_parts.append(f"Quyết định: {structured_content['decisions'][:200]}...")
        
        return "\n".join(main_parts) if main_parts else "Không có nội dung chính"

    def _extract_key_info(self, structured_content: Dict[str, Any]) -> str:
        """Trích xuất thông tin quan trọng"""
        key_parts = []
        
        if structured_content.get('people'):
            key_parts.append(f"Người tham gia: {structured_content['people'][:100]}...")
        
        if structured_content.get('dates'):
            key_parts.append(f"Ngày tháng: {structured_content['dates'][:100]}...")
        
        if structured_content.get('organizations'):
            key_parts.append(f"Tổ chức: {structured_content['organizations'][:100]}...")
        
        return "\n".join(key_parts) if key_parts else "Không có thông tin quan trọng"

    def _setup_document_styles(self, doc):
        """Thiết lập các style cho document"""
        # Style cho heading
        styles = doc.styles
        
        # Tạo style cho code/raw data
        if 'Code' not in [style.name for style in styles]:
            code_style = styles.add_style('Code', WD_STYLE_TYPE.PARAGRAPH)
            code_style.font.name = 'Courier New'
            code_style.font.size = Pt(9)
