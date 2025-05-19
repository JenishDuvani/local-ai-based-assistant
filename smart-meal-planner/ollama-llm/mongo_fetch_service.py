from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
import json

# MongoDB Setup
client = MongoClient('mongodb+srv://24mca018:SmartMealDB@smartmealcluster.jeeh1sn.mongodb.net/?retryWrites=true&w=majority&appName=SmartMealCluster')
db = client['smartmealdb']
recipes_collection = db['recipes']

# Kafka Setup
consumer = KafkaConsumer(
    'recipe-fetch-requests',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='mongo-fetch-group',
    enable_auto_commit=True
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Mongo Fetch Service Running...")

for message in consumer:
    try:
        data = message.value
        if data.get('request') == 'fetch_recipes':
            # Fetch from MongoDB
            recipes_cursor = recipes_collection.find().sort('timestamp', -1).limit(10)
            recipes = []
            for recipe in recipes_cursor:
                recipes.append({
                    'response': recipe.get('response', '')
                })

            # Send back via Kafka
            producer.send('recipe-fetch-responses', {'recipes': recipes})
            producer.flush()

    except Exception as e:
        print(f"Error in Mongo Fetch Service: {e}")
