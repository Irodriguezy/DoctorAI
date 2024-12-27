from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import json
from difflib import get_close_matches
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inicializar el cliente de Cohere
co = cohere.Client('V05CQ6r3ccHNQkVOulCVXM1jrWkS7XfYEdgAFwD9')

def load_qa_data():
    try:
        with open('preguntas.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("✓ Archivo preguntas.json cargado correctamente")
            return data
    except Exception as e:
        print(f"✗ Error loading preguntas.json: {e}")
        return {}

def find_best_match(user_question, qa_data):
    if not qa_data or 'categorias' not in qa_data:
        print("✗ Error: qa_data está vacío o no tiene el formato correcto")
        return None
    
    user_question = user_question.lower().strip()
    print(f"\n🔍 Buscando coincidencia para: '{user_question}'")
    
    # Primero buscar en saludos para priorizar estas respuestas
    if 'saludos' in qa_data['categorias']:
        for qa_item in qa_data['categorias']['saludos']:
            for variant in qa_item['pregunta']:
                if user_question in variant.lower() or variant.lower() in user_question:
                    print(f"✓ ¡Coincidencia encontrada en saludos!")
                    return qa_item['respuesta']
    
    # Luego buscar en el resto de categorías
    for categoria_nombre, categoria_data in qa_data['categorias'].items():
        if categoria_nombre != 'saludos':  # Skip saludos as we already checked
            print(f"👉 Revisando categoría: {categoria_nombre}")
            for qa_item in categoria_data:
                for variant in qa_item['pregunta']:
                    if user_question in variant.lower() or variant.lower() in user_question:
                        print(f"✓ ¡Coincidencia encontrada en {categoria_nombre}!")
                        return qa_item['respuesta']
    
    print("✗ No se encontró coincidencia en preguntas.json")
    return None

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        user_name = data.get('userName', '')
        user_last_name = data.get('userLastName', '')
        timestamp = datetime.now().strftime("%H:%M")

        print(f"\n📝 Nuevo mensaje de {user_name}: '{user_message}'")

        # Primero buscar en preguntas.json
        qa_data = load_qa_data()
        predefined_response = find_best_match(user_message, qa_data)
        
        if predefined_response:
            print("✓ Usando respuesta predefinida")
            return jsonify({
                'response': predefined_response,
                'timestamp': timestamp
            })
        
        print("→ No se encontró respuesta predefinida, usando Cohere")
        # Si no se encontró respuesta predefinida, usar Cohere
        try:
            cohere_response = co.generate(
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
            return jsonify({
                'response': cohere_response.generations[0].text.strip(),
                'timestamp': timestamp
            })
        except Exception as e:
            print(f"✗ Error with Cohere: {e}")
            return jsonify({
                'response': f'Disculpa {user_name}, tuve un problema para procesar tu consulta. ¿Podrías reformularla de otra manera?',
                'timestamp': timestamp
            })

    except Exception as e:
        print(f"✗ Error in chat: {e}")
        return jsonify({
            'response': 'Lo siento, ocurrió un error. Por favor, intenta de nuevo.',
            'timestamp': timestamp
        })

if __name__ == '__main__':
    app.run(debug=True)
