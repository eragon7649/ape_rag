#!/usr/bin/env python3
# Setup script for RAG Meeting Processor

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["documents", "output", "rag_storage"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    print("✅ All directories created")

def check_environment():
    """Check environment variables"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("⚠️  OPENAI_API_KEY not set or using default value")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your_actual_api_key_here'")
        return False
    else:
        print("✅ OPENAI_API_KEY is configured")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up RAG Meeting Processor...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Check environment
    env_ok = check_environment()
    
    print("\n" + "=" * 50)
    if env_ok:
        print("🎉 Setup completed successfully!")
        print("\nTo run the processor:")
        print("  python run_processor.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("Please configure your OpenAI API key before running the processor")
    
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
