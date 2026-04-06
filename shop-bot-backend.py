filters.StatusUpdate.WEB_APP_DATA

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data
    await update.message.reply_text(f"🛒 Order received:\n{data}\n\nSend your name, phone, address.")

app = ApplicationBuilder().token("8617548147:AAH7qLehaBLN_NNPolfGEfrsqjNTTZfJSuA").build()

app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle))

app.run_polling()