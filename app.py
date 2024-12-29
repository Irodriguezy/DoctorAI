from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import difflib
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configuración para producción
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('FLASK_ENV') != 'production'

def load_qa_data():
    try:
        with open('preguntas.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error al cargar preguntas.json: {e}")
        return {}

def find_best_match(user_question, qa_data):
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
    
    # Si no hay coincidencia cercana, sugerir preguntas similares
    suggestions = get_close_matches(user_question, [q for cat in qa_data.get('categorias', {}).values() for qa in cat for q in qa['pregunta']], n=3, cutoff=0.5)
    if suggestions:
        return f"Lo siento, no tengo una respuesta exacta. ¿Quizás quisiste decir: {' / '.join(suggestions)}?"

    return "Lo siento, no tengo información sobre eso. Intenta con otra pregunta."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        timestamp = datetime.now().strftime("%H:%M")

        qa_data = load_qa_data()
        response = find_best_match(user_message, qa_data)

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
