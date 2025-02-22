import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")  # För framtida säkerhet
    DEBUG = os.getenv("FLASK_DEBUG", True)