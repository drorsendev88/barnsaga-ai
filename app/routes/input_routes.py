from flask import Blueprint, request, jsonify
from azure.storage.blob import BlobServiceClient
import os
import uuid
from app.database import user_inputs_collection
from datetime import datetime
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

input_routes = Blueprint("input_routes", __name__)

# Azure Blob Storage-inställningar
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = "barnsaga-uploaded-images"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Tillåtna filformat
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def generate_user_id():
    """Generera ett unikt användar-ID om vi inte har riktig användarhantering."""
    return f"guest_{uuid.uuid4().hex[:6]}"


def allowed_file(filename):
    """Kollar om filen har ett tillåtet format."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@input_routes.route("/submit-text", methods=["POST"])
def submit_text():
    """Tar emot text och lagrar den i en entries-lista för dagens datum."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text krävs"}), 400

    user_id = generate_user_id()
    today_date = datetime.utcnow().strftime("%Y-%m-%d")

    # Kolla om det redan finns en post för dagens datum
    existing_entry = user_inputs_collection.find_one({"user_id": user_id, "date": today_date})

    text_entry = {
        "type": "text",
        "content": data["text"],
        "timestamp": datetime.utcnow().isoformat()
    }

    if existing_entry:
        # Lägg till text i befintlig entries-lista
        user_inputs_collection.update_one(
            {"_id": existing_entry["_id"]},
            {"$push": {"entries": text_entry}}
        )
    else:
        # Skapa ny post med dagens datum
        document = {
            "user_id": user_id,
            "date": today_date,
            "entries": [text_entry]
        }
        user_inputs_collection.insert_one(document)

    return jsonify({"message": "Text sparad!", "user_id": user_id, "date": today_date}), 201


@input_routes.route("/upload-image", methods=["POST"])
def upload_image():
    """Tar emot en bild, laddar upp den och lagrar referensen i en entries-lista för dagens datum."""
    if "image" not in request.files:
        return jsonify({"error": "Ingen bild bifogad"}), 400

    image = request.files["image"]

    if not allowed_file(image.filename):
        return jsonify({"error": "Otillåtet filformat"}), 400

    original_filename = image.filename
    image_extension = original_filename.rsplit(".", 1)[1].lower()
    stored_filename = f"{uuid.uuid4().hex}.{image_extension}"

    # Ladda upp till Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=stored_filename)
    blob_client.upload_blob(image, overwrite=True)

    image_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{stored_filename}"

    user_id = generate_user_id()
    today_date = datetime.utcnow().strftime("%Y-%m-%d")

    # Kolla om det redan finns en post för dagens datum
    existing_entry = user_inputs_collection.find_one({"user_id": user_id, "date": today_date})

    image_entry = {
        "type": "image",
        "image_url": image_url,
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "timestamp": datetime.utcnow().isoformat()
    }

    if existing_entry:
        # Lägg till bild i befintlig entries-lista
        user_inputs_collection.update_one(
            {"_id": existing_entry["_id"]},
            {"$push": {"entries": image_entry}}
        )
    else:
        # Skapa ny post med dagens datum
        document = {
            "user_id": user_id,
            "date": today_date,
            "entries": [image_entry]
        }
        user_inputs_collection.insert_one(document)

    return jsonify({"message": "Bild uppladdad!", "image_url": image_url, "user_id": user_id, "date": today_date}), 201
