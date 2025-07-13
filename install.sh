#!/bin/bash
set -e

# Setup JarvisProject

echo "<==================================INSTALLING JARVIS=================================================>"

# Check if running as root (needed for some system packages)
if [ "$EUID" -eq 0 ]; then
    echo "Running as root - installing system dependencies..."
    
    # Update package lists
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y python3-pip python3-venv ffmpeg rofi mpv aplay
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        pacman -Sy --noconfirm python-pip ffmpeg rofi mpv alsa-utils
    elif command -v dnf &> /dev/null; then
        # Fedora
        dnf install -y python3-pip ffmpeg rofi mpv alsa-utils
    else
        echo "WARNING: Unsupported package manager. Please install ffmpeg, rofi, mpv, and aplay manually."
    fi
else
    echo "Note: Some system packages may need to be installed manually if not already present."
    echo "Required: ffmpeg, rofi, mpv, aplay"
fi

# Install Piper TTS (critical for speech synthesis)
echo "Installing Piper TTS..."
if ! command -v piper &> /dev/null; then
    echo "Piper not found. Installing Piper TTS..."
    
    # Download and install Piper
    PIPER_VERSION="1.2.0"
    PIPER_ARCH="linux-x86_64"
    PIPER_URL="https://github.com/rhasspy/piper/releases/download/v${PIPER_VERSION}/piper_${PIPER_VERSION}_${PIPER_ARCH}.tar.gz"
    
    # Create temp directory for download
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    echo "Downloading Piper TTS..."
    wget -q "$PIPER_URL" -O piper.tar.gz
    
    if [ $? -eq 0 ]; then
        echo "Extracting Piper..."
        tar -xzf piper.tar.gz
        
        # Move piper to /usr/local/bin for global access
        sudo mv piper /usr/local/bin/
        sudo chmod +x /usr/local/bin/piper
        
        echo "Piper TTS installed successfully!"
    else
        echo "ERROR: Failed to download Piper TTS"
        echo "Please install Piper manually from: https://github.com/rhasspy/piper"
        exit 1
    fi
    
    # Clean up
    cd - > /dev/null
    rm -rf "$TEMP_DIR"
else
    echo "Piper TTS already installed."
fi

# Download Vosk model (required for speech recognition)
echo "Setting up Vosk speech recognition model..."
VOSK_MODEL_DIR="$HOME/Downloads"
VOSK_MODEL_NAME="vosk-model-small-en-us-0.15"
VOSK_MODEL_URL="https://alphacephei.com/vosk/models/${VOSK_MODEL_NAME}.zip"

if [ ! -d "$VOSK_MODEL_DIR/$VOSK_MODEL_NAME" ]; then
    echo "Downloading Vosk model..."
    cd "$VOSK_MODEL_DIR"
    
    if wget -q "$VOSK_MODEL_URL" -O "${VOSK_MODEL_NAME}.zip"; then
        echo "Extracting Vosk model..."
        unzip -q "${VOSK_MODEL_NAME}.zip"
        rm "${VOSK_MODEL_NAME}.zip"
        echo "Vosk model installed successfully!"
    else
        echo "ERROR: Failed to download Vosk model"
        echo "Please download manually from: https://alphacephei.com/vosk/models"
        echo "Extract to: $VOSK_MODEL_DIR/$VOSK_MODEL_NAME"
    fi
    
    cd - > /dev/null
else
    echo "Vosk model already exists."
fi

# Create venv if not exists
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Created virtual environment."
fi

source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy config and contact templates if not present
if [ ! -f config.py ]; then
  cp config_template.py config.py
  echo "Copied config_template.py to config.py. Please edit it with your API keys."
fi
if [ ! -f contact.json ]; then
  cp contact_template.json contact.json
  echo "Copied contact_template.json to contact.json. Please edit it with your contacts."
fi

# Check for face image
if [ ! -f static/known_image.jpeg ]; then
  echo "WARNING: No face image found. Please add your face image as static/known_image.jpeg for face authentication."
fi

# Verify critical dependencies
echo "Verifying installation..."
if command -v piper &> /dev/null; then
    echo "✓ Piper TTS is installed and available"
else
    echo "✗ ERROR: Piper TTS is not available. Please install manually."
fi

if [ -d "$VOSK_MODEL_DIR/$VOSK_MODEL_NAME" ]; then
    echo "✓ Vosk model is installed"
else
    echo "✗ ERROR: Vosk model is missing. Please download manually."
fi

if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg is installed"
else
    echo "✗ WARNING: FFmpeg not found. Some features may not work."
fi

if command -v rofi &> /dev/null; then
    echo "✓ Rofi is installed"
else
    echo "✗ WARNING: Rofi not found. GUI selection features may not work."
fi

if command -v mpv &> /dev/null; then
    echo "✓ MPV is installed"
else
    echo "✗ WARNING: MPV not found. Media playback features may not work."
fi

echo ""
echo "==================================SETUP COMPLETE================================================="
echo "Next steps:"
echo "1. Edit config.py with your API keys"
echo "2. Edit contact.json with your contacts"
echo "3. Add your face image as static/known_image.jpeg"
echo "4. Download voice models: bash voice_models/voice_setup.sh"
echo "5. Activate your venv: source venv/bin/activate"
echo "6. Run Jarvis: python main.py"
echo ""
echo "If you encounter any issues, check the troubleshooting section in README.md" 