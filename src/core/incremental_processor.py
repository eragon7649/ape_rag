# src/core/incremental_processor.py

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from .config import RAG_STORAGE_DIR

class IncrementalProcessor:
    """Hệ thống xử lý incremental để chỉ xử lý file mới hoặc đã thay đổi"""
    
    def __init__(self):
        self.tracking_file = os.path.join(RAG_STORAGE_DIR, "file_tracking.json")
        self.ensure_tracking_file()
    
    def ensure_tracking_file(self):
        """Đảm bảo file tracking tồn tại"""
        if not os.path.exists(self.tracking_file):
            self._create_empty_tracking_file()
    
    def _create_empty_tracking_file(self):
        """Tạo file tracking trống"""
        os.makedirs(RAG_STORAGE_DIR, exist_ok=True)
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "files": {},
                "last_scan": None
            }, f, ensure_ascii=False, indent=2)
    
    def get_file_hash(self, file_path: str) -> str:
        """Tính hash của file để phát hiện thay đổi"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Đọc toàn bộ file để tính hash chính xác
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"⚠️ Không thể tính hash cho {file_path}: {e}")
            return "unknown"
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Lấy thông tin chi tiết về file"""
        try:
            stat = os.stat(file_path)
            return {
                "path": file_path,
                "name": os.path.basename(file_path),
                "size": stat.st_size,
                "modified_time": stat.st_mtime,
                "created_time": stat.st_ctime,
                "hash": self.get_file_hash(file_path),
                "extension": os.path.splitext(file_path)[1].lower()
            }
        except Exception as e:
            print(f"⚠️ Không thể lấy thông tin file {file_path}: {e}")
            return {
                "path": file_path,
                "name": os.path.basename(file_path),
                "error": str(e)
            }
    
    def load_tracking_data(self) -> Dict[str, Any]:
        """Load dữ liệu tracking từ file"""
        try:
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Không thể load tracking data: {e}")
            return {"files": {}}
    
    def save_tracking_data(self, data: Dict[str, Any]):
        """Lưu dữ liệu tracking vào file"""
        try:
            data["last_scan"] = datetime.now().isoformat()
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Không thể lưu tracking data: {e}")
    
    def scan_directory(self, documents_dir: str) -> Dict[str, Any]:
        """Quét thư mục và so sánh với dữ liệu tracking"""
        print(f"🔍 Quét thư mục: {documents_dir}")
        
        # Load dữ liệu tracking hiện tại
        tracking_data = self.load_tracking_data()
        tracked_files = tracking_data.get("files", {})
        
        # Quét files trong thư mục
        current_files = {}
        files_to_process = []
        files_unchanged = []
        files_removed = []
        
        # Lấy danh sách files hiện tại
        if os.path.exists(documents_dir):
            for filename in os.listdir(documents_dir):
                if filename.startswith('.') or filename == 'README.md':
                    continue  # Bỏ qua file ẩn và README
                
                file_path = os.path.join(documents_dir, filename)
                if os.path.isfile(file_path):
                    file_info = self.get_file_info(file_path)
                    current_files[filename] = file_info
                    
                    # Kiểm tra xem file có cần xử lý không
                    if filename in tracked_files:
                        tracked_info = tracked_files[filename]
                        
                        # So sánh hash và thời gian sửa đổi
                        if (file_info.get("hash") != tracked_info.get("hash") or
                            file_info.get("modified_time") != tracked_info.get("modified_time")):
                            files_to_process.append(file_info)
                            print(f"🔄 File đã thay đổi: {filename}")
                        else:
                            files_unchanged.append(file_info)
                            print(f"✅ File không đổi: {filename}")
                    else:
                        files_to_process.append(file_info)
                        print(f"🆕 File mới: {filename}")
        
        # Tìm files đã bị xóa
        for filename in tracked_files:
            if filename not in current_files:
                files_removed.append(tracked_files[filename])
                print(f"🗑️ File đã xóa: {filename}")
        
        # Cập nhật tracking data
        tracking_data["files"] = current_files
        
        # Tạo báo cáo
        scan_report = {
            "scan_time": datetime.now().isoformat(),
            "total_files": len(current_files),
            "files_to_process": len(files_to_process),
            "files_unchanged": len(files_unchanged),
            "files_removed": len(files_removed),
            "files_to_process_list": files_to_process,
            "files_unchanged_list": files_unchanged,
            "files_removed_list": files_removed,
            "tracking_data": tracking_data
        }
        
        return scan_report
    
    def mark_file_processed(self, filename: str, processing_result: Dict[str, Any]):
        """Đánh dấu file đã được xử lý thành công"""
        tracking_data = self.load_tracking_data()
        
        if filename in tracking_data["files"]:
            tracking_data["files"][filename]["processed"] = True
            tracking_data["files"][filename]["processed_at"] = datetime.now().isoformat()
            tracking_data["files"][filename]["processing_result"] = processing_result
            
            self.save_tracking_data(tracking_data)
            print(f"✅ Đã đánh dấu file đã xử lý: {filename}")
    
    def mark_file_failed(self, filename: str, error_message: str):
        """Đánh dấu file xử lý thất bại"""
        tracking_data = self.load_tracking_data()
        
        if filename in tracking_data["files"]:
            tracking_data["files"][filename]["processed"] = False
            tracking_data["files"][filename]["last_error"] = error_message
            tracking_data["files"][filename]["last_error_at"] = datetime.now().isoformat()
            
            self.save_tracking_data(tracking_data)
            print(f"❌ Đã đánh dấu file xử lý thất bại: {filename}")
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Lấy trạng thái xử lý của tất cả files"""
        tracking_data = self.load_tracking_data()
        files = tracking_data.get("files", {})
        
        status = {
            "total_files": len(files),
            "processed_files": 0,
            "failed_files": 0,
            "pending_files": 0,
            "files_detail": {}
        }
        
        for filename, file_info in files.items():
            if file_info.get("processed"):
                status["processed_files"] += 1
                status["files_detail"][filename] = {
                    "status": "processed",
                    "processed_at": file_info.get("processed_at"),
                    "result": file_info.get("processing_result", {})
                }
            elif file_info.get("last_error"):
                status["failed_files"] += 1
                status["files_detail"][filename] = {
                    "status": "failed",
                    "error": file_info.get("last_error"),
                    "error_at": file_info.get("last_error_at")
                }
            else:
                status["pending_files"] += 1
                status["files_detail"][filename] = {
                    "status": "pending"
                }
        
        return status
    
    def get_files_by_status(self, status: str) -> List[str]:
        """Lấy danh sách files theo trạng thái"""
        processing_status = self.get_processing_status()
        files_detail = processing_status["files_detail"]
        
        return [filename for filename, detail in files_detail.items() 
                if detail["status"] == status]
    
    def reset_file_tracking(self, filename: Optional[str] = None):
        """Reset tracking cho file cụ thể hoặc tất cả files"""
        tracking_data = self.load_tracking_data()
        
        if filename:
            if filename in tracking_data["files"]:
                # Reset file cụ thể
                file_info = tracking_data["files"][filename]
                file_info.pop("processed", None)
                file_info.pop("processed_at", None)
                file_info.pop("processing_result", None)
                file_info.pop("last_error", None)
                file_info.pop("last_error_at", None)
                print(f"🔄 Đã reset tracking cho: {filename}")
        else:
            # Reset tất cả files
            for file_info in tracking_data["files"].values():
                file_info.pop("processed", None)
                file_info.pop("processed_at", None)
                file_info.pop("processing_result", None)
                file_info.pop("last_error", None)
                file_info.pop("last_error_at", None)
            print("🔄 Đã reset tracking cho tất cả files")
        
        self.save_tracking_data(tracking_data)
