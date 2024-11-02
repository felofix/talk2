document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const personSelect = document.getElementById('person-select');
    const loadingBubble = document.getElementById('loading-bubble');
    const selectedPersonDisplay = document.getElementById('selected-person');

    // Load available 'people'
    fetch('/people')
        .then(response => response.json())
        .then(data => {
            data.forEach(person => {
                const option = document.createElement('option');
                option.value = person;
                option.textContent = person;
                personSelect.appendChild(option);
            });
            // Set initial selected person display
            selectedPersonDisplay.textContent = personSelect.value;
        });

    // Update selected person display when dropdown changes
    personSelect.addEventListener('change', () => {
        selectedPersonDisplay.textContent = personSelect.value;
    });

    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        const person = personSelect.value;

        if (message === '') return;

        appendMessage('user', message);

        // Show loading bubble
        loadingBubble.classList.remove('hidden');

        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message, person: person })
        })
            .then(response => response.json())
            .then(data => {
                appendMessage('philosopher', data.reply);
            })
            .finally(() => {
                // Hide loading bubble after receiving response
                loadingBubble.classList.add('hidden');
            });

        userInput.value = '';
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', sender);
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
