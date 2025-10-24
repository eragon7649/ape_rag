# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup
```bash
python3 setup.py
```

### Step 2: Configure API Key
```bash
export OPENAI_API_KEY="your_actual_api_key_here"
```

### Step 3: Run the Processor
```bash
python3 run_processor.py
```

## 🔧 If You Encounter Issues

### Test Basic Functionality
```bash
python3 simple_test.py
```

### Run Diagnostics
```bash
python3 diagnose.py
```

### Check Imports
```bash
python3 test_imports.py
```

## 📁 Project Structure
```
RAG/
├── src/                    # Source code
├── documents/              # Put your meeting files here
├── output/                 # Results will appear here
├── rag_storage/           # RAG processing storage
├── run_processor.py       # Main entry point
├── setup.py              # Setup script
└── requirements.txt      # Dependencies
```

## 📋 Supported File Types
- PDF documents
- JPG/PNG images
- DOCX files
- Handwritten notes (images)

## 🎯 What It Does
1. Processes meeting documents
2. Extracts key information (decisions, participants, etc.)
3. Generates Word document summaries
4. Saves structured data

## ⚡ Expected Performance
- Processing time: < 1 minute per document
- Output: Professional Word documents + structured data
- Language: Vietnamese support

## 🆘 Need Help?
Check `TROUBLESHOOTING.md` for detailed solutions to common issues.
