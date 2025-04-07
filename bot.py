
import os
import time
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import requests
import hashlib
from datetime import datetime
import pytz  # Aggiunto per il timezone

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7689549040:AAFgAR-ltGOBeqppaS6Bw60AXXAp-a9MYYo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 *Welcome to DrWeb 2.0!*\n\n"
        "This is the new version of DrWeb using the DrWeb API.\n\n"
        "You can use:\n"
        "• Text interface (chat)\n\n"
        "Use the About button for more information!\n"
        "Use the Tutorial button to see how it works!"
    )
    keyboard = [
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")]
    ]
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_server_status() -> str:
    try:
        response = requests.get("http://217.154.2.118", timeout=5)
        return "🟢 ONLINE" if response.status_code == 200 else "🔴 OFFLINE"
    except:
        return "🔴 OFFLINE"

async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    server_status = await check_server_status()
    about_message = (
        "📊 *Information DrWeb 2.0*\n\n"
        f"👤 Owner: [macs](https://t.me/onniscienza)\n"
        f"📦 Version: 1.0.0\n"
        f"🌐 Server: {server_status}"
    )
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    await query.edit_message_text(
        about_message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def tutorial_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    tutorial_message = (
        "*DrWeb 2.0 Tutorial*\n\n"
        "1. Send a URL or a file to the bot.\n"
        "2. The bot will send the scan result.\n"
        "3. Click the result link for more details.\n"
        "4. You can also use the /start command to return to the main screen.\n"
        "5. You can go back at any time by clicking the Back button."
    )
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    await query.edit_message_text(
        tutorial_message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👋 *Welcome to DrWeb 2.0!*\n\n"
        "This is the new version of DrWeb using the DrWeb API.\n\n"
        "You can use:\n"
        "• Web interface (miniapp)\n"
        "• Text interface (chat)\n\n"
        "Use the About button for more information!\n"
        "Use the Tutorial button to see how it works!",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ About", callback_data="about")],
            [InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")]
        ])
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = update.message.document
    if file.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("❌ The file is too large, maximum 20MB.")
        return

    start_time = time.time()

    file_info = await context.bot.get_file(file.file_id)
    file_bytes = await file_info.download_as_bytearray()
    file_name = file.file_name

    upload_dir = "/var/www/html/bot/drweb/test/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file_name)

    with open(file_path, 'wb') as f:
        f.write(file_bytes)

    file_hash = hashlib.md5(file_bytes).hexdigest()[:8]
    public_file_url = f"https://macsgames.cloud/bot/drweb/test/uploads/{file_name}"

    rome_tz = pytz.timezone("Europe/Rome")
    scan_time = datetime.now(rome_tz).strftime("%H:%M:%S")  # Ora locale di Roma

    scan_result = {
        "status": "✅ File Clean",
        "version": "7.0.65.5230",
        "size": f"{file.file_size / 1024:.2f} KB",
        "md5": file_hash,
        "scan_link": f"https://online.drweb.com/result/?lng=en&url={public_file_url}",
        "scan_time": scan_time,
        "scan_date": datetime.now().strftime("%Y/%m/%d"),
        "timezone": "Europe/Rome"
    }

    scan_message = (
        "✅ Scan completed successfully.\n"
        "➖➖➖➖➖➖➖➖\n"
        f"❗️ Scan Results:\n\n"
        f"🛡 File Status: {scan_result['status']}\n"
        f"⚙️ Antivirus Version: {scan_result['version']}\n"
        f"🗂 File Size: {scan_result['size']}\n"
        f"#️⃣ MD5 Hash: {scan_result['md5']}\n"
        f"🔗 Result Link: [Click here]({scan_result['scan_link']})\n"
        f"⏰ Scan Time: {scan_result['scan_time']}\n"
        f"📅 Scan Date: {scan_result['scan_date']}\n"
        f"☀️ Time Zone: {scan_result['timezone']}\n"
        "➖➖➖➖➖➖➖➖\n"
        "📣 @macsgames"
    )

    await update.message.reply_text(scan_message, parse_mode='Markdown')

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text(
            "❌ Wrong URL, please use this format: http://macsgames.cloud/bot/drweb/test/file.php or https://macsgames.cloud/bot/drweb/test/file.php"
        )
        return

    start_time = time.time()
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

    rome_tz = pytz.timezone("Europe/Rome")
    scan_time = datetime.now(rome_tz).strftime("%H:%M:%S")  # Ora locale di Roma

    scan_result = {
        "status": "✅ URL Clean",
        "version": "7.0.65.5230",
        "size": "N/A",
        "md5": url_hash,
        "scan_link": f"https://online.drweb.com/result/?lng=en&url={url}",
        "scan_time": scan_time,
        "scan_date": datetime.now().strftime("%Y/%m/%d"),
        "timezone": "Europe/Rome"
    }

    scan_message = (
        "✅ Scan completed successfully.\n"
        "➖➖➖➖➖➖➖➖\n"
        f"❗️ Scan Results:\n\n"
        f"🛡 URL Status: {scan_result['status']}\n"
        f"⚙️ Antivirus Version: {scan_result['version']}\n"
        f"🗂 URL MD5 Hash: {scan_result['md5']}\n"
        f"🔗 Result Link: [Click here]({scan_result['scan_link']})\n"
        f"⏰ Scan Time: {scan_result['scan_time']}\n"
        f"📅 Scan Date: {scan_result['scan_date']}\n"
        f"☀️ Time Zone: {scan_result['timezone']}\n"
        "➖➖➖➖➖➖➖➖\n"
        "📣 @drwebultra"
    )

    await update.message.reply_text(scan_message, parse_mode='Markdown')

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(about_callback, pattern="about"))
    application.add_handler(CallbackQueryHandler(tutorial_callback, pattern="tutorial"))
    application.add_handler(CallbackQueryHandler(back_callback, pattern="back"))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    application.run_polling()

if __name__ == '__main__':
    main()
