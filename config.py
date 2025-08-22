import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the Government Helper AI Assistant"""
    
    # Gemini API settings
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = "gemini-1.5-flash"  # Fast and efficient model
    
    # App settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Generation settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    TOP_P = 0.9
    TOP_K = 40

    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True
