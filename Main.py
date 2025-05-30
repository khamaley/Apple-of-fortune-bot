import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("7969491495:AAEXIbFJd9hO6pDI79vePQbujmU9G3hFTD8")
HISTORIQUE_FICHIER = "historique.json"

def charger_historique():
    try:
        with open(HISTORIQUE_FICHIER, "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []

def enregistrer_historique(historique):
    with open(HISTORIQUE_FICHIER, "w") as fichier:
        json.dump(historique, fichier)

def faire_prediction(historique):
    if not historique:
        return random.sample(range(1, 6), 3)

    compteur = {i: 0 for i in range(1, 6)}
    for ligne in historique:
        for pos in ligne:
            compteur[pos] += 1

    trié = sorted(compteur.items(), key=lambda x: x[1], reverse=True)
    return [k for k, _ in trié[:3]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🍎 Bienvenue ! Utilise /prediction pour une prédiction ou /ajouter 1 2 3.")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    historique = charger_historique()
    positions = faire_prediction(historique)
    await update.message.reply_text(f"🔮 Prédiction : Positions {positions}")

async def ajouter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        positions = list(map(int, context.args))
        if all(1 <= pos <= 5 for pos in positions):
            historique = charger_historique()
            historique.append(positions)
            enregistrer_historique(historique)
            await update.message.reply_text(f"✅ Ajouté : {positions}")
        else:
            await update.message.reply_text("❌ Les positions doivent être entre 1 et 5.")
    except:
        await update.message.reply_text("❌ Format incorrect. Utilise : /ajouter 1 2 3")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("ajouter", ajouter))
    app.run_polling()
