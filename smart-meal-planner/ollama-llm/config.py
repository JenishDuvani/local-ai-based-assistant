# config.py
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://url-key"

mongo_client = MongoClient(MONGO_URI)
# You can customize these:
MONGO_DB_NAME = "smartmealdb"           # You can name your database (create if doesn't exist)
MONGO_COLLECTION_NAME = "recipes"       # Collection to store all generated recipes
