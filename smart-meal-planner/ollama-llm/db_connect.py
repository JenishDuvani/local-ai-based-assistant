from pymongo import MongoClient

# Your correct connection string
client = MongoClient('mongodb+srv://url-key')
db = client.get_database('smartmealdb')

# Choose the collection you want to check
collection = db['recipes']



for recipe in collection.find():
    print(recipe)
