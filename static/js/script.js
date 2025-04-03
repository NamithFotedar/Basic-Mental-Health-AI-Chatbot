document.addEventListener('DOMContentLoaded', function () {
    // DOM elements
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-btn');
    const resourcesButton = document.getElementById('resources-btn');
    const helpfulButton = document.getElementById('helpful-btn');
    const notHelpfulButton = document.getElementById('not-helpful-btn');
    const feedbackModal = document.getElementById('feedback-modal');
    const closeModal = document.querySelector('.close');
    const submitFeedback = document.getElementById('submit-feedback');
    const feedbackText = document.getElementById('feedback-text');

    // Session ID
    let sessionId = localStorage.getItem('chatbot_session_id') || null;

    // Function to add message to chat
    function addMessage(message, isUser = false, isCrisis = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        if (isCrisis) {
            messageDiv.classList.add('crisis-message');
        }

        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to get bot response
    async function getBotResponse(message) {
        try {
            const response = await fetch('/get', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });

            const data = await response.json();

            // Store session ID
            if (data.session_id) {
                sessionId = data.session_id;
                localStorage.setItem('chatbot_session_id', sessionId);
            }

            // Add bot message
            addMessage(data.response, false, data.is_crisis);

        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I had trouble processing your message. Please try again.', false);
        }
    }

    // Send message
    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Add user message to chat
            addMessage(message, true);

            // Clear input
            userInput.value = '';

            // Get bot response
            getBotResponse(message);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    resourcesButton.addEventListener('click', function () {
        window.location.href = '/resources';
    });

    // Feedback handling
    function openFeedbackModal(isHelpful) {
        feedbackModal.style.display = 'block';
        feedbackText.dataset.helpful = isHelpful;
    }

    helpfulButton.addEventListener('click', function () {
        openFeedbackModal(true);
    });

    notHelpfulButton.addEventListener('click', function () {
        openFeedbackModal(false);
    });

    closeModal.addEventListener('click', function () {
        feedbackModal.style.display = 'none';
    });

    window.addEventListener('click', function (e) {
        if (e.target === feedbackModal) {
            feedbackModal.style.display = 'none';
        }
    });

    submitFeedback.addEventListener('click', async function () {
        const feedback = feedbackText.value.trim();
        const isHelpful = feedbackText.dataset.helpful === 'true';

        if (feedback && sessionId) {
            try {
                const response = await fetch('/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        feedback: feedback,
                        is_helpful: isHelpful,
                        session_id: sessionId
                    })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    feedbackModal.style.display = 'none';
                    feedbackText.value = '';
                    alert('Thank you for your feedback!');
                }

            } catch (error) {
                console.error('Error submitting feedback:', error);
                alert('Sorry, there was a problem submitting your feedback.');
            }
        }
    });
});