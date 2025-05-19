from pymongo import MongoClient

# Your correct connection string
client = MongoClient('mongodb+srv://24mca018:SmartMealDB@smartmealcluster.jeeh1sn.mongodb.net/?retryWrites=true&w=majority&appName=SmartMealCluster')
db = client.get_database('smartmealdb')

# Choose the collection you want to check
collection = db['recipes']



for recipe in collection.find():
    print(recipe)
