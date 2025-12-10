import os
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Récupération des variables d'environnement
TOKEN = os.environ.get("8366434905:AAGXa4vs2Ag7A3XIBv30x567wVphwHZniRk")
WEBHOOK_URL = os.environ.get("https://davebot-1.onrender.com")

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN et WEBHOOK_URL doivent être définis comme Environment Variables sur Render.")

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Lancer le Clicker", web_app={"url": "dave33bot.netlify.app"})]
    ]
    await update.message.reply_text("Clique ici pour jouer 🎮", reply_markup=InlineKeyboardMarkup(keyboard))

# Gestion des boutons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Bouton cliqué !")

# Création de l'application Telegram
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Serveur aiohttp pour webhook
async def handle(request):
    data = await request.json()
    await app.update_queue.put(data)
    return web.Response(text="ok")

web_app = web.Application()
web_app.router.add_post("/", handle)

# Webhook setup
async def on_startup(app_web):
    await app.bot.set_webhook(url=WEBHOOK_URL)

async def on_cleanup(app_web):
    await app.bot.delete_webhook()

web_app.on_startup.append(on_startup)
web_app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(web_app, port=port)
