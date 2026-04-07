from telegram import Update
from telegram.ext import *
from flask import Flask, jsonify
import threading, json

ADMIN_ID = 1507647928

products = [
    {"id": 1, "name": "Tank Top", "price": 10, "options": ["Black", "White"]}
]

orders = []

# TELEGRAM BOT
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to BAMA Shop 🛍")

async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)

    order = f"{data['name']} ({data['option']}) - ${data['price']}"
    orders.append(order)

    await update.message.reply_text("Choose:\n1 COD\n2 Prepaid")
    await context.bot.send_message(ADMIN_ID, "📢 " + order)

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "1":
        await update.message.reply_text("COD selected. Send address.")
    elif msg == "2":
        await update.message.reply_text("Send payment screenshot.")

# ADMIN COMMAND
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    name = context.args[0]
    price = int(context.args[1])
    options = context.args[2].split(",")

    products.append({
        "id": len(products)+1,
        "name": name,
        "price": price,
        "options": options
    })

    await update.message.reply_text(f"Added {name}")

# FLASK API
app_flask = Flask(__name__)

@app_flask.route("/products")
def get_products():
    return jsonify(products)

def run_flask():
    app_flask.run(host="0.0.0.0", port=3000)

# START BOT
app = ApplicationBuilder().token("8617548147:AAH7qLehaBLN_NNPolfGEfrsqjNTTZfJSuA").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

# RUN BOTH
threading.Thread(target=run_flask).start()
app.run_polling()
