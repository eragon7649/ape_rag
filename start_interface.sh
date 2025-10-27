#!/bin/bash

# Script khởi động giao diện RAG Meeting Processor
echo "🚀 Khởi động RAG Meeting Processor Interface..."

# Kiểm tra virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment chưa được tạo. Vui lòng chạy setup.sh trước."
    exit 1
fi

# Kích hoạt virtual environment
echo "🐍 Kích hoạt virtual environment..."
source venv/bin/activate

# Kiểm tra dependencies
echo "📦 Kiểm tra dependencies..."
python -c "import streamlit, lightrag_hku, raganything" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Thiếu dependencies. Vui lòng chạy: pip install -r requirements.txt"
    exit 1
fi

# Kiểm tra LibreOffice
if ! command -v soffice &> /dev/null; then
    echo "⚠️  LibreOffice chưa được cài đặt. Một số file .docx có thể không xử lý được."
    echo "   Để cài đặt: brew install --cask libreoffice"
fi

# Khởi động Streamlit
echo "🌐 Khởi động giao diện web..."
echo "📱 Truy cập: http://localhost:8501"
echo "⏹️  Nhấn Ctrl+C để dừng"
echo ""

streamlit run test_interface.py
