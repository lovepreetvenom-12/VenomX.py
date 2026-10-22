import os
import re
import json
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ===== FLASK FOR RENDER - FIXED =====
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "VenomX Bot is Online ⚡"
def run_flask(): 
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 8779030405
ADMIN_USERNAME = "Lovepreetn"
FREE_LINK = "https://gplinks.co/auto-hill-climb-premium"

USERS_FILE = "users.json"
WARNINGS_FILE = "warnings.json"

BANNED_WORDS = [
    "fuck","shit","bitch","asshole","bastard","dick","pussy","slut",
    "bc","mc","bkl","bhosdi","bhosdike","chutiya","chut","loda","lodu","gandu","randi","behenchod","madarchod","bhenchod","betichod","harami","kamina","kutta",
    "penchod","lann","lull","kanjar","khotta"
]
LINK_PATTERN = r"(https?://|www\.|t\.me/|telegram\.me/|\.com|\.in|\.net|\.org|\.xyz|\.shop)"

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
    warnings = load_data(WARNINGS_FILE)
    if warnings.get(user_id, 0) >= 3 and int(user_id) != ADMIN_ID:
        if update.message:
            await update.message.reply_text("🚫 Tu 3 warning ke baad BAN hai! Owner se contact kar.")
        else:
            await update.callback_query.answer("Tu BAN hai!", show_alert=True)
        return

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
    banned_count = sum(1 for c in warnings.values() if c >= 3)
    await update.message.reply_text(f"📊 VENOMX DASHBOARD\n\n👥 Total Users: {len(users)}\n⚠️ Warned Users: {len(warnings)}\n🚫 Banned Users: {banned_count}\n\nBot 24/7 Active ✅")

async def banned_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    warnings = load_data(WARNINGS_FILE)
    users = load_data(USERS_FILE)
    banned = {uid: users.get(uid, "Unknown") for uid, count in warnings.items() if count >= 3}
    if not banned:
        await update.message.reply_text("✅ Koi ban nahi hai.")
        return
    msg = "🚫 Banned List:\n\n"
    for uid, name in banned.items():
        msg += f"👤 {name} - ID: `{uid}`\n"
    msg += "\nUnban: /unban ID"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        await update.message.reply_text("Use: /unban USER_ID")
        return
    target_id = context.args[0]
    warnings = load_data(WARNINGS_FILE)
    if target_id in warnings:
        del warnings[target_id]
        save_data(WARNINGS_FILE, warnings)
        await update.message.reply_text(f"✅ User {target_id} Unbanned!")
    else:
        await update.message.reply_text("❌ Ye ID ban list me nahi hai.")

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if update.effective_user.id == ADMIN_ID: return
    msg = update.message.text.lower()
    user_id = str(update.effective_user.id)
    is_abuse = False
    if re.search(LINK_PATTERN, msg): is_abuse = True
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
            await update.message.reply_text(f"⚠️ Warning 1/3: @{update.effective_user.first_name} Gaali/Link mat bhej!")
        elif count == 2:
            await update.message.reply_text(f"⚠️ Warning 2/3: Last warning hai!")
        else:
            await update.message.reply_text(f"🚫 BAN! 3 warning ke baad ban kar diya.")
        try: await update.message.delete()
        except: pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'free_panel':
        text = f"🎁 **FREE SYMBIOTE PANEL** 🎁\n\nLink par click karke ads dekho aur apna FREE panel le lo."
        keyboard = [[InlineKeyboardButton("🔗 GET FREE PANEL 🔗", url=FREE_LINK)], [InlineKeyboardButton("🔙 BACK 🔙", callback_data='back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'main_panel':
        text = f"👑 **MAIN ID - ROOT PANEL** 👑\n\nPremium ke liye admin se contact karo."
        keyboard = [[InlineKeyboardButton("👑 CONTACT ADMIN 👑", url=f"https://t.me/{ADMIN_USERNAME}")], [InlineKeyboardButton("🔙 BACK 🔙", callback_data='back')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'back':
        await start(update, context)

def main():
    if not TOKEN:
        print("ERROR: TOKEN nahi mila! Render Environment me TOKEN add kar.")
        return
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users_count))
    app.add_handler(CommandHandler("banned", banned_list))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))
    print("VenomX Final Bot Started...")
    # YE LINE SABSE ZARURI HAI - Isse bot reply dega
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
