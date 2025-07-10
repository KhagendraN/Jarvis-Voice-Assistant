# Jarvis Voice Assistant

Jarvis is an AI-powered voice assistant for Linux with features like voice recognition, natural language processing, text-to-speech, face authentication, email, weather, news, system control, reminders, jokes, AI image generation, YouTube integration, and more.

---

## 🚀 Key Features
- **Real-time voice model switching**: Change the assistant’s voice instantly by saying commands like "change voice" or "switch voice".
- **Face authentication**: Secure access using your own face image.
- **Email, weather, news, reminders, jokes, system control, and more**
- **AI-powered responses and image generation**
- **YouTube integration, clipboard, file search, and more**

---

## 🎤 Real-Time Voice Model Switching

You can change the assistant’s voice in real time by saying:
- "Change voice"
- "Switch voice"
- "Use a different voice"
- "Try a different voice model"

Jarvis will cycle through all available voice models and announce the change:

```
User: "Can you change your voice?"
Jarvis: "Voice changed to Samantha."
```

**Available voices:**
- Nepali_voice
- Samantha
- Jarvis
- male_Voice
- female_voice
- kristin_voice
- normal_female
- AI_type

You can add/remove voices by placing `.onnx` and `.onnx.json` files in the `voice_models/` directory.

---

## ⚡ Quickstart

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/jarvis-voice-assistant.git
   cd jarvis-voice-assistant
   ```
2. **Run the install script:**
   ```bash
   bash install.sh
   # or
   python setup_jarvis.py
   ```
3. **Edit your config and contacts:**
   - Open `config.py` and add your API keys.
   - Open `contact.json` and add your contacts.
4. **Add your face image:**
   - Place a clear photo of your face as `static/known_image.jpeg` for face authentication.
5. **Activate your virtual environment and run Jarvis:**
   ```bash
   source venv/bin/activate
   python main.py
   ```

---

## 🛠️ Setup Details

### Configuration Files
- `config.py` (API keys, settings):
  - Not included by default. Copy from `config_template.py` and fill in your own keys.
- `contact.json` (email contacts):
  - Not included by default. Copy from `contact_template.json` and fill in your own contacts.
- `static/known_image.jpeg` (face authentication):
  - Not included by default. Add your own face image for authentication.

### First-Time Setup
The install script or setup script will:
- Create a Python virtual environment
- Install all dependencies
- Copy template files if needed
- Remind you to add your API keys, contacts, and face image

### API Keys
- Add your own API keys in `config.py` (see `config_template.py` for required fields)

### Contacts
- Add your own contacts in `contact.json` (see `contact_template.json` for format)

### Face Authentication
- Place your face image as `static/known_image.jpeg`

---

## 🐞 Troubleshooting
- If you see errors about missing `config.py`, `contact.json`, or `static/known_image.jpeg`, follow the setup instructions above.
- The assistant will show helpful errors if any required files are missing.
- For issues with dependencies, ensure you are using the provided virtual environment.

---

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License
MIT License. See [LICENSE](LICENSE).

## 📬 Support
For questions or issues, open a GitHub issue or discussion. 