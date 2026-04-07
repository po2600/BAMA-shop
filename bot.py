from telegram import Update
from telegram.ext import *
import json

ADMIN_ID = 123456789

products = []
orders = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to BAMA Shop 🛍")

# 🛒 Handle order
async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)

    order = f"{data['name']} ({data['option']}) - ${data['price']}"
    orders.append(order)

    await update.message.reply_text(
        f"🛒 Order: {order}\n\nReply:\n1 = COD\n2 = Prepaid"
    )

    await context.bot.send_message(ADMIN_ID, f"📢 New Order:\n{order}")

# 💬 Payment choice
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "1":
        await update.message.reply_text("✅ COD selected. Send name + address.")
    elif msg == "2":
        await update.message.reply_text("💳 Send payment screenshot.")
    else:
        if update.message.from_user.id == ADMIN_ID:
            await update.message.reply_text("Admin message noted.")

# 🛠 ADMIN COMMANDS

# Add product
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        name = context.args[0]
        price = int(context.args[1])
        options = context.args[2].split(",")

        products.append({
            "name": name,
            "price": price,
            "options": options
        })

        await update.message.reply_text(f"✅ Added {name}")

    except:
        await update.message.reply_text("Usage:\n/add TankTop 10 Black,White")

# View products
async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📦 Products:\n"
    for p in products:
        text += f"{p['name']} - ${p['price']}\n"
    await update.message.reply_text(text)

# View orders
async def list_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🧾 Orders:\n"
    for o in orders:
        text += o + "\n"
    await update.message.reply_text(text)

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_product))
app.add_handler(CommandHandler("products", list_products))
app.add_handler(CommandHandler("orders", list_orders))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

app.run_polling()
