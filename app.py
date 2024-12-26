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
        with open('preguntas.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            qa_list = []
            for categoria in data['categorias'].values():
                for qa in categoria:
                    for pregunta in qa['pregunta']:
                        qa_list.append({
                            'pregunta': pregunta.lower().strip(),
                            'respuesta': qa['respuesta']
                        })
            return qa_list
    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return None

def find_best_match(user_question, questions):
    user_question = user_question.lower().strip()
    
    # Buscar coincidencia exacta
    for qa in questions:
        if user_question == qa['pregunta']:
            return qa['respuesta']
    
    # Buscar coincidencia parcial
    best_matches = difflib.get_close_matches(
        user_question,
        [q['pregunta'] for q in questions],
        n=1,
        cutoff=0.6
    )
    
    if best_matches:
        for qa in questions:
            if qa['pregunta'] == best_matches[0]:
                return qa['respuesta']
    
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

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': '¿En qué puedo ayudarte con tu consulta dental?'})

        # Verificar si es una consulta sobre clínicas
        if any(keyword in user_message.lower() for keyword in ["clinica", "donde", "atender", "consulta", "recomend"]):
            response = get_clinic_recommendations(user_message)
            return jsonify({'response': response})

        # Cargar datos del JSON
        qa_data = load_qa_data()
        if not qa_data:
            return jsonify({'response': 'Lo siento, hay un problema con la base de datos de preguntas.'})

        # Buscar la mejor coincidencia
        best_match = find_best_match(user_message, qa_data)
        if best_match:
            return jsonify({'response': best_match})

        # Si no se encuentra en el JSON, usar Cohere
        try:
            response = co.generate(
                model='command',
                prompt=f"""Eres un asistente dental profesional que responde en español latinoamericano.
                          Debes responder de manera clara y profesional, usando términos que cualquier 
                          persona pueda entender. Si no estás seguro de una respuesta, indica que es 
                          mejor consultar directamente con un dentista.
                          
                          Pregunta del usuario: {user_message}""",
                max_tokens=500,
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            return jsonify({'response': response.generations[0].text.strip()})
        except Exception as e:
            print(f"Error con Cohere: {e}")
            return jsonify({'response': 'Lo siento, no pude entender tu pregunta. ¿Podrías reformularla?'})

    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({'response': 'Lo siento, ocurrió un error en el servidor.'})

if __name__ == '__main__':
    app.run(debug=True)