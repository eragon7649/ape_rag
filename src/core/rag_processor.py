# src/core/rag_processor.py

import os
import asyncio
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
from raganything import RAGAnything
from .config import (
    RAG_CONFIG, LLM_MODEL, VLM_MODEL, EMBEDDING_MODEL, EMBEDDING_DIM, OPENAI_API_KEY, OPENAI_BASE_URL
)
from data.extraction_prompts import QUERY_TEMPLATE, SYSTEM_PROMPT, CHANGELOG_TEMPLATE
from .document_parser import DocumentParser
from .content_extractor import ContentExtractor
from .error_handler import ErrorHandler
from .config_validator import ConfigValidator
from .incremental_processor import IncrementalProcessor
from typing import List, Dict, Any

class MeetingProcessor:
    def __init__(self, api_key: str = OPENAI_API_KEY, base_url: str = OPENAI_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.rag = self._initialize_raganything()
        
        # Khởi tạo các component mới
        self.document_parser = DocumentParser(self.rag)
        self.content_extractor = ContentExtractor(self.rag)
        self.error_handler = ErrorHandler()
        self.config_validator = ConfigValidator()
        self.incremental_processor = IncrementalProcessor()

    # --- Khởi tạo các hàm Mô hình LLM/VLM/Embedding ---
    def _llm_model_func(self, prompt, system_prompt=None, history_messages=[], **kwargs):
        """Hàm cho các tác vụ LLM (văn bản)"""
        return openai_complete_if_cache(
            LLM_MODEL, prompt, system_prompt=system_prompt, 
            history_messages=history_messages, api_key=self.api_key, base_url=self.base_url, **kwargs,
        )

    def _vision_model_func(self, prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs):
        """Hàm cho các tác vụ VLM (OCR viết tay, phân tích ảnh)"""
        # (Sử dụng logic phức tạp hơn cho VLM Enhanced Query như đã giải thích)
        if messages:
            return openai_complete_if_cache(VLM_MODEL, "", messages=messages, api_key=self.api_key, base_url=self.base_url, **kwargs)
        elif image_data:
            # Tạo messages từ image_data và prompt (để xử lý OCR viết tay)
            image_url_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            user_content = [{"type": "text", "text": prompt}, image_url_content]
            
            system_message = [{"role": "system", "content": system_prompt}] if system_prompt else []
            user_message = [{"role": "user", "content": user_content}]
            
            return openai_complete_if_cache(VLM_MODEL, "", messages=system_message + user_message, api_key=self.api_key, base_url=self.base_url, **kwargs)
        else:
            return self._llm_model_func(prompt, system_prompt, history_messages, **kwargs)

    def _embedding_func(self, texts: List[str]):
        """Hàm cho Embedding"""
        return openai_embed(texts, model=EMBEDDING_MODEL, api_key=self.api_key, base_url=self.base_url)

    # --- Khởi tạo RAG-Anything ---
    def _initialize_raganything(self) -> RAGAnything:
        embedding_func_wrapper = EmbeddingFunc(
            embedding_dim=EMBEDDING_DIM,
            max_token_size=8192,
            func=self._embedding_func,
        )
        
        rag = RAGAnything(
            config=RAG_CONFIG,
            llm_model_func=self._llm_model_func,
            vision_model_func=self._vision_model_func,
            embedding_func=embedding_func_wrapper,
        )
        # Khởi tạo storage (load dữ liệu cũ nếu có)
        # Note: RAGAnything handles storage initialization automatically
        return rag

    # --- Hàm chính: Xử lý tệp End-to-End với cải tiến ---
    async def process_document_and_extract(self, file_path: str) -> Dict[str, Any]:
        """
        Thực hiện xử lý tài liệu với các cải tiến mới:
        - Validation trước khi xử lý
        - Error handling với retry mechanism
        - Trích xuất nội dung toàn diện
        """
        print(f"🚀 Bắt đầu xử lý: {file_path}")
        
        # 1. Validation file input
        validation_result = self.config_validator.validate_file_input(file_path)
        if not validation_result['valid']:
            error_msg = f"File validation failed: {', '.join(validation_result['errors'])}"
            print(f"❌ {error_msg}")
            return {"error": error_msg, "validation": validation_result}
        
        if validation_result['warnings']:
            print(f"⚠️ Warnings: {', '.join(validation_result['warnings'])}")
        
        # 2. Parse document với error handling
        try:
            parse_result = await self.error_handler.retry_with_backoff(
                self.document_parser.parse_document, file_path
            )
            print(f"✅ Hoàn tất parsing cho: {file_path}")
        except Exception as e:
            error_info = self.error_handler.handle_parsing_error(e, file_path)
            print(f"❌ Parsing failed: {error_info['error_message']}")
            return {"error": f"Parsing failed: {error_info['error_message']}", "error_info": error_info}

        # 3. Trích xuất nội dung toàn diện
        try:
            comprehensive_data = await self.content_extractor.extract_comprehensive_content(file_path)
            print(f"✅ Hoàn tất trích xuất nội dung toàn diện cho: {file_path}")
        except Exception as e:
            print(f"⚠️ Lỗi trích xuất nội dung: {e}")
            # Fallback: chỉ lấy raw content
            comprehensive_data = {
                'file_info': validation_result['file_info'],
                'raw_content': await self._extract_raw_content_fallback(file_path),
                'structured_content': {},
                'metadata': {},
                'extraction_timestamp': None
            }
        
        # 4. Truy vấn Thông minh và Trích xuất JSON (Intelligent Query & Extraction)
        try:
            extraction_result = await self.error_handler.retry_with_backoff(
                self._perform_intelligent_extraction, file_path
            )
            
            # Parse JSON response
            parsed_json = self._parse_json_response(extraction_result)
            comprehensive_data.update(parsed_json)
            
        except Exception as e:
            error_info = self.error_handler.handle_api_error(e, "RAG Query")
            print(f"⚠️ Intelligent extraction failed: {error_info['error_message']}")
            # Vẫn trả về comprehensive data dù không có JSON extraction
            comprehensive_data['extraction_error'] = error_info
        
        # 5. Trả về kết quả toàn diện
        return comprehensive_data
    
    async def _perform_intelligent_extraction(self, file_path: str):
        """Thực hiện intelligent extraction với fallback"""
        try:
            # Thử với hybrid mode trước
            return await self.rag.aquery(
                QUERY_TEMPLATE,
                mode="hybrid",
                user_prompt=SYSTEM_PROMPT,
                vlm_enhanced=True,
                top_k=20,
                enable_rerank=False
            )
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print(f"⚠️ Rate limit hit, thử với context nhỏ hơn...")
                # Fallback với context nhỏ hơn
                return await self.rag.aquery(
                    QUERY_TEMPLATE,
                    mode="vector",
                    user_prompt=SYSTEM_PROMPT,
                    vlm_enhanced=False,
                    top_k=10,
                    enable_rerank=False
                )
            else:
                raise e
    
    def _parse_json_response(self, extraction_result):
        """Parse JSON response từ LLM"""
        import json
        import re
        
        try:
            # Lấy text response
            if hasattr(extraction_result, 'answer'):
                response_text = extraction_result.answer
            else:
                response_text = str(extraction_result)
            
            # Loại bỏ markdown code block
            if response_text.startswith('```json'):
                response_text = re.sub(r'^```json\s*', '', response_text)
                response_text = re.sub(r'\s*```$', '', response_text)
            elif response_text.startswith('```'):
                response_text = re.sub(r'^```\s*', '', response_text)
                response_text = re.sub(r'\s*```$', '', response_text)
            
            # Xử lý JSON bị cắt ngắn
            response_text = response_text.strip()
            open_braces = response_text.count('{')
            close_braces = response_text.count('}')
            
            if open_braces > close_braces:
                missing_braces = open_braces - close_braces
                response_text += '}' * missing_braces
            
            # Tìm vị trí cuối của JSON object
            if response_text.startswith('{'):
                brace_count = 0
                json_end = -1
                for i, char in enumerate(response_text):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                
                if json_end > 0:
                    response_text = response_text[:json_end]
            
            parsed_json = json.loads(response_text)
            return {'extracted_json': parsed_json, 'json_parsing_success': True}
            
        except Exception as e:
            print(f"⚠️ JSON parsing failed: {e}")
            return {
                'extracted_json': {},
                'json_parsing_success': False,
                'json_error': str(e),
                'raw_response': response_text[:500] if 'response_text' in locals() else str(extraction_result)[:500]
            }
    
    async def _extract_raw_content_fallback(self, file_path: str) -> str:
        """Fallback method để lấy raw content"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"Không thể đọc file {file_ext} trong fallback mode"
        except Exception as e:
            return f"Lỗi fallback: {e}"

    async def _extract_raw_content(self, file_path: str, parsed_data: Dict[str, Any]):
        """Trích xuất nội dung gốc từ tài liệu đã được parse"""
        try:
            file_base_name = os.path.splitext(os.path.basename(file_path))[0]
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Xử lý theo loại file
            if file_ext == '.txt':
                # Đọc file text
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                    print(f"📄 Đã đọc file text cho {file_base_name} ({len(raw_content)} ký tự)")
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        raw_content = f.read()
                    print(f"📄 Đã đọc file text với encoding latin-1 cho {file_base_name} ({len(raw_content)} ký tự)")
            elif file_ext == '.pdf':
                # Đối với PDF, lấy nội dung đã được parse từ RAG
                try:
                    # Đọc file markdown đã được parse
                    parsed_md_path = os.path.join(
                        self.rag.config.working_dir, 
                        "parsed_docs", 
                        file_base_name, 
                        "auto", 
                        f"{file_base_name}.md"
                    )
                    
                    if os.path.exists(parsed_md_path):
                        with open(parsed_md_path, 'r', encoding='utf-8') as f:
                            raw_content = f.read()
                        print(f"📄 Đã đọc nội dung PDF đã parse cho {file_base_name} ({len(raw_content)} ký tự)")
                    else:
                        raw_content = f"Không tìm thấy file parsed cho {file_base_name}\n"
                        raw_content += f"Đường dẫn tìm kiếm: {parsed_md_path}"
                        print(f"⚠️ Không tìm thấy file parsed: {parsed_md_path}")
                except Exception as e:
                    raw_content = f"Không thể đọc nội dung PDF đã parse {file_path}: {str(e)}"
                    print(f"⚠️ Lỗi đọc PDF parsed: {e}")
            else:
                # File khác
                raw_content = f"File {file_ext} chưa được hỗ trợ trích xuất nội dung gốc.\n"
                raw_content += f"Tên file: {file_base_name}\n"
                raw_content += f"Đường dẫn: {file_path}"
                print(f"📄 File {file_ext} không được hỗ trợ cho {file_base_name}")
            
            # Lưu raw content vào parsed_data
            parsed_data['_raw_content'] = raw_content
            
        except Exception as e:
            print(f"⚠️ Không thể trích xuất nội dung gốc: {e}")
            # Fallback: sử dụng raw response nếu có
            parsed_data['_raw_content'] = parsed_data.get('_raw_response', 'Không thể trích xuất nội dung')
    
    # --- Hàm xử lý incremental ---
    async def process_incremental(self, documents_dir: str) -> Dict[str, Any]:
        """
        Xử lý incremental - chỉ xử lý file mới hoặc đã thay đổi
        """
        print("🔄 Bắt đầu quét incremental...")
        
        # 1. Quét thư mục để tìm file cần xử lý
        scan_report = self.incremental_processor.scan_directory(documents_dir)
        
        files_to_process = scan_report["files_to_process_list"]
        
        if not files_to_process:
            print("✅ Không có file nào cần xử lý")
            return {
                "status": "no_changes",
                "message": "Tất cả files đã được xử lý và không có thay đổi",
                "scan_report": scan_report
            }
        
        print(f"📋 Tìm thấy {len(files_to_process)} file(s) cần xử lý")
        
        # 2. Xử lý từng file
        processing_results = []
        
        for file_info in files_to_process:
            file_path = file_info["path"]
            filename = file_info["name"]
            
            print(f"\n{'='*50}")
            print(f"🚀 Xử lý file: {filename}")
            
            try:
                # Xử lý file
                result = await self.process_document_and_extract(file_path)
                
                if result.get('error'):
                    print(f"❌ Xử lý thất bại: {result['error']}")
                    self.incremental_processor.mark_file_failed(filename, result['error'])
                    processing_results.append({
                        'file_path': file_path,
                        'success': False,
                        'error': result['error']
                    })
                else:
                    print(f"✅ Xử lý thành công: {filename}")
                    self.incremental_processor.mark_file_processed(filename, {
                        'success': True,
                        'extracted_data_keys': list(result.keys()),
                        'has_json': bool(result.get('extracted_json'))
                    })
                    processing_results.append({
                        'file_path': file_path,
                        'success': True,
                        'result': result
                    })
                    
            except Exception as e:
                error_msg = f"Lỗi không mong đợi: {str(e)}"
                print(f"❌ {error_msg}")
                self.incremental_processor.mark_file_failed(filename, error_msg)
                processing_results.append({
                    'file_path': file_path,
                    'success': False,
                    'error': error_msg
                })
        
        # 3. Tạo báo cáo tổng kết
        successful_count = len([r for r in processing_results if r['success']])
        failed_count = len(processing_results) - successful_count
        
        print(f"\n🎉 Hoàn tất xử lý incremental!")
        print(f"✅ Thành công: {successful_count} files")
        print(f"❌ Thất bại: {failed_count} files")
        
        return {
            "status": "completed",
            "total_files": len(files_to_process),
            "successful_files": successful_count,
            "failed_files": failed_count,
            "processing_results": processing_results,
            "scan_report": scan_report
        }
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Lấy trạng thái xử lý của tất cả files"""
        return self.incremental_processor.get_processing_status()
    
    def reset_file_tracking(self, filename: str = None):
        """Reset tracking cho file cụ thể hoặc tất cả files"""
        self.incremental_processor.reset_file_tracking(filename)

# Lớp OutputFormatter sẽ được viết sau (để chuyển JSON sang Word/PDF/DB)
