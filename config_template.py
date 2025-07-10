# Configuration Template for Jarvis Voice Assistant
# Copy this file to config.py and fill in your API keys

# Mistral AI API Key (for language processing)
# Get your key from: https://console.mistral.ai/
MISTRAL_API_KEY = "your_mistral_api_key_here"

# Gmail Configuration (for email features)
# Use App Password for Gmail (not your regular password)
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_gmail_app_password_here"

# OpenWeatherMap API Key (for weather information)
# Get your key from: https://openweathermap.org/api
WEATHER_API_KEY = "your_openweathermap_api_key_here"

# NewsAPI Key (for news updates)
# Get your key from: https://newsapi.org/
NEWS_API_KEY = "your_newsapi_key_here"

# OpenAI API Key (for image generation)
# Get your key from: https://platform.openai.com/
OPENAI_API_KEY = "your_openai_api_key_here"

# ElevenLabs API Key (for alternative TTS)
# Get your key from: https://elevenlabs.io/
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"

# ElevenLabs Voice ID (for specific voice)
JARVIS_VOICE_ID = "your_voice_id_here"

# Unsplash API Keys (for image features)
# Get your keys from: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY = "your_unsplash_access_key_here"
UNSPLASH_SECRET_KEY = "your_unsplash_secret_key_here"

# Runway API Key (for video features)
# Get your key from: https://runwayml.com/
RUNAWAY_API_KEY = "your_runway_api_key_here"

# Instructions:
# 1. Copy this file to config.py
# 2. Replace all "your_*_key_here" values with your actual API keys
# 3. Keep your config.py file secure and never commit it to version control
# 4. The .gitignore file is configured to exclude config.py from commits

# Optional: Customize paths for your system
VOICE_MODELS_PATH = "/home/your_username/piper_voices"
VOSK_MODEL_PATH = "/home/your_username/Downloads/vosk-model-small-en-us-0.15"
CONTACTS_FILE_PATH = "/home/your_username/programs/python/JarvisProject/contact.json"
KNOWN_IMAGE_PATH = "/home/your_username/programs/python/JarvisProject/static/known_image.jpeg" 