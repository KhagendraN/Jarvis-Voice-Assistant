# Jarvis Voice Assistant

Jarvis is a sophisticated AI-powered voice assistant for Linux that combines cutting-edge speech recognition, natural language processing, and system automation. Built with Python and leveraging multiple AI services, it provides a comprehensive personal assistant experience with features like face authentication, email management, weather updates, system control, AI code generation, and much more.

---

## 🚀 Key Features

### 🎤 **Advanced Voice Processing**
- **Dual Speech Recognition**: Combines Vosk (offline) and Whisper (AI-powered) for robust transcription
- **Real-time Voice Model Switching**: Instantly change between 9 different voice personalities
- **High-Quality TTS**: Piper-based text-to-speech with ONNX models
- **Multi-language Support**: English and Nepali voice models included

### 🔐 **Security & Authentication**
- **Face Authentication**: Secure access using facial recognition with multiple attempt handling
- **Authorization Checks**: Required for sensitive operations (shutdown, system changes)
- **Safe Code Execution**: Timeout limits and error handling for generated code

### 🤖 **AI-Powered Intelligence**
- **Intent Classification**: Semantic similarity-based command recognition with 1000+ training examples
- **Code Generation**: Automatically generates and executes Python scripts for unknown requests
- **Mistral AI Integration**: Natural language processing and intelligent responses
- **Secondary Classifier**: Determines code-worthiness of user requests

### 📧 **Communication & Information**
- **Email Management**: Read unread emails, send emails with grammar checking
- **Weather & News**: Real-time weather forecasts and top news headlines
- **Web Search**: DuckDuckGo integration with result summarization
- **Wikipedia Integration**: Quick knowledge lookups and summaries

### 💻 **System Control & Automation**
- **Hardware Control**: Volume, brightness, screenshots, wallpaper management
- **Music Player**: Local music playback with rofi interface
- **System Monitoring**: Battery status, CPU/RAM usage, uptime tracking
- **File Operations**: Search, backup, note-taking, voice notes
- **Process Management**: Kill processes, system updates, package management

### 🎨 **Creative & Utility Features**
- **AI Image Generation**: Create images using OpenAI DALL-E
- **YouTube Integration**: Search and play videos
- **Currency Conversion**: Real-time exchange rates
- **PDF Reading**: Extract and summarize document content
- **Network Tools**: Port scanning, WiFi analysis, IP address lookup
- **Reminders & Scheduling**: Time-based task reminders with notifications

---

## 🏗️ Technical Architecture

### **Core Components**
- **Main Application** (`main.py`): Central orchestrator and interaction loop
- **Utility Functions** (`utils.py`): 1170+ lines of helper functions and integrations
- **Intent Classification** (`intent_classifier.py`): AI-powered command recognition
- **Secondary Classifier** (`secondaryClassifier.py`): Code-worthiness detection
- **Face Authentication** (`faceAuthorization/`): Computer vision security layer
- **Shell Scripts** (`scripts/`): System integration and hardware control
- **Voice Models** (`voice_models/`): Text-to-speech capabilities

### **AI & ML Stack**
- **PyTorch**: Deep learning framework for intent classification
- **Sentence Transformers**: Semantic similarity for command recognition
- **OpenCV**: Computer vision for face detection and authentication
- **Whisper**: Advanced speech recognition
- **Mistral AI**: Natural language processing and code generation

### **System Integration**
- **Shell Scripts**: Music, volume, brightness, screenshot control
- **Rofi**: GUI selection interfaces for user interaction
- **MPV**: Media playback engine
- **Piper**: High-quality text-to-speech
- **System APIs**: Battery, system stats, file operations

---

## 🎤 Real-Time Voice Model Switching

You can change the assistant's voice in real time by saying:
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
- **Nepali_voice**: Nepali language support
- **Samantha**: Professional female voice
- **Jarvis**: Classic assistant voice
- **male_Voice**: Male voice option
- **female_voice**: Female voice option
- **kristin_voice**: Kristin personality
- **normal_female**: Natural female voice
- **AI_type**: Futuristic AI voice

You can add/remove voices by placing `.onnx` and `.onnx.json` files in the `voice_models/` directory.

---

## 🧠 AI Code Generation

Jarvis features an advanced AI code generation system that can:

- **Analyze Requests**: Determine if a task requires code generation
- **Generate Python Scripts**: Create functional, executable code using Mistral AI
- **Auto-install Dependencies**: Automatically install missing Python packages
- **Safe Execution**: Run generated code with timeout limits and error handling
- **Code Formatting**: Apply Black formatting for clean, readable code

Example interaction:
```
User: "Create a script to plot a sine wave"
Jarvis: *Generates and executes matplotlib code*
```

---

## ⚡ Quickstart

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

### 2. **Run Automated Setup**
```bash
# Option 1: Bash script (recommended)
bash install.sh

# Option 2: Python script
python setup_jarvis.py
```

**The setup scripts will automatically:**
- Install system dependencies (ffmpeg, rofi, mpv, aplay)
- Download and install Piper TTS (required for speech synthesis)
- Download Vosk speech recognition model
- Create Python virtual environment
- Install Python dependencies
- Copy configuration templates

### 3. **Download Voice Models**
```bash
bash voice_models/voice_setup.sh
# or
python voice_models/voice_setup.py
```

### 4. **Configure Your Setup**
- **API Keys**: Edit `config.py` with your API keys (Mistral, Weather, News, etc.)
- **Contacts**: Edit `contact.json` with your email contacts
- **Face Image**: Place your photo as `static/known_image.jpeg` for authentication

### 5. **Activate and Run**
```bash
source venv/bin/activate
python main.py
```

---

## 🗑️ Uninstall Script

A new `uninstall.sh` script is included for easy removal of Jarvis and its dependencies. Key points:

- **One-Command Uninstall**: Run `bash uninstall.sh` to remove all installed files, virtual environments, and dependencies added by Jarvis.
- **Removes Voice Models**: Deletes all downloaded voice models from the `voice_models/` directory.
- **Cleans Virtual Environment**: Removes the Python virtual environment created during setup.
- **Deletes Config Files**: Optionally removes configuration files (`config.py`, `contact.json`, etc.) after confirmation.
- **System Cleanup**: Uninstalls system packages (if installed by Jarvis) such as Piper, Vosk models, and other binaries.
- **Safe Operation**: Prompts for confirmation before deleting important files or directories.
- **Log Output**: Provides detailed output of all actions performed for transparency.
- **Cross-Platform**: Designed for compatibility with major Linux distributions.

**Usage Example:**
```bash
bash uninstall.sh
```
Follow the on-screen prompts to complete the uninstallation process.

---

## 🛠️ Troubleshooting & Error Handling

### Common Issues
- **Missing or Invalid Config**: If you see a message about missing or invalid config values, check your `config.py` and ensure all API keys and file paths are set and valid. The assistant will not start if required config is missing.
- **Missing Scripts or Files**: If a script (e.g., music player, wallpaper selector) is missing or not executable, you will receive a clear error message. Ensure all scripts in the `scripts/` directory are present and have execute permissions.
- **Face Authentication Fails**: If face authentication fails, sensitive operations (shutdown, update, backup, etc.) will be denied. Ensure your face image is present and clear at `static/known_image.jpeg`.
- **Sudo Password Required**: For operations requiring `sudo` (e.g., system update), passwordless sudo is required. If not configured, the operation will be denied and an error will be logged.
- **Dependency Issues**: All dependencies are now unified between `requirements.txt` and `pyproject.toml`. If you encounter missing packages, run `pip install -r requirements.txt`.
- **Test Failures**: Tests are now run with `pytest` and include mocks for hardware and network dependencies. See the `tests/` directory for details.

### Logging
- All errors, warnings, and important events are now logged using Python's `logging` module. Check your console output for detailed logs.

### Config Validation
- The assistant validates your config at startup. If any required key or file is missing, you will see a clear error and the program will exit.

---

## 🆕 Notable Changes
- **Intent Phrases**: All intent phrases are now stored in `intents.json` for easier maintenance and extension.
- **Structured Logging**: All modules use structured logging for errors and important events.
- **Unified Dependency Management**: `requirements.txt` and `pyproject.toml` are now consistent.
- **Security**: All sensitive operations require successful face authentication and passwordless sudo where needed.
- **User Experience**: All user input is now via voice or consistent UI; no more blocking `input()` calls.
- **Testing**: Tests use `pytest` and mock hardware/network dependencies for reliability.

---

## 🛠️ Setup Details

### **Critical System Dependencies**
The setup scripts automatically install these essential components:

#### **Piper TTS** (Required for Speech Synthesis)
- **What it is**: High-quality text-to-speech engine
- **Why needed**: Jarvis uses Piper for all voice output
- **Installation**: Automatically downloaded and installed to `/usr/local/bin/`
- **Version**: 1.2.0 (latest stable)

#### **Vosk Speech Recognition Model** (Required for Speech Input)
- **What it is**: Offline speech recognition model
- **Why needed**: Provides reliable speech-to-text conversion
- **Installation**: Automatically downloaded to `~/Downloads/vosk-model-small-en-us-0.15/`
- **Size**: ~50MB compressed

#### **System Packages**
- **FFmpeg**: Audio/video processing
- **Rofi**: GUI selection interface
- **MPV**: Media playback
- **ALSA Utils**: Audio playback (aplay)

### **Required Configuration Files**
- **`config.py`**: API keys and settings (copy from `config_template.py`)
- **`contact.json`**: Email contacts (copy from `contact_template.json`)
- **`static/known_image.jpeg`**: Your face image for authentication

### **API Keys Required**
- **Mistral AI**: For natural language processing and code generation
- **Weather API**: For weather forecasts and current conditions
- **News API**: For latest news headlines
- **Email**: Gmail credentials for email functionality
- **OpenAI**: For AI image generation (optional)

### **System Dependencies**
- **Python 3.8+**: Core runtime
- **FFmpeg**: Audio/video processing
- **Rofi**: GUI selection interface
- **MPV**: Media playback
- **Piper**: Text-to-speech engine

---

## 📦 Dependencies

The project uses **48+ Python packages** including:
- **Core**: numpy, pillow, opencv-python, python-dotenv
- **AI/ML**: torch, transformers, sentence-transformers, whisper
- **Audio**: sounddevice, scipy, vosk, SpeechRecognition
- **APIs**: aiohttp, openai, duckduckgo-search
- **Utilities**: psutil, pyjokes, PyMuPDF, markdown, wikipedia

---

## 🔧 Advanced Features

### **System Integration**
- **Hardware Control**: Volume, brightness, screenshots, wallpaper
- **Process Management**: System monitoring, updates, package management
- **File Operations**: Search, backup, note-taking, voice notes
- **Network Tools**: Port scanning, WiFi analysis, IP lookup

### **Communication**
- **Email**: Read unread emails, send with grammar checking
- **Web Search**: DuckDuckGo integration with summarization
- **News**: Latest headlines from multiple sources
- **Weather**: Current conditions and forecasts

### **Creative Tools**
- **AI Image Generation**: Create images from text descriptions
- **YouTube Integration**: Search and play videos
- **PDF Reading**: Extract and summarize documents
- **Currency Conversion**: Real-time exchange rates

### **Productivity**
- **Reminders**: Time-based task scheduling
- **Notes**: Voice and text note-taking
- **File Search**: Find files by name
- **Clipboard Management**: Access clipboard content

---

## 🐞 Troubleshooting

### **Common Issues**

#### **Piper TTS Not Found**
```bash
# Check if Piper is installed
which piper

# If not found, install manually
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_1.2.0_linux-x86_64.tar.gz
tar -xzf piper_1.2.0_linux-x86_64.tar.gz
sudo mv piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper
```

#### **Vosk Model Missing**
```bash
# Check if model exists
ls ~/Downloads/vosk-model-small-en-us-0.15/

# If missing, download manually
cd ~/Downloads
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

#### **System Dependencies**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg rofi mpv alsa-utils

# Arch Linux
sudo pacman -S ffmpeg rofi mpv alsa-utils

# Fedora
sudo dnf install ffmpeg rofi mpv alsa-utils
```

### **Error Messages**
- The assistant provides helpful error messages for missing files
- Check console output for detailed error information
- Verify API keys are correctly configured

### **Performance**
- **Speech Recognition**: Ensure microphone is properly configured
- **Face Authentication**: Use clear, well-lit photos
- **Code Generation**: Complex requests may take longer to process

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and formatting
- Testing requirements
- Pull request process
- Feature development

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📬 Support

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: Check the code comments and docstrings

---

## 🎯 Roadmap

Future enhancements planned:
- **Multi-language Support**: Additional language models
- **Plugin System**: Extensible architecture for custom features
- **Web Interface**: Browser-based control panel
- **Cloud Integration**: Sync settings and data across devices

---

*Jarvis Voice Assistant - Your AI-powered Linux companion* 