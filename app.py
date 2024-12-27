from flask import Flask, request, jsonify, render_template
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
import cohere
from difflib import get_close_matches
from datetime import datetime

app = Flask(__name__)
CORS(app)
load_dotenv()

co = cohere.Client(os.getenv('COHERE_API_KEY'))

# Cargar datos de preguntas y respuestas
def load_qa_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'preguntas.json')

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            qa_list = []
            for categoria, preguntas in data['categorias'].items():
                for qa_pair in preguntas:
                    for pregunta in qa_pair['pregunta']:
                        qa_list.append({
                            'pregunta': pregunta.lower().strip(),
                            'respuesta': qa_pair['respuesta']
                        })
            return qa_list
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return []

# Buscar la mejor coincidencia en las preguntas predefinidas
def find_best_match(user_question, qa_data):
    user_question = user_question.lower().strip()

    # Buscar coincidencia exacta
    for qa in qa_data:
        if user_question == qa['pregunta']:
            return qa['respuesta']

    # Buscar coincidencia aproximada
    preguntas = [qa['pregunta'] for qa in qa_data]
    matches = get_close_matches(user_question, preguntas, n=1, cutoff=0.6)
    if matches:
        for qa in qa_data:
            if qa['pregunta'] == matches[0]:
                return qa['respuesta']

    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        timestamp = datetime.now().strftime("%H:%M")

        # Cargar preguntas y respuestas
        qa_data = load_qa_data()

        # Intentar encontrar una respuesta predefinida
        response = find_best_match(user_message, qa_data)
        if response:
            return jsonify({
                'response': response,
                'timestamp': timestamp
            })

        # Si no hay respuesta, usar Cohere
        cohere_response = co.generate(
            model='command',
            prompt=f"""Eres un dentista profesional chileno respondiendo en español chileno informal.
                      IMPORTANTE: SIEMPRE debes responder en español chileno, NUNCA en inglés.
                      
                      Pregunta del paciente: {user_message}
                      
                      Responde como dentista profesional, incluyendo:
                      1. Reconocimiento del problema o consulta
                      2. Explicación clara y sencilla en español chileno
                      3. Recomendaciones específicas
                      4. Sugerencia de consultar a un profesional si es necesario""",
            max_tokens=300,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )

        return jsonify({
            'response': cohere_response.generations[0].text.strip(),
            'timestamp': timestamp
        })

    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({
            'response': 'Lo siento, ocurrió un error. Por favor, intenta nuevamente.',
            'timestamp': timestamp
        })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Página no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/health')
def health_check():
    """Endpoint para verificar que la aplicación está funcionando"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
