# 🤖 J.A.R.V.I.S. - Autonomous AI Voice Assistant

An advanced, full-featured **JARVIS-style AI Assistant** built with Python, FastAPI, WebSockets, and modern Web Speech APIs. Powered by OpenRouter (`openrouter/free`), JARVIS features a HUD interface, deep male voice synthesis, live speech recognition, and real-world task automation (YouTube playback, email drafting, app launching, and system logging).

![JARVIS Assistant Banner](https://img.shields.io/badge/JARVIS-AI--OS-00f3ff?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## ✨ Features

- **🎙️ Real-time Live Speech-to-Text:** Hands-free voice recognition directly inside the browser using Web Speech APIs.
- **🔊 Deep J.A.R.V.I.S. Voice Synthesis:** Configured speech synthesis tuned for a deep, commanding, non-robotic English male voice tone.
- **⚡ Autonomous Tool Execution:** Powered by OpenAI Function/Tool Calling schema via OpenRouter to perform real tasks on your PC:
  - **YouTube Automation:** Search and auto-play specific songs/videos.
  - **Email Dispatcher:** Draft and prepare structured emails.
  - **Application Launcher:** Open programs like Notepad, Calculator, or Chrome.
  - **Messaging Protocols:** Launch WhatsApp Web directly.
  - **System Logger:** Record reminders and quick notes to local storage.
  - **Time & Utilities:** Get real-time updates and clock information.
- **🌐 Interactive Sci-Fi HUD Interface:** Embedded Arc Reactor canvas visualizer with rotating HUD orbits, real-time status indicators, and an interactive terminal log.

---

## 📂 Project Structure

```text
jarvis-assistant/
│
├── static/
│   └── index.html      # Sci-Fi J.A.R.V.I.S. HUD Web Canvas UI
├── main.py             # FastAPI WebSocket Backend & Tool Execution Engine
├── README.md           # Project Documentation
└── requirements.txt    # Python Dependencies
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/usama1095/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
# Create Virtual Environment (Optional but recommended)
python -m venv venv

# Activate Virtual Environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install fastapi uvicorn websockets openai
```

---

## 🚀 Running J.A.R.V.I.S.

1. Start the FastAPI backend server using `uvicorn`:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your web browser (Google Chrome or Microsoft Edge recommended for voice support) and navigate to:
   ```text
   http://localhost:8000
   ```

3. Enter your **OpenRouter API Key** in the top-right field of the HUD interface.

4. Click the central **Arc Reactor / Microphone button** or type into the terminal input to give JARVIS instructions!

---

## 💬 Example Voice / Text Commands

- *"Play Blinding Lights by The Weeknd on YouTube"*
- *"Send an email to alex@example.com about the project report"*
- *"Open Notepad on my computer"*
- *"Open WhatsApp Web"*
- *"Save a note: Remember to submit the report by 5 PM"*
- *"What time is it right now?"*

---

## 🛠️ Configuration & API Key

JARVIS uses [OpenRouter](https://openrouter.ai/) for free model routing. Get your free API key at **openrouter.ai** and paste it into the UI setting input.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Developed with ❤️ by <a href="https://github.com/usama1095"><b>usama1095</b></a>
</p>
