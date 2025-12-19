#!/usr/bin/env python3
"""
Simple CLI runner for AI Research & Decision Assistant.
"""
import sys
import os

def main():
    """Run the AI Research Assistant with better error handling."""
    try:
        # Check if .env file exists
        if not os.path.exists('.env'):
            print("❌ .env file not found!")
            print("📝 Please create a .env file with your API keys:")
            print("   GROQ_API_KEY=your_groq_api_key_here")
            print("   LANGCHAIN_API_KEY=your_langsmith_api_key_here (optional)")
            print("\n💡 You can copy .env.example to .env and edit it")
            return 1
        
        # Import and run main application
        from main import main as run_main
        run_main()
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Please install requirements: pip install -r requirements.txt")
        return 1
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("🔧 Please check your setup and try again")
        return 1

if __name__ == "__main__":
    sys.exit(main())