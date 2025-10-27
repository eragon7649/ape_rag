# run_incremental_processor.py

#!/usr/bin/env python3
# Main entry point for the RAG Meeting Processor with Incremental Processing

import sys
import os
import asyncio

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.rag_processor import MeetingProcessor
from core.output_formatter import OutputFormatter
from core.config import DOCUMENTS_DIR, OUTPUT_DIR

async def run_incremental_processing():
    """Main incremental processing pipeline"""
    print("🚀 Starting RAG Meeting Processor with Incremental Processing...")
    
    if not os.path.exists(DOCUMENTS_DIR):
        print(f"❌ Input directory does not exist: {DOCUMENTS_DIR}")
        print("Please create the 'documents' directory and place meeting files there.")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize processor and formatter
    try:
        processor = MeetingProcessor()
        formatter = OutputFormatter(OUTPUT_DIR)
        print("✅ Processor and formatter initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize processor: {e}")
        return
    
    # Run incremental processing
    try:
        result = await processor.process_incremental(DOCUMENTS_DIR)
        
        if result["status"] == "no_changes":
            print(f"✅ {result['message']}")
            return
        
        # Generate outputs for successfully processed files
        processing_results = result["processing_results"]
        successful_results = [r for r in processing_results if r["success"]]
        
        if successful_results:
            print(f"\n--- Generating Outputs for {len(successful_results)} files ---")
            
            for result_item in successful_results:
                file_path = result_item["file_path"]
                filename = os.path.basename(file_path)
                file_base_name = os.path.splitext(filename)[0]
                extracted_data = result_item["result"]
                
                print(f"📄 Generating outputs for: {filename}")
                
                # Generate simplified outputs (only 2 files)
                try:
                    # 1. File tóm tắt
                    summary_path = formatter.create_summary_txt(extracted_data, file_base_name)
                    
                    # 2. File nội dung đầy đủ  
                    full_content_path = formatter.create_full_content_txt(extracted_data, file_base_name)
                    
                    print(f"✅ Simplified outputs generated for: {filename}")
                    print(f"📄 Summary: {summary_path}")
                    print(f"📄 Full content: {full_content_path}")
                    
                except Exception as e:
                    print(f"⚠️ Error generating outputs for {filename}: {e}")
        
        # Print final summary
        print(f"\n🎉 Incremental processing completed!")
        print(f"📊 Summary:")
        print(f"   - Total files processed: {result['total_files']}")
        print(f"   - Successful: {result['successful_files']}")
        print(f"   - Failed: {result['failed_files']}")
        print(f"📁 Check the '{OUTPUT_DIR}' directory for results")
        
    except Exception as e:
        print(f"❌ Error during incremental processing: {e}")
        return

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Run the incremental processing pipeline
    try:
        asyncio.run(run_incremental_processing())
    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
