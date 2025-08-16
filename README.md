

---

````markdown
# 🤖 Local AI-Based Assistant (Smart Meal Planner + Voice Assistant)

A privacy-friendly, offline-first AI-powered assistant that helps you **plan meals smartly**, **interact via voice**, and **generate healthy recipes** based on dietary needs — powered by LLMs, Kafka, Vosk, and more.

---

## 🌟 Key Features

- 🧠 **Offline AI**: Uses LLaMA 3 (8B) locally via Ollama.
- 🗣️ **Voice Commands**: Interact with your assistant using Vosk (offline speech-to-text).
- 📊 **Smart Meal Planning**: Get meal suggestions based on time, diet, and health goals.
- 🧾 **Recipe Generator**: Generates recipes from voice commands or typed input.
- 🧱 **Microservices Architecture**: Modular design using Kafka and Flask-based services.
- 🌐 **Web Interface**: User-friendly front-end built with Flask and Bootstrap.
- 🔕 **Privacy Respecting**: No data leaves your machine. Entirely local.

---

## 🛠️ Tech Stack

| Component           | Tech                                |
|---------------------|-------------------------------------|
| LLM Engine          | Ollama + LLaMA 3 (8B)               |
| Voice Recognition   | Vosk                                |
| Backend             | Python (Flask, FastAPI)             |
| Messaging           | Kafka                               |
| Data Flow           | JSON-based microservices            |
| UI                  | Flask + HTML/CSS/JS + Bootstrap     |
| Offline LLM         | Ollama API via local network        |

---

## 📦 Requirements

- Python 3.9+
- Git
- [Git LFS](https://git-lfs.github.com/)
- Kafka (locally running)
- Ollama with LLaMA 3.1 8B installed
- `ffmpeg` (for Vosk)
- Virtualenv (optional but recommended)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/JenishDuvani/local-ai-based-assistant.git
cd local-ai-based-assistant
````

### 2. Install Git LFS and Fetch Large Files

```bash
git lfs install
git lfs pull
```

---

### 3. Set Up Python Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS

pip install -r requirements.txt
```

---

### 4. Set Up Ollama (if not already)

* Install from: [https://ollama.com](https://ollama.com)
* Start Ollama server
* Pull model:

```bash
ollama run llama3
```

Verify by:

```bash
curl http://localhost:11434/api/tags
```

---

### 5. Run Kafka (Locally)

Start Zookeeper and Kafka server:

```bash
# Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Kafka
bin/kafka-server-start.sh config/server.properties
```

> Or use Docker if configured in the project.

---

### 6. Start the Project

In one terminal (API/Backend):

```bash
python app.py
```

In another terminal (voice assistant or microservices):

```bash
python voice_service.py
python recipe_generator_service.py
```

---

## 🧪 Testing the App

* Open your browser and go to: [http://localhost:3001](http://localhost:3001)
* Try speaking or typing something like:

  > "Suggest me a healthy breakfast"
* The assistant will process it using Vosk + LLaMA 3.

---

## 📁 Project Structure

```bash
smart-meal-planner/
├── app.py                      # Main Flask app
├── ollama-llm/                 # LLM communication
├── kafka/                      # Kafka services
├── vosk-stt/                   # Speech-to-text services
├── templates/                  # HTML UI
├── static/                     # CSS, JS
└── requirements.txt
```

---

## 🧠 Future Enhancements

* Add calorie and nutrition-based filtering
* Expand voice commands with NLP classification
* Dockerize full stack with Kafka, Flask, Ollama
* Android PWA interface

---

## ⚠️ Git LFS Note

This project uses [Git Large File Storage](https://git-lfs.github.com/) to manage `.jar`, `.bin`, and model files over 50MB.

Make sure to run:

```bash
git lfs install
git lfs pull
```

---

## 👨‍💻 Contributors

* Jenish Duvani
* Hetashvi Bhagat

  Student of Master Of Computer Applications,
  Insitute of Technology, Nirma University ,Ahemdabad

---

## 📄 License

This project is for educational and personal use. All models used (e.g., LLaMA 3) are subject to their respective licenses.

---

```
