# demo_incremental.py

#!/usr/bin/env python3
# Demo script để test incremental processing

import asyncio
import os
import sys
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.rag_processor import MeetingProcessor
from core.config import DOCUMENTS_DIR, OUTPUT_DIR

async def demo_incremental_processing():
    """Demo incremental processing functionality"""
    print("🚀 Demo Incremental Processing")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("💡 Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize processor
    try:
        processor = MeetingProcessor()
        print("✅ Processor initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize processor: {e}")
        return
    
    # Ensure directories exist
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"📁 Documents directory: {DOCUMENTS_DIR}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    # Check current status
    print("\n📊 Current Processing Status:")
    status = processor.get_processing_status()
    print(f"   - Total files: {status['total_files']}")
    print(f"   - Processed: {status['processed_files']}")
    print(f"   - Failed: {status['failed_files']}")
    print(f"   - Pending: {status['pending_files']}")
    
    # Show file details
    if status['files_detail']:
        print("\n📋 File Details:")
        for filename, detail in status['files_detail'].items():
            status_icon = "✅" if detail['status'] == 'processed' else "❌" if detail['status'] == 'failed' else "⏳"
            print(f"   {status_icon} {filename}: {detail['status']}")
            
            if detail['status'] == 'processed' and 'processed_at' in detail:
                print(f"      Processed at: {detail['processed_at']}")
            elif detail['status'] == 'failed' and 'error' in detail:
                print(f"      Error: {detail['error']}")
    
    # Run incremental processing
    print(f"\n🔄 Running incremental processing...")
    print("-" * 30)
    
    try:
        result = await processor.process_incremental(DOCUMENTS_DIR)
        
        print(f"\n📊 Processing Results:")
        print(f"   - Status: {result['status']}")
        
        if result['status'] == 'no_changes':
            print(f"   - Message: {result['message']}")
        else:
            print(f"   - Total files processed: {result['total_files']}")
            print(f"   - Successful: {result['successful_files']}")
            print(f"   - Failed: {result['failed_files']}")
            
            # Show scan report
            scan_report = result['scan_report']
            print(f"\n🔍 Scan Report:")
            print(f"   - Files to process: {scan_report['files_to_process']}")
            print(f"   - Files unchanged: {scan_report['files_unchanged']}")
            print(f"   - Files removed: {scan_report['files_removed']}")
            
            # Show files that were processed
            if scan_report['files_to_process_list']:
                print(f"\n📄 Files Processed:")
                for file_info in scan_report['files_to_process_list']:
                    print(f"   - {file_info['name']} ({file_info['size']:,} bytes)")
            
            # Show files that were unchanged
            if scan_report['files_unchanged_list']:
                print(f"\n✅ Files Unchanged:")
                for file_info in scan_report['files_unchanged_list']:
                    print(f"   - {file_info['name']} ({file_info['size']:,} bytes)")
    
    except Exception as e:
        print(f"❌ Error during incremental processing: {e}")
        return
    
    # Show final status
    print(f"\n📊 Final Status:")
    final_status = processor.get_processing_status()
    print(f"   - Total files: {final_status['total_files']}")
    print(f"   - Processed: {final_status['processed_files']}")
    print(f"   - Failed: {final_status['failed_files']}")
    print(f"   - Pending: {final_status['pending_files']}")
    
    # Show output files
    print(f"\n📁 Output Files:")
    if os.path.exists(OUTPUT_DIR):
        output_files = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]
        if output_files:
            for filename in sorted(output_files):
                file_path = os.path.join(OUTPUT_DIR, filename)
                size = os.path.getsize(file_path)
                modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"   - {filename} ({size:,} bytes, {modified})")
        else:
            print("   No output files found")
    else:
        print("   Output directory does not exist")
    
    print(f"\n🎉 Demo completed!")
    print(f"💡 To run the web interface: streamlit run test_interface.py")

if __name__ == "__main__":
    try:
        asyncio.run(demo_incremental_processing())
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
