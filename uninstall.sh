#!/bin/bash
set -e

# Uninstall JarvisProject

echo "<==================================UNINSTALLING JARVIS===============================================>"

# Function to ask for confirmation
confirm_uninstall() {
    echo "This will remove Jarvis and all its dependencies including:"
    echo "- Python virtual environment (venv/)"
    echo "- Configuration files (config.py, contact.json)"
    echo "- Face authentication image (static/known_image.jpeg)"
    echo "- Downloaded voice models (voice_models/)"
    echo "- Generated AI files (AIGenerated/)"
    echo "- Piper TTS (if installed by this script)"
    echo "- Vosk model (if downloaded by this script)"
    echo ""
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Uninstall cancelled."
        exit 0
    fi
}

# Function to remove system packages (optional)
remove_system_packages() {
    echo "Removing system packages..."
    read -p "Remove system packages (ffmpeg, rofi, mpv, alsa-utils)? This may affect other applications. (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v apt-get &> /dev/null; then
            # Debian/Ubuntu
            sudo apt-get remove -y ffmpeg rofi mpv alsa-utils
            sudo apt-get autoremove -y
        elif command -v pacman &> /dev/null; then
            # Arch Linux
            sudo pacman -R --noconfirm ffmpeg rofi mpv alsa-utils
        elif command -v dnf &> /dev/null; then
            # Fedora
            sudo dnf remove -y ffmpeg rofi mpv alsa-utils
        else
            echo "Please remove system packages manually: ffmpeg, rofi, mpv, alsa-utils"
        fi
        echo "System packages removed."
    else
        echo "System packages kept (may be used by other applications)."
    fi
}

# Function to remove Piper TTS
remove_piper() {
    echo "Removing Piper TTS..."
    if command -v piper &> /dev/null; then
        read -p "Remove Piper TTS? This will affect text-to-speech functionality. (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Check if piper is in /usr/local/bin (where we install it)
            if [ -f "/usr/local/bin/piper" ]; then
                sudo rm -f /usr/local/bin/piper
                echo "Piper TTS removed from /usr/local/bin/"
            else
                echo "Piper TTS not found in /usr/local/bin/ (may have been installed elsewhere)"
            fi
        else
            echo "Piper TTS kept."
        fi
    else
        echo "Piper TTS not found in PATH."
    fi
}

# Function to remove Vosk model
remove_vosk_model() {
    echo "Removing Vosk speech recognition model..."
    VOSK_MODEL_DIR="$HOME/Downloads"
    VOSK_MODEL_NAME="vosk-model-small-en-us-0.15"
    VOSK_MODEL_PATH="$VOSK_MODEL_DIR/$VOSK_MODEL_NAME"
    
    if [ -d "$VOSK_MODEL_PATH" ]; then
        read -p "Remove Vosk model (~50MB)? This will affect speech recognition. (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VOSK_MODEL_PATH"
            echo "Vosk model removed from $VOSK_MODEL_PATH"
        else
            echo "Vosk model kept."
        fi
    else
        echo "Vosk model not found in $VOSK_MODEL_PATH"
    fi
}

# Function to remove Python virtual environment
remove_venv() {
    echo "Removing Python virtual environment..."
    if [ -d "venv" ]; then
        rm -rf venv
        echo "Virtual environment (venv/) removed."
    else
        echo "Virtual environment not found."
    fi
}

# Function to remove configuration files
remove_config_files() {
    echo "Removing configuration files..."
    
    # Remove config.py
    if [ -f "config.py" ]; then
        read -p "Remove config.py (contains your API keys)? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f config.py
            echo "config.py removed."
        else
            echo "config.py kept."
        fi
    fi
    
    # Remove contact.json
    if [ -f "contact.json" ]; then
        read -p "Remove contact.json (contains your contacts)? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f contact.json
            echo "contact.json removed."
        else
            echo "contact.json kept."
        fi
    fi
    
    # Remove face image
    if [ -f "static/known_image.jpeg" ]; then
        read -p "Remove face authentication image? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f static/known_image.jpeg
            echo "Face authentication image removed."
        else
            echo "Face authentication image kept."
        fi
    fi
}

# Function to remove voice models
remove_voice_models() {
    echo "Removing voice models..."
    if [ -d "voice_models" ]; then
        read -p "Remove voice models (~500MB)? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf voice_models
            echo "Voice models removed."
        else
            echo "Voice models kept."
        fi
    else
        echo "Voice models directory not found."
    fi
}

# Function to remove generated files
remove_generated_files() {
    echo "Removing generated files..."
    
    # Remove AIGenerated directory
    if [ -d "AIGenerated" ]; then
        read -p "Remove AI-generated files? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf AIGenerated
            echo "AI-generated files removed."
        else
            echo "AI-generated files kept."
        fi
    fi
    
    # Remove __pycache__ directories
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo "Python cache files removed."
    
    # Remove .pyc files
    find . -name "*.pyc" -delete 2>/dev/null || true
    echo "Python compiled files removed."
}

# Function to remove notes and voice notes
remove_user_data() {
    echo "Removing user data..."
    
    # Remove notes
    NOTES_DIR="$HOME/Documents/Notes"
    if [ -d "$NOTES_DIR" ]; then
        read -p "Remove all notes from $NOTES_DIR? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$NOTES_DIR"
            echo "Notes directory removed."
        else
            echo "Notes kept."
        fi
    fi
    
    # Remove voice notes
    VOICE_NOTES_DIR="$HOME/Documents/VoiceNotes"
    if [ -d "$VOICE_NOTES_DIR" ]; then
        read -p "Remove all voice notes from $VOICE_NOTES_DIR? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VOICE_NOTES_DIR"
            echo "Voice notes directory removed."
        else
            echo "Voice notes kept."
        fi
    fi
}

# Function to remove webcam photos
remove_webcam_photos() {
    echo "Removing webcam photos..."
    PICTURES_DIR="$HOME/Pictures"
    
    # Count webcam photos
    WEBCAM_COUNT=$(find "$PICTURES_DIR" -name "webcam_*.jpg" 2>/dev/null | wc -l)
    
    if [ "$WEBCAM_COUNT" -gt 0 ]; then
        read -p "Remove $WEBCAM_COUNT webcam photos from $PICTURES_DIR? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            find "$PICTURES_DIR" -name "webcam_*.jpg" -delete
            echo "Webcam photos removed."
        else
            echo "Webcam photos kept."
        fi
    else
        echo "No webcam photos found."
    fi
}

# Function to remove temporary files
remove_temp_files() {
    echo "Removing temporary files..."
    
    # Remove temporary Jarvis files
    find /tmp -name "jarvis_*" -delete 2>/dev/null || true
    echo "Temporary Jarvis files removed."
}

# Function to check if we're in the Jarvis directory
check_jarvis_directory() {
    if [ ! -f "main.py" ] || [ ! -f "utils.py" ]; then
        echo "ERROR: This doesn't appear to be a Jarvis installation directory."
        echo "Please run this script from the Jarvis project root directory."
        exit 1
    fi
}

# Main uninstall process
main() {
    # Check if we're in the right directory
    check_jarvis_directory
    
    # Ask for confirmation
    confirm_uninstall
    
    echo "Starting uninstall process..."
    echo ""
    
    # Remove user data first (most important)
    remove_user_data
    remove_webcam_photos
    echo ""
    
    # Remove generated and temporary files
    remove_generated_files
    remove_temp_files
    echo ""
    
    # Remove voice models
    remove_voice_models
    echo ""
    
    # Remove configuration files
    remove_config_files
    echo ""
    
    # Remove Python virtual environment
    remove_venv
    echo ""
    
    # Remove Vosk model
    remove_vosk_model
    echo ""
    
    # Remove Piper TTS
    remove_piper
    echo ""
    
    # Remove system packages (optional)
    remove_system_packages
    echo ""
    
    echo "==================================UNINSTALL COMPLETE============================================="
    echo ""
    echo "Jarvis has been uninstalled. The following items may still remain:"
    echo "- Project source code (you can delete the entire directory manually)"
    echo "- System packages (if you chose to keep them)"
    echo "- Piper TTS (if you chose to keep it)"
    echo "- Vosk model (if you chose to keep it)"
    echo "- Configuration files (if you chose to keep them)"
    echo ""
    echo "To completely remove everything, you can:"
    echo "1. Delete this entire directory: rm -rf $(pwd)"
    echo "2. Remove any remaining system packages manually"
    echo "3. Remove Piper TTS manually if needed"
    echo ""
    echo "Thank you for using Jarvis!"
}

# Run main function
main 