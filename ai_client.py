import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from config import Config

logger = logging.getLogger(__name__)

class GeminiClient:
    """Handles Gemini 1.5 Flash model interactions with enhanced error handling"""

    def __init__(self):
        self.model = None
        self.model_name = Config.GEMINI_MODEL
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the Gemini client"""
        try:
            Config.validate_config()
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                self.model_name,
                generation_config=genai.types.GenerationConfig(
                    temperature=Config.TEMPERATURE,
                    top_p=Config.TOP_P,
                    top_k=Config.TOP_K,
                    max_output_tokens=Config.MAX_TOKENS,
                )
            )
            logger.info(f"✅ Successfully initialized Gemini client: {self.model_name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            self.model = None

    def is_available(self) -> bool:
        """Check if client is available"""
        return self.model is not None

    def generate_response(self, prompt: str) -> Optional[str]:
        """Generate response using Gemini 1.5 Flash with improved error handling"""
        if not self.model:
            logger.error("Gemini model not available")
            return None

        try:
            # Add safety check for prompt
            if not prompt or len(prompt.strip()) == 0:
                logger.error("Empty prompt provided")
                return None

            response = self.model.generate_content(prompt)
            
            if response and response.text:
                logger.info("✅ Gemini response generated successfully")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response")
                return None

        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get client status information"""
        return {
            'available': self.is_available(),
            'model': self.model_name,
            'type': 'gemini_1_5_flash',
            'api_key_set': bool(Config.GEMINI_API_KEY)
        }
