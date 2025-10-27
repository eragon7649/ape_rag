Phương pháp 1: Sử dụng Môi trường Ảo (Virtual Environment) — Rất Khuyến nghị ✅
Đây là cách chuẩn để phát triển các dự án Python, cô lập raganything khỏi hệ thống của anh.

Tạo môi trường ảo: (Giả sử anh đang ở thư mục dự án)

Bash

python3 -m venv .venv
Lệnh này tạo một thư mục .venv chứa bản sao Python, pip độc lập.

Kích hoạt môi trường:

Bash

source .venv/bin/activate
(Anh sẽ thấy (.venv) xuất hiện trước dấu nhắc lệnh.)

Cài đặt gói: Sử dụng lệnh pip (không cần pip3) trong môi trường đã kích hoạt:

Bash

python3 setup.py 

python src/main.py

Run Giao diện: streamlit run test_interface.py