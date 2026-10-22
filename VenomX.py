import os
import re
import json
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "VenomX Bot is Online ⚡"
def run_flask(): flask_app.run(host='0.0.0.0', port=10000)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 8779030405 # Teri ID daal di hai
ADMIN_USERNAME = "Lovepreetn"
FREE_LINK = "https://gplinks.co/auto-hill-climb-premium"

USERS_FILE = "users.json"
WARNINGS_FILE = "warnings.json"

BANNED_WORDS = [
    "fuck", "shit", "bitch", "asshole", "bastard", "dick", "pussy", "slut",
    "bc", "mc", "bkl", "bhosdi", "bhosdike", "chutiya", "chut", "loda", "lodu", "gandu", "randi", "behenchod", "madarchod", "bhenchod", "betichod", "harami", "kamina",
    "penchod", "lann", "lull", "kanjar"
]
LINK_PATTERN = r"(https?://|www\.|t\.me/|telegram\.me/|\.com|\.in|\.net|\.org|\.xyz)"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, 'w') as f: json.dump(f, data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_data(USERS_FILE)
    if user_id not in users:
        users[user_id] = update.effective_user.first_name
        save_data(USERS_FILE, users)
    
    name = update.effective_user.first_name
    text = f"⚡━━━『 𝐕𝐄𝐍𝐎𝐌-𝐗 』━━━⚡\n\n🔥 𝐇𝐞𝐲 {name} 🔥\n\n👇 𝐒𝐄𝐋𝐄𝐂𝐓 𝐘𝐎𝐔𝐑 𝐏𝐀𝐍𝐄𝐋 👇"
    keyboard = [
        [InlineKeyboardButton("🎁  𝐅𝐑𝐄𝐄 𝐏𝐀𝐍𝐄𝐋  🎁", callback_data='free_panel')],
        [InlineKeyboardButton("👑  𝐌𝐀𝐈𝐍 𝐈𝐃 𝐏𝐀𝐍𝐄𝐋  👑", callback_data='main_panel')],
        [InlineKeyboardButton("💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ⚡", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Ye sirf Owner ke liye hai!")
        return
    users = load_data(USERS_FILE)
    warnings = load_data(WARNINGS_FILE)
    await update.message.reply_text(f"📊 VENOMX DASHBOARD\n\n👥 Total Users: {len(users)}\n⚠️ Warned Users: {len(warnings)}\n\nBot is 24/7 Active ✅")

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if update.effective_user.id == ADMIN_ID: return

    msg = update.message.text.lower()
    user_id = str(update.effective_user.id)
    
    is_abuse = False
    if re.search(LINK_PATTERN, msg):
        is_abuse = True
    for word in BANNED_WORDS:
        if word in msg:
            is_abuse = True
            break

    if is_abuse:
        warnings = load_data(WARNINGS_FILE)
        warnings[user_id] = warnings.get(user_id, 0) + 1
        save_data(WARNINGS_FILE, warnings)
        count = warnings[user_id]
        
        if count == 1:
            await update.message.reply_text(f"⚠️ Warning 1/3: Gaali / Link mat bhej!")
        elif count == 2:
            await update.message.reply_text(f"⚠️ Warning 2/3: Last warning! Agli baar BAN!")
        elif count >= 3:
            await update.message.reply_text(f"🚫 BAN! 3 warning ke baad ban ho gaya hai.")
        try:
            await update.message.delete()
        except:
            pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'free_panel':
        text = f"🎁 FREE PANEL\n\nLink par click karke ads dekho."
        keyboard = [[InlineKeyboardButton("🔗 GET FREE PANEL 🔗", url=FREE_LINK)], [InlineKeyboardButton("🔙 BACK 🔙", callback_data='back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'main_panel':
        text = f"👑 MAIN ID PANEL\n\nPremium ke liye admin se contact karo."
        keyboard = [[InlineKeyboardButton("👑 CONTACT ADMIN 👑", url=f"https://t.me/{ADMIN_USERNAME}")], [InlineKeyboardButton("🔙 BACK 🔙", callback_data='back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'back':
        await start(update, context)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users_count))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))
    print("VenomX Bot Started with Owner ID 8779030405...")
    app.run_polling()

if __name__ == '__main__':
    main()
