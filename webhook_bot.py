import os
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Lire les variables Render
TOKEN = os.environ.get("8366434905:AAGXa4vs2Ag7A3XIBv30x567wVphwHZniRk")
WEBHOOK_URL = os.environ.get("https://davebot-1.onrender.com/")

print("DEBUG TOKEN =", repr(TOKEN))
print("DEBUG WEBHOOK_URL =", repr(WEBHOOK_URL))

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("Variables BOT_TOKEN ou WEBHOOK_URL manquantes")

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Lancer le jeu", web_app={"url": "https://dave33bot.netlify.app/"})]
    ]
    await update.message.reply_text("Bienvenue ! Cliquez pour jouer :", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("OK !")

# Configuration du bot Telegram
tg_app = ApplicationBuilder().token(TOKEN).build()
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CallbackQueryHandler(button))

# Serveur webhook via aiohttp
async def telegram_webhook(request):
    data = await request.json()
    await tg_app.update_queue.put(data)
    return web.Response(text="ok")

web_app = web.Application()
web_app.router.add_post("/", telegram_webhook)

# Setup webhook
async def on_startup(app):
    await tg_app.bot.set_webhook(WEBHOOK_URL)

web_app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    web.run_app(web_app, port=port)
