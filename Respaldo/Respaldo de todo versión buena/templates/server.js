const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

// Tu clave API de Cohere
const COHERE_API_KEY = 'TU_CLAVE_API_DE_COHERE';

// Configurar el servidor para parsear JSON
app.use(express.json());

// Las preguntas y respuestas predeterminadas
const responses = {
    "hola": "¡Hola! ¿Cómo puedo ayudarte con tu consulta dental?",
    "me duele un diente": "Si te duele un diente, podría ser una caries, inflamación o un problema más profundo. Es mejor que consultes a un dentista. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "que hago si me sangran las encías": "Si te sangran las encías, podrías tener gingivitis. Usa hilo dental y consulta un especialista pronto. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "tengo mal aliento": "El mal aliento puede deberse a problemas dentales o estomacales. Una evaluación dental es clave. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "que es la caries": "La caries es una enfermedad dental que daña el esmalte y requiere tratamiento. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "me duele la muela del juicio": "El dolor de la muela del juicio puede indicar inflamación o falta de espacio. Acude a un odontólogo. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "por que se me mueven los dientes": "Dientes flojos pueden ser señal de problemas periodontales. Consulta un periodoncista. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "necesito ortodoncia": "Si necesitas ortodoncia, busca un especialista en ortodoncia para evaluar tus opciones. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "como puedo blanquear mis dientes": "Para blanquear tus dientes, consulta un dentista que ofrezca tratamientos seguros. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "me duele mucho": "Si te duele mucho, es importante que consultes con un dentista lo más pronto posible. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "me está sangrando": "Si te está sangrando, puede ser una señal de gingivitis o una afección periodontal. Es importante que acudas a un especialista. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    "me duele una muela": "Si te duele una muela, puede ser una caries o un problema en la encía. Acude a un dentista para una evaluación. Si quieres que te pueda orientar mejor, dame más detalles o bien adjunta alguna radiografía.",
    // Añade más respuestas predeterminadas aquí
};

// Configuración del servidor
app.post('/chat', async (req, res) => {
    const { userMessage, conversationHistory } = req.body;

    // Normalizar el mensaje para quitar signos innecesarios y convertirlo a minúsculas
    const normalizedMessage = userMessage.toLowerCase().replace(/[^\w\sáéíóú]/g, '');

    let aiMessage = responses[normalizedMessage] || "Lo siento, no entendí tu consulta.";

    if (!responses[normalizedMessage]) {
        try {
            const response = await axios.post('https://api.cohere.ai/v1/chat', {
                model: 'command-xlarge-nightly',  // Este modelo puede cambiar
                messages: conversationHistory.concat({ role: 'user', content: userMessage }),
            }, {
                headers: {
                    'Authorization': `Bearer ${COHERE_API_KEY}`,
                    'Content-Type': 'application/json',
                },
            });

            aiMessage = response.data.response;
        } catch (error) {
            console.error('Error al consultar a Cohere:', error);
            aiMessage = "Hubo un problema al procesar tu consulta. Intenta nuevamente.";
        }
    }

    res.json({ aiMessage });
});

app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
});
