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

def faire_prediction(historique, game_id=None):
    if game_id:
        historique = [h for h in historique if h["id"] == game_id]
    if not historique:
        return random.sample(range(1, 6), 3)

    compteur = {i: 0 for i in range(1, 6)}
    for ligne in historique:
        for pos in ligne["positions"]:
            compteur[pos] += 1

    trié = sorted(compteur.items(), key=lambda x: x[1], reverse=True)
    return [k for k, _ in trié[:3]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🍎 Bienvenue ! Utilise /prediction ID123 pour une prédiction spécifique, ou /ajouter 1 2 3 ID123.")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        game_id = context.args[0] if context.args else None
        historique = charger_historique()
        positions = faire_prediction(historique, game_id)
        if game_id:
            await update.message.reply_text(f"🔮 Prédiction pour {game_id} : {positions}")
        else:
            await update.message.reply_text(f"🔮 Prédiction globale : {positions}")
    except:
        await update.message.reply_text("❌ Format : /prediction [ID]")

async def ajouter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        positions = list(map(int, args[:3]))
        game_id = args[3] if len(args) > 3 else "default"
        if all(1 <= pos <= 5 for pos in positions):
            historique = charger_historique()
            historique.append({
                "positions": positions,
                "id": game_id
            })
            enregistrer_historique(historique)
            await update.message.reply_text(f"✅ Enregistré pour {game_id} : {positions}")
        else:
            await update.message.reply_text("❌ Les positions doivent être entre 1 et 5.")
    except:
        await update.message.reply_text("❌ Format : /ajouter 1 2 3 ID123")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("ajouter", ajouter))
    app.run_polling()
