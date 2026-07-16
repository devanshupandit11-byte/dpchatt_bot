import os
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Main Daku hoon!\n\n"
        "⚡ Daku AI Online.\n"
        "🔥 Sawal tera... jawab Daku ka."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 Commands:\n"
        "/start\n"
        "/help\n"
        "/ping"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prompt = update.message.text

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "❌ AI Error. Thodi der baad try karo."
        )


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Daku AI Started...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
