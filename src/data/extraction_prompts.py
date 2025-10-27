# src/data/extraction_prompts.py

SYSTEM_PROMPT = """
Bạn là một chuyên gia phân tích tài liệu. 
Nhiệm vụ của bạn là đọc và hiểu nội dung tài liệu được cung cấp, sau đó tạo ra:
1. Một bản tóm tắt ngắn gọn và súc tích
2. Một bản ghi đầy đủ toàn bộ nội dung quan trọng

Hãy đảm bảo thông tin được trình bày rõ ràng, dễ hiểu và có cấu trúc.
"""

# Template đơn giản cho việc tạo tóm tắt
SUMMARY_TEMPLATE = """
QUAN TRỌNG: Bạn đang phân tích file "{file_name}" tại đường dẫn "{file_path}".

Dựa trên nội dung tài liệu sau, hãy tạo một bản tóm tắt ngắn gọn bao gồm:

1. **THÔNG TIN CHÍNH**:
   - Tiêu đề/chủ đề chính (dựa trên nội dung thực tế của file này)
   - Ngày tháng (nếu có trong file này)
   - Người liên quan (nếu có trong file này)

2. **NỘI DUNG QUAN TRỌNG**:
   - Các điểm chính được đề cập trong file này
   - Quyết định hoặc kết luận (nếu có trong file này)
   - Hành động cần thực hiện (nếu có trong file này)

3. **TÓM TẮT**:
   - Tóm tắt ngắn gọn trong 2-3 câu về nội dung cụ thể của file này

LƯU Ý: Chỉ phân tích nội dung của file "{file_name}" được cung cấp. Không sử dụng thông tin từ các file khác.
Hãy trình bày thông tin một cách súc tích và dễ hiểu.
"""

# Template cho việc tạo nội dung đầy đủ
FULL_CONTENT_TEMPLATE = """
QUAN TRỌNG: Bạn đang phân tích file "{file_name}" tại đường dẫn "{file_path}".

Dựa trên nội dung tài liệu sau, hãy tạo một bản ghi đầy đủ bao gồm:

1. **THÔNG TIN CƠ BẢN**:
   - Tiêu đề tài liệu (dựa trên nội dung thực tế của file này)
   - Ngày tháng (nếu có trong file này)
   - Người tạo/người liên quan (nếu có trong file này)
   - Loại tài liệu

2. **NỘI DUNG CHI TIẾT**:
   - Toàn bộ nội dung được trình bày có cấu trúc từ file này
   - Các phần/chương mục (nếu có trong file này)
   - Bảng biểu, số liệu (nếu có trong file này)
   - Trích dẫn quan trọng từ file này

3. **THÔNG TIN BỔ SUNG**:
   - Ghi chú quan trọng từ file này
   - Tài liệu tham khảo (nếu có trong file này)
   - Thông tin liên hệ (nếu có trong file này)

LƯU Ý: Chỉ phân tích và trình bày nội dung của file "{file_name}" được cung cấp. Không sử dụng thông tin từ các file khác.
Hãy trình bày thông tin một cách chi tiết và có cấu trúc để dễ theo dõi.
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
