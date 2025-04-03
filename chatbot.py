import json
import random
import re
import logging
import nltk
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

logger = logging.getLogger('mental_health_chatbot')

class MentalHealthChatbot:
    def __init__(self, intents_file):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = self.load_intents(intents_file)
        self.crisis_patterns = [
            r"(?i)(?:want|feel like|thinking about|thoughts of|considering)\s+(?:suicide|killing myself|taking my life|ending my life|dying)",
            r"(?i)(?:suicidal|self-harm|hurt\s+(?:myself|my\s+body))",
            r"(?i)(?:don't|do not)\s+(?:want|feel like)\s+(?:living|being alive|continuing|going on)",
            r"(?i)(?:plan|planning)\s+(?:to|on)\s+(?:suicide|kill|hurt|harm)",
            r"(?i)life\s+(?:isn't|is not|isn't|isnt)\s+worth\s+(?:living|it)"
        ]
        
    def load_intents(self, intents_file):
        try:
            with open(intents_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading intents file: {e}")
            # Provide basic fallback intents
            return {
                "intents": [
                    {
                        "tag": "greeting",
                        "patterns": ["hi", "hello", "hey"],
                        "responses": ["Hello! How are you feeling today?", "Hi there! How can I support you today?"]
                    },
                    {
                        "tag": "goodbye",
                        "patterns": ["bye", "goodbye", "see you"],
                        "responses": ["Take care of yourself!", "I'm here if you need to talk again."]
                    },
                    {
                        "tag": "fallback",
                        "patterns": [],
                        "responses": ["I'm here to listen. Could you tell me more about how you're feeling?", 
                                      "I want to understand better. Can you share more about what's going on?"]
                    }
                ]
            }
    
    def preprocess(self, text):
        # Tokenize and lemmatize the text
        tokens = nltk.word_tokenize(text.lower())
        return [self.lemmatizer.lemmatize(word) for word in tokens]
    
    def detect_crisis(self, message):
        for pattern in self.crisis_patterns:
            if re.search(pattern, message):
                return True
        return False
    
    def find_intent(self, processed_message):
        # Simple keyword matching for intent detection
        best_match = {"tag": "fallback", "score": 0}
        
        message_set = set(processed_message)
        
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                pattern_tokens = self.preprocess(pattern)
                pattern_set = set(pattern_tokens)
                
                # Calculate simple overlap score
                if message_set and pattern_set:
                    overlap = len(message_set.intersection(pattern_set))
                    score = overlap / max(len(message_set), len(pattern_set))
                    
                    if score > best_match["score"]:
                        best_match = {"tag": intent["tag"], "score": score}
        
        return best_match["tag"] if best_match["score"] > 0.2 else "fallback"
    
    def get_response(self, intent_tag):
        for intent in self.intents["intents"]:
            if intent["tag"] == intent_tag:
                return random.choice(intent["responses"])
        
        # Fallback responses
        fallback_responses = [
            "I'm here to listen. Could you tell me more about how you're feeling?",
            "I want to understand better. Can you share more about what's going on?"
        ]
        return random.choice(fallback_responses)
    
    def get_crisis_response(self):
        crisis_responses = [
            "I'm concerned about what you're sharing. If you're thinking about harming yourself, please call the 988 Suicide & Crisis Lifeline at 988, or text HOME to 741741 to reach the Crisis Text Line. Would you like me to provide more resources?",
            "It sounds like you're going through a really difficult time. Please reach out to the 988 Suicide & Crisis Lifeline by calling or texting 988. They have trained counselors available 24/7. Your life matters.",
            "I'm really concerned about your safety right now. Please call 988 immediately to speak with a trained counselor who can help. Would you like me to share additional mental health resources?"
        ]
        return random.choice(crisis_responses)
    
    def chat(self, message, conversation_history=None):
        if not message.strip():
            return {"text": "I'm here when you're ready to talk.", "is_crisis": False}
        
        # Check for crisis language
        is_crisis = self.detect_crisis(message)
        if is_crisis:
            return {"text": self.get_crisis_response(), "is_crisis": True}
        
        # Process the message
        processed_message = self.preprocess(message)
        
        # Find matching intent
        intent_tag = self.find_intent(processed_message)
        
        # Get response based on intent
        response = self.get_response(intent_tag)
        
        return {"text": response, "is_crisis": False}