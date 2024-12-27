<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Doctor - Consultas Dentales</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 40px;
            background-color: #f0f2f5;
            min-height: 100vh;
            margin: 0;
        }

        .modal {
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .modal-content {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 400px;
        }

        .form-group {
            margin: 20px 0;
            position: relative;
        }

        .form-group.required label::after {
            content: " *";
            color: #dc3545;
        }

        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus {
            border-color: #007bff;
            outline: none;
        }

        .form-group.error input {
            border-color: #dc3545;
        }

        .helper-text {
            display: block;
            font-size: 0.8em;
            color: #666;
            margin-top: 4px;
        }

        .error-message {
            display: none;
            color: #dc3545;
            font-size: 0.8em;
            margin-top: 4px;
        }

        .error-message.visible {
            display: block;
        }

        .required-fields {
            font-size: 0.8em;
            color: #666;
            margin-top: 20px;
            text-align: center;
        }

        .hidden {
            display: none !important;
        }

        .side-image {
            width: 400px;
            height: auto;
            object-fit: contain;
            position: sticky;
            top: 50%;
            transform: translateY(-50%);
        }

        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 60%;
            margin: 0 40px;
            min-height: 80vh;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            text-align: center;
            margin-bottom: 40px;
            padding: 0 40px;
            color: #2c3e50;
        }

        .user-info {
            text-align: right;
            padding: 20px 40px;
            color: #666;
            font-size: 0.9em;
            border-bottom: 1px solid #eee;
            margin-bottom: 40px;
        }

        #chat-history {
            flex-grow: 1;
            overflow-y: auto;
            margin: 40px 0;
            padding: 0 40px;
            background-color: #ffffff;
        }

        .message {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
            position: relative;
            background-color: #f8f9fa;
        }

        .user-message {
            margin-left: auto;
            color: #333;
        }

        .user-name {
            font-weight: bold !important;
            color: #28a745 !important;
        }

        .bot-name {
            font-weight: bold;
            color: #007bff;
        }

        .message-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }

        .message-time {
            color: #666;
            font-size: 0.8em;
            margin-left: 10px;
        }

        .message-content {
            margin-top: 5px;
            line-height: 1.4;
        }

        .input-container {
            display: flex;
            gap: 10px;
            padding: 15px;
            border-top: 1px solid #eee;
            background-color: white;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            position: sticky;
            bottom: 0;
        }

        #user-input {
            flex-grow: 1;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }

        #user-input:focus {
            border-color: #007bff;
            outline: none;
        }

        button {
            padding: 12px 25px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }

        button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }

        .typing-indicator {
            display: none;
            padding: 15px;
            background-color: #f1f0f0;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <img src="static/Logo1.png" alt="Dental Care" class="side-image">
    
    <div class="chat-container">
        <div class="chat-header">
            <h1>AI Doctor - Consultas Dentales</h1>
            <p>Tu asistente dental virtual</p>
        </div>

        <div id="user-info" class="user-info hidden">
            <span id="display-name"></span>
        </div>

        <div id="chat-history"></div>

        <div class="typing-indicator">
            <span>AI Doctor está escribiendo...</span>
        </div>

        <div class="input-container">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje..." disabled>
            <button id="send-button" disabled>Enviar</button>
        </div>
    </div>

    <img src="static/Logo2.png" alt="Dental Care" class="side-image">

    <div id="welcome-modal" class="modal">
        <div class="modal-content">
            <h2>Bienvenido a AI Doctor</h2>
            <p>Por favor, ingresa tus datos para comenzar:</p>
            
            <div class="form-group required">
                <label for="user-nombre">Nombre</label>
                <input type="text" id="user-nombre" placeholder="Tu nombre">
                <span class="error-message"></span>
            </div>

            <div class="form-group required">
                <label for="user-apellido">Apellido</label>
                <input type="text" id="user-apellido" placeholder="Tu apellido">
                <span class="error-message"></span>
            </div>

            <div class="form-group">
                <label for="user-telefono">Teléfono</label>
                <input type="tel" id="user-telefono" placeholder="+56912345678">
                <span class="helper-text">Formato: +56912345678</span>
                <span class="error-message"></span>
            </div>

            <div class="form-group">
                <label for="user-email">Email</label>
                <input type="email" id="user-email" placeholder="tucorreo@ejemplo.com">
                <span class="error-message"></span>
            </div>

            <button onclick="startChat()">Comenzar Chat</button>
            
            <p class="required-fields">* Campos obligatorios</p>
        </div>
    </div>

    <script>
        let userName = '';
        let userLastName = '';
        let userPhone = '';
        let userEmail = '';

        function validateEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }

        function validatePhone(phone) {
            return /^\+569\d{8}$/.test(phone);
        }

        function showError(fieldId, message) {
            const field = document.getElementById(fieldId);
            const errorSpan = field.nextElementSibling;
            field.parentElement.classList.add('error');
            errorSpan.textContent = message;
            errorSpan.classList.add('visible');
        }

        function clearError(fieldId) {
            const field = document.getElementById(fieldId);
            field.parentElement.classList.remove('error');
            const errorSpan = field.nextElementSibling;
            errorSpan.classList.remove('visible');
        }

        function getCurrentTime() {
            const now = new Date();
            return now.toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' });
        }

        function startChat() {
            const nombre = document.getElementById('user-nombre').value.trim();
            const apellido = document.getElementById('user-apellido').value.trim();
            const telefono = document.getElementById('user-telefono').value.trim();
            const email = document.getElementById('user-email').value.trim();
            let isValid = true;

            if (!nombre) {
                showError('user-nombre', 'El nombre es obligatorio');
                isValid = false;
            }

            if (!apellido) {
                showError('user-apellido', 'El apellido es obligatorio');
                isValid = false;
            }

            if (telefono && !validatePhone(telefono)) {
                showError('user-telefono', 'Formato: +56912345678');
                isValid = false;
            }

            if (email && !validateEmail(email)) {
                showError('user-email', 'Ingresa un email válido');
                isValid = false;
            }

            if (!isValid) return;

            userName = nombre;
            userLastName = apellido;
            userPhone = telefono;
            userEmail = email;

            document.getElementById('welcome-modal').classList.add('hidden');
            document.getElementById('user-info').classList.remove('hidden');
            document.getElementById('display-name').textContent = `${nombre} ${apellido}`;
            document.getElementById('user-input').disabled = false;
            document.getElementById('send-button').disabled = false;
            document.getElementById('user-input').focus();

            // Mensaje de bienvenida
            addMessage('¡Hola! ¿En qué te puedo ayudar con tu salud dental? Pregúntame cualquier duda que tengas sobre tus dientes.', false);
        }

        function showTypingIndicator() {
            const typingIndicator = document.querySelector('.typing-indicator');
            typingIndicator.style.display = 'block';
        }

        function hideTypingIndicator() {
            const typingIndicator = document.querySelector('.typing-indicator');
            typingIndicator.style.display = 'none';
        }

        function addMessage(message, isUser) {
            const chatHistory = document.getElementById('chat-history');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

            const headerDiv = document.createElement('div');
            headerDiv.className = 'message-header';
            
            const nameSpan = document.createElement('span');
            nameSpan.className = isUser ? 'user-name' : 'bot-name';
            nameSpan.textContent = isUser ? `${userName} ${userLastName}` : 'AI Doctor';
            
            const timeSpan = document.createElement('span');
            timeSpan.className = 'message-time';
            timeSpan.textContent = getCurrentTime();

            headerDiv.appendChild(nameSpan);
            headerDiv.appendChild(timeSpan);

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = message;

            messageDiv.appendChild(headerDiv);
            messageDiv.appendChild(contentDiv);
            
            chatHistory.appendChild(messageDiv);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            const message = input.value.trim();
            
            if (!message) return;

            addMessage(message, true);
            input.value = '';
            input.disabled = true;
            sendButton.disabled = true;
            showTypingIndicator();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        message: message,
                        userName: userName,
                        userLastName: userLastName,
                        userPhone: userPhone,
                        userEmail: userEmail
                    })
                });

                const data = await response.json();
                hideTypingIndicator();
                addMessage(data.response, false);
            } catch (error) {
                console.error('Error:', error);
                hideTypingIndicator();
                addMessage('Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta nuevamente.', false);
            } finally {
                input.disabled = false;
                sendButton.disabled = false;
                input.focus();
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            const sendButton = document.getElementById('send-button');
            const userInput = document.getElementById('user-input');

            sendButton.addEventListener('click', function(e) {
                e.preventDefault();
                sendMessage();
            });

            sendButton.addEventListener('touchend', function(e) {
                e.preventDefault();
                sendMessage();
            });

            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey && !this.disabled) {
                    e.preventDefault();
                    sendMessage();
                }
            });
        });

        document.getElementById('user-nombre').addEventListener('input', function() {
            this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
            if (this.value.trim()) {
                clearError('user-nombre');
            }
        });

        document.getElementById('user-apellido').addEventListener('input', function() {
            this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
            if (this.value.trim()) {
                clearError('user-apellido');
            }
        });

        document.getElementById('user-telefono').addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9+]/g, '');
            if (this.value && !validatePhone(this.value)) {
                showError('user-telefono', 'Formato: +56912345678');
            } else {
                clearError('user-telefono');
            }
        });

        document.getElementById('user-email').addEventListener('input', function() {
            if (this.value && !validateEmail(this.value)) {
                showError('user-email', 'Ingresa un email válido');
            } else {
                clearError('user-email');
            }
        });

        window.onload = function() {
            document.getElementById('user-nombre').focus();
        };
    </script>
</body>
</html>
