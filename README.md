# Mental Health Support Chatbot

A supportive AI chatbot designed to provide mental health resources and emotional support while directing users to professional resources when needed.

## Overview

This Mental Health Support Chatbot is a Flask-based web application that uses natural language processing to engage with users about their mental health concerns. The chatbot provides supportive responses, coping strategies, and can detect crisis language to offer appropriate resources.

## Features

- **Conversational Support**: Engages with users about various mental health topics including anxiety, depression, sleep issues, and more
- **Crisis Detection**: Monitors conversations for concerning language and provides immediate crisis resources
- **Conversation History**: Maintains session-based conversation history for context
- **Feedback System**: Allows users to provide feedback on the helpfulness of conversations
- **Resource Directory**: Dedicated page with mental health resources including hotlines, professional services, and self-help tools

## Technology Stack

- **Backend**: Python, Flask
- **NLP Processing**: NLTK (Natural Language Toolkit)
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: In-memory (for development; should be replaced with a database for production)

## Project Structure

```
mental-health-chatbot/
├── app.py                 # Main Flask application
├── chatbot.py             # Chatbot logic and NLP processing
├── intents.json           # Response patterns and templates
├── static/
│   ├── css/
│   │   └── style.css      # Styling for the application
│   └── js/
│       └── script.js      # Frontend JavaScript functionality
├── templates/
│   ├── index.html         # Main chat interface
│   └── resources.html     # Mental health resources page
└── chatbot.log            # Application logs
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mental-health-chatbot.git
   cd mental-health-chatbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install flask nltk
   ```

4. Download required NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('wordnet')
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Development

### Adding New Intents

To expand the chatbot's capabilities, add new patterns and responses to the `intents.json` file:

```json
{
  "tag": "new_topic",
  "patterns": [
    "example question 1",
    "example question 2"
  ],
  "responses": [
    "Example response 1",
    "Example response 2"
  ]
}
```

### Improving Crisis Detection

The crisis detection patterns can be expanded in `chatbot.py` by adding new regex patterns to the `crisis_patterns` list.

## Important Notes

- **Not a Replacement for Professional Help**: This chatbot is designed as a supportive tool and should not replace professional mental health services.
- **Development Mode**: The current configuration uses Flask's development server, which is not suitable for production.
- **Data Privacy**: The application currently stores conversation history in memory. For a production environment, implement proper data security measures.

## Future Improvements

- Database integration for persistent storage of anonymized conversations and feedback
- Improved NLP with machine learning for better understanding of user concerns
- User accounts for those who want to maintain a history of their conversations
- Integration with telehealth services for immediate professional support

## Disclaimer

This chatbot is not a substitute for professional mental health services. In case of emergency, users should contact their local emergency services or crisis hotlines such as the 988 Suicide & Crisis Lifeline.

## Contact

fotedarnamith@gmail.com
