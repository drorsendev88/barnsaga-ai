import os
from pymongo import MongoClient

# Hämta MongoDB Connection String från miljövariabel
MONGO_URI = os.getenv("MONGO_URI")

# Skapa en MongoDB-klient
client = MongoClient(MONGO_URI)

# Anslut till rätt databas och collections
db = client["barnsaga_db"]

# Huvudcollection där vi lagrar text & bilder
user_inputs_collection = db["user_inputs"]

# Framtida collection för AI-genererade sagor
generated_stories_collection = db["generated_stories"]

# Testa anslutningen
try:
    collections = db.list_collection_names()
    print("Anslutning till MongoDB lyckades!")
    print("Collections i databasen:", collections)
except Exception as e:
    print("Kunde inte ansluta till MongoDB:", e)