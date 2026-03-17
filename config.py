import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URI = "sqlite:///ponto24.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Config email (para enviar código ao cliente)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

