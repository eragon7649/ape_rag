#!/bin/bash
# run_commands.sh - Script để chạy các lệnh RAG Meeting Processor

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 RAG Meeting Processor - Command Runner${NC}"
echo "================================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}💡 Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "YOUR_OPENAI_API_KEY_HERE" ]; then
    echo -e "${RED}❌ OPENAI_API_KEY not set!${NC}"
    echo -e "${YELLOW}💡 Please set your API key:${NC}"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo -e "${YELLOW}Or run this script with API key:${NC}"
    echo "   OPENAI_API_KEY='your-key' ./run_commands.sh"
    exit 1
fi

echo -e "${GREEN}✅ API Key found: ${OPENAI_API_KEY:0:10}...${NC}"

# Function to show menu
show_menu() {
    echo ""
    echo -e "${BLUE}📋 Available Commands:${NC}"
    echo "1. 🌐 Run Web Interface (Streamlit)"
    echo "2. 🔄 Run Incremental Processing"
    echo "3. 🧪 Run Demo Script"
    echo "4. 🔧 Run Diagnostic Test"
    echo "5. 📊 Check Processing Status"
    echo "6. 🗑️ Reset File Tracking"
    echo "7. ❌ Exit"
    echo ""
}

# Function to run web interface
run_web_interface() {
    echo -e "${YELLOW}🌐 Starting Streamlit web interface...${NC}"
    echo -e "${GREEN}✅ Web interface will be available at: http://localhost:8501${NC}"
    echo -e "${YELLOW}💡 Press Ctrl+C to stop${NC}"
    streamlit run test_interface.py --server.port 8501
}

# Function to run incremental processing
run_incremental() {
    echo -e "${YELLOW}🔄 Running incremental processing...${NC}"
    python run_incremental_processor.py
}

# Function to run demo
run_demo() {
    echo -e "${YELLOW}🧪 Running demo script...${NC}"
    python demo_incremental.py
}

# Function to run diagnostic test
run_diagnostic() {
    echo -e "${YELLOW}🔧 Running diagnostic test...${NC}"
    python test_fix.py
}

# Function to check status
check_status() {
    echo -e "${YELLOW}📊 Checking processing status...${NC}"
    python -c "
import sys
sys.path.insert(0, 'src')
from core.rag_processor import MeetingProcessor
processor = MeetingProcessor()
status = processor.get_processing_status()
print(f'Total files: {status[\"total_files\"]}')
print(f'Processed: {status[\"processed_files\"]}')
print(f'Failed: {status[\"failed_files\"]}')
print(f'Pending: {status[\"pending_files\"]}')
"
}

# Function to reset tracking
reset_tracking() {
    echo -e "${YELLOW}🗑️ Resetting file tracking...${NC}"
    python -c "
import sys
sys.path.insert(0, 'src')
from core.rag_processor import MeetingProcessor
processor = MeetingProcessor()
processor.reset_file_tracking()
print('✅ File tracking reset successfully')
"
}

# Main menu loop
while true; do
    show_menu
    read -p "Choose an option (1-7): " choice
    
    case $choice in
        1)
            run_web_interface
            ;;
        2)
            run_incremental
            ;;
        3)
            run_demo
            ;;
        4)
            run_diagnostic
            ;;
        5)
            check_status
            ;;
        6)
            reset_tracking
            ;;
        7)
            echo -e "${GREEN}👋 Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid option. Please choose 1-7.${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
