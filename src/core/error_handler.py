# src/core/error_handler.py

import asyncio
import logging
from typing import Dict, Any, Callable, Optional
from datetime import datetime
import traceback

class ErrorHandler:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            'max_retries': 3,
            'backoff_factor': 2,
            'initial_delay': 1,
            'max_delay': 60,
            'retry_on': ['rate_limit', 'timeout', 'connection_error', '429', '500', '502', '503', '504'],
            'log_errors': True,
            'log_level': 'INFO'
        }
        
        # Setup logging
        if self.config['log_errors']:
            logging.basicConfig(
                level=getattr(logging, self.config['log_level']),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None
    
    async def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """Retry function với exponential backoff"""
        last_exception = None
        
        for attempt in range(self.config['max_retries']):
            try:
                if self.logger:
                    self.logger.info(f"Thử lần {attempt + 1}/{self.config['max_retries']} cho function {func.__name__}")
                
                result = await func(*args, **kwargs)
                
                if attempt > 0 and self.logger:
                    self.logger.info(f"Thành công sau {attempt + 1} lần thử")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                if self.logger:
                    self.logger.warning(f"Lần thử {attempt + 1} thất bại: {str(e)}")
                
                # Kiểm tra có nên retry không
                if not self._should_retry(e) or attempt >= self.config['max_retries'] - 1:
                    break
                
                # Tính delay cho lần thử tiếp theo
                delay = min(
                    self.config['initial_delay'] * (self.config['backoff_factor'] ** attempt),
                    self.config['max_delay']
                )
                
                if self.logger:
                    self.logger.info(f"Chờ {delay}s trước khi thử lại...")
                
                await asyncio.sleep(delay)
        
        # Nếu tất cả retry đều thất bại
        if self.logger:
            self.logger.error(f"Tất cả {self.config['max_retries']} lần thử đều thất bại")
        
        raise last_exception
    
    def _should_retry(self, error: Exception) -> bool:
        """Kiểm tra có nên retry không dựa trên loại lỗi"""
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # Kiểm tra các pattern lỗi có thể retry
        for retry_pattern in self.config['retry_on']:
            if retry_pattern.lower() in error_str or retry_pattern.lower() in error_type:
                return True
        
        return False
    
    async def safe_execute(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Thực thi function một cách an toàn với error handling"""
        start_time = datetime.now()
        
        try:
            result = await self.retry_with_backoff(func, *args, **kwargs)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'attempts': 1,  # Sẽ được cập nhật trong retry_with_backoff
                'error': None
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            error_info = {
                'success': False,
                'result': None,
                'execution_time': execution_time,
                'attempts': self.config['max_retries'],
                'error': {
                    'type': type(e).__name__,
                    'message': str(e),
                    'traceback': traceback.format_exc()
                }
            }
            
            if self.logger:
                self.logger.error(f"Function {func.__name__} thất bại: {error_info}")
            
            return error_info
    
    def handle_parsing_error(self, error: Exception, file_path: str) -> Dict[str, Any]:
        """Xử lý lỗi parsing cụ thể"""
        error_info = {
            'file_path': file_path,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'suggestions': []
        }
        
        # Đưa ra gợi ý dựa trên loại lỗi
        if 'encoding' in str(error).lower():
            error_info['suggestions'].append("Thử với encoding khác (utf-8, latin-1, cp1252)")
            error_info['suggestions'].append("Kiểm tra file có bị corrupt không")
        
        elif 'permission' in str(error).lower():
            error_info['suggestions'].append("Kiểm tra quyền đọc file")
            error_info['suggestions'].append("Chạy với quyền administrator nếu cần")
        
        elif 'not found' in str(error).lower():
            error_info['suggestions'].append("Kiểm tra đường dẫn file")
            error_info['suggestions'].append("Đảm bảo file tồn tại")
        
        elif 'rate_limit' in str(error).lower() or '429' in str(error):
            error_info['suggestions'].append("Chờ một lúc rồi thử lại")
            error_info['suggestions'].append("Giảm số lượng request đồng thời")
        
        elif 'timeout' in str(error).lower():
            error_info['suggestions'].append("Tăng timeout setting")
            error_info['suggestions'].append("Kiểm tra kết nối mạng")
        
        return error_info
    
    def handle_api_error(self, error: Exception, api_name: str) -> Dict[str, Any]:
        """Xử lý lỗi API cụ thể"""
        error_info = {
            'api_name': api_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'suggestions': []
        }
        
        # Gợi ý dựa trên loại lỗi API
        if 'rate_limit' in str(error).lower():
            error_info['suggestions'].append("Chờ rate limit reset")
            error_info['suggestions'].append("Sử dụng API key khác")
            error_info['suggestions'].append("Giảm tần suất request")
        
        elif 'authentication' in str(error).lower() or '401' in str(error):
            error_info['suggestions'].append("Kiểm tra API key")
            error_info['suggestions'].append("Kiểm tra quyền truy cập")
        
        elif 'quota' in str(error).lower():
            error_info['suggestions'].append("Kiểm tra quota còn lại")
            error_info['suggestions'].append("Nâng cấp plan nếu cần")
        
        return error_info
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log lỗi với context"""
        if not self.logger:
            return
        
        error_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        self.logger.error(f"Error occurred: {error_data}")
    
    def get_error_summary(self, errors: list) -> Dict[str, Any]:
        """Tạo tóm tắt các lỗi"""
        if not errors:
            return {'total_errors': 0, 'error_types': {}, 'most_common': None}
        
        error_types = {}
        for error in errors:
            error_type = error.get('error_type', 'Unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        most_common = max(error_types.items(), key=lambda x: x[1]) if error_types else None
        
        return {
            'total_errors': len(errors),
            'error_types': error_types,
            'most_common': most_common,
            'success_rate': 1 - (len(errors) / (len(errors) + 1))  # Giả định có ít nhất 1 success
        }
    
    def create_error_report(self, processing_results: list) -> str:
        """Tạo báo cáo lỗi chi tiết"""
        errors = [result for result in processing_results if not result.get('success', True)]
        successes = [result for result in processing_results if result.get('success', True)]
        
        report = f"""
========================================
BÁO CÁO XỬ LÝ TÀI LIỆU
========================================
Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TỔNG QUAN:
- Tổng số file: {len(processing_results)}
- Thành công: {len(successes)}
- Thất bại: {len(errors)}
- Tỷ lệ thành công: {len(successes)/len(processing_results)*100:.1f}%

"""
        
        if errors:
            report += "CHI TIẾT LỖI:\n"
            for i, error in enumerate(errors, 1):
                report += f"{i}. File: {error.get('file_path', 'Unknown')}\n"
                report += f"   Lỗi: {error.get('error_type', 'Unknown')}\n"
                report += f"   Message: {error.get('error_message', 'No message')}\n"
                if error.get('suggestions'):
                    report += f"   Gợi ý: {', '.join(error['suggestions'])}\n"
                report += "\n"
        
        if successes:
            report += "FILE XỬ LÝ THÀNH CÔNG:\n"
            for success in successes:
                report += f"- {success.get('file_path', 'Unknown')}\n"
        
        return report
