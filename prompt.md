## SLIDE 1: GIẢI PHÁP TỔNG QUAN
**Tiêu đề**: "APE RAG - Hệ Thống Xử Lý Tài Liệu Thông Minh"

**Nội dung chính**:
- **Định nghĩa**: Hệ thống RAG (Retrieval-Augmented Generation) tự động hóa việc xử lý, phân tích và trích xuất thông tin từ tài liệu cuộc họp
- **Core Technology**: RAGAnything + LightRAG + OpenAI API
- **Processing Capability**: 
  • Xử lý đa định dạng: PDF (với OCR), DOCX, TXT, HTML, Markdown
  • Trích xuất thông tin có cấu trúc: entities, relationships, metadata
  • Tạo tóm tắt và nội dung đầy đủ tự động
  • Hỗ trợ xử lý incremental (chỉ xử lý file mới/thay đổi)
- **Output**: Summary + Full Content (TXT format) với cấu trúc rõ ràng

**Visual**: Icon 🤖 + sơ đồ tổng quan input → processing → output

## SLIDE 2: KIẾN TRÚC HỆ THỐNG
**Tiêu đề**: "Kiến Trúc Hệ Thống APE RAG"

**Sơ đồ kiến trúc 5 tầng**:

**Tầng Input** 📄
- Document Upload (PDF, DOCX, TXT, HTML, MD)
- File Validation & Preprocessing
- Encoding Detection (UTF-8, Latin-1, CP1252)

**Tầng Processing Engine** ⚙️
- RAGAnything Core Engine
- LightRAG Framework (Knowledge Graph)
- Document Parser (Multi-method parsing)
- Content Extractor (Structured extraction)

**Tầng AI Models** 🧠
- **LLM**: OpenAI GPT-4o-mini (Text processing)
- **VLM**: OpenAI GPT-4o (OCR, Image analysis)
- **Embedding**: text-embedding-3-large (3072 dimensions)
- **Parser**: MinerU (PDF parsing with OCR)

**Tầng Storage** 💾
- Vector Database (Chunks, Entities, Relations)
- JSON Storage (Metadata, Cache, Tracking)
- File System (Parsed documents, Images)
- Incremental Tracking System

**Tầng Output** 📤
- Output Formatter (Summary, Full Content)
- Streamlit Web Interface
- Error Handling & Reporting

**Visual**: Sơ đồ flow từ trên xuống với arrows và tech stack details

## SLIDE 3: TÍNH NĂNG CHÍNH
**Tiêu đề**: "Tính Năng Cốt Lõi & Khả Năng Xử Lý"

**4 nhóm tính năng chính**:

**1. Xử Lý Đa Định Dạng** 📋
- **PDF**: OCR viết tay, table extraction, layout analysis
- **DOCX**: Paragraph + table extraction, formatting preservation
- **TXT**: Multi-encoding support (UTF-8, Latin-1, CP1252)
- **HTML/MD**: BeautifulSoup parsing, content cleaning
- **Batch Processing**: Multiple files simultaneously

**2. Trích Xuất Thông Minh** 🔍
- **Entity Extraction**: People, Organizations, Dates, Decisions
- **Structured Data**: Headings, Tables, Lists, Meeting Info
- **Metadata Analysis**: File type detection, language detection
- **Relationship Mapping**: Entity relationships, decision flows

**3. AI-Powered Content Generation** ✍️
- **Summary Generation**: Template-based, structured summaries
- **Full Content**: Comprehensive content with formatting
- **Multi-language Support**: Vietnamese + English detection
- **Context-Aware**: File-specific analysis and extraction

**4. Advanced Processing Features** 🚀
- **Incremental Processing**: Only process new/changed files
- **Error Handling**: Retry with exponential backoff (3 retries)
- **Real-time Status**: Live processing updates
- **File Tracking**: Hash-based change detection

**Visual**: 4 columns với icons và technical specifications

## SLIDE 4: QUY TRÌNH XỬ LÝ
**Tiêu đề**: "Workflow Xử Lý Tài Liệu Chi Tiết"

**5 bước chính với timing**:

**Bước 1: Upload & Validation** 📤 
- File upload qua Streamlit interface
- Format validation (PDF, DOCX, TXT, HTML, MD)
- Size check và encoding detection
- File info extraction (size, modified time, hash)

**Bước 2: Document Parsing** 🔧 
- **PDF**: MinerU parsing với multiple methods (auto, OCR, layout, table)
- **DOCX**: python-docx extraction (paragraphs + tables)
- **TXT**: Multi-encoding fallback parsing
- **HTML**: BeautifulSoup cleaning và text extraction
- Fallback methods nếu primary parsing fails

**Bước 3: AI Analysis** 🤖 
- **RAG Processing**: Document chunking và vectorization
- **Entity Extraction**: 8 structured queries (headings, tables, people, etc.)
- **Content Analysis**: Metadata extraction, language detection
- **Relationship Mapping**: Entity relationships và decision flows

**Bước 4: Content Generation** 📝 
- **Summary Creation**: Template-based với file-specific data
- **Full Content**: Comprehensive structured output
- **Error Handling**: Retry với exponential backoff
- **Quality Assurance**: Content validation và formatting

**Bước 5: Output & Storage** 💾 
- **File Generation**: Summary.txt + Full_Content.txt
- **Vector Storage**: Chunks, entities, relations
- **Tracking Update**: File processing status
- **Download Ready**: Immediate download availability

**Performance**: Total processing time: 20-65 seconds per document

**Visual**: Horizontal workflow với timing estimates và error handling paths

## SLIDE 5: CÔNG NGHỆ SỬ DỤNG
**Tiêu đề**: "Tech Stack & Infrastructure Requirements"

**4 nhóm công nghệ chi tiết**:

**AI/ML Framework** 🧠
- **OpenAI GPT-4o-mini**: Text generation, content analysis
- **OpenAI GPT-4o**: Vision processing, OCR, image analysis
- **text-embedding-3-large**: Vector embeddings (3072 dims)
- **RAGAnything**: Document processing engine
- **LightRAG**: Knowledge graph construction

**Backend Technologies** ⚙️
- **Python 3.13**: Core language với asyncio
- **Pydantic**: Data validation và serialization
- **BeautifulSoup4 + lxml**: HTML/XML parsing
- **python-docx**: Microsoft Word processing
- **hashlib**: File change detection (MD5)

**Frontend & Interface** 🖥️
- **Streamlit**: Web interface với real-time updates
- **Custom CSS**: Professional styling
- **File Upload/Download**: Drag-drop interface
- **Progress Tracking**: Real-time processing status

**Storage & Infrastructure** 💾
- **Vector Database**: Chunk storage (3072-dim vectors)
- **JSON Storage**: Metadata, cache, file tracking
- **File System**: Parsed documents, images, layouts
- **Incremental System**: Hash-based change detection



**Visual**: 4 sections với tech logos, performance specs, và cost estimates

## YÊU CẦU THIẾT KẾ:
- **Color Scheme**: Blue (#1f77b4), Green (#28a745), Gray (#6c757d), Orange (#ff7f0e)
- **Icons**: Tech-specific icons (🤖, ⚙️, 🧠, 💾, 📊)
- **Layout**: Technical diagrams, performance charts, cost breakdowns
- **Typography**: Monospace cho code/tech specs, clear hierarchy
- **Visual Elements**: Architecture diagrams, workflow charts, tech stack visualization
- **Data Points**: Specific numbers, timing, costs, performance metrics