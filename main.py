import os
import json
import subprocess
import platform
import datetime
import webbrowser
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from openai import OpenAI

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------------------------------------
# COMPREHENSIVE ACTION TOOL DEFINITIONS
# ---------------------------------------------------------

def play_youtube_song(song_name: str):
    """Searches and opens a specific song or video on YouTube."""
    try:
        query_encoded = song_name.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={query_encoded}"
        webbrowser.open(url)
        return f"Accessing YouTube networks. Playing {song_name}, Sir."
    except Exception as e:
        return f"Failed to access YouTube: {str(e)}"

def send_email_tool(recipient: str, subject: str, body: str):
    """Opens mail client to draft and send an email."""
    try:
        import urllib.parse
        sub_enc = urllib.parse.quote(subject)
        body_enc = urllib.parse.quote(body)
        webbrowser.open(f"mailto:{recipient}?subject={sub_enc}&body={body_enc}")
        return f"Prepared email transmission pipeline for {recipient}."
    except Exception as e:
        return f"Email dispatch error: {str(e)}"

def send_whatsapp_message(contact_name: str, message: str):
    """Launches WhatsApp web dashboard for messaging."""
    try:
        webbrowser.open("https://web.whatsapp.com/")
        return f"Opened WhatsApp Web interface to dispatch message to {contact_name}."
    except Exception as e:
        return f"WhatsApp protocol error: {str(e)}"

def open_application(app_name: str):
    """Launches local system applications."""
    app = app_name.lower()
    system = platform.system()
    try:
        if "notepad" in app or "text" in app:
            if system == "Windows": subprocess.Popen(["notepad.exe"])
            elif system == "Darwin": subprocess.Popen(["open", "-a", "TextEdit"])
            else: subprocess.Popen(["gedit"])
        elif "calculator" in app:
            if system == "Windows": subprocess.Popen(["calc.exe"])
            elif system == "Darwin": subprocess.Popen(["open", "-a", "Calculator"])
        elif "browser" in app or "chrome" in app:
            webbrowser.open("https://www.google.com")
        else:
            webbrowser.open(f"https://www.google.com/search?q={app_name}")
        return f"Successfully executed protocol to open {app_name}, Sir."
    except Exception as e:
        return f"Could not launch application: {str(e)}"

def save_system_note(note_content: str):
    """Saves text notes or reminders locally."""
    try:
        with open("jarvis_logs.txt", "a") as f:
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {note_content}\n")
        return "Noted and saved securely to system logs, Sir."
    except Exception as e:
        return f"Failed to log note: {str(e)}"

def get_current_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current system time is {now}."

# Mapping for Tool Calls
available_tools = {
    "play_youtube_song": play_youtube_song,
    "send_email_tool": send_email_tool,
    "send_whatsapp_message": send_whatsapp_message,
    "open_application": open_application,
    "save_system_note": save_system_note,
    "get_current_time": get_current_time,
}

# OpenAI schema format for OpenRouter tool routing
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "play_youtube_song",
            "description": "Play a specific song, artist, or video query on YouTube.",
            "parameters": {
                "type": "object",
                "properties": {"song_name": {"type": "string", "description": "Name of song or video."}},
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email_tool",
            "description": "Send or draft an email with recipient, subject, and body content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string", "description": "Email address of target."},
                    "subject": {"type": "string", "description": "Email subject line."},
                    "body": {"type": "string", "description": "Main message text content."}
                },
                "required": ["recipient", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_whatsapp_message",
            "description": "Send a message or file reference via WhatsApp.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_name": {"type": "string", "description": "Recipient contact name."},
                    "message": {"type": "string", "description": "Message content to send."}
                },
                "required": ["contact_name", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Open local computer programs like Notepad, Calculator, or Web Browser.",
            "parameters": {
                "type": "object",
                "properties": {"app_name": {"type": "string", "description": "Name of the app."}},
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_system_note",
            "description": "Save text notes or reminders locally to storage.",
            "parameters": {
                "type": "object",
                "properties": {"note_content": {"type": "string", "description": "Content of note."}},
                "required": ["note_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current local time.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

# ---------------------------------------------------------
# WEBSOCKET CONTROL & REASONING LOOP
# ---------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are JARVIS, an advanced, elite AI assistant. Address the user respectfully as 'Sir'. "
                "When given tasks like playing songs, sending emails, opening applications, or saving notes, "
                "you MUST utilize the provided tool-calling functions to execute them directly. "
                "Keep your responses sharp, efficient, and conversational."
            )
        }
    ]

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_prompt = payload.get("prompt", "")
            api_key = payload.get("api_key", "")

            if not user_prompt:
                continue

            messages.append({"role": "user", "content": user_prompt})

            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )

            # Query OpenRouter using free auto-router with tools capability enabled
            response = client.completions.create if False else client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=tools_schema,
                tool_choice="auto",
                extra_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "JARVIS AI Automation",
                }
            )

            response_message = response.choices[0].message
            
            # Check if model wants to trigger tool execution
            if response_message.tool_calls:
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments or "{}")
                    
                    if func_name in available_tools:
                        tool_output = available_tools[func_name](**func_args)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": func_name,
                            "content": tool_output
                        })
                
                # Fetch final feedback narrative after tool execution
                second_response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=messages
                )
                reply = second_response.choices[0].message.content
            else:
                reply = response_message.content

            messages.append({"role": "assistant", "content": reply})
            await websocket.send_json({"reply": reply})

    except WebSocketDisconnect:
        print("Web client disconnected.")