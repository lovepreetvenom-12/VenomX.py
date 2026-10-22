import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================= FLASK SERVER (BOT KO ONLINE RAKHNE KE LIYE) =================
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "VenomX Bot is Online ⚡"

def run_flask():
    flask_app.run(host='0.0.0.0', port=10000)

# ================= BOT SETTING =================
TOKEN = os.getenv("TOKEN")
ADMIN_USERNAME = "Lovepreetn"
FREE_LINK = "https://gplinks.co/auto-hill-climb-premium"
PAID_LINK = "https://gplinks.co/paid-panel-link" # Yahan apna paid wala link daal de

# ================= /START COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    
    text = (
        f"⚡━━━『 𝐕𝐄𝐍𝐎𝐌-𝐗 』━━━⚡\n\n"
        f"🔥 𝐇𝐞𝐲 {name} 🔥\n\n"
        f"╔════════════════════╗\n"
        f"║ 🤖 PREMIUM PANELS  ║\n"
        f"║ 💎 VIP ACCESS      ║\n"
        f"║ ⚡ 100% TRUSTED     ║\n"
        f"╚════════════════════╝\n\n"
        f"👇 𝐒𝐄𝐋𝐄𝐂𝐓 𝐘𝐎𝐔𝐑 𝐏𝐀𝐍𝐄𝐋 👇"
    )

    keyboard = [
        [InlineKeyboardButton("🎁  𝐅𝐑𝐄𝐄 𝐏𝐀𝐍𝐄𝐋  🎁", callback_data='free_panel')],
        [InlineKeyboardButton("👑  𝐌𝐀𝐈𝐍 𝐈𝐃 𝐏𝐀𝐍𝐄𝐋  👑", callback_data='main_panel')],
        [InlineKeyboardButton("💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ⚡", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    
    markup = InlineKeyboardMarkup(keyboard)

    # Agar /start command hai to naya message
    if update.message:
        await update.message.reply_text(text, reply_markup=markup)
    # Agar BACK button hai to same message edit hoga
    else:
        await update.callback_query.edit_message_text(text, reply_markup=markup)

# ================= BUTTONS PE CLICK KARNE PAR =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'free_panel':
        text = (
            f"🎁 **FREE SYMBIOTE PANEL** 🎁\n\n"
            f"Link par click karke ads dekho aur apna FREE panel le lo.\n\n"
            f"👇 𝐋𝐈𝐍𝐊 👇"
        )
        keyboard = [
            [InlineKeyboardButton("🔗 GET FREE PANEL 🔗", url=FREE_LINK)],
            [InlineKeyboardButton("🔙 BACK TO MENU 🔙", callback_data='back')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'main_panel':
        text = (
            f"👑 **MAIN ID - ROOT PANEL** 👑\n\n"
            f"Ye premium wala hai, isme full access milega.\n\n"
            f"👇 𝐋𝐈𝐍𝐊 👇"
        )
        keyboard = [
            [InlineKeyboardButton("💎 GET MAIN PANEL 💎", url=PAID_LINK)],
            [InlineKeyboardButton("🔙 BACK TO MENU 🔙", callback_data='back')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'back':
        await start(update, context)

# ================= BOT START =================
def main():
    # Flask ko background me chalao
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Telegram Bot start
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("VenomX Bot Started Successfully...")
    app.run_polling()

if __name__ == '__main__':
    main()
