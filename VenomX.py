import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Flask server - Render ko jagaye rakhega (15 min offline fix)
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "VenomX is Live!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=10000)

TOKEN = os.getenv("TOKEN")
ADMIN_USERNAME = "Lovepreetn"
FREE_LINK = "https://gplinks.co/auto-hill-climb-premium"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    text = f"Namaste {name} Ji 🙏\n\n🤖 VENOM-X BOT 🤖\n👇 Select Karo:"
    keyboard = [
        [InlineKeyboardButton("🆓 FREE PANEL 🎁", callback_data='free_panel')],
        [InlineKeyboardButton("💎 MAIN ID PANEL 👑", callback_data='main_panel')]
    ]
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'free_panel':
        text = "🎁 *FREE PANEL*\n\n🔗 Link Ready Hai\n\n📖 *Kaise Kholna Hai:*\n1️⃣ DOWNLOAD NOW dabao\n2️⃣ 10 Sec Wait karo\n3️⃣ Continue dabao\n4️⃣ File Mil Jayegi ✅"
        keyboard = [
            [InlineKeyboardButton("🚀 DOWNLOAD NOW 🔗", url=FREE_LINK)],
            [InlineKeyboardButton("🏠 Back to Home", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'main_panel':
        text = "👑 *MAIN ID PANEL - @VenomX*\n\n✅ No Ads - Direct File\n✅ Lifetime Access\n✅ VIP Support"
        keyboard = [
            [InlineKeyboardButton("💬 ADMIN KO MESSAGE KARO 💎", url=f"https://t.me/{ADMIN_USERNAME}")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'home':
        await start(update, context)

def main():
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("VenomX Running...")
    app.run_polling()

if __name__ == '__main__':
    main()
