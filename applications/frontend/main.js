// This file contains the JavaScript code that handles user interactions for the chatbot interface.

const chatUrl = "";

// Generar UUID v4
function generateUUIDv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Generar sessionId único al cargar la página
let sessionId = generateUUIDv4();

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatDisplay = document.getElementById('chat-display');
    const charCounter = document.getElementById('charCounter');
    const resetButton = document.getElementById('resetButton');
    const maxLength = 500;

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
        if (message && !sendButton.disabled) {
            addMessage(message, 'user');
            messageInput.value = '';
            messageInput.disabled = true;
            sendButton.disabled = true;

            // En móviles, enfocar el input puede causar problemas con el scroll
            if (window.innerWidth > 768) {
                messageInput.blur();
            }

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
                    question: message,
                    sessionId: sessionId
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
                    
                    // Solo hacer focus automático en desktop
                    if (window.innerWidth > 768) {
                        messageInput.focus();
                    }
                    updateSendButton();
                    updateCharCounter();
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                    removeTypingIndicator();
                    addMessage('Sorry, an error occurred while processing your message. Please try again.', 'bot');
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    
                    // Solo hacer focus automático en desktop
                    if (window.innerWidth > 768) {
                        messageInput.focus();
                    }
                    updateSendButton();
                    updateCharCounter();
                });
        }
    }

    function updateSendButton() {
        const isInputEmpty = messageInput.value.trim() === '';
        sendButton.disabled = isInputEmpty;
    }

    function updateCharCounter() {
        const currentLength = messageInput.value.length;
        charCounter.textContent = `${currentLength}/${maxLength}`;
        
        // Cambiar color según la proximidad al límite
        charCounter.classList.remove('warning', 'limit');
        if (currentLength >= maxLength) {
            charCounter.classList.add('limit');
        } else if (currentLength >= maxLength * 0.8) { // 80% del límite
            charCounter.classList.add('warning');
        }
    }

    function resetChat() {
        // Generar nuevo sessionId
        sessionId = generateUUIDv4();
        
        // Limpiar el área de mensajes
        chatDisplay.innerHTML = '';
        
        // Limpiar y resetear el input
        messageInput.value = '';
        messageInput.disabled = false;
        sendButton.disabled = true;
        
        // Actualizar contador
        updateCharCounter();
        
        // Mostrar nuevo sessionId en consola
        console.log('Chat reseteado. Nuevo Session ID:', sessionId);
        
        // Agregar mensaje de bienvenida después de un breve delay
        setTimeout(() => {
            showTypingIndicator();
            setTimeout(() => {
                removeTypingIndicator();
                addMessage('¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?', 'bot');
            }, 1500);
        }, 500);
        
        // Focus en el input (solo en desktop)
        if (window.innerWidth > 768) {
            messageInput.focus();
        }
    }

    // Event listener for send button
    sendButton.addEventListener('click', sendMessage);

    // Event listener for reset button
    resetButton.addEventListener('click', resetChat);

    // Event listener to detect input changes
    messageInput.addEventListener('input', () => {
        updateSendButton();
        updateCharCounter();
    });

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

    // Ajusta el área de mensajes cuando el teclado aparece en mobile
    let initialViewportHeight = window.innerHeight;
    let isKeyboardVisible = false;

    function adjustForMobileKeyboard() {
        if (window.innerWidth <= 768) {
            const currentHeight = window.innerHeight;
            const heightDifference = initialViewportHeight - currentHeight;
            
            // Considerar que el teclado está visible si la diferencia es significativa
            const keyboardThreshold = 150;
            const newKeyboardVisible = heightDifference > keyboardThreshold;
            
            if (newKeyboardVisible !== isKeyboardVisible) {
                isKeyboardVisible = newKeyboardVisible;
                
                if (isKeyboardVisible) {
                    document.body.classList.add('keyboard-visible');
                    // Pequeño delay para asegurar que el scroll funcione correctamente
                    setTimeout(() => {
                        chatDisplay.scrollTop = chatDisplay.scrollHeight;
                    }, 100);
                } else {
                    document.body.classList.remove('keyboard-visible');
                }
            }
        }
    }

    // Función específica para iOS Safari
    function handleIOSViewport() {
        if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
            const setViewportHeight = () => {
                const vh = window.innerHeight * 0.01;
                document.documentElement.style.setProperty('--vh', `${vh}px`);
            };
            
            setViewportHeight();
            window.addEventListener('resize', setViewportHeight);
            window.addEventListener('orientationchange', () => {
                setTimeout(setViewportHeight, 500);
            });
        }
    }

    // Event listeners para el teclado móvil
    messageInput.addEventListener('focus', () => {
        if (window.innerWidth <= 768) {
            setTimeout(adjustForMobileKeyboard, 300);
            setTimeout(() => {
                chatDisplay.scrollTop = chatDisplay.scrollHeight;
            }, 500);
        }
    });

    messageInput.addEventListener('blur', () => {
        if (window.innerWidth <= 768) {
            setTimeout(adjustForMobileKeyboard, 300);
        }
    });

    // Detectar cambios en el viewport
    window.addEventListener('resize', () => {
        adjustForMobileKeyboard();
        setTimeout(() => {
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        }, 100);
    });

    window.addEventListener('orientationchange', () => {
        setTimeout(() => {
            initialViewportHeight = window.innerHeight;
            adjustForMobileKeyboard();
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        }, 500);
    });

    // Inicializar viewport handling
    handleIOSViewport();
    
    // Asegurar scroll correcto en móviles
    if (window.innerWidth <= 768) {
        const observer = new MutationObserver(() => {
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        });
        
        observer.observe(chatDisplay, { 
            childList: true, 
            subtree: true 
        });
    }

    // Mostrar sessionId en consola para debugging
    console.log('Session ID generado:', sessionId);

    // Focus input when page loads (solo en desktop)
    if (window.innerWidth > 768) {
        messageInput.focus();
    }
    
    // Inicializar contador de caracteres
    updateCharCounter();
});