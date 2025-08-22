import logging
from typing import Dict, Any
from ai_client import GeminiClient
from prompts import SystemPrompts

logger = logging.getLogger(__name__)

class ResponseHandler:
    """Handles generating responses using Gemini AI with enhanced error handling"""

    def __init__(self):
        self.ai_client = GeminiClient()

    def get_response(self, user_message: str) -> Dict[str, Any]:
        """Get response using Gemini AI with proper error handling"""
        logger.info(f"Processing user question: {user_message}")

        # Validate input
        if not user_message or len(user_message.strip()) == 0:
            return {
                'response': 'దయచేసి మీ ప్రశ్న టైప్ చేయండి (Please type your question)',
                'source': 'validation_error',
                'status': 'error'
            }

        # Check if AI client is available
        if not self.ai_client.is_available():
            return {
                'response': '''క్షమించండి, ప్రస్తుతం AI సేవ అందుబాటులో లేదు. దయచేసి Gemini API కీ సెటప్ చేసి మళ్ళీ ప్రయత్నించండి.

Sorry, AI service is currently unavailable. Please setup Gemini API key and try again.

మీరు ఈ విషయాలను స్వయంగా తనిఖీ చేయవచ్చు:
1. ఆధార్ కార్డ్: uidai.gov.in
2. పెన్షన్: nsap.nic.in  
3. ఆదాయ సర్టిఫికేట్: webland.ap.gov.in (AP) లేదా webland.telangana.gov.in (TS)''',
                'source': 'ai_unavailable',
                'status': 'error'
            }

        try:
            # Create optimized prompt for Gemini
            prompt = SystemPrompts.create_prompt(user_message)
            
            # Generate response using Gemini
            ai_response = self.ai_client.generate_response(prompt)
            
            if ai_response and len(ai_response.strip()) > 0:
                logger.info("✅ Gemini AI response generated successfully")
                return {
                    'response': ai_response,
                    'source': 'gemini_ai',
                    'status': 'success'
                }
            else:
                logger.warning("Gemini returned empty response")
                return {
                    'response': '''క్షమించండి, ప్రస్తుతం AI సమాధానం రాలేదు. దయచేసి మీ ప్రశ్నను మరొకసారి అడగండి.

Sorry, couldn't generate AI response. Please try asking your question again.

సాధారణ సహాయం కోసం:
• ఆధార్ కార్డ్ హెల్ప్లైన్: 1947
• ప్రభుత్వ సేవల పోర్టల్: ap.gov.in లేదా telangana.gov.in''',
                    'source': 'empty_response',
                    'status': 'warning'
                }
                
        except Exception as e:
            logger.error(f"Error in response generation: {e}")
            return {
                'response': '''క్షమించండి, ప్రస్తుతం సర్వర్ బిజీగా ఉంది. దయచేసి మళ్ళీ ప్రయత్నించండి.

Sorry, server is busy. Please try again.

తక్షణ సహాయం కోసం:
• ఆధార్ కేంద్రాలు: uidai.gov.in/contact-support
• ప్రభుత్వ హెల్ప్లైన్: 1100''',
                'source': 'server_error',
                'status': 'error'
            }
