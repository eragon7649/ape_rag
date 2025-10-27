# test_interface.py

import streamlit as st
import asyncio
import os
import json
from datetime import datetime
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.rag_processor import MeetingProcessor
from core.output_formatter import OutputFormatter
from core.config import DOCUMENTS_DIR, OUTPUT_DIR

# Page configuration
st.set_page_config(
    page_title="Bộ Xử Lý Tài Liệu Cuộc Họp RAG - Giao Diện Kiểm Thử",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .menu-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .file-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = None
if 'formatter' not in st.session_state:
    st.session_state.formatter = None
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

def initialize_processor(api_key):
    """Initialize processor with API key"""
    try:
        os.environ["OPENAI_API_KEY"] = api_key
        processor = MeetingProcessor(api_key=api_key)
        formatter = OutputFormatter(OUTPUT_DIR)
        st.session_state.processor = processor
        st.session_state.formatter = formatter
        st.session_state.api_key_set = True
        return True
    except Exception as e:
        st.error(f"❌ Không thể khởi tạo bộ xử lý: {e}")
        return False

def get_documents_list():
    """Get list of documents in documents folder"""
    if not os.path.exists(DOCUMENTS_DIR):
        return []
    
    files = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if not filename.startswith('.') and filename != 'README.md':
            file_path = os.path.join(DOCUMENTS_DIR, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'path': file_path,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    return sorted(files, key=lambda x: x['modified'], reverse=True)

def get_output_files_for_document(document_name):
    """Get list of output files for a specific document"""
    if not os.path.exists(OUTPUT_DIR):
        return []
    
    base_name = os.path.splitext(document_name)[0]
    output_files = []
    
    for filename in os.listdir(OUTPUT_DIR):
        if filename.startswith(f"SUMMARY_{base_name}") or \
           filename.startswith(f"FULL_CONTENT_{base_name}"):
            file_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                output_files.append({
                    'name': filename,
                    'path': file_path,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'type': get_file_type(filename)
                })
    
    return sorted(output_files, key=lambda x: x['modified'], reverse=True)

def get_file_type(filename):
    """Determine file type based on filename"""
    if filename.endswith('.txt'):
        if 'FULL_CONTENT' in filename:
            return 'Nội Dung Đầy Đủ'
        elif 'SUMMARY' in filename:
            return 'Báo Cáo Tóm Tắt'
        else:
            return 'Tệp Văn Bản'
    else:
        return 'Không Xác Định'

def display_file_content(file_path, file_type):
    """Display content of a file based on its type"""
    try:
        if file_type in ['Nội Dung Đầy Đủ', 'Báo Cáo Tóm Tắt', 'Tệp Văn Bản']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            st.text_area("Nội Dung Tệp", content, height=400)
        else:
            st.info("Xem trước tệp không khả dụng cho loại tệp này")
    except Exception as e:
        st.error(f"Lỗi khi đọc tệp: {e}")

# Main interface
st.markdown('<h1 class="main-header">🤖 Bộ Xử Lý Tài Liệu Cuộc Họp RAG</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666;">Giao Diện Kiểm Thử</h2>', unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Cấu Hình")
    
    api_key = st.text_input(
        "Khóa API OpenAI", 
        type="password",
        help="Nhập khóa API OpenAI của bạn",
        value=os.environ.get("OPENAI_API_KEY", "")
    )
    
    if st.button("Khởi Tạo Bộ Xử Lý", type="primary"):
        if api_key:
            with st.spinner("Đang khởi tạo..."):
                if initialize_processor(api_key):
                    st.success("✅ Bộ xử lý đã được khởi tạo thành công!")
                else:
                    st.error("❌ Không thể khởi tạo bộ xử lý")
        else:
            st.error("❌ Vui lòng nhập khóa API")

# Main content area
if not st.session_state.api_key_set:
    st.warning("⚠️ Vui lòng khởi tạo bộ xử lý với khóa API của bạn trong thanh bên")
    st.stop()

# Menu selection
menu = st.selectbox(
    "Chọn Menu",
    ["📁 Tải Lên & Xử Lý", "📊 Xem Báo Cáo"],
    help="Chọn giữa tải lên tệp mới hoặc xem báo cáo hiện có"
)

if menu == "📁 Tải Lên & Xử Lý":
    st.header("📁 Tải Lên & Xử Lý Tài Liệu")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tải Lên Tài Liệu Mới")
        
        uploaded_file = st.file_uploader(
            "Chọn tệp để tải lên",
            type=['pdf', 'jpg', 'jpeg', 'png', 'docx', 'txt'],
            help="Tải lên tài liệu cuộc họp để xử lý"
        )
        
        if uploaded_file:
            st.success(f"✅ Tệp đã tải lên: {uploaded_file.name}")
            
            # File info
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.metric("Kích Thước Tệp", f"{uploaded_file.size:,} bytes")
            with col_info2:
                st.metric("Loại Tệp", uploaded_file.type)
    
    with col2:
        st.subheader("Tùy Chọn Xử Lý")
        
        # Process buttons
        st.markdown("**Tùy Chọn Xử Lý:**")
        st.info("""
        - **Xử Lý Tệp Đã Tải**: Tải lên một tệp và xử lý nó bằng xử lý tăng dần
        - **Xử Lý Tất Cả Tệp**: Chạy xử lý tăng dần trên tất cả tệp trong thư mục tài liệu
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Xử Lý Tệp Đã Tải", type="primary", disabled=not uploaded_file):
                if uploaded_file:
                    with st.spinner("🔄 Đang xử lý tài liệu..."):
                        try:
                            st.info("🔍 Bước 1: Bắt đầu xử lý tệp đã tải")
                            
                            # Save uploaded file temporarily
                            st.info("🔍 Bước 2: Lưu tệp tạm thời")
                            temp_path = os.path.join(DOCUMENTS_DIR, uploaded_file.name)
                            st.text(f"📁 Đường dẫn tệp: {temp_path}")
                            
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            st.success("✅ Đã lưu tệp thành công")
                            
                            # Run incremental processor script
                            st.info("🔍 Bước 3: Chuẩn bị chạy script incremental")
                            import subprocess
                            
                            script_path = os.path.join(os.path.dirname(__file__), "run_incremental_processor.py")
                            st.text(f"📄 Script path: {script_path}")
                            st.text(f"📄 Script exists: {os.path.exists(script_path)}")
                            
                            # Use virtual environment python
                            st.info("🔍 Bước 4: Xác định Python command")
                            venv_python = os.path.join(os.path.dirname(__file__), "venv", "bin", "python")
                            st.text(f"🐍 Venv python: {venv_python}")
                            st.text(f"🐍 Venv exists: {os.path.exists(venv_python)}")
                            
                            if os.path.exists(venv_python):
                                python_cmd = venv_python
                                st.info("✅ Sử dụng Python từ virtual environment")
                            else:
                                python_cmd = sys.executable
                                st.info("✅ Sử dụng Python hệ thống")
                            
                            st.text(f"🐍 Final python cmd: {python_cmd}")
                            st.text(f"📁 Working directory: {os.path.dirname(__file__)}")
                            
                            st.info("🔍 Bước 5: Chạy subprocess")
                            result = subprocess.run([python_cmd, script_path], 
                                                   capture_output=True, text=True, 
                                                   cwd=os.path.dirname(__file__),
                                                   timeout=300)  # 5 minutes timeout
                            
                            st.info("🔍 Bước 6: Kiểm tra kết quả")
                            st.text(f"📊 Return code: {result.returncode}")
                            st.text(f"📊 Stdout length: {len(result.stdout)}")
                            st.text(f"📊 Stderr length: {len(result.stderr)}")
                            
                            if result.stdout:
                                st.text("📄 Stdout:")
                                st.text(result.stdout)
                            
                            if result.stderr:
                                st.text("❌ Stderr:")
                                st.text(result.stderr)
                            
                            if result.returncode == 0:
                                st.success(f"✅ {uploaded_file.name} đã được xử lý thành công!")
                            else:
                                st.error(f"❌ {uploaded_file.name} xử lý thất bại")
                            
                        except subprocess.TimeoutExpired:
                            st.error("❌ Xử lý quá thời gian (5 phút)")
                        except Exception as e:
                            st.error(f"❌ Lỗi: {str(e)}")
                            st.text(f"🔍 Chi tiết lỗi: {type(e).__name__}")
                            import traceback
                            st.text(f"🔍 Traceback:")
                            st.text(traceback.format_exc())
        
        with col2:
            if st.button("🔄 Xử Lý Tất Cả Tệp", type="secondary"):
                with st.spinner("🔄 Đang xử lý tất cả tệp..."):
                    try:
                        st.info("🔍 Bước 1: Bắt đầu xử lý tất cả tệp")
                        
                        # Run processor script
                        st.info("🔍 Bước 2: Chuẩn bị chạy script processor")
                        import subprocess
                        
                        script_path = os.path.join(os.path.dirname(__file__), "run_processor.py")
                        st.text(f"📄 Script path: {script_path}")
                        st.text(f"📄 Script exists: {os.path.exists(script_path)}")
                        
                        # Use virtual environment python
                        st.info("🔍 Bước 3: Xác định Python command")
                        venv_python = os.path.join(os.path.dirname(__file__), "venv", "bin", "python")
                        st.text(f"🐍 Venv python: {venv_python}")
                        st.text(f"🐍 Venv exists: {os.path.exists(venv_python)}")
                        
                        if os.path.exists(venv_python):
                            python_cmd = venv_python
                            st.info("✅ Sử dụng Python từ virtual environment")
                        else:
                            python_cmd = sys.executable
                            st.info("✅ Sử dụng Python hệ thống")
                        
                        st.text(f"🐍 Final python cmd: {python_cmd}")
                        st.text(f"📁 Working directory: {os.path.dirname(__file__)}")
                        
                        st.info("🔍 Bước 4: Chạy subprocess")
                        result = subprocess.run([python_cmd, script_path], 
                                               capture_output=True, text=True, 
                                               cwd=os.path.dirname(__file__),
                                               timeout=300)  # 5 minutes timeout
                        
                        st.info("🔍 Bước 5: Kiểm tra kết quả")
                        st.text(f"📊 Return code: {result.returncode}")
                        st.text(f"📊 Stdout length: {len(result.stdout)}")
                        st.text(f"📊 Stderr length: {len(result.stderr)}")
                        
                        if result.stdout:
                            st.text("📄 Stdout:")
                            st.text(result.stdout)
                        
                        if result.stderr:
                            st.text("❌ Stderr:")
                            st.text(result.stderr)
                        
                        if result.returncode == 0:
                            st.success("✅ Xử lý tất cả tệp hoàn thành thành công!")
                        else:
                            st.error("❌ Xử lý tất cả tệp thất bại")
                        
                    except subprocess.TimeoutExpired:
                        st.error("❌ Xử lý quá thời gian (5 phút)")
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
                        st.text(f"🔍 Chi tiết lỗi: {type(e).__name__}")
                        import traceback
                        st.text(f"🔍 Traceback:")
                        st.text(traceback.format_exc())

elif menu == "📊 Xem Báo Cáo":
    st.header("📊 Xem Báo Cáo")
    
    # Get list of documents
    documents = get_documents_list()
    
    if not documents:
        st.warning("Không tìm thấy tài liệu nào trong thư mục documents")
        st.stop()
    
    # Document selection
    st.subheader("Chọn Tài Liệu")
    
    document_names = [doc['name'] for doc in documents]
    selected_doc_name = st.selectbox(
        "Chọn một tài liệu để xem báo cáo",
        document_names,
        help="Chọn một tài liệu để xem các báo cáo đã tạo"
    )
    
    if selected_doc_name:
        # Show document info
        selected_doc = next(doc for doc in documents if doc['name'] == selected_doc_name)
        
        st.markdown(f"""
        <div class="file-info">
            <h4>📄 {selected_doc['name']}</h4>
            <p><strong>Kích Thước:</strong> {selected_doc['size']:,} bytes</p>
            <p><strong>Chỉnh Sửa Lần Cuối:</strong> {selected_doc['modified']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get output files for selected document
        output_files = get_output_files_for_document(selected_doc_name)
        
        if not output_files:
            st.warning(f"Không tìm thấy tệp đầu ra nào cho {selected_doc_name}")
            st.info("Hãy xử lý tài liệu trước bằng menu Tải Lên & Xử Lý")
        else:
            st.subheader(f"📁 Tệp Đầu Ra ({len(output_files)} tệp)")
            
            # Show output files
            for output_file in output_files:
                with st.expander(f"📄 {output_file['name']} ({output_file['type']})"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Loại:** {output_file['type']}")
                        st.write(f"**Kích Thước:** {output_file['size']:,} bytes")
                    
                    with col2:
                        st.write(f"**Chỉnh Sửa:** {output_file['modified']}")
                    
                    with col3:
                        if st.button(f"Xem", key=f"view_{output_file['name']}"):
                            st.session_state[f"viewing_{output_file['name']}"] = True
                    
                    # Show content if viewing
                    if st.session_state.get(f"viewing_{output_file['name']}", False):
                        st.subheader(f"Nội Dung: {output_file['name']}")
                        display_file_content(output_file['path'], output_file['type'])
                        
                        if st.button(f"Đóng", key=f"close_{output_file['name']}"):
                            st.session_state[f"viewing_{output_file['name']}"] = False
                            st.rerun()

# Footer
st.markdown("---")
st.markdown("**Bộ Xử Lý Tài Liệu Cuộc Họp RAG** - Hệ thống xử lý tài liệu được hỗ trợ bởi AI với xử lý tăng dần")
