import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import asyncio

# Configurazione logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token del bot (da sostituire con il tuo token)
TOKEN = "IL_TUO_TOKEN_QUI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il comando /start"""
    welcome_message = (
        "👋 *Benvenuto in MrWeb 2.0!*\n\n"
        "Questa è la nuova versione di MrWeb che utilizza l'API di MrWeb.\n\n"
        "Puoi utilizzare:\n"
        "• L'interfaccia web (miniapp)\n"
        "• L'interfaccia testuale (chat)\n\n"
        "Usa il pulsante About per maggiori informazioni!"
    )
    
    keyboard = [
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def check_server_status() -> str:
    """Controlla lo stato del server"""
    try:
        response = requests.get("http://217.154.2.118", timeout=5)
        return "🟢 ONLINE" if response.status_code == 200 else "🔴 OFFLINE"
    except:
        return "🔴 OFFLINE"

async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il callback del pulsante About"""
    query = update.callback_query
    await query.answer()
    
    server_status = await check_server_status()
    
    about_message = (
        "📊 *Informazioni MrWeb 2.0*\n\n"
        f"👤 Owner: [macs](https://t.me/onniscienza)\n"
        f"📦 Versione: 1.0.0\n"
        f"🌐 Server: {server_status}"
    )
    
    await query.edit_message_text(
        about_message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ℹ️ About", callback_data="about")]])
    )

def main() -> None:
    """Avvia il bot"""
    # Crea l'applicazione
    application = Application.builder().token(TOKEN).build()

    # Aggiungi i gestori
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(about_callback, pattern="^about$"))

    # Avvia il bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 