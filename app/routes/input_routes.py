from flask import Blueprint, request, jsonify
from azure.storage.blob import BlobServiceClient
import os
import uuid
from app.database import user_inputs_collection, image_collection
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

input_routes = Blueprint("input_routes", __name__)

# Ladda in Azure Blob Storage-inställningar
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = "barnsaga-uploaded-images"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

@input_routes.route("/submit-text", methods=["POST"])
def submit_text():
    """Tar emot text från användaren och sparar i MongoDB med metadata."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text krävs"}), 400

    user_id = f"guest_{uuid.uuid4().hex[:6]}"

    document = {
        "user_id": user_id,  # Automatisk användar-ID
        "text": data["text"],
        "tags": [],  # Tom lista för framtida taggning
        "source": "text",  # Indikerar att detta är textinput
        "location": "Sverige",  # Standardvärde, kan byggas ut senare
        "timestamp": datetime.utcnow().isoformat()  # Konsistent tidsformat
    }

    inserted_id = user_inputs_collection.insert_one(document).inserted_id

    return jsonify({
        "message": "Text sparad!",
        "id": str(inserted_id),
        "user_id": user_id
    }), 201


@input_routes.route("/upload-image", methods=["POST"])
def upload_image():
    """Tar emot en bild, laddar upp den till Azure Blob Storage och sparar referensen i MongoDB med metadata."""
    if "image" not in request.files:
        return jsonify({"error": "Ingen bild bifogad"}), 400

    image = request.files["image"]
    original_filename = image.filename  # Spara användarens filnamn
    image_extension = original_filename.split(".")[-1]

    # Skapa unikt filnamn
    stored_filename = f"{uuid.uuid4().hex}.{image_extension}"

    # Ladda upp bilden till Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=stored_filename)
    blob_client.upload_blob(image, overwrite=True)

    # Skapa bildens URL i Azure
    image_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{stored_filename}"

    # Skapa en automatisk user_id om vi inte har riktig användarhantering
    user_id = f"guest_{uuid.uuid4().hex[:6]}"

    # Spara metadata i MongoDB
    document = {
        "user_id": user_id,  # Automatisk användar-ID
        "original_filename": original_filename,  # Användarens filnamn
        "stored_filename": stored_filename,  # Filnamn vi skapar
        "image_url": image_url,  # Länk till bilden i Azure Blob Storage
        "source": "upload",  # Indikerar att detta är en uppladdad bild
        "tags": [],  # Tom lista för framtida taggning
        "timestamp": datetime.utcnow().isoformat()  # Konsistent tidsformat
    }

    inserted_id = image_collection.insert_one(document).inserted_id

    return jsonify({
        "message": "Bild uppladdad!",
        "image_url": image_url,
        "original_filename": original_filename,
        "id": str(inserted_id),
        "user_id": user_id
    }), 201
