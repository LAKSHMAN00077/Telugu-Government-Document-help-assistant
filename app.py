from flask import Flask, request, jsonify, render_template_string
import logging
from config import Config
from response_handler import ResponseHandler
from templates import HTMLTemplate

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GovernmentHelperApp:
    """Main Flask application class with enhanced error handling"""

    def __init__(self):
        self.app = Flask(__name__)
        self.response_handler = ResponseHandler()
        self._setup_routes()
        
        # Log startup status
        status = self.response_handler.ai_client.get_status()
        logger.info(f"🚀 Application started with AI status: {status}")

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def home():
            """Serve the main interface"""
            try:
                return render_template_string(HTMLTemplate.MAIN_TEMPLATE)
            except Exception as e:
                logger.error(f"Error serving home page: {e}")
                return f"Error loading application: {e}", 500

        @self.app.route('/chat', methods=['POST'])
        def chat():
            """Handle chat messages with comprehensive error handling"""
            try:
                # Validate request
                if not request.is_json:
                    return jsonify({
                        'error': 'Content-Type must be application/json',
                        'status': 'error'
                    }), 400

                data = request.get_json()
                if not data:
                    return jsonify({
                        'error': 'Invalid JSON data',
                        'status': 'error'
                    }), 400

                user_message = data.get('message', '').strip()
                
                if not user_message:
                    return jsonify({
                        'error': 'దయచేసి మీ ప్రశ్న టైప్ చేయండి (Please type your question)',
                        'status': 'error'
                    }), 400

                # Validate message length
                if len(user_message) > 500:
                    return jsonify({
                        'error': 'ప్రశ్న చాలా పెద్దది. దయచేసి చిన్నగా అడగండి (Question too long. Please keep it shorter)',
                        'status': 'error'
                    }), 400

                # Get response from handler
                result = self.response_handler.get_response(user_message)
                
                # Return success response
                return jsonify(result)

            except Exception as e:
                logger.error(f"Error in chat endpoint: {e}")
                return jsonify({
                    'error': 'దయచేసి మళ్ళీ ప్రయత్నించండి (Please try again)',
                    'status': 'error',
                    'details': str(e) if Config.DEBUG else None
                }), 500

        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            try:
                status = self.response_handler.ai_client.get_status()
                return jsonify({
                    'status': 'healthy',
                    'timestamp': status,
                    'ai_available': status['available'],
                    'model': status['model'],
                    'version': '3.0.0'
                })
            except Exception as e:
                logger.error(f"Error in health check: {e}")
                return jsonify({
                    'status': 'unhealthy',
                    'error': str(e)
                }), 500

        @self.app.route('/status')
        def get_status():
            """Get detailed application status"""
            try:
                ai_status = self.response_handler.ai_client.get_status()
                return jsonify({
                    'application': 'Government Helper',
                    'version': '3.0.0',
                    'ai_client': ai_status,
                    'endpoints': {
                        'chat': '/chat',
                        'health': '/health',
                        'status': '/status'
                    }
                })
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                return jsonify({'error': str(e)}), 500

    def run(self):
        """Run the Flask application"""
        logger.info(f"🌐 Starting server on {Config.HOST}:{Config.PORT}")
        logger.info("📱 Visit http://localhost:5000 to use the application")
        self.app.run(
            debug=Config.DEBUG,
            host=Config.HOST,
            port=Config.PORT
        )

def main():
    """Main entry point"""
    try:
        app = GovernmentHelperApp()
        app.run()
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main()
