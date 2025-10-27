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
    page_title="RAG Meeting Processor - Test Interface",
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
        st.error(f"❌ Failed to initialize processor: {e}")
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
           filename.startswith(f"COMPREHENSIVE_{base_name}") or \
           filename.startswith(f"DATA_{base_name}") or \
           filename.startswith(f"RAW_CONTENT_{base_name}"):
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
    if filename.endswith('.docx'):
        return 'Word Document'
    elif filename.endswith('.json'):
        return 'JSON Data'
    elif filename.endswith('.txt'):
        if 'COMPREHENSIVE' in filename:
            return 'Comprehensive Report'
        elif 'RAW_CONTENT' in filename:
            return 'Raw Content'
        elif 'SUMMARY' in filename:
            return 'Summary Report'
        else:
            return 'Text File'
    else:
        return 'Unknown'

def display_file_content(file_path, file_type):
    """Display content of a file based on its type"""
    try:
        if file_type == 'JSON Data':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            st.json(data)
        elif file_type in ['Comprehensive Report', 'Raw Content', 'Summary Report', 'Text File']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            st.text_area("File Content", content, height=400)
        else:
            st.info("File preview not available for this file type")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Main interface
st.markdown('<h1 class="main-header">🤖 RAG Meeting Processor</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666;">Test Interface</h2>', unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "OpenAI API Key", 
        type="password",
        help="Enter your OpenAI API key",
        value=os.environ.get("OPENAI_API_KEY", "")
    )
    
    if st.button("Initialize Processor", type="primary"):
        if api_key:
            with st.spinner("Initializing..."):
                if initialize_processor(api_key):
                    st.success("✅ Processor initialized successfully!")
                else:
                    st.error("❌ Failed to initialize processor")
        else:
            st.error("❌ Please enter API key")

# Main content area
if not st.session_state.api_key_set:
    st.warning("⚠️ Please initialize the processor with your API key in the sidebar")
    st.stop()

# Menu selection
menu = st.selectbox(
    "Select Menu",
    ["📁 Upload & Process", "📊 View Reports"],
    help="Choose between uploading new files or viewing existing reports"
)

if menu == "📁 Upload & Process":
    st.header("📁 Upload & Process Documents")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload New Document")
        
        uploaded_file = st.file_uploader(
            "Choose a file to upload",
            type=['pdf', 'jpg', 'jpeg', 'png', 'docx', 'txt'],
            help="Upload a meeting document to process"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # File info
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.metric("File Size", f"{uploaded_file.size:,} bytes")
            with col_info2:
                st.metric("File Type", uploaded_file.type)
    
    with col2:
        st.subheader("Processing Options")
        
        # Processing options
        enable_vlm = st.checkbox("Enable VLM Enhanced", value=True, help="For image processing")
        enable_table = st.checkbox("Enable Table Processing", value=True)
        enable_equation = st.checkbox("Enable Equation Processing", value=True)
        
        # Query options
        mode = st.selectbox("Query Mode", ["hybrid", "vector", "graph"], index=0)
        top_k = st.slider("Top K Results", 5, 50, 20)
        
        # Process buttons
        st.markdown("**Processing Options:**")
        st.info("""
        - **Process Uploaded File**: Upload a file and process it using incremental processing
        - **Process All Files**: Run incremental processing on all files in the documents folder
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Process Uploaded File", type="primary", disabled=not uploaded_file):
                if uploaded_file:
                    with st.spinner("🔄 Processing document with incremental processing..."):
                        try:
                            # Save uploaded file temporarily
                            temp_path = os.path.join(DOCUMENTS_DIR, uploaded_file.name)
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Use incremental processing instead of single file processing
                            result = asyncio.run(st.session_state.processor.process_incremental(DOCUMENTS_DIR))
                            
                            if result["status"] == "no_changes":
                                st.info(f"ℹ️ {result['message']}")
                            elif result["status"] == "completed":
                                # Show processing results
                                successful_count = result["successful_files"]
                                failed_count = result["failed_files"]
                                total_count = result["total_files"]
                                
                                if successful_count > 0:
                                    st.success(f"✅ Processing completed! {successful_count}/{total_count} files processed successfully")
                                    
                                    # Show scan report
                                    scan_report = result["scan_report"]
                                    if scan_report["files_to_process_list"]:
                                        st.info(f"📄 Files processed: {', '.join([f['name'] for f in scan_report['files_to_process_list']])}")
                                    
                                    # Show processing results for uploaded file
                                    processing_results = result["processing_results"]
                                    uploaded_file_result = None
                                    for pr in processing_results:
                                        if pr["file_path"] == temp_path:
                                            uploaded_file_result = pr
                                            break
                                    
                                    if uploaded_file_result and uploaded_file_result["success"]:
                                        st.success(f"✅ {uploaded_file.name} processed successfully!")
                                    elif uploaded_file_result and not uploaded_file_result["success"]:
                                        st.error(f"❌ {uploaded_file.name} processing failed: {uploaded_file_result.get('error', 'Unknown error')}")
                                else:
                                    st.error("❌ No files were processed successfully")
                                
                                if failed_count > 0:
                                    st.warning(f"⚠️ {failed_count} files failed to process")
                            else:
                                st.error(f"❌ Processing failed with status: {result['status']}")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        with col2:
            if st.button("🔄 Process All Files", type="secondary"):
                with st.spinner("🔄 Running incremental processing on all files..."):
                    try:
                        # Run incremental processing on all files in documents directory
                        result = asyncio.run(st.session_state.processor.process_incremental(DOCUMENTS_DIR))
                        
                        if result["status"] == "no_changes":
                            st.info(f"ℹ️ {result['message']}")
                        elif result["status"] == "completed":
                            # Show processing results
                            successful_count = result["successful_files"]
                            failed_count = result["failed_files"]
                            total_count = result["total_files"]
                            
                            if successful_count > 0:
                                st.success(f"✅ Processing completed! {successful_count}/{total_count} files processed successfully")
                                
                                # Show scan report
                                scan_report = result["scan_report"]
                                if scan_report["files_to_process_list"]:
                                    st.info(f"📄 Files processed: {', '.join([f['name'] for f in scan_report['files_to_process_list']])}")
                                
                                if scan_report["files_unchanged_list"]:
                                    st.info(f"✅ Files unchanged: {', '.join([f['name'] for f in scan_report['files_unchanged_list']])}")
                            else:
                                st.error("❌ No files were processed successfully")
                            
                            if failed_count > 0:
                                st.warning(f"⚠️ {failed_count} files failed to process")
                        else:
                            st.error(f"❌ Processing failed with status: {result['status']}")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Show processing status
    st.subheader("📊 Processing Status")
    
    try:
        status = st.session_state.processor.get_processing_status()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", status["total_files"])
        with col2:
            st.metric("Processed", status["processed_files"], delta=None)
        with col3:
            st.metric("Failed", status["failed_files"], delta=None)
        
        # Show detailed status
        if status["files_detail"]:
            st.subheader("File Details")
            for filename, detail in status["files_detail"].items():
                status_color = "success" if detail["status"] == "processed" else "error" if detail["status"] == "failed" else "warning"
                st.markdown(f"**{filename}**: <span class='status-{status_color}'>{detail['status'].upper()}</span>", unsafe_allow_html=True)
                
                if detail["status"] == "processed" and "processed_at" in detail:
                    st.caption(f"Processed at: {detail['processed_at']}")
                elif detail["status"] == "failed" and "error" in detail:
                    st.caption(f"Error: {detail['error']}")
    
    except Exception as e:
        st.error(f"Error getting processing status: {e}")

elif menu == "📊 View Reports":
    st.header("📊 View Reports")
    
    # Get list of documents
    documents = get_documents_list()
    
    if not documents:
        st.warning("No documents found in the documents folder")
        st.stop()
    
    # Document selection
    st.subheader("Select Document")
    
    document_names = [doc['name'] for doc in documents]
    selected_doc_name = st.selectbox(
        "Choose a document to view reports",
        document_names,
        help="Select a document to view its generated reports"
    )
    
    if selected_doc_name:
        # Show document info
        selected_doc = next(doc for doc in documents if doc['name'] == selected_doc_name)
        
        st.markdown(f"""
        <div class="file-info">
            <h4>📄 {selected_doc['name']}</h4>
            <p><strong>Size:</strong> {selected_doc['size']:,} bytes</p>
            <p><strong>Last Modified:</strong> {selected_doc['modified']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get output files for selected document
        output_files = get_output_files_for_document(selected_doc_name)
        
        if not output_files:
            st.warning(f"No output files found for {selected_doc_name}")
            st.info("Process the document first using the Upload & Process menu")
        else:
            st.subheader(f"📁 Output Files ({len(output_files)} files)")
            
            # Show output files
            for output_file in output_files:
                with st.expander(f"📄 {output_file['name']} ({output_file['type']})"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Type:** {output_file['type']}")
                        st.write(f"**Size:** {output_file['size']:,} bytes")
                    
                    with col2:
                        st.write(f"**Modified:** {output_file['modified']}")
                    
                    with col3:
                        if st.button(f"View", key=f"view_{output_file['name']}"):
                            st.session_state[f"viewing_{output_file['name']}"] = True
                    
                    # Show content if viewing
                    if st.session_state.get(f"viewing_{output_file['name']}", False):
                        st.subheader(f"Content: {output_file['name']}")
                        display_file_content(output_file['path'], output_file['type'])
                        
                        if st.button(f"Close", key=f"close_{output_file['name']}"):
                            st.session_state[f"viewing_{output_file['name']}"] = False
                            st.rerun()

# Footer
st.markdown("---")
st.markdown("**RAG Meeting Processor** - AI-powered document processing system with incremental processing")
