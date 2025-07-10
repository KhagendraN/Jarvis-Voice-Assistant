# example.py
import os
import base64
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import config
import tempfile

# Load environment variables (if any)
load_dotenv()

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)

# Step 1: Create voice previews based on description + input text
voices = client.text_to_voice.create_previews(
    voice_description="A calm, polite British male voice. Clear and articulate, with a confident and professional tone. Ideal for a virtual assistant or narrator. Friendly and trustworthy.",
    text="Greetings little human. I am a mighty giant from a far away land. Would you like me to tell you a story?"
)

# Step 2: Play all previews returned
for i, preview in enumerate(voices.previews):
    # Convert base64-encoded audio to bytes
    audio_buffer = base64.b64decode(preview.audio_base_64)

    # # Save to temp file to play
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
    #     temp_audio.write(audio_bytes)
    #     temp_audio_path = temp_audio.name

    print(f"🎧 Playing preview {i+1}: {preview.generated_voice_id}")
    play(audio_buffer)

# Step 3: Create a new voice based on one of the previews
choice = int(input("Enter choice: "))
voice = client.text_to_voice.create_voice_from_preview(
    voice_name="Jarvis",
    voice_description="A calm, polite British male voice. Clear and articulate, with a confident and professional tone. Ideal for a virtual assistant or narrator. Friendly and trustworthy.",
    generated_voice_id=voices.previews[choice].generated_voice_id  # Using the first one
)

print(f"✅ Custom voice created! Voice ID: {voice.voice_id}")
