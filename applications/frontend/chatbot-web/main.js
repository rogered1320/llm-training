// This file contains the JavaScript code that handles user interactions for the chatbot interface.

const chatUrl = "";

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatDisplay = document.getElementById('chat-display');

    // Configure marked with basic options
    marked.setOptions({
        breaks: true, // Convert line breaks to <br>
        gfm: true     // GitHub Flavored Markdown
    });

    function addMessage(text, sender = 'user') {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble');
        
        // If it's from the bot, process Markdown and show typing effect
        if (sender === 'bot') {
            messageElement.appendChild(messageBubble);
            chatDisplay.appendChild(messageElement);
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
            
            // Typing effect for bot messages
            typeText(messageBubble, text);
        } else {
            messageBubble.textContent = text;
            messageElement.appendChild(messageBubble);
            chatDisplay.appendChild(messageElement);
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        }
    }

    function typeText(element, text) {
        let index = 0;
        let currentText = '';
        
        function typeCharacter() {
            if (index < text.length) {
                currentText += text[index];
                
                // Process markdown of current text without cursor
                element.innerHTML = marked.parse(currentText);
                
                // Ensure all links open in a new tab
                const links = element.querySelectorAll('a');
                links.forEach(link => {
                    link.setAttribute('target', '_blank');
                    link.setAttribute('rel', 'noopener noreferrer');
                });
                
                // Auto scroll
                chatDisplay.scrollTop = chatDisplay.scrollHeight;
                
                index++;
                
                // Variable speed: faster for spaces and punctuation
                let delay = 20; // base speed increased (was 50ms)
                if (text[index - 1] === ' ') delay = 5;  // much faster for spaces (was 20ms)
                if (text[index - 1] === '.' || text[index - 1] === '!' || text[index - 1] === '?') delay = 150; // reduced pause (was 300ms)
                if (text[index - 1] === ',') delay = 75; // reduced pause (was 150ms)
                
                setTimeout(typeCharacter, delay);
            }
        }
        
        typeCharacter();
    }

    function showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.classList.add('typing-indicator');
        typingElement.id = 'typing-indicator';
        
        const typingBubble = document.createElement('div');
        typingBubble.classList.add('typing-bubble');
        
        const typingDots = document.createElement('div');
        typingDots.classList.add('typing-dots');
        
        // Create three animated dots
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingDots.appendChild(dot);
        }
        
        typingBubble.appendChild(typingDots);
        typingElement.appendChild(typingBubble);
        chatDisplay.appendChild(typingElement);
        chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            messageInput.disabled = true;
            sendButton.disabled = true;

            // Show typing indicator
            setTimeout(() => {
                showTypingIndicator();
            }, 500);

            // Make the real API call with POST
            fetch(chatUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message
                })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json(); // Change to .json() to parse JSON
                })
                .then(data => {
                    removeTypingIndicator();
                    // Extract message from JSON response
                    const botMessage = data.message || 'Sorry, I did not receive a valid response.';
                    addMessage(botMessage, 'bot');
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    messageInput.focus();
                    updateSendButton();
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                    removeTypingIndicator();
                    addMessage('Sorry, an error occurred while processing your message. Please try again.', 'bot');
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    messageInput.focus();
                    updateSendButton();
                });
        }
    }

    function updateSendButton() {
        const isInputEmpty = messageInput.value.trim() === '';
        sendButton.disabled = isInputEmpty;
    }

    // Event listener for send button
    sendButton.addEventListener('click', sendMessage);

    // Event listener to detect input changes
    messageInput.addEventListener('input', updateSendButton);

    // Event listener to send message with Enter
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !sendButton.disabled) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Add welcome message with typing indicator
    setTimeout(() => {
        showTypingIndicator();
        setTimeout(() => {
            removeTypingIndicator();
            addMessage('¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?', 'bot');
        }, 1500);
    }, 500);

    // Focus input when page loads
    messageInput.focus();
});