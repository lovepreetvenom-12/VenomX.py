import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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
    text = (
        f"⚡━━━『 𝐕𝐄𝐍𝐎𝐌-𝐗 』━━━⚡\n\n"
        f"🔥 𝐇𝐞𝐲 {name} 🔥\n"
        f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 𝐓𝐡𝐞 𝐅𝐮𝐭𝐮𝐫𝐞\n\n"
        f"╔══════════════════╗\n"
        f"║ 🤖 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐏𝐀𝐍𝐄𝐋𝐒 ║\n"
        f"║ 💎 𝐕𝐈𝐏 𝐀𝐂𝐂𝐄𝐒𝐒      ║\n"
        f"║ ⚡ 𝟏𝟎𝟎% 𝐓𝐑𝐔𝐒𝐓𝐄𝐃   ║\n"
        f"╚══════════════════╝\n\n"
        f"👇 𝐒𝐄𝐋𝐄𝐂𝐓 𝐊𝐀𝐑𝐎 𝐁𝐀𝐃𝐒𝐇𝐀𝐇 👇"
    )
    keyboard = [
        [InlineKeyboardButton("🎁  𝐅𝐑𝐄𝐄 𝐏𝐀𝐍𝐄𝐋  🎁", callback_data='free_panel')],
        [InlineKeyboardButton("👑  𝐌𝐀𝐈𝐍 𝐈𝐃 𝐏𝐀𝐍𝐄𝐋  👑", callback_data='main_panel')],
        [InlineKeyboardButton("💬 𝐒𝐔𝐏𝐎𝐑𝐓 | 𝐇𝐄𝐋𝐏 ⚡", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'free_panel':
        text = "🎁 *FREE PANEL UNLOCKED* 🎁\n\n🔥 Hill Climb Premium Ready Hai\n\n⚡ 1 Click Me Download Ho Jayega"
        keyboard = [
            [InlineKeyboardButton("🚀 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐍𝐎𝐖 🔥", url=FREE_LINK)],
            [InlineKeyboardButton("🔙 𝐁𝐀𝐂𝐊 𝐓𝐎 𝐇𝐎𝐌𝐄", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'main_panel':
        text = "👑 *VENOM-X MAIN PANEL* 👑\n\n💎 No Ads - Direct File\n🔥 Lifetime + VIP Support\n⚡ Instant Delivery"
        keyboard = [
            [InlineKeyboardButton("💎 𝐁𝐔𝐘 𝐍𝐎𝐖 - 𝐀𝐃𝐌𝐈𝐍 𝐒𝐄 𝐁𝐀𝐀𝐓 𝐊𝐀𝐑𝐎 👑", url=f"https://t.me/{ADMIN_USERNAME}")],
            [InlineKeyboardButton("🔙 𝐁𝐀𝐂𝐊 𝐓𝐎 𝐇𝐎𝐌𝐄", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'home':
        await start(update, context)

def main():
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("VenomX VIP Running...")
    app.run_polling()

if __name__ == '__main__':
    main()
