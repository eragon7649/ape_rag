#!/usr/bin/env python3
# Test script to check imports

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from core.config import DOCUMENTS_DIR, OUTPUT_DIR
    print("✅ Config import successful")
    print(f"Documents dir: {DOCUMENTS_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")
except ImportError as e:
    print(f"❌ Config import failed: {e}")

try:
    from core.rag_processor import MeetingProcessor
    print("✅ RAG Processor import successful")
except ImportError as e:
    print(f"❌ RAG Processor import failed: {e}")

try:
    from core.output_formatter import OutputFormatter
    print("✅ Output Formatter import successful")
except ImportError as e:
    print(f"❌ Output Formatter import failed: {e}")

try:
    from data.extraction_prompts import QUERY_TEMPLATE, SYSTEM_PROMPT
    print("✅ Extraction prompts import successful")
except ImportError as e:
    print(f"❌ Extraction prompts import failed: {e}")

print("\nAll imports tested!")
