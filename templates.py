class HTMLTemplate:
    """HTML templates for the application"""

    MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Government Helper - మీ సర్కారీ పత్రాల కోసం AI సహాయకుడు</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 15px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: white;
            border: 1px solid #dee2e6;
            margin-right: auto;
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #dee2e6;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
        }
        
        #userInput {
            flex: 1;
            padding: 15px;
            border: 2px solid #dee2e6;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        #userInput:focus {
            border-color: #007bff;
        }
        
        #sendButton {
            padding: 15px 25px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        
        #sendButton:hover {
            background: #0056b3;
        }
        
        #sendButton:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #6c757d;
        }
        
        .status {
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ Government Helper</h1>
            <p>సర్కారీ పత్రాలు మరియు ప్రక్రియల గురించి ఏదైనా అడగండి</p>
            <p>Ask me anything about government documents and procedures</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                <strong>🤖 సర్కారీ సహాయకుడు:</strong><br>
                నమస్కారం! నేను మీ సర్కారీ పత్రాల సహాయకుడిని. మీకు ఏవైనా ప్రశ్నలు ఉంటే అడగండి:<br><br>
                • ఆధార్ కార్డ్ ఎలా చేయాలి?<br>
                • పెన్షన్ దరఖాస్తు ఎలా చేయాలి?<br>
                • ఆదాయ సర్టిఫికేట్ కోసం ఏ పత్రాలు కావాలి?<br>
                • జనన సర్టిఫికేట్ ఎలా తీసుకోవాలి?
            </div>
        </div>
        
        <div class="loading" id="loading">
            <p>⏳ దయచేసి వేచి ఉండండి... AI సమాధానం తయారు చేస్తోంది</p>
        </div>
        
        <div class="input-container">
            <div class="input-group">
                <input 
                    type="text" 
                    id="userInput" 
                    placeholder="మీ ప్రశ్న ఇక్కడ టైప్ చేయండి... (Type your question here...)"
                    maxlength="500"
                >
                <button id="sendButton">Send 📤</button>
            </div>
            <div class="status" id="status">
                ✅ AI Ready - Powered by Gemini
            </div>
        </div>
    </div>

    <script>
        // Fixed JavaScript - No regex issues
        class ChatApp {
            constructor() {
                this.chatContainer = document.getElementById('chatContainer');
                this.userInput = document.getElementById('userInput');
                this.sendButton = document.getElementById('sendButton');
                this.loading = document.getElementById('loading');
                this.status = document.getElementById('status');
                
                this.init();
            }
            
            init() {
                // Event listeners
                this.sendButton.addEventListener('click', () => this.sendMessage());
                this.userInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.sendMessage();
                    }
                });
                
                // Focus on input
                this.userInput.focus();
            }
            
            async sendMessage() {
                const message = this.userInput.value.trim();
                
                if (!message) {
                    this.showStatus('దయచేసి మీ ప్రశ్న టైప్ చేయండి', 'error');
                    return;
                }
                
                // Show user message
                this.addMessage(message, 'user');
                this.userInput.value = '';
                
                // Show loading
                this.setLoading(true);
                this.showStatus('AI సమాధానం తయారు చేస్తోంది...', 'loading');
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    // Show AI response
                    this.addMessage(data.response, 'ai');
                    this.showStatus('✅ సమాధానం పూర్తయింది', 'success');
                    
                } catch (error) {
                    console.error('Error:', error);
                    this.addMessage(
                        'క్షమించండి, ప్రస్తుతం సర్వర్ బిజీగా ఉంది. దయచేసి మళ్ళీ ప్రయత్నించండి।\\n\\nSorry, the server is currently busy. Please try again.',
                        'ai'
                    );
                    this.showStatus('❌ Error: ' + error.message, 'error');
                } finally {
                    this.setLoading(false);
                }
            }
            
            addMessage(text, type) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                
                if (type === 'user') {
                    messageDiv.innerHTML = `<strong>👤 You:</strong><br>${this.escapeHtml(text)}`;
                } else {
                    messageDiv.innerHTML = `<strong>🤖 సర్కారీ సహాయకుడు:</strong><br>${this.formatResponse(text)}`;
                }
                
                this.chatContainer.appendChild(messageDiv);
                this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
            }
            
            formatResponse(text) {
                // Simple text formatting - NO REGEX
                return this.escapeHtml(text)
                    .replace(/\\n/g, '<br>')
                    .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/\\*(.+?)\\*/g, '<em>$1</em>');
            }
            
            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            setLoading(show) {
                this.loading.style.display = show ? 'block' : 'none';
                this.sendButton.disabled = show;
                this.userInput.disabled = show;
            }
            
            showStatus(message, type = 'info') {
                this.status.textContent = message;
                this.status.style.color = type === 'error' ? '#dc3545' : 
                                         type === 'success' ? '#28a745' : 
                                         type === 'loading' ? '#ffc107' : '#6c757d';
            }
        }
        
        // Initialize app when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            new ChatApp();
        });
    </script>
</body>
</html>
    """
