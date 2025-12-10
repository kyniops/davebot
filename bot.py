# bot.py — long polling (dev)
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import logging

load_dotenv()
TOKEN = os.getenv("8366434905:AAGXa4vs2Ag7A3XIBv30x567wVphwHZniRk")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Salut 👋", callback_data="hello")],
        [InlineKeyboardButton("Aide", callback_data="help")]
    ]
    await update.message.reply_text(
        "Bonjour ! Je suis ton bot.\nChoisis :", reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "hello":
        await query.edit_message_text("Salut ! 😊")
    else:
        await query.edit_message_text("Commandes : /start")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Tu as dit : {update.message.text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    logger.info("Bot démarré (long polling)")
    app.run_polling()

if __name__ == "__main__":
    main()
