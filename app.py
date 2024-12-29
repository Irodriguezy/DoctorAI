from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import difflib
import os
from dotenv import load_dotenv
from datetime import datetime
import cohere

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configuración para producción
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('FLASK_ENV') != 'production'

# Inicializar cliente de Cohere
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def load_qa_data():
    """Carga las preguntas y respuestas desde preguntas.json"""
    try:
        with open('preguntas.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error al cargar preguntas.json: {e}")
        return {}

def find_best_match(user_question, qa_data):
    """Busca la mejor coincidencia para la pregunta del usuario."""
    user_question = user_question.lower().strip()
    highest_similarity = 0
    best_match = None

    # Buscar coincidencia exacta y calcular similitud
    for category, questions in qa_data.get('categorias', {}).items():
        for item in questions:
            for question in item['pregunta']:
                similarity = difflib.SequenceMatcher(None, user_question, question.lower()).ratio()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = item

    # Si hay una coincidencia cercana (60% o más), devolver la respuesta
    if highest_similarity >= 0.6:
        return best_match['respuesta']
    
    return None

def generate_cohere_response(user_message, user_name, user_last_name):
    """Genera una respuesta usando Cohere."""
    try:
        response = co.generate(
            model='command',
            prompt=f"""Eres un dentista profesional chileno respondiendo en español chileno informal.
                          IMPORTANTE: SIEMPRE debes responder en español chileno, NUNCA en inglés.

                          Nombre del paciente: {user_name} {user_last_name}
                          Pregunta del paciente: {user_message}

                          Responde como dentista profesional, incluyendo:
                          1. Reconocimiento del problema o consulta
                          2. Explicación clara y sencilla en español chileno
                          3. Recomendaciones específicas
                          4. Sugerencia de consultar a un profesional si es necesario""",
            max_tokens=500,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error con Cohere: {e}")
        return "Disculpa, tuve un problema para procesar tu consulta. ¿Podrías reformularla de otra manera?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Maneja las consultas del usuario."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        user_name = data.get('userName', 'Usuario')
        user_last_name = data.get('userLastName', '')
        timestamp = datetime.now().strftime("%H:%M")

        # Cargar datos de preguntas y respuestas
        qa_data = load_qa_data()

        # Buscar coincidencia en preguntas.json
        response = find_best_match(user_message, qa_data)

        if not response:
            print("No se encontró respuesta en preguntas.json, usando Cohere")
            response = generate_cohere_response(user_message, user_name, user_last_name)

        return jsonify({
            'response': response,
            'timestamp': timestamp
        })

    except Exception as e:
        print(f"Error en el chat: {e}")
        return jsonify({
            'response': 'Lo siento, ocurrió un error. Por favor, intenta de nuevo.',
            'timestamp': datetime.now().strftime("%H:%M")
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
