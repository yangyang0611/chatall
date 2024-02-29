document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://127.0.0.1:5000/chatroom');
  
    // Send message to server when user clicks send button
    const sendButton = document.querySelector('.send-button');
    const messageInput = document.querySelector('.message-input');
  
    sendButton.addEventListener('click', () => {
      console.log('send button clicked');
      const message = messageInput.value;
      socket.emit('message', message);
      messageInput.value = '';
    });
  
    // Update the chat when a new message is received
    socket.on('message', (data) => {
      const message = data['message'];
      const messagesContainer = document.querySelector('.messages-container');
  
      // Create a new message element
      const messageElement = document.createElement('div');
      messageElement.classList.add('message');
  
      // Add the message text to the element
      const messageText = document.createElement('p');
      messageText.classList.add('message-text');
      messageText.textContent = message;
      messageElement.appendChild(messageText);
  
      // Add the message element to the messages container
      messagesContainer.appendChild(messageElement);
  
      // Scroll to the bottom of the messages container
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
  });
  