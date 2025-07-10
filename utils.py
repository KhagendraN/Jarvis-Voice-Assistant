# Standard Library
import os
import re
import shlex
import time
import json
import queue
import asyncio
import string
import tempfile
import subprocess
import threading
import collections
from datetime import datetime, timedelta
import webbrowser
import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from intent_classifier import detect_intent
import psutil
import pyjokes
#from googletrans import Translator
import fitz  # PyMuPDF
import socket
import secrets
import markdown 
import wikipedia
import cv2

# Third-party Libraries
import aiohttp
import openai
import schedule
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from googlesearch import search
from duckduckgo_search import DDGS
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
#from playsound import playsound
import webrtcvad
import keyword
import ast
import tokenize
import io
import textwrap
import black
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

# Local Imports
import config
#import web_ui

MISTRAL_API_KEY = config.MISTRAL_API_KEY

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Script paths - now relative to project directory
MUSIC_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "music_player.sh")
WALLPAPER_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "wallpaper_selector.sh")
SCREENSHOT_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "screenshot.sh")
VOLUME_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "volume_control.sh")
BRIGHTNESS_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "brightness_control.sh")

# Other paths
CONTACTS_FILE = os.path.join(PROJECT_ROOT, "contact.json")
VOSK_MODEL_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "vosk-model-small-en-us-0.15")

# Weather Information
async def get_weather(city="Kathmandu"):
    """
    Fetch current weather details for a given city using OpenWeatherMap API.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_API_KEY}&units=metric"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"📡 API Status: {response.status}")  # Debug print

                if response.status == 200:
                    data = await response.json()
                    print("✅ Weather API response received")

                    weather_description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']

                    return (
                        f"The current weather in {city} is {weather_description} "
                        f"with a temperature of {temperature}°C and humidity of {humidity}%."
                    )
                else:
                    error_text = await response.text()
                    print(f"❌ API Error: {error_text}")
                    return "Sorry, I couldn't fetch the weather details at the moment."

    except Exception as e:
        print(f"❗ Exception in get_weather: {e}")
        return "An error occurred while trying to get the weather."

#open application
def open_application(app_name):
    """
    Opens a specified application based on the user's voice command.
    """
    try:
        subprocess.run([app_name], check=True)
        return "Opening {app_name} for you."
    except Exception as e:
        print(f"Error opening application: {e}")
        return "Sorry, I couldn't open {app_name}."
        
# web search using google 
def web_search(query):
    """
    Perform a DuckDuckGo search, speak the top result, and return its link.
    
    Returns:
        str: The URL of the top search result, or None if not found.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
        
        if results:
            top = results[0]
            title = top.get("title", "No title")
            snippet = top.get("body", "")
            link = top.get("href", None)

            summary = f"{title}: {snippet}"
            return summary, link
            
        else:
            return "Sorry, I couldn't find anything useful.", None

    except Exception as e:
        return "There was an issue while searching the web." , None



#function to read unread mails 
def get_date_n_days_ago(n=7):
    date_n_days_ago = (datetime.now() - timedelta(days=n)).strftime("%d-%b-%Y")
    return date_n_days_ago

def count_recent_unread_emails(imap_server: str, email: str, password: str, days=7) -> int:
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email, password)
        mail.select("inbox")

        since_date = get_date_n_days_ago(days)
        search_criteria = f'(UNSEEN SINCE {since_date})'
        status, response = mail.search(None, search_criteria)

        if status != "OK":
            print("Failed to search mailbox.")
            return 0

        unread_msg_nums = response[0].split()
        mail.logout()
        return len(unread_msg_nums)

    except Exception as e:
        print(f"Error: {e}")
        return 0
    

def read_recent_unread_emails(imap_server: str, email_address: str, password: str, days=7, max_to_read=5):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        mail.select("inbox")

        since_date = get_date_n_days_ago(days)
        search_criteria = f'(UNSEEN SINCE {since_date})'
        status, response = mail.search(None, search_criteria)

        if status != "OK":
            print("Failed to search emails.")
            return

        unread_msg_nums = response[0].split()
        #print(f"\nFound {len(unread_msg_nums)} unread emails from the past {days} days.\n")

        for num in unread_msg_nums[:max_to_read]:
            status, data = mail.fetch(num, '(RFC822)')
            if status != "OK":
                print(f"Could not fetch email with ID {num.decode()}")
                continue

            msg = email.message_from_bytes(data[0][1])
            subject = email.header.decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            from_ = msg.get("From")
            date_ = msg.get("Date")

            return from_, subject, date_, unread_msg_nums

        mail.logout()

    except Exception as e:
        return "Error: {e}"

    
# function to send email 
def send_email(email_user, email_password, to_address, subject, body):
    """
    Send an email using SMTP.
    
    Args:
        email_user (str): The sender's email address.
        email_password (str): The sender's email password.
        to_address (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body of the email.
    
    Returns:
        str: Success or failure message.
    """
    try:
        # Set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)  
        server.starttls()  
        server.login(email_user, email_password)

        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = to_address
        msg["Subject"] = subject

        # Attach the email body
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        server.sendmail(email_user, to_address, msg.as_string())

        server.quit()

        return "Email sent successfully."

    except Exception as e:
        print(f"Error: {e}")
        return "Failed to send email."

# function to load contacts 
def load_contacts(filename=CONTACTS_FILE):
    with open(filename, "r") as f:
        return json.load(f)

# function to listen 
def listen(model="tiny", language="en"):
    # Vosk configuration
    vosk_model_paths = {
        "en": VOSK_MODEL_PATH
        #"en": "/home/khagendra/Downloads/vosk-model-small-en-in-0.4"
        # You can extend this with other language paths if needed
    }

    if language not in vosk_model_paths:
        raise ValueError(f"No Vosk model path configured for language: {language}")

    vosk_model_path = vosk_model_paths[language]
    print("🔁 Loading Vosk model...")
    vosk_model = Model(vosk_model_path)
    vosk_recognizer = KaldiRecognizer(vosk_model, 16000)
    vosk_recognizer.SetWords(True)

    print(f"🧠 Loading Whisper model ({model})...")
    whisper_model = whisper.load_model(model)

    # Audio stream setup
    q = queue.Queue()
    samplerate = 16000
    blocksize = 8000

    def audio_callback(indata, frames, time, status):
        if status:
            print("⚠️", status)
        q.put(bytes(indata))

    def save_audio_to_temp_file(audio_chunks):
        audio = b''.join(audio_chunks)
        audio_np = np.frombuffer(audio, dtype=np.int16)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            write(tmpfile.name, samplerate, audio_np)
            return tmpfile.name

    print("\n🎙️ Speak into the mic... (Ctrl+C to stop)\n")
    audio_chunks = []

    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=blocksize, dtype='int16',
                               channels=1, callback=audio_callback):
            while True:
                data = q.get()
                audio_chunks.append(data)

                if vosk_recognizer.AcceptWaveform(data):
                    result = json.loads(vosk_recognizer.Result())
                    final_text = result.get("text", "").strip()
                    if final_text:
                        print(f"\n✅ Vosk Final: {final_text}")
                        
                        print("🧠 Passing to Whisper for better transcription...")
                        audio_path = save_audio_to_temp_file(audio_chunks)
                        whisper_result = whisper_model.transcribe(audio_path, language=language)
                        whisper_text = whisper_result.get("text", "").strip()
                        os.remove(audio_path)

                        print(f"🔍 Whisper: {whisper_text}\n")
                        audio_chunks = []

                        # Return transcription if you want to exit after one sentence
                        return whisper_text

                else:
                    partial_result = json.loads(vosk_recognizer.PartialResult())
                    partial_text = partial_result.get("partial", "").strip()
                    if partial_text:
                        print(f"📝 Vosk Partial: {partial_text}", end="\r", flush=True)

    except KeyboardInterrupt:
        print("\n🛑 Stopped listening.")
        return None


async def get_mistral_response(prompt):
    """Get response from Mistral AI API"""
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "ministral-8b-latest",  # Corrected model name
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            data = await response.json()
            if "choices" in data:
                response_text = data["choices"][0]["message"]["content"].strip()
                return response_text
            return "Sorry, I couldn't process that request."

    
def clean_text_for_speech(text):
    """
    Cleans the input text by removing emojis, special characters, and markdown artifacts
    to make it sound more natural when spoken.
    """
    # Remove emojis and non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove Markdown-like symbols (optional)
    text = re.sub(r'[*_`#>\[\](){}]', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text
    
def trim_response(text, max_length=300):
    """
    Trims the response to a maximum number of characters.
    Adds ellipsis if the text is too long.
    """
    if len(text) > max_length:
        return text[:max_length].rsplit(' ', 1)[0] + "..."
    return text

def clean_input(text):
    # Remove punctuation and extra spaces
    return text.translate(str.maketrans("", "", string.punctuation)).strip().lower()

def get_date_n_days_ago(n=7):
    date_n_days_ago = (datetime.now() - timedelta(days=n)).strftime("%d-%b-%Y")
    return date_n_days_ago


def speak(text, model):
    """
    Convert text to speech using subprocess and Piper TTS.
    """
    try:
        # Safely escape the text using shlex.quote
        escaped_text = shlex.quote(text)

        # Use subprocess to execute the echo command and pipe it to piper
        command = f"echo {escaped_text} | piper --model {model} --output-raw | aplay -r 22050 -f S16_LE -t raw -"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while trying to speak: {e}")


# load_dotenv()
# def speak(textInput, voice_id_selected):
#     client = ElevenLabs(

#     api_key=config.ELEVENLABS_API_KEY,

#     )

#     audio = client.text_to_speech.convert(

#         text=textInput,

#         voice_id=voice_id_selected,

#         model_id="eleven_multilingual_v2",

#         output_format="mp3_44100_128",

#     )

#     play(audio)

        
def sleep_now(selected_model):
    model = "tiny"
    speak("Okay sir!", selected_model)
    while True:
            audio_input = listen(model, language="en")
            if not audio_input: 
                continue
            command = audio_input.lower()
            intent , confidence = detect_intent(command)
            if intent == "wake_up":
                speak("I'm here, sir!", selected_model)
                return 
            
def play_music(selected_model):
    """
    Launches the music player script to handle music playback.
    """
    model = whisper.load_model("tiny")
    try:
        subprocess.Popen([MUSIC_SCRIPT, "play"])
        speak("Launching your music player now. Enjoy the vibes.", selected_model)
        while True:
            audio_input = listen(model, language="en")
            if not audio_input:
                continue
            command = audio_input.lower()
            intent, confidence = detect_intent(command)
            if intent == "stop_music":
                stop_music()
                break
    except Exception as e:
        #speak("Sorry, I couldn't start the music.", selected_model)
        print(f"Error launching music script: {e}")


def stop_music(selected_model):
    """
    Stops currently playing music by running the music script with stop command.
    """
    try:
        subprocess.Popen([MUSIC_SCRIPT, "stop"])
        speak("Music stopped. Let me know if you'd like me to play something else.", selected_model)
    except Exception as e:
        speak("Sorry, I couldn't stop the music.", selected_model)
        print(f"Error stopping music: {e}")

def shutdown(selected_model):
    command = "poweroff"
    speak("shutting down sir!", selected_model)
    subprocess.run(command, shell=True, check=True)

def update():
    command = "sudo pacman -Syu"
    subprocess.run(command, shell=True,check=True)
    
def change_wallpaper(selected_model):
    subprocess.run([WALLPAPER_SCRIPT, "select"], check=True)
    speak("Please select the wallpaper", selected_model)
    speak("Applying your selected wallpaper", selected_model)
    
# remainder and task schedule 
reminders = []

def add_reminder(task, time_str, selected_model):
    schedule.every().day.at(time_str).do(speak, f"Reminder: {task}", selected_model)
    reminders.append((task, time_str))
    return f"Reminder set for {time_str}: {task}"

def list_reminders():
    return "\n".join([f"{t} at {tm}" for t, tm in reminders]) or "No reminders set."

def run_schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

# fetch latest news
async def get_top_news(api_key, country="us"):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                articles = data.get("articles", [])[:5]
                news_summary = "\n".join([f"{i+1}. {a['title']}" for i, a in enumerate(articles)])
                return news_summary
            return "Couldn't fetch news at the moment."
#Take a Screenshot
def take_screenshot():
    subprocess.run([SCREENSHOT_SCRIPT, "area"], check=True)
    return "screenshot saved successfully!"

# enable rainbow boarder
def rainbow():
    command = "/home/khagendra/.config/hypr/UserScripts/RainbowBorders.sh"
    subprocess.run(command, shell=True, check=True)
    return "Rainbow boarder activated successfully!"

# add volume 
def increase_volume():
    subprocess.run([VOLUME_SCRIPT, "increase", "5"], check=True)
    return "Volume increased by 5 percent"

# decrease volume
def decrease_volume():
    subprocess.run([VOLUME_SCRIPT, "decrease", "5"], check=True)
    return "Volume decreased by 5 percent"

# get battery status
def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        battery_percentage = round(battery.percent,2)
        battery_plugged_status = battery.power_plugged
        if(battery_plugged_status):
            return battery_percentage, "Charger plugged in."
        else:
            return battery_percentage, "Charger is not plugged in."
    except Exception as e:
        return f"Could not retrieve battery status: {e}"

# get wiki summery
def wiki_summary(query, sentences=2):
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return clean_text_for_speech(summary)
    except Exception as e:
        return f"Sorry, couldn't find anything on that topic. {e}"

# get ip address
def get_ip():
    import socket
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Your IP address is {ip_address}"
    except Exception as e:
        return f"Couldn't retrieve IP: {e}"
# get system status
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return f"CPU usage: {cpu}%, RAM usage: {ram}%, Disk usage: {disk}%"

# google translator
def translate_text(text, dest_language="es"):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return f"Translation to {dest_language}: {translation.text}"
    except Exception as e:
        return f"Translation failed: {e}"

# count down function
def start_timer(seconds, selected_model):
    speak(f"Timer set for {seconds} seconds.", selected_model)
    time.sleep(seconds)
    speak("Time's up!", selected_model)
    
# for jokes
def tell_joke():
    return pyjokes.get_joke()
# create note
def create_note(content):
    filename = f"note_{int(time.time())}.txt"
    path = os.path.join(os.path.expanduser("~/Documents/Notes"), filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)

    return f"Note saved as {filename}"

# control brightness
def increase_brightness():
    subprocess.run([BRIGHTNESS_SCRIPT, "increase", "100"], check=True)
    return "Brightness increased by 1 percent"

# decrease volume
def decrease_brightness():
    subprocess.run([BRIGHTNESS_SCRIPT, "decrease", "100"], check=True)
    return "Brightness decreased by 1 percent"

# get current date and time
def get_current_datetime():
    now = datetime.now()
    return now.strftime("It's %A, %B %d, %Y and the time is %I:%M %p")

# search on youtube
def play_youtube(query):
    try:
        search_cmd = f'yt-dlp "ytsearch:{query}" --get-id'
        video_id = subprocess.check_output(search_cmd, shell=True).decode().strip().split("\n")[0]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        subprocess.Popen(["mpv", video_url])
        return f"Playing: {query}"
    except Exception as e:
        return f"Couldn't play YouTube video: {e}"

# find file by name
def find_file(filename, search_path="~"):
    search_path = os.path.expanduser(search_path)
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if filename.lower() in file.lower():
                return os.path.join(root, file)
    return "No file found matching that name."
# clipboard manager
def get_clipboard():
    try:
        result = subprocess.check_output("xclip -selection clipboard -o", shell=True)
        return result.decode("utf-8")
    except Exception as e:
        return f"Clipboard error: {e}"

# currency converter
async def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if "result" in data:
                return f"{amount} {from_currency} = {data['result']:.2f} {to_currency}"
            return "Failed to convert currency."
# generate ai image
async def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/images/generations", json=payload, headers=headers) as res:
            data = await res.json()
            return data["data"][0]["url"]
# delete all notes
def self_destruct(folder="~/Documents/Notes"):
    folder_path = os.path.expanduser(folder)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            os.remove(os.path.join(root, file))
    return "All notes deleted. Mission accomplished. 💣"

# pdf reader
def read_pdf(path, max_pages=5):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc[:max_pages]:
            text += page.get_text()
        return text[:1000] + "..." if len(text) > 1000 else text
    except Exception as e:
        return f"Error reading PDF: {e}"

# weather forecast
async def get_weather_forecast(city="Kathmandu", days=3):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={config.WEATHER_API_KEY}&units=metric"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                forecasts = data.get("list", [])[:days*8:8]  # Get daily approx
                summary = []
                for forecast in forecasts:
                    date = forecast["dt_txt"].split(" ")[0]
                    desc = forecast["weather"][0]["description"]
                    temp = forecast["main"]["temp"]
                    summary.append(f"{date}: {desc}, {temp}°C")
                return "\n".join(summary)
    except Exception as e:
        return f"Forecast error: {e}"
# auto update assistant to git repo
def update_assistant_code():
    try:
        subprocess.run(["git", "-C", PROJECT_ROOT, "pull"], check=True)
        return "Assistant updated with latest changes."
    except Exception as e:
        return f"Update failed: {e}"
# time based greeting
def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    elif 18 <= hour < 22:
        return "Good evening!"
    else:
        return "Working late? Good night!"
    

# system up time 
def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours} hours {minutes} minutes and {secs} seconds"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_str = convert_seconds(uptime_seconds)
            return f"System has been up for {uptime_str}"
    except Exception as e:
        return f"Couldn't retrieve uptime: {e}"


# port scanner 
def scan_ports(host, ports=[22, 80, 443, 8080]):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
    return f"Open ports on {host}: {open_ports}" if open_ports else "No common ports open."

# get public ip
def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Failed to get public IP."
# scan wifi
def scan_wifi():
    try:
        output = subprocess.check_output(["nmcli", "-f", "SSID,SIGNAL", "dev", "wifi"]).decode("utf-8")
        return output.strip()
    except Exception as e:
        return f"Error scanning Wi-Fi: {e}"
# voice note
def save_voice_note(text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"voice_note_{timestamp}.txt"
    path = os.path.join(os.path.expanduser("~/Documents/VoiceNotes"), filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    return f"Saved voice note: {filename}"

# daily motivation 
def get_daily_affirmation():
    affirmations = [
        "You are capable of achieving amazing things.",
        "Keep pushing forward, no matter what.",
        "Today is full of opportunities waiting for you.",
        "You are stronger than you think.",
        "Your potential is limitless."
    ]
    return np.random.choice(affirmations)
# battery saver toggle
def toggle_battery_saver(mode="on"):
    try:
        if mode == "on":
            subprocess.run(["sudo", "tlp", "start"])
            return "Battery saver activated."
        else:
            subprocess.run(["sudo", "tlp", "stop"])
            return "Battery saver deactivated."
    except Exception as e:
        return f"Battery saver error: {e}"
# play sound
def play_ambient_sound(type="rain"):
    sounds = {
        "rain": "/path/to/rain.mp3",
        "ocean": "/path/to/ocean.mp3",
        "forest": "/path/to/forest.mp3"
    }
    if type in sounds:
        subprocess.Popen(["mpv", sounds[type]])
        return f"Playing {type} ambiance..."
    return "Sound type not found."

# capture photo 
def take_webcam_photo():
    filename = f"webcam_{int(time.time())}.jpg"
    pictures_dir = os.path.expanduser("~/Pictures")
    os.makedirs(pictures_dir, exist_ok=True)
    path = os.path.join(pictures_dir, filename)

    # Open default camera (0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Error: Could not open webcam."

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Error: Failed to capture image."

    cv2.imwrite(path, frame)
    return f"Photo saved to picture directory", path

# back up important file 
def backup_files(source_folder, backup_folder):
    try:
        source = os.path.expanduser(source_folder)
        backup = os.path.expanduser(backup_folder)
        os.makedirs(backup, exist_ok=True)
        subprocess.run(["rsync", "-av", source, backup])
        return "Backup completed."
    except Exception as e:
        return f"Backup failed: {e}"
# download instagram reels
def download_instagram_reel(url):
    try:
        subprocess.run(["yt-dlp", url, "-o", "~/Downloads/reel.%(ext)s"], check=True)
        return "Instagram reel downloaded."
    except Exception as e:
        return f"Failed to download reel: {e}"

# toggle night mode
#---------------------- add here

# mark down to html converter 
def convert_md_to_html(md_text):
    return markdown.markdown(md_text)

# generate password 
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(chars) for _ in range(length))

# check updates
def check_linux_updates():
    try:
        output = subprocess.check_output(["checkupdates"]).decode()
        return output if output else "System is up to date!"
    except:
        return "Unable to check updates. Try running as root or installing checkupdates tool."

# handle unknown request 
OUTPUT_DIR = "AIGenerated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def is_valid_python_line(line: str) -> bool:
    try:
        ast.parse(line)
        return True
    except:
        return False


def split_statements(line: str):
    # Split multiple statements jammed together on a single line
    parts = re.split(
        r'(?<=[\)\w\"])\s+(?=\w+\s*=|plt\.|np\.|print\(|return\b|import\b|from\b)',
        line,
    )
    return [part.strip() for part in parts if part.strip()]


def clean_code_format(code: str) -> str:
    lines = code.split('\n')
    cleaned_lines = []
    indent_level = 0
    indent_str = "    "

    for raw_line in lines:
        raw_line = raw_line.strip()

        # Skip empty lines
        if not raw_line:
            cleaned_lines.append("")
            continue

        # Break apart mashed-up statements
        sub_lines = split_statements(raw_line)

        for line in sub_lines:
            # Check for block headers like def, if, for, etc.
            if re.match(r'^(def|if|for|while|with|try|except|elif|else)\b.*:\s*$', line):
                cleaned_lines.append(indent_str * indent_level + line)
                indent_level += 1
                continue

            # If there's a block header with code after colon, split and indent
            if ":" in line and any(line.strip().startswith(k) for k in ['def', 'if', 'for', 'while', 'with']):
                header, rest = line.split(":", 1)
                cleaned_lines.append(indent_str * indent_level + header.strip() + ":")
                indent_level += 1
                # Handle rest of line after :
                if rest.strip():
                    sub_rest = split_statements(rest.strip())
                    for rest_line in sub_rest:
                        cleaned_lines.append(indent_str * indent_level + rest_line.strip())
                continue

            # Reduce indentation if block is ending (we guess based on `if __name__ == "__main__"` or dedents)
            if line.startswith("return") or line.startswith("pass"):
                cleaned_lines.append(indent_str * indent_level + line)
                indent_level = max(0, indent_level - 1)
                continue

            # Comment out non-code garbage lines
            if not is_valid_python_line(line):
                cleaned_lines.append(indent_str * indent_level + "# " + line)
                continue

            cleaned_lines.append(indent_str * indent_level + line)

    return "\n".join(cleaned_lines)

def format_with_black(code: str) -> str:
    try:
        return black.format_str(code, mode=black.Mode())
    except black.InvalidInput:
        return "# Failed to format with black\n" + code



async def handle_unknown_request(command, selected_model):
    """Handle unknown requests by generating Python code."""
    try:
        # Check if the command is code-worthy
        if not is_code_worthy(command):
            return "I'm not sure how to help with that. Could you please rephrase your request?"
        
        # Generate Python code using Mistral
        prompt = f"""
        Generate a Python script to: {command}
        
        Requirements:
        - Only return the Python code, no explanations
        - Make it functional and executable
        - Include necessary imports
        - Handle errors gracefully
        - Use best practices
        """
        
        response = await get_mistral_response(prompt)
        
        # Clean and format the code
        cleaned_code = clean_code_format(response)
        
        # Save the code to a temporary file
        temp_file = f"/tmp/jarvis_generated_{int(time.time())}.py"
        with open(temp_file, 'w') as f:
            f.write(cleaned_code)
        
        # Execute the generated code
        result = subprocess.run(['python3', temp_file], 
                              capture_output=True, text=True, timeout=30)
        
        # Clean up
        os.remove(temp_file)
        
        if result.returncode == 0:
            return f"Task completed successfully! Output: {result.stdout}"
        else:
            return f"Task completed but with errors: {result.stderr}"
            
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"
