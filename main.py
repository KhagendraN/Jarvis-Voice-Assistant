import sys

from intent_classifier import detect_intent
from utils import read_recent_unread_emails , clean_text_for_speech, trim_response, clean_input, speak, sleep_now, change_wallpaper
from utils import listen, get_mistral_response, get_weather, web_search, load_contacts, send_email, count_recent_unread_emails
from utils import play_music, stop_music, shutdown, update, add_reminder, list_reminders, run_schedule_loop, get_top_news
import config, asyncio, subprocess
from secondaryClassifier import is_code_worthy
from utils import get_battery_status, wiki_summary, get_ip, get_system_stats, start_timer, tell_joke, create_note
from utils import get_current_datetime, play_youtube, find_file, get_clipboard, convert_currency, generate_image, self_destruct
from utils import read_pdf, get_weather_forecast, update_assistant_code, get_time_based_greeting, get_uptime, scan_ports, get_public_ip
from utils import scan_wifi, save_voice_note, get_daily_affirmation, toggle_battery_saver, play_ambient_sound, take_webcam_photo
from utils import backup_files, download_instagram_reel, convert_md_to_html, generate_password, check_linux_updates, handle_unknown_request
from utils import decrease_volume, decrease_brightness, increase_volume, increase_brightness
from faceAuthorization.faceDetection import check_authorization
import os

EMAIL_USER = config.EMAIL_USER
EMAIL_PASSWORD = config.EMAIL_PASSWORD
imap_server = 'imap.gmail.com' 

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Voice model paths - now relative to project directory
VOICE_MODELS = {
    "Nepali_voice": os.path.join(PROJECT_ROOT, "voice_models", "ne_NP-google-medium.onnx"),
    "Samantha": os.path.join(PROJECT_ROOT, "voice_models", "en_US-hfc_female-medium.onnx"),
    "Jarvis": os.path.join(PROJECT_ROOT, "voice_models", "en_US-john-medium.onnx"),
    "male_Voice": os.path.join(PROJECT_ROOT, "voice_models", "en_US-bryce-medium.onnx"),
    "female_voice": os.path.join(PROJECT_ROOT, "voice_models", "en_US-amy-medium.onnx"),
    "kristin_voice": os.path.join(PROJECT_ROOT, "voice_models", "en_US-kristin-medium.onnx"),
    "normal_female": os.path.join(PROJECT_ROOT, "voice_models", "en_US-lessac-medium.onnx"),
    "AI_type": os.path.join(PROJECT_ROOT, "voice_models", "en_US-arctic-medium.onnx"),
}

# Default voice model
DEFAULT_VOICE = os.path.join(PROJECT_ROOT, "voice_models", "en_US-amy-medium.onnx")

# Voice change functionality
current_voice_index = 0
voice_model_names = list(VOICE_MODELS.keys())

def cycle_voice_model():
    """Cycle to the next voice model"""
    global current_voice_index
    current_voice_index = (current_voice_index + 1) % len(voice_model_names)
    voice_name = voice_model_names[current_voice_index]
    voice_path = VOICE_MODELS[voice_name]
    return voice_path, voice_name

def get_current_voice_info():
    """Get current voice model path and name"""
    voice_name = voice_model_names[current_voice_index]
    voice_path = VOICE_MODELS[voice_name]
    return voice_path, voice_name

# --- Setup checks for required files ---
missing = []
if not os.path.exists('config.py'):
    missing.append('config.py (copy from config_template.py and add your API keys)')
if not os.path.exists('contact.json'):
    missing.append('contact.json (copy from contact_template.json and add your contacts)')
if not os.path.exists(os.path.join('static', 'known_image.jpeg')):
    missing.append('static/known_image.jpeg (add your face image for face authentication)')
if missing:
    print("\nERROR: The following required files are missing:")
    for m in missing:
        print(f"  - {m}")
    print("\nPlease follow the setup instructions in the README.md.")
    sys.exit(1)

async def main():
    """Main interaction loop"""
    speak("Initialization sequence complete .. Connection established!", VOICE_MODELS["Jarvis"])

    while True:
        model = "tiny"

        # Wake word loop
        while True:
            selected_voice_model, current_voice_name = get_current_voice_info()
            audio_input = listen(model, language="en")
            if not audio_input:
                continue
            command = audio_input.lower()
            intent, confidence = detect_intent(command)
            print("Intent:", intent)
            if intent == "wake_up":
                if check_authorization(os.path.join(PROJECT_ROOT, "static", "known_image.jpeg")):
                    print("Authentication successful!!")
                    break
                else:
                    speak("Authentication failed!", selected_voice_model)
                    continue

        speak(get_time_based_greeting(), selected_voice_model)

        # Main conversation loop
        while True:
            command = listen(model, language="en")
            if not command:
                continue
            commandFinal = command.lower()
            intent, confidence = detect_intent(commandFinal)
            print("Intent:", intent)

            selected_voice_model, current_voice_name = get_current_voice_info()
            if not intent:
                if is_code_worthy(commandFinal):
                    print("Writing python script to perform the provided task!")
                    response = await handle_unknown_request(commandFinal, selected_voice_model)
                    speak(response, selected_voice_model)
                else:
                    print("It wasn't code worthy command!")
                    response = await get_mistral_response(commandFinal)
                    clean_response = clean_text_for_speech(response)
                    short_response = trim_response(clean_response)
                    speak(short_response, selected_voice_model)
                continue


            # Core system functions
            if intent == "exit":
                speak("Okay take care sir", selected_voice_model)
                return
            elif intent == "sleep":
                sleep_now(selected_voice_model)
            elif intent == "change_voice":
                new_voice_path, new_voice_name = cycle_voice_model()
                speak(f"Voice changed to {new_voice_name}", new_voice_path)
                continue
            elif intent == "shutdown":
                if check_authorization(os.path.join(PROJECT_ROOT, "static", "known_image.jpeg")):
                    speak("do you really want to shutdown??", selected_voice_model)
                    command = listen(model, language="en")
                    intent , confidence = detect_intent(command)
                    if intent == "yes":
                        shutdown(selected_voice_model)
                    else:
                        speak("Okay sir", selected_voice_model)
                else:
                    speak("authentication failed!")
            elif intent == "play_music":
                play_music(selected_voice_model)
            elif intent == "stop_music":
                stop_music(selected_voice_model)
            elif intent == "get_weather":
                weather_info = await get_weather_forecast("Kathmandu")
                speak(weather_info, selected_voice_model)

            # Email
            elif intent == "read_email":
                speak("Checking your inbox...", selected_voice_model)
                unread = count_recent_unread_emails(imap_server, EMAIL_USER, EMAIL_PASSWORD, 7)
                speak(f"You have {unread} unread emails in the last 7 days", selected_voice_model)
                speak("Do you want me to read them?", selected_voice_model)
                reply = listen(model, language="en")
                if detect_intent(reply.lower())[0] == "yes":
                    from_, subject, date_, unread_msg_nums = read_recent_unread_emails(imap_server, EMAIL_USER, EMAIL_PASSWORD, 7, 4)
                    command = f"Summarize this mail \n_from_: {from_} \ndate: {date_}\nSubject: {subject}"
                    response = await get_mistral_response(command)
                    speak(clean_text_for_speech(response), selected_voice_model)

            elif intent == "send_email":
                contacts = load_contacts()
                speak("Who do you want to send the email to?", selected_voice_model)
                name = clean_input(listen(model, language="en"))
                email = contacts.get(name)
                if email:
                    speak("Subject?", selected_voice_model)
                    subject = listen(model, language="en")
                    speak("Body?", selected_voice_model)
                    body = listen(model, language="en")
                    speak("Want me to check grammar?", selected_voice_model)
                    if detect_intent(listen(model, language="en").lower())[0] == "yes":
                        body = await get_mistral_response(f"Fix grammar: {body}")
                    send_email(EMAIL_USER, EMAIL_PASSWORD, email, subject, body)
                    speak(f"Email sent to {name}.", selected_voice_model)
                else:
                    speak(f"No email found for {name}.", selected_voice_model)

            # Web search
            elif intent == "web_search":
                speak("What should I search?", selected_voice_model)
                query = listen(model, language="en")
                speak("Searching, please wait.", selected_voice_model)
                output, link = web_search(query)
                summary = await get_mistral_response(f"Summarize this in under 100 words:\n{output}")
                speak(clean_text_for_speech(summary), selected_voice_model)
                speak("Open in browser?", selected_voice_model)
                if detect_intent(listen(model, language="en").lower())[0] == "yes":
                    subprocess.run(f'firefox "{link}"', shell=True)

            # Assistant Utility Features
            elif intent == "change_wallpaper":
                change_wallpaper(selected_voice_model)

            elif intent == "add_reminder":
                speak("What should I remind you about?", selected_voice_model)
                task = listen(model, language="en")
                speak("When should I remind you? (e.g., 14:30)", selected_voice_model)
                time_str = listen(model, language="en")
                result = add_reminder(task, time_str, selected_voice_model)
                speak(result, selected_voice_model)

            elif intent == "list_reminders":
                result = list_reminders()
                speak(result, selected_voice_model)

            elif intent == "news":
                news = await get_top_news(config.NEWS_API_KEY)
                speak(news, selected_voice_model)

            elif intent == "battery_status":
                percentage , status = get_battery_status()
                speak(f"Battery remaining {percentage} and {status}", selected_voice_model)

            elif intent == "wiki_summary":
                speak("What should I look up?", selected_voice_model)
                query = listen(model, language="en")
                result = wiki_summary(query)
                speak(result, selected_voice_model)

            elif intent == "get_ip":
                speak(get_ip(), selected_voice_model)

            elif intent == "get_stats":
                stats = get_system_stats()
                speak(stats, selected_voice_model)

            elif intent == "translate":
                speak("What text should I translate?", selected_voice_model)
                text = listen(model, language="en")
                speak("To which language?", selected_voice_model)
                lang = listen(model, language="en")
                translated = translate_text(text, lang)
                speak(translated, selected_voice_model)

            elif intent == "start_timer":
                speak("How many seconds?", selected_voice_model)
                try:
                    seconds = int(listen(model, language="en"))
                    start_timer(seconds, selected_voice_model)
                except ValueError:
                    speak("That wasn't a number.", selected_voice_model)

            elif intent == "joke":
                speak(tell_joke(), selected_voice_model)

            elif intent == "create_note":
                speak("What should I write?", selected_voice_model)
                note = listen(model, language="en")
                result = create_note(note)
                speak(result, selected_voice_model)

            elif intent == "current_datetime":
                speak(get_current_datetime(), selected_voice_model)

            elif intent == "youtube_search":
                speak("What should I play?", selected_voice_model)
                query = listen(model, language="en")
                result = play_youtube(query)
                speak(result, selected_voice_model)

            elif intent == "find_file":
                speak("What file are you looking for?", selected_voice_model)
                filename = listen(model, language="en")
                path = find_file(filename)
                speak(path, selected_voice_model)

            elif intent == "clipboard":
                content = get_clipboard()
                speak(f"Clipboard contains: {content}", selected_voice_model)

            elif intent == "convert_currency":
                speak("How much and which currency?", selected_voice_model)
                info = listen(model, language="en")
                parts = info.split()
                if len(parts) == 3:
                    amount, from_curr, to_curr = parts
                    result = await convert_currency(amount, from_curr.upper(), to_curr.upper())
                    speak(result, selected_voice_model)
                else:
                    speak("Please say amount, from and to currency.", selected_voice_model)

            elif intent == "generate_image":
                speak("What should I generate?", selected_voice_model)
                prompt = listen(model, language="en")
                image_url = await generate_image(prompt)
                speak(f"Image generated: {image_url}", selected_voice_model)

            elif intent == "delete_notes":
                result = self_destruct()
                speak(result, selected_voice_model)

            elif intent == "read_pdf":
                speak("Enter PDF file path", selected_voice_model)
                path = input("PDF path: ")
                text = read_pdf(path)
                speak(text[:500], selected_voice_model)  # Read a preview

            elif intent == "update_assistant":
                result = update_assistant_code()
                speak(result, selected_voice_model)

            elif intent == "greeting":
                speak(get_time_based_greeting(), selected_voice_model)

            elif intent == "uptime":
                speak(get_uptime(), selected_voice_model)

            elif intent == "port_scan":
                speak("Which IP or host to scan?", selected_voice_model)
                host = listen(model, language="en")
                result = scan_ports(host)
                speak(result, selected_voice_model)

            elif intent == "public_ip":
                ip = get_public_ip()
                speak(f"Your public IP is {ip}", selected_voice_model)

            elif intent == "wifi_scan":
                result = scan_wifi()
                speak(result, selected_voice_model)

            elif intent == "save_voice_note":
                speak("Speak your note.", selected_voice_model)
                text = listen(model, language="en")
                result = save_voice_note(text)
                speak(result, selected_voice_model)

            elif intent == "motivation":
                speak(get_daily_affirmation(), selected_voice_model)

            elif intent == "battery_saver":
                speak("Turn battery saver on or off?", selected_voice_model)
                mode = listen(model, language="en").lower()
                result = toggle_battery_saver(mode)
                speak(result, selected_voice_model)

            elif intent == "play_ambient":
                speak("What ambient sound? (rain, forest, ocean)", selected_voice_model)
                type_ = listen(model, language="en")
                result = play_ambient_sound(type_)
                speak(result, selected_voice_model)

            elif intent == "take_screenshot":
                result = take_screenshot()
                speak(result, selected_voice_model)

            elif intent == "take_photo":
                speak("Are you ready?", selected_voice_model)
                user_status = listen(model="tiny", language="en")
                intent , confidence = detect_intent(user_status)
                if intent == "yes":
                    speak("cheese!", selected_voice_model)
                    result, path = take_webcam_photo()
                    speak(result, selected_voice_model)
                    speak("You want me to open your photo?", selected_voice_model)
                    user_choice = listen(model="tiny", language="en")
                    intent , confidence = detect_intent(user_choice)
                    if intent == "yes":
                        command = f'firefox {path}'
                        subprocess.run(command, shell = True, check = True)
                        speak("please check firefox", selected_voice_model)
                    else:
                        speak("okay", selected_voice_model)
                else:
                    speak("okay", selected_voice_model)

            elif intent == "backup_files":
                result = backup_files()
                speak(result, selected_voice_model)

            elif intent == "download_instagram":
                speak("Paste the Instagram reel URL.", selected_voice_model)
                url = input("URL: ")
                result = download_instagram_reel(url)
                speak(result, selected_voice_model)

            elif intent == "toggle_night_mode":
                result = toggle_night_mode()
                speak(result, selected_voice_model)
            elif intent == "increase_volume":
                speak(increase_volume(), selected_voice_model)
            elif intent == "decrease_volume":
                speak(decrease_volume(), selected_voice_model)
            elif intent == "increase_brightness":
                speak(increase_brightness(), selected_voice_model)
            elif intent == "decrease_brightness":
                speak(decrease_brightness(), selected_voice_model)
                
# main entry point
if __name__ == "__main__":
    asyncio.run(main())
