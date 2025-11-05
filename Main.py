import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')

def get_token_price(token):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={token.lower()}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url)
        data = response.json()
        if token.lower() in data:
            price = data[token.lower()]['usd']
            change = data[token.lower()]['usd_24h_change']
            return f"${token.upper()}: ${price:,.6f} | 24h: {change:+.2f}%"
        else:
            return f"Token {token} no encontrado. Usa ID de CoinGecko (ej. soon-svm)"
    except:
        return "Error de API"

def scan_x_mock(query):
    mock = [
        "soon_svm: Pool x402 100% - Listing live!",
        "CryptoCapo: Short $SOON @ $2.85 → TP $2.40",
        "binance: ¿Nuevo token AI en Alpha?"
    ]
    return "\n".join([f"• {p}" for p in mock[:3]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "CryptoAlertBot ON\n\n"
        "/update SOON\n"
        "/scanx announcement SOON\n"
        "/shortsetup SOON\n"
        "/help"
    )

async def update_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /update SOON")
        return
    token = context.args[0]
    info = get_token_price(token)
    await update.message.reply_text(info)

async def scan_x(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /scanx announcement SOON")
        return
    query = " ".join(context.args)
    results = scan_x_mock(query)
    await update.message.reply_text(f"Scan X: '{query}'\n{results}")

async def short_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /shortsetup SOON")
        return
    token = context.args[0].upper()
    setup = f"""
SHORT SETUP ${token}
Entrada: $2.80 (rechazo)
SL: $3.00 (1.5%)
TP1: $2.60 (50%)
TP2: $2.40 (30%)
R/R: 1:10+
    """
    await update.message.reply_text(setup)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/update [token]\n"
        "/scanx [query]\n"
        "/shortsetup [token]\n"
        "/help"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("update", update_token))
    app.add_handler(CommandHandler("scanx", scan_x))
    app.add_handler(CommandHandler("shortsetup", short_setup))
    app.add_handler(CommandHandler("help", help_cmd))
    app.run_polling()

if __name__ == '__main__':
    main()
