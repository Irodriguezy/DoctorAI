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
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            qa_list = []
            # Recorremos las categorías
            for categoria, preguntas in data['categorias'].items():  # Añadido 'categorias'
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
        return []  # Retornar lista vacía en lugar de None

def find_best_match(user_question, questions):
    user_question = user_question.lower().strip()
    
    # Buscar coincidencia exacta primero
    for qa in questions:
        if user_question in qa['pregunta']:
            return qa['respuesta']
    
    # Si no hay coincidencia exacta, buscar coincidencia parcial
    best_match = None
    highest_ratio = 0
    
    for qa in questions:
        ratio = difflib.SequenceMatcher(None, user_question, qa['pregunta']).ratio()
        if ratio > highest_ratio and ratio > 0.6:  # Umbral de coincidencia del 60%
            highest_ratio = ratio
            best_match = qa['respuesta']
    
    return best_match

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
        user_message = request.json.get('message', '').strip()
        timestamp = datetime.now().strftime("%H:%M")
        
        if not user_message:
            return jsonify({
                'response': '¡Hola! ¿En qué te puedo ayudar con tu salud dental? Pregúntame cualquier duda que tengas sobre tus dientes.',
                'timestamp': timestamp,
                'user': 'Usuario',
                'ai': 'AI Doctor'
            })

        # Intentar primero con preguntas predefinidas
        qa_data = load_qa_data()
        best_match = find_best_match(user_message, qa_data)
        
        if best_match:
            return jsonify({
                'response': best_match,
                'timestamp': timestamp,
                'user': 'Usuario',
                'ai': 'AI Doctor'
            })

        # Si es consulta sobre clínicas
        if any(keyword in user_message.lower() for keyword in ["clinica", "donde", "atender", "consulta", "recomend"]):
            response = get_clinic_recommendations(user_message)
            return jsonify({
                'response': response,
                'timestamp': timestamp,
                'user': 'Usuario',
                'ai': 'AI Doctor'
            })

        # Si no hay coincidencia, usar Cohere
        try:
            response = co.generate(
                model='command',
                prompt=f"""Eres un dentista profesional respondiendo en español chileno informal.
                          Debes responder de manera clara y amigable, usando términos que cualquier 
                          persona pueda entender. Usa modismos chilenos ocasionalmente.
                          
                          Pregunta del paciente: {user_message}
                          
                          Responde como dentista profesional, incluyendo:
                          1. Reconocimiento del problema o consulta
                          2. Explicación clara y sencilla
                          3. Recomendaciones específicas
                          4. Sugerencia de consultar a un profesional si es necesario""",
                max_tokens=500,
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            return jsonify({
                'response': response.generations[0].text.strip(),
                'timestamp': timestamp,
                'user': 'Usuario',
                'ai': 'AI Doctor'
            })
        except Exception as e:
            print(f"Error con Cohere: {e}")
            return jsonify({
                'response': 'Pucha, tuve un problema para procesar tu consulta. ¿Podrías reformularla de otra manera?',
                'timestamp': timestamp,
                'user': 'Usuario',
                'ai': 'AI Doctor'
            })

    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({
            'response': 'Lo siento, ocurrió un error. Por favor, intenta de nuevo.',
            'timestamp': timestamp,
            'user': 'Usuario',
            'ai': 'AI Doctor'
        })
