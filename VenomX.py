import os, threading, asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "VenomX Rooted"
def run_flask(): flask_app.run(host='0.0.0.0', port=10000)

TOKEN = os.getenv("TOKEN")
ADMIN_USERNAME = "Lovepreetn"
FREE_LINK = "https://gplinks.co/auto-hill-climb-premium"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    chat = update.effective_chat
    
    msg = await chat.send_message("```\nroot@venom-x:~# ./start.sh\n```", parse_mode='Markdown')
    
    logs = [
        "```\nroot@venom-x:~# ./start.sh\n[●] Connecting to tg-api... OK\n```",
        "```\nroot@venom-x:~# ./start.sh\n[●] Connecting to tg-api... OK\n[●] User Found: {}\n[●] ID: {}***\n```".format(name, str(update.effective_user.id)[:4]),
        "```\n[●] Bypassing firewall... ████░░░░ 40%\n[●] Decrypting database...```",
        "```\n[●] Bypassing firewall... ████████ 100% [DONE]\n[●] Decrypting database... ██████░░ 75%\n[●] Injecting payload: venom_symbiote.exe\n```",
        "```\n[✓] Firewall Bypassed\n[✓] Database Decrypted\n[✓] Payload Injected\n[✓] Root Access Granted\n\n> ACCESS GRANTED_\n```"
    ]

    for log in logs:
        await asyncio.sleep(1.0)
        try: await msg.edit_text(log, parse_mode='Markdown')
        except: pass

    await asyncio.sleep(1)
    final_text = (
        f"☠️ ROOT@VENOM-X:~# ACCESS GRANTED ☠️\n\n"
        f"┌──[ {name}@symbiote ]\n"
        f"│   ├─ ID: {str(update.effective_user.id)[:4]}****\n"
        f"│   ├─ STATUS: INFECTED 🕷️\n"
        f"│   └─ MODE: DARK VENOM 💀\n"
        f"└──╼ $ select_panel\n\n"
        f"⚡ VENOM-X DARK PANELS READY ⚡"
    )
    keyboard = [
        [InlineKeyboardButton("🕷️ FREE SYMBIOTE [FREE]", callback_data='free_panel')],
        [InlineKeyboardButton("💀 ROOT SYMBIOTE [PAID]", callback_data='main_panel')],
        [InlineKeyboardButton("⚡ CONTACT ROOT", url=f"https://t.me/{
