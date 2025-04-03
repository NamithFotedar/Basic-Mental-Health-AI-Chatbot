import os
import uuid
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session
from chatbot import MentalHealthChatbot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('chatbot.log'), logging.StreamHandler()]
)
logger = logging.getLogger('mental_health_chatbot')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_for_sessions')

# Initialize the chatbot
chatbot = MentalHealthChatbot('intents.json')

# Store conversation history
conversation_histories = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=['GET', 'POST'])
def get_bot_response():
    if request.method == 'POST':
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id')
    else:
        user_message = request.args.get('msg', '')
        session_id = request.args.get('session_id')
    
    # Create or get session
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Initialize conversation history if needed
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    
    # Get response from chatbot
    response_data = chatbot.chat(user_message, conversation_histories[session_id])
    
    # Add to conversation history
    conversation_histories[session_id].append({
        'user': user_message,
        'bot': response_data.get('text', ''),
        'timestamp': datetime.now().isoformat()
    })
    
    # Clean up old sessions (in a real app, this would be done periodically)
    if len(conversation_histories) > 1000:
        oldest_session = min(conversation_histories.keys(), 
                           key=lambda k: conversation_histories[k][0]['timestamp'] if conversation_histories[k] else datetime.now().isoformat())
        del conversation_histories[oldest_session]
    
    # Return response with session ID
    return jsonify({
        'response': response_data.get('text', ''),
        'session_id': session_id,
        'is_crisis': response_data.get('is_crisis', False)
    })

@app.route("/feedback", methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = data.get('feedback')
    session_id = data.get('session_id')
    
    if feedback and session_id:
        logger.info(f"Feedback received for session {session_id}: {feedback}")
        # In a real implementation, you would store this feedback in a database
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Invalid feedback data'})

@app.route("/resources")
def mental_health_resources():
    return render_template("resources.html")

if __name__ == "__main__":
    app.run(debug=True)