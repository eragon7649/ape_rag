# Troubleshooting Guide

## Common Issues and Solutions

### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: 
- Use the main entry point: `python run_processor.py`
- Or run from src directory: `cd src && python main.py`

### 2. Shell/Terminal Issues

**Problem**: `spawn /bin/zsh ENOENT` or similar shell errors

**Solutions**:
1. Try using `python3` instead of `python`
2. Check if Python is properly installed: `which python3`
3. Use the diagnostic script: `python3 diagnose.py`

### 3. API Key Issues

**Problem**: `OPENAI_API_KEY not set`

**Solution**:
```bash
export OPENAI_API_KEY="your_actual_api_key_here"
```

### 4. Missing Dependencies

**Problem**: `ModuleNotFoundError` for required packages

**Solution**:
```bash
pip install -r requirements.txt
```

### 5. Directory Structure Issues

**Problem**: Files not found or directories missing

**Solution**: Run the setup script:
```bash
python setup.py
```

## Testing Steps

### Step 1: Basic Functionality Test
```bash
python3 simple_test.py
```

### Step 2: Diagnostic Check
```bash
python3 diagnose.py
```

### Step 3: Import Test
```bash
python3 test_imports.py
```

### Step 4: Full System Test
```bash
python3 run_processor.py
```

## Environment Setup

### Required Environment Variables
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export OPENAI_BASE_URL="your_base_url"  # Optional
```

### Required System Dependencies
- Python 3.8+
- LibreOffice (for document processing)
- pip (for package management)

## File Structure Verification

Ensure your project has this structure:
```
RAG/
├── src/
│   ├── core/
│   │   ├── config.py
│   │   ├── rag_processor.py
│   │   └── output_formatter.py
│   ├── data/
│   │   └── extraction_prompts.py
│   └── main.py
├── documents/
├── output/
├── rag_storage/
├── requirements.txt
├── run_processor.py
├── setup.py
└── README.md
```

## Getting Help

If you continue to experience issues:

1. Check the diagnostic output: `python3 diagnose.py`
2. Verify your Python installation: `python3 --version`
3. Check your API key configuration
4. Ensure all dependencies are installed: `pip list`

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `spawn /bin/zsh ENOENT` | Shell configuration issue | Use `python3` instead of `python` |
| `ModuleNotFoundError` | Missing dependencies | Run `pip install -r requirements.txt` |
| `OPENAI_API_KEY not set` | Missing API key | Set environment variable |
| `Directory not found` | Missing directories | Run `python setup.py` |
