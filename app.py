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

    # Si hay una coincidencia cercana (50% o más), devolver la respuesta
    if highest_similarity >= 0.5:
        print(f"Coincidencia encontrada con {highest_similarity*100:.2f}% de similitud.")
        return best_match['respuesta']

    print("No se encontró una coincidencia cercana en preguntas.json.")
    return None

def generate_cohere_response(user_message):
    """Genera una respuesta usando Cohere."""
    try:
        response = co.generate(
            model='command',
            prompt=f"""Eres un dentista profesional chileno respondiendo exclusivamente en español informal.
Responde solo preguntas relacionadas con odontología. Si el mensaje no tiene sentido, responde con un mensaje genérico en español.

Pregunta del paciente: {user_message}

Responde de forma clara y breve, enfocándote en la odontología y manteniendo el idioma español.""",
            max_tokens=100,
            temperature=0.5,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        respuesta = response.generations[0].text.strip()
        if not respuesta or not any(char.isalpha() for char in respuesta):
            return "Lo siento, no puedo procesar tu consulta en este momento."
        return respuesta
    except Exception as e:
        print(f"Error con Cohere: {e}")
        return "Lo siento, no puedo procesar tu consulta en este momento."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Maneja las consultas del usuario."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        timestamp = datetime.now().strftime("%H:%M")

        # Cargar datos de preguntas y respuestas
        qa_data = load_qa_data()

        # Buscar coincidencia en preguntas.json
        response = find_best_match(user_message, qa_data)

        if not response:
            print("No se encontró respuesta en preguntas.json, usando Cohere.")
            response = generate_cohere_response(user_message)

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

