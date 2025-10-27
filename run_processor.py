#!/usr/bin/env python3
# Main entry point for the RAG Meeting Processor

import sys
import os
import asyncio

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.rag_processor import MeetingProcessor
from core.output_formatter import OutputFormatter
from core.config import DOCUMENTS_DIR, OUTPUT_DIR

async def run_processing_pipeline():
    """Main processing pipeline"""
    print("🚀 Starting RAG Meeting Processor...")
    
    if not os.path.exists(DOCUMENTS_DIR):
        print(f"❌ Input directory does not exist: {DOCUMENTS_DIR}")
        print("Please create the 'documents' directory and place meeting files there.")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if there are any files to process
    files_to_process = [f for f in os.listdir(DOCUMENTS_DIR) 
                       if not f.startswith('.') and f != 'README.md']
    
    if not files_to_process:
        print(f"📁 No files found in {DOCUMENTS_DIR}")
        print("Please add meeting documents (PDF, JPG, DOCX) to the documents folder.")
        return
    
    print(f"📋 Found {len(files_to_process)} files to process")
    
    # Initialize processor and formatter
    try:
        processor = MeetingProcessor()
        formatter = OutputFormatter(OUTPUT_DIR)
        print("✅ Processor and formatter initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize processor: {e}")
        return
    
    # Process each file
    for file_name in files_to_process:
        file_path = os.path.join(DOCUMENTS_DIR, file_name)
        
        print(f"\n{'='*50}")
        print(f"🚀 Processing: {file_name}")
        
        try:
            # Process document and extract data
            extracted_data = await processor.process_document_and_extract(file_path)
            
            if extracted_data.get("error"):
                print(f"🛑 Processing failed for {file_name}: {extracted_data['error']}")
                continue
                
            print("✅ Document processed successfully")
            print(f"📊 Extracted data: {extracted_data.get('meeting_title', 'Unknown')}")
            
            # Generate simplified outputs (only 2 files)
            print("\n--- Generating Simplified Outputs ---")
            
            file_base_name = os.path.splitext(file_name)[0]
            
            # 1. File tóm tắt
            summary_path = formatter.create_summary_txt(extracted_data, file_base_name)
            
            # 2. File nội dung đầy đủ  
            full_content_path = formatter.create_full_content_txt(extracted_data, file_base_name)
            
            print(f"✅ Processing completed for {file_name}")
            print(f"📄 Summary: {summary_path}")
            print(f"📄 Full content: {full_content_path}")
            
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
            continue
    
    print(f"\n🎉 Processing pipeline completed!")
    print(f"📁 Check the '{OUTPUT_DIR}' directory for results")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Run the processing pipeline
    try:
        asyncio.run(run_processing_pipeline())
    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
