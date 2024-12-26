const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const fs = require('fs');

// Configuración del cliente
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox'],
    }
});

// Evento cuando se genera el código QR
client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
    console.log('QR Code generado. Por favor escanea usando WhatsApp en tu teléfono');
});

// Evento cuando el cliente está listo
client.on('ready', () => {
    console.log('Cliente WhatsApp conectado y listo para usar!');
});

// Manejo de mensajes
client.on('message', async msg => {
    const lowercaseMsg = msg.body.toLowerCase();

    // Comando de ayuda
    if (lowercaseMsg === '!ayuda') {
        const helpMessage = `
*Comandos disponibles:*
!consulta [tu pregunta] - Realiza una consulta dental
!clinicas - Ver clínicas disponibles
!urgencia - Información sobre urgencias
!contacto - Información de contacto

Ejemplo: !consulta ¿cada cuánto debo ir al dentista?`;
        
        msg.reply(helpMessage);
        return;
    }

    // Procesar consultas
    if (lowercaseMsg.startsWith('!consulta')) {
        const question = msg.body.slice(9).trim();
        if (!question) {
            msg.reply('Por favor, incluye tu pregunta después de !consulta');
            return;
        }

        try {
            // Aquí iría la misma lógica de procesamiento que usamos en el chat web
            const response = await processMessage(question);
            msg.reply(response);
        } catch (error) {
            console.error('Error:', error);
            msg.reply('Lo siento, hubo un error al procesar tu consulta. Por favor, intenta nuevamente.');
        }
    }

    // Comando para ver clínicas
    if (lowercaseMsg === '!clinicas') {
        const clinicasMessage = `
*Clínicas Dentales Disponibles:*
1. Clínica Dental San Cristóbal - Providencia
2. Clínica Dental Las Condes
3. Clínica Dental Providencia

Para más información sobre una clínica específica, usa:
!clinica [número]`;
        
        msg.reply(clinicasMessage);
    }

    // Comando para urgencias
    if (lowercaseMsg === '!urgencia') {
        const urgenciaMessage = `
*Información de Urgencias Dentales*
Si tienes una emergencia dental, puedes:

1. Llamar al: +56 9 XXXX XXXX
2. Dirigirte a: [Dirección de clínica de urgencia]
3. Contactar con: [Información adicional]

*Horario de atención de urgencias:*
24/7 para emergencias graves
Lunes a Domingo 8:00 - 20:00 para otras urgencias`;
        
        msg.reply(urgenciaMessage);
    }
});

// Función para procesar mensajes (misma lógica que el chat web)
async function processMessage(message) {
    // Aquí implementarías la misma lógica de procesamiento que usas en el chat web
    // Por ahora, retornamos una respuesta de ejemplo
    return `Respuesta a tu consulta: "${message}"`;
}

// Inicializar el cliente
client.initialize();