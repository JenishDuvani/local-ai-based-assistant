from flask import Flask, request, jsonify, render_template, session
import requests
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import os
import wave
from pymongo import MongoClient
import datetime
from config import mongo_client
import time
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
import random




app = Flask(__name__)


db = mongo_client["smartmealdb"]  # Database name
recipes_collection = db["recipes"]  # Collection name

#kafka
# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# consumer = KafkaConsumer(
#     'recipe-fetch-responses',
#     bootstrap_servers='localhost:9092',
#     value_deserializer=lambda v: json.loads(v.decode('utf-8')),
#     auto_offset_reset='earliest',
#     group_id='flask-group',
#     enable_auto_commit=True
# )

# Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',  # Kafka running locally
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize Python dict to JSON bytes
# )



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate-recipe')
def generate_recipe_page():
    return render_template("recipe_generate.html")

@app.route('/voice')
def voice_page():
    return render_template("voice.html")

#   Working Generate Meal Without DB Storing
# @app.route('/generate-meal', methods=['POST'])
# def generate_meal():
#     try:
#         data = request.json
#         ingredients = data.get("ingredients", [])
#         diet = data.get("diet", "balanced")

#         prompt = f"Suggest a healthy {diet} meal using these ingredients: {', '.join(ingredients)}.Make sure to give proper instruction with time duration as well. The Response Should Be Limited to 500 Words."

#         response = requests.post("http://localhost:11434/api/generate", json={
#             "model": "llama3.1:8b",
#             "prompt": prompt,
#             "stream": False
#         })

#         result = response.json()
#         return jsonify({"meal_plan": result.get("response")})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Helper function to load recipes
# def load_recipes():
#     if os.path.exists('recipes.json'):
#         with open('recipes.json', 'r') as f:
#             return json.load(f)
#     return []

# # Helper function to save a new recipe
# def save_recipe(meal_plan):
#     recipes = load_recipes()
#     recipes.append({'meal_plan': meal_plan})
#     with open('recipes.json', 'w') as f:
#         json.dump(recipes, f, indent=4)

# Working With MOngo Without Kafka
@app.route('/generate-meal', methods=['POST'])
def generate_meal():
    try:
        data = request.json
        ingredients = data.get("ingredients", [])
        diet = data.get("diet", "balanced")

        prompt = f"Suggest a healthy {diet} meal using these ingredients: {', '.join(ingredients)}. Make sure to give proper instruction with time duration as well. The Response Should Be Limited to 250 Words."

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        })

        result = response.json()
        meal_plan = result.get("response")

        # Save to MongoDB
        recipes_collection.insert_one({
            "ingredients": ingredients,
            "diet": diet,
            "prompt": prompt,
            "response": meal_plan,
            "timestamp": datetime.datetime.utcnow()
        })

        return jsonify({"meal_plan": meal_plan})
    
    except Exception as e:
        import traceback
        print(f"🔥 Error in /generate-meal: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


#   Try Kafka 1

# @app.route('/generate-meal', methods=['POST'])
# def generate_meal():
#     try:
#         data = request.json
#         ingredients = data.get("ingredients", [])
#         diet = data.get("diet", "balanced")

#         prompt = f"Suggest a healthy {diet} meal using these ingredients: {', '.join(ingredients)}. Make sure to give proper instruction with time duration as well. The Response Should Be Limited to 250 Words."

#         response = requests.post("http://localhost:11434/api/generate", json={
#             "model": "llama3.1:8b",
#             "prompt": prompt,
#             "stream": False
#         })

#         result = response.json()
#         meal_plan = result.get("response")

#         # Save to MongoDB
#         recipes_collection.insert_one({
#             "ingredients": ingredients,
#             "diet": diet,
#             "prompt": prompt,
#             "response": meal_plan,
#             "timestamp": datetime.datetime.utcnow()
#         })

#         # Send to Kafka topic
#         producer.send('meal_plans', {
#     "ingredients": ingredients,
#     "diet": diet,
#     "meal_plan": meal_plan
# })
#         producer.flush()
#         print("✅ Sent meal plan to Kafka topic 'meal_plans'")

#         return jsonify({"meal_plan": meal_plan})
#     except Exception as e:
#         print(f"🔥 Error in /generate-meal: {e}")
#         return jsonify({"error": str(e)}), 500

# # Try Kafka 2
# @app.route('/generate-meal', methods=['POST'])
# def generate_meal():
#     try:
#         data = request.json
#         ingredients = data.get("ingredients", [])
#         diet = data.get("diet", "balanced")

#         prompt = f"Suggest a healthy {diet} meal using these ingredients: {', '.join(ingredients)}. Make sure to give proper instruction with time duration as well. The Response Should Be Limited to 250 Words."

#         response = requests.post("http://localhost:11434/api/generate", json={
#             "model": "llama3.1:8b",
#             "prompt": prompt,
#             "stream": False
#         })

#         result = response.json()
#         meal_plan = result.get("response")

#         # Save to MongoDB
#         recipes_collection.insert_one({
#             "ingredients": ingredients,
#             "diet": diet,
#             "prompt": prompt,
#             "response": meal_plan,
#             "timestamp": datetime.datetime.utcnow()
#         })

#         # Send to Kafka topic
#         producer.send('meal_plans', value=json.dumps({
#             "ingredients": ingredients,
#             "diet": diet,
#             "meal_plan": meal_plan
#         }).encode('utf-8'))
        
#         producer.flush()
#         print("✅ Sent meal plan to Kafka topic 'meal_plans'")

#         return jsonify({"meal_plan": meal_plan})
#     except Exception as e:
#         print(f"🔥 Error in /generate-meal: {e}")
#         return jsonify({"error": str(e)}), 500

# Working Previous Meal Fetch Without Kafka
@app.route('/previous-recipes', methods=['GET'])
def previous_recipes():
    try:
        recipes_cursor = recipes_collection.find()
        recipes = []
        for recipe in recipes_cursor:
            recipes.append({
                "response": recipe.get('response', '')
            })
        return jsonify({'recipes': recipes})
    except Exception as e:
        import traceback
        print(f"Error fetching previous recipes: {e}")
        traceback.print_exc()  # 👈 Add this
        return jsonify({'recipes': []}), 500

# Initialize Kafka consumer inside the route (better for fresh reads)
# Try 1 Kafka
# @app.route('/previous-recipes', methods=['GET'])
# def previous_recipes():
#     try:
#         consumer = KafkaConsumer(
#             'meal_plans',
#             bootstrap_servers='localhost:9092',
#             auto_offset_reset='earliest',
#             enable_auto_commit=False,  # don't auto commit offsets
#             group_id=None,             # no consumer group = always fresh
#             value_deserializer=lambda m: json.loads(m.decode('utf-8'))
#         )

#         recipes = []

#         # Poll all available messages
#         records = consumer.poll(timeout_ms=3000)

#         for topic_partition, messages in records.items():
#             for message in messages:
#                 data = message.value
#                 recipes.append(data.get('meal_plan', ''))

#         consumer.close()

#         return jsonify({'recipes': recipes})
#     except Exception as e:
#         print(f"Error fetching previous recipes: {e}")
#         return jsonify({'recipes': []}), 500

# Try 2 Kafka 
# @app.route('/previous-recipes', methods=['GET'])
# def previous_recipes():
#     try:
#         # Initialize a new Kafka consumer each time the route is called
#         consumer = KafkaConsumer(
#             'meal_plans',                            # Topic name
#             bootstrap_servers='localhost:9092',      # Kafka broker
#             auto_offset_reset='earliest',             # Start from the beginning of the topic
#             enable_auto_commit=False,                 # Don't commit offsets
#             group_id=None,                            # No group, fetches fresh each time
#             value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Convert bytes -> JSON
#         )

#         recipes = []

#         # Poll all available messages
#         records = consumer.poll(timeout_ms=5000)  # Wait up to 3 seconds for any messages

#         for topic_partition, messages in records.items():
#             for message in messages:
#                 data = message.value
#                 recipes.append(data.get('meal_plan', ''))

#         consumer.close()  # Always close the consumer after use

#         return jsonify({'recipes': recipes})
#     except Exception as e:
#         print(f"Error fetching previous recipes: {e}")
#         return jsonify({'recipes': []}), 500

# Try 3 Kafka
# @app.route('/previous-recipes', methods=['GET'])
# def previous_recipes():
#     try:
#         consumer = KafkaConsumer(
#             'meal_plans',
#             bootstrap_servers='localhost:9092',
#             auto_offset_reset='earliest',
#             enable_auto_commit=False,
#             group_id='meal_planner_consumer_' + str(random.randint(1, 100000)),  # random group_id
#             value_deserializer=lambda m: json.loads(m.decode('utf-8'))
#         )

#         recipes = []

#         end_time = datetime.datetime.now() + datetime.timedelta(seconds=3)
#         while datetime.datetime.now() < end_time:
#             msg_pack = consumer.poll(timeout_ms=500)
#             for tp, messages in msg_pack.items():
#                 for message in messages:
#                     data = message.value
#                     recipes.append(data.get('meal_plan', ''))

#         consumer.close()

#         return jsonify({'recipes': recipes})
#     except Exception as e:
#         print(f"🔥 Error fetching previous recipes: {e}")
#         return jsonify({'recipes': []}), 500

# @app.route('/generate-meal', methods=['POST'])
# def generate_meal():
#     try:
#         data = request.json
#         ingredients = data.get("ingredients", [])
#         diet = data.get("diet", "balanced")

#         prompt = f"Suggest a healthy {diet} meal using these ingredients: {', '.join(ingredients)}. Make sure to give proper instruction with time duration as well. The Response Should Be Limited to 500 Words."

#         response = requests.post("http://localhost:11434/api/generate", json={
#             "model": "llama3.1:8b",
#             "prompt": prompt,
#             "stream": False
#         })

#         print("Response Status Code:", response.status_code)
#         print("Response JSON:", response.text)

#         result = response.json()
        
#         if not result.get("response"):
#             return jsonify({"error": "Model response was empty."}), 500

#         # Save to MongoDB
        # recipes_collection.insert_one({
        #     "ingredients": ingredients,
        #     "diet": diet,
        #     "prompt": prompt,
        #     "response": result.get("response"),
        #     "timestamp": datetime.datetime.utcnow()
        # })

#         return jsonify({"meal_plan": result.get("response")})
#     except Exception as e:
#         print("❌ Error during meal generation:", str(e))
#         return jsonify({"error": str(e)}), 500


@app.route('/generate-from-voice', methods=['POST'])
def generate_from_voice():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"recipe": None}), 400

        # Create a detailed prompt with instructions
        full_prompt = f"Based on the following input, generate a detailed recipe with ingredients and instructions: {prompt}. Make sure it includes steps, time duration, and stays under 500 words."

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.1:8b",
            "prompt": full_prompt,
            "stream": False
        })

        result = response.json()
        return jsonify({"recipe": result.get("response")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Load Vosk model globally
vosk_model = Model("models/vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(vosk_model, 16000)
q = queue.Queue()

def record_audio(duration=5):
    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        audio_data = b''
        for _ in range(int(duration * 16000 / 8000)):
            audio_data += q.get()
        return audio_data

@app.route('/transcribe-audio', methods=['GET'])
def transcribe_audio():
    rec.Reset()  # Clears any previous context

    try:
        print("🎤 Recording...")
        audio = record_audio(duration=5)

        if rec.AcceptWaveform(audio):
            result = json.loads(rec.Result())
            print("✅ Full result:", result)
            text = result.get("text", "")
        else:
            partial = json.loads(rec.PartialResult())
            print("⚠️ Partial result:", partial)
            text = partial.get("partial", "")

        return jsonify({"transcription": text if text else "Could not recognize speech."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
