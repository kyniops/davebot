from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.ext import AIORateLimiter
from aiohttp import web
import os

TOKEN = os.getenv("BOT_TOKEN")  # On récupère le token depuis Render (Environment Variable)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # L'URL publique Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Lancer le jeu", web_app={"url": "https://ton-jeu.netlify.app"})]
    ]
    await update.message.reply_text("Clique ici pour jouer 🎮", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Bouton cliqué !")

async def handle(request):
    data = await request.json()
    await app.update_queue.put(data)
    return web.Response()

app = ApplicationBuilder().token(TOKEN).rate_limiter(AIORateLimiter()).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Serveur aiohttp
web_app = web.Application()
web_app.router.add_post("/", handle)

async def on_startup(app_web):
    await app.bot.set_webhook(url=WEBHOOK_URL)

async def on_cleanup(app_web):
    await app.bot.delete_webhook()

web_app.on_startup.append(on_startup)
web_app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    web.run_app(web_app, port=int(os.getenv("PORT", 8080)))
