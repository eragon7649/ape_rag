#!/bin/bash

# Script setup cho RAG Meeting Processor
echo "🔧 Thiết lập RAG Meeting Processor..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 chưa được cài đặt. Vui lòng cài đặt Python3 trước."
    exit 1
fi

# Tạo virtual environment
echo "🐍 Tạo virtual environment..."
python3 -m venv venv

# Kích hoạt virtual environment
echo "📦 Kích hoạt virtual environment và cài đặt dependencies..."
source venv/bin/activate

# Cài đặt dependencies
echo "📥 Cài đặt dependencies từ requirements.txt..."
pip install -r requirements.txt

# Kiểm tra LibreOffice
if ! command -v soffice &> /dev/null; then
    echo "⚠️  LibreOffice chưa được cài đặt."
    echo "📥 Đang cài đặt LibreOffice..."
    brew install --cask libreoffice
fi

# Tạo thư mục cần thiết
echo "📁 Tạo thư mục cần thiết..."
mkdir -p documents
mkdir -p output
mkdir -p rag_storage

echo ""
echo "✅ Thiết lập hoàn tất!"
echo ""
echo "🚀 Để khởi động giao diện, chạy:"
echo "   ./start_interface.sh"
echo ""
echo "📁 Hoặc chạy trực tiếp:"
echo "   source venv/bin/activate && streamlit run test_interface.py"
