from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import difflib
import os
from dotenv import load_dotenv
import cohere
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configuración para producción
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('FLASK_ENV') != 'production'

co = cohere.Client(os.getenv('COHERE_API_KEY'))

def load_qa_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'preguntas.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            qa_list = []
            for categoria, preguntas in data['categorias'].items():
                for qa_pair in preguntas:
                    if isinstance(qa_pair['pregunta'], list):
                        for pregunta in qa_pair['pregunta']:
                            qa_list.append({
                                'pregunta': pregunta.lower().strip(),
                                'respuesta': qa_pair['respuesta']
                            })
                    else:
                        qa_list.append({
                            'pregunta': qa_pair['pregunta'].lower().strip(),
                            'respuesta': qa_pair['respuesta']
                        })
            return qa_list
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return []
# ... existing code ...

def find_best_match(user_input, qa_data):
    user_input = user_input.lower().strip()
    best_match = None
    highest_similarity = 0

    # Primero buscar coincidencias parciales de palabras clave
    user_words = set(user_input.split())
    
    for qa in qa_data:
        if user_input == qa['pregunta']:  # Coincidencia exacta
            return qa['respuesta']
            
        question_words = set(qa['pregunta'].split())
        # Si hay al menos 2 palabras clave en común
        common_words = user_words.intersection(question_words)
        if len(common_words) >= 2:
            return qa['respuesta']

    # Si no hay coincidencias por palabras clave, usar similitud
    for qa in qa_data:
        similarity = difflib.SequenceMatcher(None, user_input, qa['pregunta']).ratio()
        
        if similarity > 0.7:  # Coincidencia del 70% o más
            return qa['respuesta']
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = qa['respuesta']

    # Si encontramos una coincidencia con al menos 50% de similitud
    if highest_similarity > 0.5:
        return best_match

    # Si no encontramos ninguna coincidencia buena
    return None
# Base de datos de clínicas
CLINICAS = {
    "san_cristobal": {
        "nombre": "Clínica Dental San Cristóbal",
        "web": "https://www.clinicasancristobal.cl/",
        "comuna": "providencia",
        "tratamientos": ["Odontología general", "Endodoncia", "Ortodoncia", "Implantes dentales", "Prótesis", "Blanqueamiento dental"],
        "rango_precios": "20.000 - 500.000 CLP",
        "descripcion": "Clínica con amplia experiencia en tratamientos dentales integrales."
    },
    "las_condes": {
        "nombre": "Clínica Dental Las Condes",
        "web": "https://www.clinicadental.cl/",
        "comuna": "las condes",
        "tratamientos": ["Odontología estética", "Implantes", "Ortodoncia", "Endodoncia", "Periodoncia", "Odontopediatría"],
        "rango_precios": "30.000 - 300.000 CLP",
        "descripcion": "Especialistas en odontología estética y tratamientos avanzados."
    },
    "providencia": {
        "nombre": "Clínica Dental Providencia",
        "web": "https://www.clinicadentalprovidencia.cl/",
        "comuna": "providencia",
        "tratamientos": ["Odontología general", "Implantes", "Ortodoncia", "Cirugía oral", "Periodoncia", "Odontopediatría"],
        "rango_precios": "25.000 - 250.000 CLP",
        "descripcion": "Atención integral para toda la familia con tecnología de punta."
    },
    "vitacura": {
        "nombre": "Clínica Dental Vitacura",
        "web": "https://www.clinicadentalvitacura.cl/",
        "comuna": "vitacura",
        "tratamientos": ["Odontología estética", "Implantes", "Ortodoncia invisible", "Blanqueamiento dental", "Endodoncia"],
        "rango_precios": "35.000 - 400.000 CLP",
        "descripcion": "Especialistas en estética dental y tratamientos invisibles."
    },
    "lo_barnechea": {
        "nombre": "Clínica Dental Lo Barnechea",
        "web": "https://www.clinicadentalbarnecheas.cl/",
        "comuna": "lo barnechea",
        "tratamientos": ["Odontología general", "Implantes", "Ortodoncia", "Odontopediatría", "Cirugía maxilofacial"],
        "rango_precios": "20.000 - 350.000 CLP",
        "descripcion": "Atención personalizada con los mejores especialistas."
    },
    "la_reina": {
        "nombre": "Clínica Dental La Reina",
        "web": "https://www.clinicadentallareina.cl/",
        "comuna": "la reina",
        "tratamientos": ["Odontología integral", "Implantes", "Ortodoncia", "Endodoncia", "Periodoncia", "Odontopediatría"],
        "rango_precios": "25.000 - 400.000 CLP",
        "descripcion": "Soluciones dentales integrales para toda la familia."
    },
    "nunoa": {
        "nombre": "Clínica Dental Ñuñoa",
        "web": "https://www.clinicadentalnunoa.cl/",
        "comuna": "ñuñoa",
        "tratamientos": ["Odontología general", "Implantes", "Ortodoncia", "Cirugía oral", "Blanqueamiento dental"],
        "rango_precios": "20.000 - 300.000 CLP",
        "descripcion": "Atención cercana y profesional en el corazón de Ñuñoa."
    },
    "unasalud": {
        "nombre": "Unasalud",
        "web": "https://unasalud.cl/",
        "comuna": "santiago",
        "tratamientos": ["Odontología general", "Implantes", "Ortodoncia", "Endodoncia", "Periodoncia", "Odontopediatría"],
        "rango_precios": "20.000 - 350.000 CLP",
        "descripcion": "Red de clínicas con cobertura en múltiples comunas."
    },
    "everest": {
        "nombre": "Clínica Dental Everest",
        "web": "https://www.clinicaeverest.cl/",
        "comuna": "providencia",
        "tratamientos": ["Odontología integral", "Implantes", "Ortodoncia", "Cirugía maxilofacial", "Odontopediatría"],
        "rango_precios": "25.000 - 400.000 CLP",
        "descripcion": "Tecnología de vanguardia y profesionales de excelencia."
    },
    "ino": {
        "nombre": "INO.CL",
        "web": "https://ino.cl/",
        "comuna": "las condes",
        "tratamientos": ["Odontología estética", "Implantes", "Ortodoncia invisible", "Blanqueamiento dental", "Odontopediatría"],
        "rango_precios": "30.000 - 450.000 CLP",
        "descripcion": "Especialistas en ortodoncia invisible y estética dental."
    },
    "dr_simple": {
        "nombre": "Dr. Simple",
        "web": "https://drsimple.cl/",
        "comuna": "santiago",
        "tratamientos": ["Odontología general", "Implantes", "Ortodoncia", "Endodoncia", "Blanqueamiento dental"],
        "rango_precios": "20.000 - 300.000 CLP",
        "descripcion": "Tratamientos accesibles con calidad garantizada."
    },
    "integramedica": {
        "nombre": "Integramédica",
        "web": "https://www.integramedica.cl/",
        "comuna": "multiple",
        "tratamientos": ["Odontología integral", "Implantes", "Ortodoncia", "Cirugía oral", "Periodoncia"],
        "rango_precios": "25.000 - 450.000 CLP",
        "descripcion": "Red de centros médicos y dentales en todo Santiago."
    }
}
def load_qa_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'preguntas.json')
        
        print(f"Intentando cargar JSON desde: {json_path}")  # Debug log
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            qa_list = []
            
            # Debug log
            print(f"Categorías encontradas: {list(data['categorias'].keys())}")
            
            for categoria, preguntas in data['categorias'].items():
                for qa_pair in preguntas:
                    if isinstance(qa_pair['pregunta'], list):
                        for pregunta in qa_pair['pregunta']:
                            qa_list.append({
                                'pregunta': pregunta.lower().strip(),
                                'respuesta': qa_pair['respuesta']
                            })
                    else:
                        qa_list.append({
                            'pregunta': qa_pair['pregunta'].lower().strip(),
                            'respuesta': qa_pair['respuesta']
                        })
            
            # Debug log
            print(f"Total de preguntas cargadas: {len(qa_list)}")
            return qa_list
            
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return []

# ... rest of the code ...

def find_best_match(user_input, qa_data):
    user_input = user_input.lower().strip()
    best_match = None
    highest_similarity = 0

    # Primero buscar coincidencia exacta
    for qa in qa_data:
        if user_input == qa['pregunta']:
            return qa['respuesta']

    # Si no hay coincidencia exacta, usar similitud
    for qa in qa_data:
        # Calcular similitud usando difflib
        similarity = difflib.SequenceMatcher(None, user_input, qa['pregunta']).ratio()
        
        # Si la similitud es mayor a 0.8 (80%), consideramos que es una buena coincidencia
        if similarity > 0.8:
            return qa['respuesta']
        
        # Actualizar la mejor coincidencia si encontramos una similitud mayor
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = qa['respuesta']

    # Si encontramos una coincidencia con al menos 60% de similitud
    if highest_similarity > 0.6:
        return best_match

    # Si no encontramos ninguna coincidencia buena
    return None

def get_clinic_recommendations(user_message):
    user_message = user_message.lower()
    
    # Detectar comuna
    comunas = ["las condes", "providencia", "vitacura", "lo barnechea", "la reina", "ñuñoa", "santiago"]
    comuna_mencionada = next((comuna for comuna in comunas if comuna in user_message), None)
    
    # Detectar tipo de tratamiento
    tratamientos = {
        "ortodoncia": ["ortodoncia", "brackets", "frenillos"],
        "implantes": ["implantes", "implante dental"],
        "estetica": ["estética", "blanqueamiento", "carillas"],
        "general": ["general", "limpieza", "caries"]
    }
    
    tratamiento_buscado = None
    for tipo, keywords in tratamientos.items():
        if any(keyword in user_message for keyword in keywords):
            tratamiento_buscado = tipo
            break

    # Filtrar clínicas
    clinicas_filtradas = CLINICAS.copy()
    
    if comuna_mencionada:
        clinicas_filtradas = {k: v for k, v in clinicas_filtradas.items() 
                            if v['comuna'] == comuna_mencionada or v['comuna'] == 'multiple'}
    
    if tratamiento_buscado:
        if tratamiento_buscado == "ortodoncia":
            clinicas_filtradas = {k: v for k, v in clinicas_filtradas.items() 
                                if any("ortodoncia" in t.lower() for t in v['tratamientos'])}
        elif tratamiento_buscado == "implantes":
            clinicas_filtradas = {k: v for k, v in clinicas_filtradas.items() 
                                if any("implantes" in t.lower() for t in v['tratamientos'])}
        elif tratamiento_buscado == "estetica":
            clinicas_filtradas = {k: v for k, v in clinicas_filtradas.items() 
                                if any(t.lower() in ["odontología estética", "blanqueamiento dental"] for t in v['tratamientos'])}

    # Si no hay filtros o no hay resultados, seleccionar 3 clínicas al azar
    if not clinicas_filtradas:
        selected_clinics = dict(random.sample(list(CLINICAS.items()), 3))
    else:
        # Si hay más de 3 clínicas filtradas, seleccionar 3 al azar
        if len(clinicas_filtradas) > 3:
            selected_clinics = dict(random.sample(list(clinicas_filtradas.items()), 3))
        else:
            selected_clinics = clinicas_filtradas

    return format_clinic_response(selected_clinics, comuna_mencionada, tratamiento_buscado)

def format_clinic_response(clinicas, comuna=None, tratamiento=None):
    intro = "Te recomiendo estas clínicas dentales"
    if comuna:
        intro += f" en {comuna.title()}"
    if tratamiento:
        intro += f" especializadas en {tratamiento}"
    intro += ":\n\n"
    
    response = intro
    for clinica in clinicas.values():
        response += f"🏥 {clinica['nombre']}\n"
        response += f"📍 Comuna: {clinica['comuna'].title()}\n"
        response += f"🌐 Web: {clinica['web']}\n"
        response += f"🦷 Tratamientos principales: {', '.join(clinica['tratamientos'][:3])}\n"
        response += f"💰 Rango de precios: {clinica['rango_precios']}\n"
        response += f"ℹ️ {clinica['descripcion']}\n\n"
    
    response += "💡 Te recomiendo contactar directamente con las clínicas para obtener presupuestos actualizados y confirmar disponibilidad."
    
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Endpoint para verificar que la aplicación está funcionando"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Página no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        user_name = data.get('userName', '')
        user_last_name = data.get('userLastName', '')
        timestamp = datetime.now().strftime("%H:%M")
        
        # Estructura de respuesta consistente
        response_template = {
            'response': '',
            'timestamp': timestamp,
            'user': f'**{user_name} {user_last_name}**',
            'ai': '**AI Doctor**'
        }

        # Primero intentar con preguntas predefinidas
        qa_data = load_qa_data()
        best_match = find_best_match(user_message, qa_data)
        
        if best_match:
            response_template['response'] = best_match
            return jsonify(response_template)

        # Si no hay coincidencia, usar Cohere
        try:
            response = co.generate(
                model='command',
                prompt=f"""Eres un dentista profesional. Debes:
                          1. Preguntar primero por los síntomas o el problema específico
                          2. No dar información hasta que el paciente describa su problema
                          3. Usar español latinoamericano formal
                          4. Ser breve y directo
                          
                          Mensaje del paciente: {user_message}
                          
                          Responde preguntando por los síntomas específicos.""",
                max_tokens=100,
                temperature=0.7
            )
            response_template['response'] = response.generations[0].text.strip()
            return jsonify(response_template)
            
        except Exception as e:
            print(f"Error con Cohere: {e}")
            response_template['response'] = 'Disculpa, ¿podrías describir tu problema o molestia dental?'
            return jsonify(response_template)

    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({
            'response': 'Lo siento, ocurrió un error. Por favor, intenta de nuevo.',
            'timestamp': timestamp,
            'user': f'**{user_name} {user_last_name}**',
            'ai': '**AI Doctor**'
        })
