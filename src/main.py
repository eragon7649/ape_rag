# src/main.py

import asyncio
import os
import sys
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.rag_processor import MeetingProcessor
from core.output_formatter import OutputFormatter
from core.config import DOCUMENTS_DIR, OUTPUT_DIR
from core.config_validator import ConfigValidator
from core.error_handler import ErrorHandler

# --- Hàm kiểm tra trạng thái và khởi động ---
async def run_processing_pipeline():
    if not os.path.exists(DOCUMENTS_DIR):
        print(f"❌ Thư mục đầu vào không tồn tại: {DOCUMENTS_DIR}")
        print("Vui lòng tạo thư mục 'documents' và đặt tệp biên bản vào đó.")
        sys.exit(1)
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Khởi tạo các component
    processor = MeetingProcessor()
    formatter = OutputFormatter(OUTPUT_DIR)
    validator = ConfigValidator()
    error_handler = ErrorHandler()
    
    # 2. Validation toàn bộ thư mục
    print("🔍 Đang validate thư mục documents...")
    dir_validation = validator.validate_directory(DOCUMENTS_DIR)
    
    if not dir_validation['valid']:
        print(f"❌ Validation thư mục thất bại: {', '.join(dir_validation['errors'])}")
        return
    
    print(f"📁 Tìm thấy {dir_validation['summary']['total_files']} file(s) trong thư mục documents")
    print(f"✅ {dir_validation['summary']['valid_files']} file hợp lệ, {dir_validation['summary']['invalid_files']} file không hợp lệ")
    
    # 3. Xử lý từng file với error handling
    processing_results = []
    
    for file_info in dir_validation['files']:
        file_name = file_info['name']
        file_path = file_info['path']
        file_validation = file_info['validation']
        
        if not file_validation['valid']:
            print(f"⏭️  Bỏ qua file không hợp lệ: {file_name}")
            processing_results.append({
                'file_path': file_path,
                'success': False,
                'error': f"Validation failed: {', '.join(file_validation['errors'])}"
            })
            continue
        
        print("\n==============================================")
        print(f"🚀 Bắt đầu xử lý Tệp: {file_name}")
        
        # Xử lý file với error handling
        try:
            result = await error_handler.safe_execute(
                processor.process_document_and_extract, file_path
            )
            
            if result['success']:
                extracted_data = result['result']
                
                if extracted_data.get("error"):
                    print(f"🛑 Xử lý thất bại cho {file_name}: {extracted_data['error']}")
                    processing_results.append({
                        'file_path': file_path,
                        'success': False,
                        'error': extracted_data['error']
                    })
                    continue
                
                print("\n--- TẠO ĐẦU RA (AUTOMATED OUTPUT) ---")
                
                # Tạo nhiều loại output
                file_base_name = os.path.splitext(file_name)[0]
                
                # 1. Database (mô phỏng)
                formatter.to_database(extracted_data.get('extracted_json', {}))
                
                # 2. Word document (nếu có JSON data)
                if extracted_data.get('extracted_json'):
                    formatter.to_word_document(extracted_data['extracted_json'], f"SUMMARY_{file_base_name}")
                
                # 3. Raw content TXT
                raw_content = extracted_data.get('raw_content', '')
                formatter.to_raw_content_txt(raw_content, file_base_name)
                
                # 4. Comprehensive TXT (mới)
                formatter.to_comprehensive_txt(extracted_data, file_base_name)
                
                # 5. JSON output (mới)
                formatter.to_json_output(extracted_data, file_base_name)
                
                # 6. Summary report (mới)
                formatter.to_summary_report(extracted_data, file_base_name)
                
                processing_results.append({
                    'file_path': file_path,
                    'success': True,
                    'execution_time': result['execution_time']
                })
                
            else:
                print(f"❌ Xử lý thất bại {file_name}: {result['error']['message']}")
                processing_results.append({
                    'file_path': file_path,
                    'success': False,
                    'error': result['error']['message']
                })
                
        except Exception as e:
            print(f"❌ Lỗi không mong đợi {file_name}: {str(e)}")
            processing_results.append({
                'file_path': file_path,
                'success': False,
                'error': str(e)
            })
    
    # 4. Tạo báo cáo tổng kết
    print("\n" + "="*50)
    print("📊 BÁO CÁO TỔNG KẾT")
    print("="*50)
    
    error_report = error_handler.create_error_report(processing_results)
    print(error_report)
    
    # Lưu báo cáo vào file
    report_path = os.path.join(OUTPUT_DIR, f"PROCESSING_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(error_report)
    print(f"📄 Báo cáo đã được lưu tại: {report_path}")

if __name__ == "__main__":
    # Đảm bảo thư mục được tạo trước khi chạy
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Chạy quy trình chính
    asyncio.run(run_processing_pipeline())
