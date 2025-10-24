# src/core/config_validator.py

import os
import mimetypes
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib

class ConfigValidator:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            'max_file_size': 50 * 1024 * 1024,  # 50MB
            'min_file_size': 100,  # 100 bytes
            'supported_formats': ['.pdf', '.txt', '.docx', '.md', '.html'],
            'max_filename_length': 255,
            'allowed_mime_types': [
                'application/pdf',
                'text/plain',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/markdown',
                'text/html'
            ],
            'check_encoding': True,
            'check_corruption': True
        }
    
    def validate_file_input(self, file_path: str) -> Dict[str, Any]:
        """Validate file input trước khi xử lý"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'file_info': {},
            'recommendations': []
        }
        
        try:
            # 1. Kiểm tra file tồn tại
            if not os.path.exists(file_path):
                validation_result['valid'] = False
                validation_result['errors'].append(f"File không tồn tại: {file_path}")
                return validation_result
            
            # 2. Lấy thông tin file
            file_info = self._get_file_info(file_path)
            validation_result['file_info'] = file_info
            
            # 3. Kiểm tra quyền đọc
            if not os.access(file_path, os.R_OK):
                validation_result['valid'] = False
                validation_result['errors'].append(f"Không có quyền đọc file: {file_path}")
            
            # 4. Kiểm tra kích thước file
            file_size = file_info.get('size', 0)
            if file_size < self.config['min_file_size']:
                validation_result['valid'] = False
                validation_result['errors'].append(f"File quá nhỏ (< {self.config['min_file_size']} bytes)")
            
            if file_size > self.config['max_file_size']:
                validation_result['warnings'].append(f"File quá lớn ({file_size / 1024 / 1024:.1f}MB), có thể xử lý chậm")
                validation_result['recommendations'].append("Xem xét chia nhỏ file hoặc tăng timeout")
            
            # 5. Kiểm tra tên file
            filename = os.path.basename(file_path)
            if len(filename) > self.config['max_filename_length']:
                validation_result['warnings'].append(f"Tên file quá dài ({len(filename)} ký tự)")
            
            # 6. Kiểm tra format
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.config['supported_formats']:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Format {file_ext} không được hỗ trợ. Các format hỗ trợ: {self.config['supported_formats']}")
            
            # 7. Kiểm tra MIME type
            mime_type = file_info.get('mime_type')
            if mime_type and mime_type not in self.config['allowed_mime_types']:
                validation_result['warnings'].append(f"MIME type {mime_type} không khớp với extension {file_ext}")
            
            # 8. Kiểm tra encoding (cho text files)
            if self.config['check_encoding'] and file_ext in ['.txt', '.md', '.html']:
                encoding_check = self._check_encoding(file_path)
                if not encoding_check['valid']:
                    validation_result['warnings'].append(f"Vấn đề encoding: {encoding_check['message']}")
                    validation_result['recommendations'].append(f"Thử encoding: {', '.join(encoding_check['suggested_encodings'])}")
            
            # 9. Kiểm tra corruption (cho PDF)
            if self.config['check_corruption'] and file_ext == '.pdf':
                corruption_check = self._check_pdf_corruption(file_path)
                if not corruption_check['valid']:
                    validation_result['warnings'].append(f"File PDF có thể bị corrupt: {corruption_check['message']}")
            
            # 10. Kiểm tra nội dung cơ bản
            content_check = self._check_basic_content(file_path, file_ext)
            if not content_check['valid']:
                validation_result['warnings'].append(f"File có thể trống hoặc không có nội dung hữu ích")
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Lỗi validation: {str(e)}")
        
        return validation_result
    
    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Lấy thông tin chi tiết về file"""
        try:
            stat = os.stat(file_path)
            filename = os.path.basename(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Lấy MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            
            # Tính hash để kiểm tra integrity
            file_hash = self._calculate_file_hash(file_path)
            
            return {
                'name': filename,
                'path': file_path,
                'size': stat.st_size,
                'format': file_ext,
                'mime_type': mime_type,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK),
                'hash': file_hash,
                'size_mb': round(stat.st_size / 1024 / 1024, 2)
            }
        except Exception as e:
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'error': f"Không thể lấy thông tin file: {e}"
            }
    
    def _check_encoding(self, file_path: str) -> Dict[str, Any]:
        """Kiểm tra encoding của file text"""
        encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'ascii']
        successful_encodings = []
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read(1000)  # Chỉ đọc 1000 ký tự đầu
                successful_encodings.append(encoding)
            except UnicodeDecodeError:
                continue
            except Exception:
                continue
        
        if successful_encodings:
            return {
                'valid': True,
                'supported_encodings': successful_encodings,
                'recommended': successful_encodings[0]
            }
        else:
            return {
                'valid': False,
                'message': 'Không thể đọc file với các encoding thông dụng',
                'suggested_encodings': encodings_to_try
            }
    
    def _check_pdf_corruption(self, file_path: str) -> Dict[str, Any]:
        """Kiểm tra file PDF có bị corrupt không"""
        try:
            with open(file_path, 'rb') as f:
                # Đọc header
                header = f.read(8)
                if not header.startswith(b'%PDF-'):
                    return {
                        'valid': False,
                        'message': 'File không có PDF header hợp lệ'
                    }
                
                # Đọc footer
                f.seek(-100, 2)  # Đọc 100 bytes cuối
                footer = f.read()
                if b'%%EOF' not in footer:
                    return {
                        'valid': False,
                        'message': 'File không có PDF footer hợp lệ'
                    }
                
                return {
                    'valid': True,
                    'message': 'File PDF có vẻ hợp lệ'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'message': f'Không thể kiểm tra PDF: {e}'
            }
    
    def _check_basic_content(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Kiểm tra nội dung cơ bản của file"""
        try:
            if file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000)  # Đọc 1000 ký tự đầu
                    if len(content.strip()) < 10:
                        return {
                            'valid': False,
                            'message': 'File text có vẻ trống hoặc quá ngắn'
                        }
            
            elif file_ext == '.pdf':
                with open(file_path, 'rb') as f:
                    content = f.read(1000)
                    if len(content) < 100:
                        return {
                            'valid': False,
                            'message': 'File PDF quá nhỏ, có thể bị corrupt'
                        }
            
            return {
                'valid': True,
                'message': 'File có nội dung hợp lệ'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'Không thể kiểm tra nội dung: {e}'
            }
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Tính hash của file để kiểm tra integrity"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Chỉ đọc 1MB đầu để tính hash nhanh
                chunk = f.read(1024 * 1024)
                hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return "unknown"
    
    def validate_directory(self, dir_path: str) -> Dict[str, Any]:
        """Validate thư mục chứa files"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'files': [],
            'summary': {}
        }
        
        try:
            if not os.path.exists(dir_path):
                validation_result['valid'] = False
                validation_result['errors'].append(f"Thư mục không tồn tại: {dir_path}")
                return validation_result
            
            if not os.path.isdir(dir_path):
                validation_result['valid'] = False
                validation_result['errors'].append(f"Đường dẫn không phải là thư mục: {dir_path}")
                return validation_result
            
            if not os.access(dir_path, os.R_OK):
                validation_result['valid'] = False
                validation_result['errors'].append(f"Không có quyền đọc thư mục: {dir_path}")
                return validation_result
            
            # Liệt kê files
            files = []
            for filename in os.listdir(dir_path):
                if filename.startswith('.'):
                    continue  # Bỏ qua file ẩn
                
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    file_validation = self.validate_file_input(file_path)
                    files.append({
                        'name': filename,
                        'path': file_path,
                        'validation': file_validation
                    })
            
            validation_result['files'] = files
            
            # Tạo summary
            total_files = len(files)
            valid_files = len([f for f in files if f['validation']['valid']])
            files_with_warnings = len([f for f in files if f['validation']['warnings']])
            
            validation_result['summary'] = {
                'total_files': total_files,
                'valid_files': valid_files,
                'invalid_files': total_files - valid_files,
                'files_with_warnings': files_with_warnings,
                'success_rate': (valid_files / total_files * 100) if total_files > 0 else 0
            }
            
            if valid_files == 0 and total_files > 0:
                validation_result['valid'] = False
                validation_result['errors'].append("Không có file nào hợp lệ trong thư mục")
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Lỗi validate thư mục: {str(e)}")
        
        return validation_result
    
    def get_validation_report(self, validation_results: List[Dict[str, Any]]) -> str:
        """Tạo báo cáo validation"""
        total_files = len(validation_results)
        valid_files = len([r for r in validation_results if r['valid']])
        invalid_files = total_files - valid_files
        
        report = f"""
========================================
BÁO CÁO VALIDATION FILES
========================================
Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TỔNG QUAN:
- Tổng số file: {total_files}
- File hợp lệ: {valid_files}
- File không hợp lệ: {invalid_files}
- Tỷ lệ thành công: {(valid_files/total_files*100):.1f}%

"""
        
        if invalid_files > 0:
            report += "FILE KHÔNG HỢP LỆ:\n"
            for i, result in enumerate(validation_results, 1):
                if not result['valid']:
                    report += f"{i}. {result['file_info'].get('name', 'Unknown')}\n"
                    for error in result['errors']:
                        report += f"   ❌ {error}\n"
                    report += "\n"
        
        # Thống kê warnings
        files_with_warnings = [r for r in validation_results if r['warnings']]
        if files_with_warnings:
            report += f"FILE CÓ CẢNH BÁO ({len(files_with_warnings)} files):\n"
            for result in files_with_warnings:
                report += f"- {result['file_info'].get('name', 'Unknown')}\n"
                for warning in result['warnings']:
                    report += f"  ⚠️ {warning}\n"
        
        return report
