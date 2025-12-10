from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 Lancer le Clicker Game",
                web_app={"url": "https://dave33bot.netlify.app/"}   # Mets ton URL Netlify ici !
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Clique ici pour lancer le Clicker Game 🎯👇",
        reply_markup=reply_markup
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token("8366434905:AAGXa4vs2Ag7A3XIBv30x567wVphwHZniRk").build()
    app.add_handler(CommandHandler("start", start))

    print("Bot lancé…")
    app.run_polling()
