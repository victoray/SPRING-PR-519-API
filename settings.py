import os

from dotenv import load_dotenv

load_dotenv()

DATABASE = "Gallery"
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://addressStore:PuWYYPhpqXjSgaou@cluster0.rntu3.mongodb.net/<dbname>?retryWrites=true&w=majority",
)