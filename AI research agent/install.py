#!/usr/bin/env python3
"""
Simple installation script for AI Research & Decision Assistant.
"""
import subprocess
import sys
import os


def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False


def setup_env_file():
    """Setup environment file."""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("📝 Creating .env file from template...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ .env file created")
        else:
            print("⚠️  .env.example not found")
    else:
        print("✅ .env file already exists")


def main():
    """Main installation function."""
    print("🚀 AI Research & Decision Assistant - Installation")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup environment file
    setup_env_file()
    
    print("\n🎉 Installation complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys:")
    print("   - GROQ_API_KEY (required)")
    print("   - LANGCHAIN_API_KEY (optional, for LangSmith tracing)")
    print("2. Run: python main.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)