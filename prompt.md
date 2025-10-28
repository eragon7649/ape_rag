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

**Visual**: 
```
┌─────────────────────────────────────────────────────────────┐
│                    APE RAG SYSTEM                          │
│              🤖 AI-Powered Document Processing             │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INPUT     │───▶│ PROCESSING  │───▶│   OUTPUT    │
│             │    │             │    │             │
│ 📄 PDF      │    │ 🧠 AI       │    │ 📝 Summary  │
│ 📄 DOCX     │    │ ⚙️ RAG      │    │ 📄 Full     │
│ 📄 TXT      │    │ 🔍 Extract  │    │ 📊 Metadata │
│ 📄 HTML/MD  │    │ 🔄 Increment│    │ 💾 Storage  │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Key Metrics**:
- ⚡ Processing Speed: 20-65s per document
- 🎯 Accuracy: 95%+ information extraction
- 🔄 Incremental: Only process changed files
- 📊 Output: Structured TXT format

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

**Visual**: 
```
┌─────────────────────────────────────────────────────────────────┐
│                        APE RAG ARCHITECTURE                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   INPUT LAYER   │    │ PROCESSING LAYER │    │   AI MODELS     │
│                 │    │                  │    │                 │
│ 📄 PDF/DOCX/TXT │───▶│ ⚙️ RAGAnything   │───▶│ 🧠 GPT-4o-mini  │
│ 🔍 Validation   │    │ 🔗 LightRAG      │    │ 👁️ GPT-4o (VLM) │
│ 📝 Encoding     │    │ 📊 Parser        │    │ 🔢 Embeddings   │
│                 │    │ 🔍 Extractor     │    │ 📄 MinerU       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ STORAGE LAYER   │    │  OUTPUT LAYER    │    │   INTERFACE     │
│                 │    │                  │    │                 │
│ 💾 Vector DB    │◀───│ 📝 Summary.txt   │◀───│ 🖥️ Streamlit    │
│ 📊 JSON Cache   │    │ 📄 Full_Content  │    │ 📊 Real-time    │
│ 📁 File System  │    │ 📈 Error Reports │    │ 🔄 Progress     │
│ 🔄 Incremental  │    │ 💾 Storage       │    │ 📱 Web UI       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Tech Stack Details**:
- **Models**: GPT-4o-mini, GPT-4o, text-embedding-3-large
- **Frameworks**: RAGAnything, LightRAG, Streamlit
- **Storage**: Vector DB (3072-dim), JSON, File System
- **Processing**: Async Python 3.13, Multi-threading

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

**Visual**: 
```
┌─────────────────────────────────────────────────────────────────┐
│                    CORE FEATURES & CAPABILITIES                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 1. MULTI-FORMAT │  │ 2. SMART EXTRACT│  │ 3. AI GENERATION│  │ 4. ADVANCED     │
│    PROCESSING   │  │                 │  │                 │  │    FEATURES     │
│                 │  │                 │  │                 │  │                 │
│ 📄 PDF          │  │ 👥 People       │  │ 📝 Summary      │  │ 🔄 Incremental  │
│    OCR Handwriting│  │ 🏢 Organizations│  │ 📄 Full Content │  │    Processing   │
│    Table Extract │  │ 📅 Dates        │  │ 🎯 Template-based│  │                 │
│    Layout Analysis│  │ ⚖️ Decisions    │  │ 🌐 Multi-lang   │  │ ⚡ Error Handling│
│                 │  │                 │  │                 │  │    (3 retries)  │
│ 📄 DOCX         │  │ 📊 Headings     │  │ 🎨 Context-Aware│  │                 │
│    Paragraphs   │  │ 📋 Tables       │  │                 │  │ 📊 Real-time    │
│    Tables       │  │ 📝 Lists        │  │                 │  │    Status       │
│    Format Preserve│  │ 🏢 Meeting Info │  │                 │  │                 │
│                 │  │                 │  │                 │  │ 🔍 File Tracking│
│ 📄 TXT          │  │ 🔍 Metadata     │  │                 │  │    (MD5 Hash)   │
│    Multi-encoding│  │    Analysis     │  │                 │  │                 │
│    UTF-8/Latin-1│  │ 🌐 Language     │  │                 │  │                 │
│    CP1252       │  │    Detection    │  │                 │  │                 │
│                 │  │                 │  │                 │  │                 │
│ 📄 HTML/MD      │  │ 🔗 Relationship │  │                 │  │                 │
│    BeautifulSoup│  │    Mapping      │  │                 │  │                 │
│    Content Clean│  │ 🔄 Decision     │  │                 │  │                 │
│    Text Extract │  │    Flows        │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Performance Metrics**:
- 📊 **Processing Speed**: 20-65s per document
- 🎯 **Accuracy**: 95%+ information extraction
- 🔄 **Efficiency**: Only process changed files
- 🛡️ **Reliability**: 3-retry error handling

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

**Visual**: 
```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT PROCESSING WORKFLOW                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   STEP 1    │    │   STEP 2    │    │   STEP 3    │    │   STEP 4    │    │   STEP 5    │
│ UPLOAD &    │───▶│ DOCUMENT    │───▶│ AI ANALYSIS │───▶│ CONTENT     │───▶│ OUTPUT &    │
│ VALIDATION  │    │ PARSING     │    │             │    │ GENERATION  │    │ STORAGE     │
│             │    │             │    │             │    │             │    │             │
│ 📤 Upload   │    │ 🔧 PDF:     │    │ 🧠 RAG      │    │ 📝 Summary  │    │ 📄 Files    │
│   1-2s      │    │    MinerU   │    │    Processing│    │    Creation │    │    Generated│
│             │    │   5-15s     │    │   10-30s    │    │   5-15s     │    │   1-3s      │
│ 🔍 Validate │    │ 🔧 DOCX:    │    │ 🔍 Entity   │    │ 📄 Full     │    │ 💾 Vector   │
│    Format   │    │    python-  │    │    Extract  │    │    Content  │    │    Storage  │
│             │    │    docx     │    │   8 queries │    │             │    │             │
│ 📊 File     │    │ 🔧 TXT:     │    │ 📊 Metadata │    │ ⚡ Error    │    │ 🔄 Tracking │
│    Info     │    │    Multi-   │    │    Analysis │    │    Handling │    │    Update   │
│             │    │    encoding │    │             │    │             │    │             │
│ 🔄 Encoding │    │ 🔧 HTML:    │    │ 🔗 Relation │    │ ✅ Quality  │    │ 📥 Download │
│    Detect   │    │    Beautiful│    │    Mapping  │    │    Check    │    │    Ready    │
│             │    │    Soup     │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │                   │                   │
        ▼                   ▼                   ▼                   ▼                   ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
   │ SUCCESS │         │ SUCCESS │         │ SUCCESS │         │ SUCCESS │         │ SUCCESS │
   │   ✅    │         │   ✅    │         │   ✅    │         │   ✅    │         │   ✅    │
   └─────────┘         └─────────┘         └─────────┘         └─────────┘         └─────────┘
        │                   │                   │                   │                   │
        ▼                   ▼                   ▼                   ▼                   ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
   │ FALLBACK│         │ FALLBACK│         │ FALLBACK│         │ FALLBACK│         │ FALLBACK│
   │   🔄    │         │   🔄    │         │   🔄    │         │   🔄    │         │   🔄    │
   └─────────┘         └─────────┘         └─────────┘         └─────────┘         └─────────┘

TOTAL PROCESSING TIME: 20-65 seconds per document
```

**Error Handling Flow**:
- 🔄 **Retry Logic**: 3 attempts with exponential backoff
- ⏱️ **Backoff**: 1s → 2s → 4s delays
- 🛡️ **Fallback**: Alternative parsing methods
- 📊 **Monitoring**: Real-time status updates

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



**Visual**: 
```
┌─────────────────────────────────────────────────────────────────┐
│                    TECH STACK & INFRASTRUCTURE                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ AI/ML FRAMEWORK │  │ BACKEND TECH    │  │ FRONTEND & UI   │  │ STORAGE & INFRA │
│                 │  │                 │  │                 │  │                 │
│ 🧠 GPT-4o-mini  │  │ 🐍 Python 3.13 │  │ 🖥️ Streamlit    │  │ 💾 Vector DB    │
│    Text Gen     │  │    Async/Await  │  │    Web UI       │  │    3072-dim     │
│    $0.01-0.03   │  │                 │  │                 │  │                 │
│                 │  │ 📊 Pydantic     │  │ 🎨 Custom CSS   │  │ 📊 JSON Storage │
│ 👁️ GPT-4o (VLM) │  │    Validation  │  │    Professional │  │    Metadata     │
│    OCR/Image    │  │                 │  │                 │  │    Cache        │
│    $0.05-0.15   │  │ 🌐 BeautifulSoup│  │ 📁 File Upload  │  │                 │
│                 │  │    HTML/XML     │  │    Drag-Drop    │  │ 📁 File System  │
│ 🔢 Embeddings   │  │                 │  │                 │  │    Parsed Docs  │
│    text-embedding│  │ 📄 python-docx │  │ 📊 Progress     │  │    Images       │
│    3-large      │  │    Word Proc    │  │    Tracking     │  │    Layouts      │
│    $0.001       │  │                 │  │                 │  │                 │
│                 │  │ 🔐 hashlib      │  │ 🔄 Real-time    │  │ 🔄 Incremental  │
│ ⚙️ RAGAnything  │  │    MD5 Hash     │  │    Updates      │  │    System       │
│    Doc Engine   │  │                 │  │                 │  │    Change Det.  │
│                 │  │                 │  │                 │  │                 │
│ 🔗 LightRAG     │  │                 │  │                 │  │                 │
│    Knowledge    │  │                 │  │                 │  │                 │
│    Graph        │  │                 │  │                 │  │                 │
│                 │  │                 │  │                 │  │                 │
│ 📄 MinerU       │  │                 │  │                 │  │                 │
│    PDF Parser   │  │                 │  │                 │  │                 │
│    OCR Support  │  │                 │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Infrastructure Requirements**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM REQUIREMENTS                         │
└─────────────────────────────────────────────────────────────────┘

💾 MEMORY:           🖥️ STORAGE:           🌐 NETWORK:           ⚡ CPU:
┌─────────────┐     ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Min: 8GB    │     │ Min: 10GB   │      │ Stable      │      │ Multi-core  │
│ Rec: 16GB   │     │ Rec: 50GB   │      │ Internet    │      │ Recommended │
│             │     │             │      │ OpenAI API  │      │             │
└─────────────┘     └─────────────┘      └─────────────┘      └─────────────┘
```

**Cost Breakdown (Per Document)**:
```
┌─────────────────────────────────────────────────────────────────┐
│                        API COSTS                               │
└─────────────────────────────────────────────────────────────────┘

📊 GPT-4o-mini:     👁️ GPT-4o (VLM):     🔢 Embeddings:        📈 TOTAL:
┌─────────────┐     ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ $0.01-0.03  │  +  │ $0.05-0.15  │  +   │ $0.001     │  =   │ $0.061-0.181│
│ Text Proc   │     │ Image Proc  │      │ Vector Gen  │      │ Per Doc     │
└─────────────┘     └─────────────┘      └─────────────┘      └─────────────┘
```

## YÊU CẦU THIẾT KẾ:
- **Color Scheme**: Blue (#1f77b4), Green (#28a745), Gray (#6c757d), Orange (#ff7f0e)
- **Icons**: Tech-specific icons (🤖, ⚙️, 🧠, 💾, 📊)
- **Layout**: Technical diagrams, performance charts, cost breakdowns
- **Typography**: Monospace cho code/tech specs, clear hierarchy
- **Visual Elements**: Architecture diagrams, workflow charts, tech stack visualization
- **Data Points**: Specific numbers, timing, costs, performance metrics