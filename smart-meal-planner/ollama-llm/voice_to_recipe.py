import speech_recognition as sr
import requests
import json

def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now (e.g. 'Make something with chicken and spinach, keto diet'):")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError:
        print("❌ Speech Recognition service error")
    return None

def send_to_ollama(prompt_text):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.1:8b",  # or llama3:8b if you explicitly tagged it
        "prompt": f"Suggest a meal recipe based on this: {prompt_text}",
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.ok:
        output = response.json()["response"]
        print("\n🍽️ AI Recipe Suggestion:\n", output)
    else:
        print("❌ Failed to get recipe from Ollama")

# Run the tool
query = listen_to_user()
if query:
    send_to_ollama(query)
