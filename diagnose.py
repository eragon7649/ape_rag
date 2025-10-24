#!/usr/bin/env python3
"""
Diagnostic script to check the RAG Meeting Processor setup
"""

import os
import sys

def main():
    print("🔍 RAG Meeting Processor Diagnostic")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check if required directories exist
    required_dirs = ["src", "documents", "output", "rag_storage"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
    
    # Check if required files exist
    required_files = [
        "src/main.py",
        "src/core/config.py", 
        "src/core/rag_processor.py",
        "src/core/output_formatter.py",
        "src/data/extraction_prompts.py",
        "requirements.txt"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
    
    # Check environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key and api_key != "YOUR_API_KEY_HERE":
        print("✅ OPENAI_API_KEY is set")
    else:
        print("⚠️  OPENAI_API_KEY not set or using default")
    
    # Try to import required modules
    print("\n📦 Testing imports...")
    
    try:
        import asyncio
        print("✅ asyncio imported successfully")
    except ImportError as e:
        print(f"❌ asyncio import failed: {e}")
    
    try:
        import json
        print("✅ json imported successfully")
    except ImportError as e:
        print(f"❌ json import failed: {e}")
    
    # Test if we can add src to path and import our modules
    sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
    
    try:
        from core.config import DOCUMENTS_DIR, OUTPUT_DIR
        print("✅ Core config imported successfully")
        print(f"   Documents dir: {DOCUMENTS_DIR}")
        print(f"   Output dir: {OUTPUT_DIR}")
    except ImportError as e:
        print(f"❌ Core config import failed: {e}")
    
    print("\n" + "=" * 50)
    print("Diagnostic completed!")

if __name__ == "__main__":
    main()
