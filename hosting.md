# 🖥️ HOSTING GUIDE - RAG Meeting Processor

## 📊 **PHÂN TÍCH PROJECT VÀ YÊU CẦU**

### **Các Model AI được sử dụng:**
- **LLM Model:** `gpt-4o-mini` (cho xử lý văn bản)
- **VLM Model:** `gpt-4o` (cho xử lý hình ảnh, OCR)
- **Embedding Model:** `text-embedding-3-large` (3072 dimensions)

### **Các thư viện chính:**
- **RAGAnything** (>=1.2.0) - Framework RAG chính
- **LightRAG** (>=0.1.0) - Xử lý graph và embedding
- **Streamlit** (>=1.28.0) - Web interface
- **MinerU** - Document parser (PDF, Office files)

### **Tính năng chính:**
- Xử lý tài liệu PDF, Word, hình ảnh
- OCR và phân tích hình ảnh
- Trích xuất thông tin từ biên bản họp
- Web interface với Streamlit
- Incremental processing

---

## 🖥️ **CẤU HÌNH SERVER TỐI THIỂU**

### **🔧 Cấu hình cơ bản (Minimum)**

| Thành phần | Yêu cầu tối thiểu | Lý do |
|------------|------------------|-------|
| **CPU** | 4-6 cores (Intel Xeon/AMD EPYC) | Xử lý document parsing, API calls |
| **RAM** | **16-32GB** | RAGAnything + LightRAG + Streamlit + document processing |
| **Storage** | **100-200GB SSD** | Source code + dependencies + processed documents |
| **Network** | 100Mbps+ | API calls đến OpenAI, upload/download files |
| **OS** | Ubuntu 20.04+ / CentOS 8+ | Python 3.8+ support |

### **⚡ Cấu hình khuyến nghị (Recommended)**

| Thành phần | Yêu cầu khuyến nghị | Lý do |
|------------|-------------------|-------|
| **CPU** | 8-12 cores (Intel Xeon/AMD EPYC) | Xử lý đồng thời nhiều documents |
| **RAM** | **32-64GB** | Buffer cho large documents, caching |
| **Storage** | **500GB-1TB NVMe SSD** | Fast I/O cho document processing |
| **Network** | 1Gbps+ | Stable API connections |
| **OS** | Ubuntu 22.04 LTS | Latest Python support, stability |

### **🚀 Cấu hình tối ưu (Optimal)**

| Thành phần | Yêu cầu tối ưu | Lý do |
|------------|---------------|-------|
| **CPU** | 16+ cores (Intel Xeon Gold/AMD EPYC) | High-throughput processing |
| **RAM** | **64-128GB** | Large document batches, caching |
| **Storage** | **1-2TB NVMe SSD** | Enterprise-grade performance |
| **Network** | 10Gbps+ | High-speed data transfer |
| **OS** | Ubuntu 22.04 LTS + Docker | Containerized deployment |

---

## 💰 **ƯỚC TÍNH CHI PHÍ HOSTING**

### **Cloud Providers (Monthly)**

| Provider | Cấu hình Minimum | Cấu hình Recommended | Cấu hình Optimal |
|----------|------------------|---------------------|------------------|
| **AWS EC2** | $50-100 | $150-300 | $500-1000 |
| **Google Cloud** | $40-80 | $120-250 | $400-800 |
| **Azure** | $45-90 | $140-280 | $450-900 |
| **DigitalOcean** | $40-80 | $120-240 | $400-800 |

### **VPS Providers (Monthly)**

| Provider | Cấu hình Minimum | Cấu hình Recommended |
|----------|------------------|---------------------|
| **Vultr** | $20-40 | $80-160 |
| **Linode** | $25-50 | $100-200 |
| **Hetzner** | $15-30 | $60-120 |

---

## 🔍 **PHÂN TÍCH CHI TIẾT TỪNG THÀNH PHẦN**

### **1. RAGAnything Framework**
- **Memory:** 2-8GB RAM cho document processing
- **CPU:** 2-4 cores cho parsing operations
- **Storage:** 50-200GB cho vector database và cache

### **2. LightRAG**
- **Memory:** 1-4GB RAM cho graph processing
- **CPU:** 1-2 cores cho embedding operations
- **Storage:** 20-100GB cho graph storage

### **3. Streamlit Web Interface**
- **Memory:** 1-2GB RAM cho web server
- **CPU:** 1-2 cores cho concurrent users
- **Network:** Bandwidth cho file uploads

### **4. Document Processing**
- **PDF Processing:** 1-4GB RAM per large document
- **Image Processing:** 2-8GB RAM cho OCR operations
- **Office Files:** 1-2GB RAM per document

---

## 📋 **CHECKLIST TRIỂN KHAI**

### **✅ Yêu cầu hệ thống**
- [ ] Python 3.8+ installed
- [ ] pip package manager
- [ ] Git for version control
- [ ] LibreOffice (cho Office file processing)
- [ ] FFmpeg (cho multimedia files)

### **✅ Environment Variables**
- [ ] `OPENAI_API_KEY` configured
- [ ] `OPENAI_BASE_URL` (nếu dùng custom endpoint)
- [ ] File permissions cho documents/ và output/ folders

### **✅ Security**
- [ ] Firewall configured
- [ ] SSL certificate cho HTTPS
- [ ] API key protection
- [ ] File upload restrictions

---

## 🎯 **KHUYẾN NGHỊ CUỐI CÙNG**

### **Cho Development/Testing:**
- **Cấu hình:** 4 cores, 16GB RAM, 200GB SSD
- **Chi phí:** $40-80/tháng
- **Phù hợp:** Testing, small-scale processing

### **Cho Production:**
- **Cấu hình:** 8 cores, 32GB RAM, 500GB NVMe SSD
- **Chi phí:** $150-300/tháng
- **Phù hợp:** Regular document processing, multiple users

### **Cho Enterprise:**
- **Cấu hình:** 16+ cores, 64GB RAM, 1TB NVMe SSD
- **Chi phí:** $500-1000/tháng
- **Phù hợp:** High-volume processing, mission-critical

---

## 🚀 **HƯỚNG DẪN TRIỂN KHAI**

### **1. Chuẩn bị Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3.8 python3.8-pip python3.8-venv -y

# Install system dependencies
sudo apt install git libreoffice ffmpeg -y

# Install Node.js (for some dependencies)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### **2. Deploy Application**
```bash
# Clone repository
git clone <your-repo-url>
cd ape_rag

# Create virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # optional

# Create necessary directories
mkdir -p documents output rag_storage
```

### **3. Run Application**
```bash
# Run web interface
streamlit run test_interface.py --server.port 8501 --server.address 0.0.0.0

# Or run command line processing
python run_processor.py
```

### **4. Setup Reverse Proxy (Nginx)**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **5. Setup SSL Certificate**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

---

## 📊 **MONITORING VÀ MAINTENANCE**

### **System Monitoring**
```bash
# Check system resources
htop
df -h
free -h

# Check application logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### **Application Monitoring**
- Monitor RAM usage during document processing
- Check API rate limits với OpenAI
- Monitor disk space cho processed documents
- Check network connectivity

### **Backup Strategy**
- Backup source code regularly
- Backup processed documents và output files
- Backup configuration files
- Setup automated backups

---

## ⚠️ **LƯU Ý QUAN TRỌNG**

1. **API Costs:** OpenAI API có chi phí theo usage, cần monitor để tránh overspend
2. **Rate Limits:** OpenAI có rate limits, cần implement retry logic
3. **File Size Limits:** Streamlit có giới hạn upload file size
4. **Memory Management:** Large documents có thể gây memory issues
5. **Security:** Bảo vệ API keys và sensitive data

---

## 📞 **SUPPORT VÀ TROUBLESHOOTING**

### **Common Issues:**
- **Memory errors:** Increase RAM hoặc optimize document size
- **API errors:** Check API key và rate limits
- **File upload errors:** Check file size limits
- **Performance issues:** Monitor CPU và RAM usage

### **Performance Optimization:**
- Use SSD storage cho better I/O
- Implement caching cho processed documents
- Optimize document parsing settings
- Use CDN cho static files

---

*Last updated: $(date)*
*Project: RAG Meeting Processor*
