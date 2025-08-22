#!/usr/bin/env python3
"""
Government Helper Application Entry Point - Gemini AI Only
"""
from dotenv import load_dotenv
from app import main
import logging

# Load environment variables first
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("🏛️ Starting Government Helper Application with Gemini AI...")
    print("📱 Visit http://localhost:5000 to use the application")
    print("🤖 Powered by Google Gemini AI")
    main()
