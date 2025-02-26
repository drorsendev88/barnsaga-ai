from flask import Blueprint, jsonify
import requests
import os
from datetime import datetime, timedelta
from app.database import user_inputs_collection
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"  # Om problem kvarstår, testa en annan modell

generate_routes = Blueprint("generate_routes", __name__)

@generate_routes.route("/generate-story", methods=["GET"])
def generate_story():
    """Genererar en saga baserat på användarens text från senaste veckan."""

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # Hämta alla inlägg senaste veckan
    user_inputs = user_inputs_collection.find(
        {"date": {"$gte": one_week_ago.strftime("%Y-%m-%d")}},
        {"entries": 1, "_id": 0}
    )

    # Extrahera endast textinlägg
    texts = [
        entry["content"]
        for doc in user_inputs
        for entry in doc.get("entries", [])
        if entry.get("type") == "text"
    ]

    if not texts:
        return jsonify({"error": "Ingen text hittades för senaste veckan."}), 404

    # Skapa en sammanhängande saga från texterna
    prompt = "\n".join(texts)  # Använder "\n" istället för " " för att bevara struktur
    full_prompt = (
        "Skriv en barnsaga på svenska baserad på följande berättelsefragment:\n\n"
        f"{prompt}\n\n"
        "Håll berättelsen tydlig, sammanhängande och barnvänlig. "
        "Använd enkel svenska och undvik konstiga ord. "
        "Börja sagan direkt utan att återupprepa instruktionerna.\n\n"
        "Avsluta sagan med en riktig mening som ger en bra avslutning."
        "Berättelsen ska innehålla en utmaning som barnet överkom"
    )

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    response = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
    headers=headers,
    json={
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 1500,  # Ökat antal tokens för att modellen ska hinna avsluta berättelsen
            "temperature": 0.7,  # Högre temperatur för kreativitet, men inte för högt
            "top_p": 0.95,
            "return_full_text": False
            }
        }
    )   


    if response.status_code != 200:
        return jsonify({"error": "Misslyckades att generera saga", "details": response.json()}), 500

    story_response = response.json()

    # Hantera svarstypen
    if isinstance(story_response, list) and "generated_text" in story_response[0]:
        story_text = story_response[0]["generated_text"]
    else:
        return jsonify({"error": "Misslyckades att tolka svaret från AI-modellen."}), 500

    # ✅ Bevara radbrytningar och returnera som JSON
    return jsonify({"story": story_text.replace("\\n", "\n")}), 200
