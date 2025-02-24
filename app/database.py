import os
from pymongo import MongoClient

# Hämta MongoDB Connection String från miljövariabel
MONGO_URI = os.getenv("MONGO_URI")  # Se till att denna är satt!

# Skapa en MongoDB-klient
client = MongoClient(MONGO_URI)

# Anslut till rätt databas och collection
db = client["barnsaga_db"]  # Din Cosmos DB-databas


# Collection för text
user_inputs_collection = db["user_input"]

# Collection för bilder
image_collection = db["uploaded_images"]

# Testa anslutningen
try:
    db.list_collection_names()  # Försök läsa collections
    print("Anslutning till MongoDB lyckades!")
except Exception as e:
    print("Kunde inte ansluta till MongoDB:", e)
