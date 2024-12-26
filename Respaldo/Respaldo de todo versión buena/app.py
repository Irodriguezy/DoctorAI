import os
import json
import re
from flask import Flask, render_template, request, jsonify
import cohere
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de las claves API
cohere_api_key = os.getenv("COHERE_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

if not cohere_api_key or not google_api_key or not google_cse_id:
    raise EnvironmentError("No se pudieron cargar las variables de entorno correctamente. Verifica tu archivo .env.")

# Inicializar cliente de Cohere
co = cohere.Client(cohere_api_key)

# Crear aplicación Flask
app = Flask(__name__)

# Variable global para contar interacciones
interaction_count = 0

# Cargar preguntas predefinidas desde el archivo JSON
def load_questions():
    try:
        with open('preguntas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar preguntas.json: {e}")
        return {"questions": []}

# Realizar búsqueda en Google
def google_search(query):
    google_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api_key}&cx={google_cse_id}"
    try:
        response = requests.get(google_url)
        if response.status_code == 200:
            return response.json().get('items', [])
    except Exception as e:
        print(f"Error en búsqueda de Google: {e}")
    return []

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar los mensajes
@app.route('/chat', methods=['POST'])
def chat():
    global interaction_count
    user_message = request.json.get('message', '').strip()

    if not user_message:
        return jsonify({"response": "No se proporcionó un mensaje."}), 400

    try:
        # Incrementar contador de interacciones
        interaction_count += 1

        # Cargar preguntas predefinidas
        questions_data = load_questions()
        user_message_lower = re.sub(r'[^\w\s]', '', user_message.lower())

        # Buscar respuesta predefinida
        for item in questions_data["questions"]:
            question_lower = re.sub(r'[^\w\s]', '', item["question"].lower())
            if question_lower in user_message_lower:
                response = item["answer"]
                # Complementar con clínicas si es la quinta interacción
                if interaction_count > 5:
                    response += "\n\nSi necesitas una recomendación de clínicas en Chile, no dudes en pedírmelo."
                return jsonify({"response": response})

        # Generar respuesta con Cohere si no hay predefinida
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=f"Responde en español y solo recomienda clínicas en Chile si el usuario lo pide explícitamente o como complemento después de la quinta interacción. Pregunta: {user_message}",
            max_tokens=300,
            temperature=0.7
        )
        ai_response = response.generations[0].text.strip()

        # Redondear la idea si la respuesta está cortada
        if ai_response.endswith(("y", "en")):
            ai_response += " más detalles según tu consulta."

        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Error en el procesamiento del mensaje: {e}")
        return jsonify({"response": "Hubo un error al procesar tu solicitud. Por favor, intenta nuevamente."}), 500

if __name__ == '__main__':
    app.run(debug=True)












