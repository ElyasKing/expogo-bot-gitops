from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess
import json
import requests

TOKEN = "8448609111:AAE9xeu7I_jS2xqfH4fkVC6EwyqW9uMIRe4"

# Fonction pour exécuter kubectl et récupérer des infos (attention : kubectl doit être configuré sur la machine où tourne le bot)
def run_kubectl(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Erreur : {result.stderr.strip()}"
    except Exception as e:
        return f"Exception : {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Je suis KubeBuddy 🚀\n\nCommandes :\n/status → état du cluster\n/pods → liste des pods\nTout le reste → je répète ce que tu dis 😄")

async def ratio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("bro est encore bloqué en 2023")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nodes = run_kubectl("kubectl get nodes --no-headers | wc -l")
    pods = run_kubectl("kubectl get pods -n default --no-headers | wc -l")
    running = run_kubectl("kubectl get pods -n default --field-selector=status.phase=Running --no-headers | wc -l")
    
    msg = f"📊 État rapide du cluster :\n- Nodes : {nodes.strip()}\n- Pods totaux (default) : {pods.strip()}\n- Pods Running : {running.strip()}"
    await update.message.reply_text(msg)

async def pods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = run_kubectl("kubectl get pods -n default -o wide --no-headers")
    if "No resources found" in output:
        msg = "Aucun pod dans le namespace default pour l'instant."
    else:
        msg = "Pods dans default :\n" + output
    await update.message.reply_text(msg)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pods", pods))
    app.add_handler(CommandHandler("ratio", ratio))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot démarré !")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()