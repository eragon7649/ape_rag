# src/data/extraction_prompts.py

SYSTEM_PROMPT = """
Bạn là một chuyên gia phân tích biên bản cuộc họp. 
Nhiệm vụ của bạn là trích xuất các thông tin quan trọng từ ngữ cảnh được cung cấp và chuẩn hóa thành định dạng JSON.
Đảm bảo tất cả các trường dữ liệu BẮT BUỘC phải được điền đầy đủ.
"""

# Mẫu JSON bắt buộc (Cấu hình động - cần được tinh chỉnh thêm)
JSON_SCHEMA_TEMPLATE = """
{
    "meeting_title": "string (Tên cuộc họp)",
    "date": "string (Ngày diễn ra cuộc họp)",
    "participants": "array of strings (Danh sách người tham gia)",
    "summary": "string (Tóm tắt chung nội dung)",
    "decisions": [
        {
            "decision_id": "integer (ID Quyết định)",
            "description": "string (Nội dung quyết định)",
            "responsible_person": "string (Người chịu trách nhiệm)",
            "due_date": "string (Deadline dự kiến, nếu có)"
        }
    ],
    "action_items_count": "integer (Tổng số mục hành động)"
}
"""

QUERY_TEMPLATE = f"""
Dựa trên biên bản cuộc họp sau, hãy trích xuất các thông tin BẮT BUỘC sau và trả về dưới định dạng JSON.
Đảm bảo tất cả các trường trong cấu trúc JSON sau được điền:
{JSON_SCHEMA_TEMPLATE}
"""

# Template cho việc tạo changelog để kiểm tra dữ liệu
CHANGELOG_TEMPLATE = """
Dựa trên biên bản cuộc họp đã được xử lý, hãy tạo một báo cáo changelog chi tiết bao gồm:

1. **THÔNG TIN CUỘC HỌP**:
   - Tên cuộc họp
   - Ngày và thời gian
   - Địa điểm
   - Người chủ trì

2. **THÀNH VIÊN THAM GIA**:
   - Danh sách đầy đủ người tham gia
   - Vai trò/chức vụ của từng người

3. **NỘI DUNG CHÍNH**:
   - Các chủ đề thảo luận
   - Vấn đề được nêu ra
   - Giải pháp đề xuất

4. **QUYẾT ĐỊNH VÀ HÀNH ĐỘNG**:
   - Các quyết định được đưa ra
   - Người chịu trách nhiệm
   - Deadline cụ thể
   - Trạng thái thực hiện

5. **THÔNG TIN BỔ SUNG**:
   - Các ghi chú quan trọng
   - Tài liệu tham khảo
   - Cuộc họp tiếp theo

Hãy trình bày thông tin một cách chi tiết và có cấu trúc để dễ theo dõi.
"""
