#!/usr/bin/env python3
"""
Simple test script to verify basic functionality
"""

import os
import sys
import json

def test_basic_functionality():
    """Test basic file operations and directory structure"""
    print("🧪 Testing Basic Functionality")
    print("=" * 40)
    
    # Test directory creation
    test_dirs = ["documents", "output", "rag_storage"]
    for dir_name in test_dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Directory {dir_name}/ created/verified")
    
    # Test file operations
    test_file = "output/test_output.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Test output file created successfully!")
    print(f"✅ Test file created: {test_file}")
    
    # Test JSON operations
    test_data = {
        "meeting_title": "Test Meeting",
        "date": "2024-01-01",
        "participants": ["John Doe", "Jane Smith"],
        "summary": "This is a test meeting summary",
        "decisions": [
            {
                "decision_id": 1,
                "description": "Test decision",
                "responsible_person": "John Doe",
                "due_date": "2024-01-15"
            }
        ],
        "action_items_count": 1
    }
    
    json_file = "output/test_data.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON file created: {json_file}")
    
    # Test reading back
    with open(json_file, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    print(f"✅ JSON file read successfully: {loaded_data['meeting_title']}")
    
    print("\n🎉 Basic functionality test completed successfully!")
    print("The system is ready for RAG processing setup.")

if __name__ == "__main__":
    test_basic_functionality()
