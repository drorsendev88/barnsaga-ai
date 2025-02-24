from flask import Blueprint, jsonify
import random

generate_routes = Blueprint("generate_routes", __name__)

@generate_routes.route("/generate-story", methods=["GET"])
def generate_story():
    """Genererar en saga automatiskt utan användarinput."""

    # Fördefinierade element för att skapa sagor
    protagonists = ["En liten pojke", "En modig prinsessa", "En gammal trollkarl", "En nyfiken kattunge", "En hjältemodig robot"]
    settings = ["i en magisk skog", "i en futuristisk stad", "på en flygande ö", "i en förtrollad grotta", "i ett gammalt slott"]
    challenges = ["möter en ond drake", "upptäcker en hemlig portal", "hittar en försvunnen skatt", "får ett mystiskt uppdrag", "träffar en vis gammal uggla"]
    endings = ["och räddar världen!", "och lär sig en viktig läxa.", "och finner sitt sanna öde.", "och får en ny vän.", "men mysteriet lever vidare..."]

    # Skapa en slumpmässig saga
    story = f"{random.choice(protagonists)} {random.choice(settings)} {random.choice(challenges)} {random.choice(endings)}"

    return jsonify({"story": story}), 200
