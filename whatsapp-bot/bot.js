const qrcode = require('qrcode-terminal');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');

const client = new Client({
    authStrategy: new LocalAuth({ clientId: "bot_session" }),
    puppeteer: {
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    }
});

// Menú principal
const MENU_PRINCIPAL = `
🦷 *MENÚ PRINCIPAL - AI DOCTOR* 🦷

Comandos disponibles:

1. *!ayuda* - Muestra este menú
2. *!consulta* [pregunta] - Realiza una consulta dental
3. *!urgencia* - Información sobre urgencias
4. *!horario* - Horarios de atención
5. *!ubicacion* - Direcciones de clínicas
6. *!contacto* - Información de contacto
7. *!servicios* - Lista de servicios disponibles
8. *!precios* - Información de precios
9. *!agendar* - Agendar una cita

_Ejemplo: !consulta ¿cada cuánto debo ir al dentista?_`;

// Manejador de mensajes
client.on('message', async msg => {
    const command = msg.body.toLowerCase();

    // Menú de ayuda
    if (command === '!ayuda' || command === '!menu') {
        await msg.reply(MENU_PRINCIPAL);
    }

    // Consultas dentales
    else if (command.startsWith('!consulta')) {
        const pregunta = msg.body.slice(9).trim();
        if (!pregunta) {
            await msg.reply('Por favor, incluye tu pregunta después de !consulta\nEjemplo: !consulta ¿cada cuánto debo cambiar mi cepillo de dientes?');
            return;
        }
        await msg.reply(`Procesando tu consulta: "${pregunta}"\n\nRespuesta: [Aquí iría la respuesta del modelo AI]`);
    }

    // Información de urgencias
    else if (command === '!urgencia') {
        await msg.reply(`
🚨 *URGENCIAS DENTALES* 🚨

*Horario de Atención:*
• Lunes a Domingo 24/7

*Números de Emergencia:*
• +56 9 XXXX XXXX (Principal)
• +56 9 XXXX XXXX (Alternativo)

*Ubicación:*
[Dirección de la clínica de urgencias]

*Casos que consideramos urgencia:*
1. Dolor dental severo
2. Traumatismos dentales
3. Inflamación grave
4. Sangrado persistente
5. Accidentes que afecten los dientes

*¿Qué hacer mientras espera atención?*
• Mantener la calma
• Aplicar frío en caso de inflamación
• No tomar medicamentos sin prescripción
• Guardar piezas dentales en leche o suero

Para más información, responda con *!contacto*`);
    }

    // Horarios de atención
    else if (command === '!horario') {
        await msg.reply(`
⏰ *HORARIOS DE ATENCIÓN* ⏰

*Consultas Regulares:*
• Lunes a Viernes: 09:00 - 19:00
• Sábados: 09:00 - 14:00

*Urgencias:*
• Disponible 24/7

*Feriados:*
• Cerrado (excepto urgencias)

Para agendar una cita, use el comando *!agendar*`);
    }

    // Ubicaciones
    else if (command === '!ubicacion') {
        await msg.reply(`
📍 *NUESTRAS CLÍNICAS* 📍

*Sede Principal:*
• [Dirección completa]
• Metro: [Estación más cercana]
• Referencias: [Puntos de referencia]

*Sede Las Condes:*
• [Dirección completa]
• Metro: [Estación más cercana]
• Referencias: [Puntos de referencia]

*Sede Providencia:*
• [Dirección completa]
• Metro: [Estación más cercana]
• Referencias: [Puntos de referencia]

Para más información de cada sede, escriba:
*!sede1*, *!sede2* o *!sede3*`);
    }

    // Servicios disponibles
    else if (command === '!servicios') {
        await msg.reply(`
🦷 *SERVICIOS DENTALES* 🦷

1. *Odontología General*
   • Limpiezas
   • Empastes
   • Extracciones

2. *Especialidades*
   • Ortodoncia
   • Implantes
   • Endodoncia
   • Periodoncia
   • Blanqueamiento

3. *Estética Dental*
   • Carillas
   • Coronas
   • Diseño de sonrisa

4. *Cirugía*
   • Extracciones complejas
   • Cirugía maxilofacial

Para más información de cada servicio:
*!servicio* [número]
Ejemplo: !servicio 1`);
    }

    // Precios
    else if (command === '!precios') {
        await msg.reply(`
💰 *LISTA DE PRECIOS* 💰

*Consulta General:*
• Evaluación: $XX.XXX
• Limpieza: $XX.XXX

*Tratamientos Básicos:*
• Empaste simple: $XX.XXX
• Extracción simple: $XX.XXX

*Tratamientos Especializados:*
• Ortodoncia desde: $XXX.XXX
• Implantes desde: $XXX.XXX

*Promociones Actuales:*
• Evaluación + Limpieza: $XX.XXX
• Blanqueamiento: $XX.XXX

_Precios referenciales, pueden variar según evaluación_

Para más detalles, agende una evaluación con *!agendar*`);
    }

    // Agendar cita
    else if (command === '!agendar') {
        await msg.reply(`
📅 *AGENDAR CITA* 📅

Para agendar una cita, necesitamos:
1. Nombre completo
2. RUT
3. Teléfono
4. Motivo de consulta

Por favor, responda con:
*!cita* [nombre] [RUT] [teléfono] [motivo]

Ejemplo:
!cita Juan Pérez 12345678-9 +56912345678 limpieza dental`);
    }

    // Contacto
    else if (command === '!contacto') {
        await msg.reply(`
📱 *INFORMACIÓN DE CONTACTO* 📱

*Teléfonos:*
• Central: +56 X XXXX XXXX
• Urgencias: +56 9 XXXX XXXX

*Correo:*
• contacto@aidoctor.cl

*Redes Sociales:*
• Instagram: @aidoctor
• Facebook: /aidoctor
• Twitter: @aidoctor

*Sitio Web:*
www.aidoctor.cl

Para urgencias, use el comando *!urgencia*`);
    }

    // Comando de prueba
    else if (command === '!ping') {
        await msg.reply('pong');
    }
});

// Evento QR
client.on('qr', qr => {
    console.clear();
    console.log('='.repeat(50));
    console.log('NUEVO CÓDIGO QR GENERADO');
    console.log('='.repeat(50));
    console.log('\n');
    qrcode.generate(qr, { small: false });
    console.log('\n');
    console.log('Escanea el código QR con WhatsApp');
});

// Evento Ready
client.on('ready', () => {
    console.clear();
    console.log('='.repeat(50));
    console.log('¡BOT CONECTADO Y LISTO!');
    console.log('='.repeat(50));
    console.log('\nEsperando mensajes...');
});

// Inicializar el cliente
client.initialize();