import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
import tempfile
import platform

def check_command(command):
    """Check if a command is available in PATH"""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_system_packages():
    """Install system packages based on the distribution"""
    print("Checking system dependencies...")
    
    # Check for required commands
    required_commands = ['ffmpeg', 'rofi', 'mpv', 'aplay']
    missing_commands = []
    
    for cmd in required_commands:
        if not check_command(cmd):
            missing_commands.append(cmd)
    
    if missing_commands:
        print(f"Missing system commands: {', '.join(missing_commands)}")
        print("Please install these packages manually:")
        
        # Detect package manager and provide installation commands
        if os.path.exists('/etc/debian_version'):
            print("  sudo apt-get install ffmpeg rofi mpv alsa-utils")
        elif os.path.exists('/etc/arch-release'):
            print("  sudo pacman -S ffmpeg rofi mpv alsa-utils")
        elif os.path.exists('/etc/fedora-release'):
            print("  sudo dnf install ffmpeg rofi mpv alsa-utils")
        else:
            print("  Please install: ffmpeg, rofi, mpv, aplay")
        
        print("Or run the bash install script with sudo: sudo bash install.sh")
    else:
        print("✓ All system dependencies are available")

def install_piper():
    """Install Piper TTS"""
    print("Installing Piper TTS...")
    
    if check_command('piper'):
        print("✓ Piper TTS already installed")
        return True
    
    try:
        # Download and install Piper
        piper_version = "1.2.0"
        piper_arch = "linux-x86_64"
        piper_url = f"https://github.com/rhasspy/piper/releases/download/v{piper_version}/piper_{piper_version}_{piper_arch}.tar.gz"
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            print("Downloading Piper TTS...")
            urllib.request.urlretrieve(piper_url, "piper.tar.gz")
            
            print("Extracting Piper...")
            subprocess.run(['tar', '-xzf', 'piper.tar.gz'], check=True)
            
            # Move to /usr/local/bin (requires sudo)
            print("Installing Piper to /usr/local/bin...")
            subprocess.run(['sudo', 'mv', 'piper', '/usr/local/bin/'], check=True)
            subprocess.run(['sudo', 'chmod', '+x', '/usr/local/bin/piper'], check=True)
            
            print("✓ Piper TTS installed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ ERROR: Failed to install Piper TTS: {e}")
        print("Please install Piper manually from: https://github.com/rhasspy/piper")
        return False

def download_vosk_model():
    """Download Vosk speech recognition model"""
    print("Setting up Vosk speech recognition model...")
    
    vosk_model_dir = os.path.expanduser("~/Downloads")
    vosk_model_name = "vosk-model-small-en-us-0.15"
    vosk_model_path = os.path.join(vosk_model_dir, vosk_model_name)
    vosk_model_url = f"https://alphacephei.com/vosk/models/{vosk_model_name}.zip"
    
    if os.path.exists(vosk_model_path):
        print("✓ Vosk model already exists")
        return True
    
    try:
        os.makedirs(vosk_model_dir, exist_ok=True)
        os.chdir(vosk_model_dir)
        
        print("Downloading Vosk model...")
        urllib.request.urlretrieve(vosk_model_url, f"{vosk_model_name}.zip")
        
        print("Extracting Vosk model...")
        with zipfile.ZipFile(f"{vosk_model_name}.zip", 'r') as zip_ref:
            zip_ref.extractall(vosk_model_dir)
        
        # Clean up zip file
        os.remove(f"{vosk_model_name}.zip")
        
        print("✓ Vosk model installed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ ERROR: Failed to download Vosk model: {e}")
        print("Please download manually from: https://alphacephei.com/vosk/models")
        print(f"Extract to: {vosk_model_path}")
        return False

def main():
    print("Setting up JarvisProject...")
    
    # Install system dependencies
    install_system_packages()
    
    # Install Piper TTS
    piper_installed = install_piper()
    
    # Download Vosk model
    vosk_installed = download_vosk_model()
    
    # Copy config template
    if not os.path.exists('config.py') and os.path.exists('config_template.py'):
        shutil.copy('config_template.py', 'config.py')
        print("Copied config_template.py to config.py. Please edit it with your API keys.")

    # Copy contact template
    if not os.path.exists('contact.json') and os.path.exists('contact_template.json'):
        shutil.copy('contact_template.json', 'contact.json')
        print("Copied contact_template.json to contact.json. Please edit it with your contacts.")

    # Check for face image
    dest_img = os.path.join('static', 'known_image.jpeg')
    if not os.path.exists(dest_img):
        print("WARNING: No face image found. Please add your face image as static/known_image.jpeg for face authentication.")

    # Verify critical dependencies
    print("\nVerifying installation...")
    if piper_installed and check_command('piper'):
        print("✓ Piper TTS is installed and available")
    else:
        print("✗ ERROR: Piper TTS is not available. Please install manually.")
    
    if vosk_installed and os.path.exists(os.path.expanduser("~/Downloads/vosk-model-small-en-us-0.15")):
        print("✓ Vosk model is installed")
    else:
        print("✗ ERROR: Vosk model is missing. Please download manually.")
    
    if check_command('ffmpeg'):
        print("✓ FFmpeg is installed")
    else:
        print("✗ WARNING: FFmpeg not found. Some features may not work.")
    
    if check_command('rofi'):
        print("✓ Rofi is installed")
    else:
        print("✗ WARNING: Rofi not found. GUI selection features may not work.")
    
    if check_command('mpv'):
        print("✓ MPV is installed")
    else:
        print("✗ WARNING: MPV not found. Media playback features may not work.")

    print("\n==================================SETUP COMPLETE=================================================")
    print("Next steps:")
    print("1. Edit config.py with your API keys")
    print("2. Edit contact.json with your contacts")
    print("3. Add your face image as static/known_image.jpeg")
    print("4. Download voice models: bash voice_models/voice_setup.sh")
    print("5. Install Python dependencies: pip install -r requirements.txt")
    print("6. Create virtual environment: python3 -m venv venv")
    print("7. Activate your venv: source venv/bin/activate")
    print("8. Run Jarvis: python main.py")
    print("")
    print("If you encounter any issues, check the troubleshooting section in README.md")

if __name__ == "__main__":
    main() 