# src/core/content_extractor.py

import os
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from raganything import RAGAnything

class ContentExtractor:
    def __init__(self, rag_processor: RAGAnything):
        self.rag = rag_processor
    
    async def extract_comprehensive_content(self, file_path: str) -> Dict[str, Any]:
        """Trích xuất nội dung toàn diện từ tài liệu"""
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        file_ext = os.path.splitext(file_path)[1].lower()
        
        print(f"🔍 Bắt đầu trích xuất nội dung toàn diện cho: {file_base_name}")
        
        result = {
            'file_info': self._get_file_info(file_path),
            'raw_content': await self._extract_raw_content(file_path),
            'structured_content': await self._extract_structured_content(file_path),
            'metadata': await self._extract_metadata(file_path),
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        # Thêm thông tin đặc biệt cho PDF
        if file_ext == '.pdf':
            result['pdf_specific'] = await self._extract_pdf_specific_content(file_path)
        
        print(f"✅ Hoàn thành trích xuất nội dung cho: {file_base_name}")
        return result
    
    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Lấy thông tin cơ bản về file"""
        try:
            stat = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'format': os.path.splitext(file_path)[1].lower(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'readable': os.access(file_path, os.R_OK)
            }
        except Exception as e:
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'error': f"Không thể lấy thông tin file: {e}"
            }
    
    async def _extract_raw_content(self, file_path: str) -> str:
        """Trích xuất nội dung gốc từ tài liệu"""
        file_ext = os.path.splitext(file_path)[1].lower()
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        try:
            if file_ext == '.txt':
                # Đọc trực tiếp file text
                encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        print(f"📄 Đã đọc file text với encoding: {encoding}")
                        return content
                    except UnicodeDecodeError:
                        continue
                return "Không thể đọc file với các encoding đã thử"
            
            elif file_ext == '.pdf':
                # Đọc nội dung đã được parse từ RAG
                parsed_md_path = os.path.join(
                    self.rag.config.working_dir, 
                    "parsed_docs", 
                    file_base_name, 
                    "auto", 
                    f"{file_base_name}.md"
                )
                
                if os.path.exists(parsed_md_path):
                    with open(parsed_md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"📄 Đã đọc nội dung PDF đã parse")
                    return content
                else:
                    return f"Không tìm thấy file parsed cho {file_base_name}"
            
            else:
                # Thử đọc như text file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    print(f"📄 Đã đọc file {file_ext} như text")
                    return content
                except Exception as e:
                    return f"Không thể đọc file {file_ext}: {e}"
        
        except Exception as e:
            return f"Lỗi trích xuất nội dung gốc: {e}"
    
    async def _extract_structured_content(self, file_path: str) -> Dict[str, Any]:
        """Trích xuất nội dung có cấu trúc"""
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        queries = {
            'headings': "Trích xuất tất cả tiêu đề và heading trong tài liệu",
            'tables': "Trích xuất tất cả bảng biểu và dữ liệu dạng bảng",
            'lists': "Trích xuất tất cả danh sách (bullet points, numbered lists)",
            'dates': "Trích xuất tất cả ngày tháng trong tài liệu",
            'people': "Trích xuất tất cả tên người được đề cập",
            'organizations': "Trích xuất tất cả tên tổ chức, công ty, phòng ban",
            'decisions': "Trích xuất tất cả quyết định và hành động",
            'meeting_info': "Trích xuất thông tin cuộc họp (thời gian, địa điểm, người tham gia)"
        }
        
        structured_data = {}
        
        for key, query in queries.items():
            try:
                print(f"🔍 Trích xuất {key}...")
                result = await self.rag.aquery(
                    query,
                    mode="hybrid",
                    user_prompt="Bạn là chuyên gia trích xuất thông tin có cấu trúc. Hãy trích xuất chính xác thông tin được yêu cầu.",
                    top_k=15,
                    vlm_enhanced=True,
                    enable_rerank=False
                )
                
                # Lấy text response
                if hasattr(result, 'answer'):
                    structured_data[key] = result.answer
                else:
                    structured_data[key] = str(result)
                
                print(f"✅ Hoàn thành trích xuất {key}")
                
            except Exception as e:
                print(f"⚠️ Lỗi trích xuất {key}: {e}")
                structured_data[key] = f"Error: {e}"
        
        return structured_data
    
    async def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Trích xuất metadata từ tài liệu"""
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        try:
            # Trích xuất metadata bằng LLM
            metadata_query = """
            Hãy trích xuất các thông tin metadata sau từ tài liệu:
            1. Loại tài liệu (biên bản họp, báo cáo, hợp đồng, etc.)
            2. Ngôn ngữ chính
            3. Chủ đề chính
            4. Từ khóa quan trọng
            5. Mức độ bảo mật (nếu có)
            6. Phiên bản tài liệu (nếu có)
            """
            
            result = await self.rag.aquery(
                metadata_query,
                mode="vector",
                user_prompt="Bạn là chuyên gia phân tích metadata tài liệu.",
                top_k=10,
                vlm_enhanced=False,
                enable_rerank=False
            )
            
            # Lấy text response
            if hasattr(result, 'answer'):
                metadata_text = result.answer
            else:
                metadata_text = str(result)
            
            return {
                'extracted_metadata': metadata_text,
                'file_type': self._detect_file_type(file_path),
                'language': self._detect_language(metadata_text),
                'keywords': self._extract_keywords(metadata_text)
            }
            
        except Exception as e:
            return {
                'error': f"Không thể trích xuất metadata: {e}",
                'file_type': self._detect_file_type(file_path)
            }
    
    async def _extract_pdf_specific_content(self, file_path: str) -> Dict[str, Any]:
        """Trích xuất nội dung đặc biệt cho PDF"""
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        try:
            # Kiểm tra các file đã được parse
            parsed_dir = os.path.join(
                self.rag.config.working_dir, 
                "parsed_docs", 
                file_base_name, 
                "auto"
            )
            
            pdf_specific = {
                'parsed_files': [],
                'images': [],
                'tables': [],
                'layout_info': {}
            }
            
            if os.path.exists(parsed_dir):
                # Liệt kê các file đã parse
                for file in os.listdir(parsed_dir):
                    pdf_specific['parsed_files'].append(file)
                    
                    # Kiểm tra file ảnh
                    if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        pdf_specific['images'].append(file)
                    
                    # Kiểm tra file layout
                    if 'layout' in file.lower():
                        try:
                            with open(os.path.join(parsed_dir, file), 'r', encoding='utf-8') as f:
                                pdf_specific['layout_info'][file] = f.read()[:500]  # Chỉ lấy 500 ký tự đầu
                        except:
                            pass
            
            return pdf_specific
            
        except Exception as e:
            return {'error': f"Không thể trích xuất thông tin PDF: {e}"}
    
    def _detect_file_type(self, file_path: str) -> str:
        """Phát hiện loại file dựa trên tên và nội dung"""
        file_name = os.path.basename(file_path).lower()
        
        if 'meeting' in file_name or 'hop' in file_name or 'bbh' in file_name:
            return 'meeting_minutes'
        elif 'report' in file_name or 'bao_cao' in file_name:
            return 'report'
        elif 'contract' in file_name or 'hop_dong' in file_name:
            return 'contract'
        elif 'proposal' in file_name or 'de_xuat' in file_name:
            return 'proposal'
        else:
            return 'unknown'
    
    def _detect_language(self, text: str) -> str:
        """Phát hiện ngôn ngữ của văn bản"""
        # Đếm ký tự tiếng Việt
        vietnamese_chars = sum(1 for c in text if '\u00C0' <= c <= '\u1EF9')
        total_chars = len([c for c in text if c.isalpha()])
        
        if total_chars > 0 and vietnamese_chars / total_chars > 0.1:
            return 'vietnamese'
        else:
            return 'english'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Trích xuất từ khóa từ văn bản"""
        # Tách từ và đếm tần suất
        words = text.lower().split()
        word_count = {}
        
        for word in words:
            # Loại bỏ ký tự đặc biệt
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3:  # Chỉ lấy từ có độ dài > 3
                word_count[clean_word] = word_count.get(clean_word, 0) + 1
        
        # Sắp xếp theo tần suất và lấy top 10
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:10]]
