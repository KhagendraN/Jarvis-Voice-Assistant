import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
import tempfile
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger("SetupJarvis")

logger = setup_logging()

def check_command(command):
    """Check if a command is available in PATH"""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_system_packages():
    """Install system packages based on the distribution"""
    logger.info("Checking system dependencies...")
    
    # Check for required commands
    required_commands = ['ffmpeg', 'rofi', 'mpv', 'aplay']
    missing_commands = []
    
    for cmd in required_commands:
        if not check_command(cmd):
            missing_commands.append(cmd)
    
    if missing_commands:
        logger.warning(f"Missing system commands: {', '.join(missing_commands)}")
        logger.info("Please install these packages manually:")
        
        # Detect package manager and provide installation commands
        if os.path.exists('/etc/debian_version'):
            logger.info("  sudo apt-get install ffmpeg rofi mpv alsa-utils")
        elif os.path.exists('/etc/arch-release'):
            logger.info("  sudo pacman -S ffmpeg rofi mpv alsa-utils")
        elif os.path.exists('/etc/fedora-release'):
            logger.info("  sudo dnf install ffmpeg rofi mpv alsa-utils")
        else:
            logger.info("  Please install: ffmpeg, rofi, mpv, aplay")
        
        logger.info("Or run the bash install script with sudo: sudo bash install.sh")
    else:
        logger.info("✓ All system dependencies are available")

def install_piper():
    """Install Piper TTS"""
    logger.info("Installing Piper TTS...")
    
    if check_command('piper'):
        logger.info("✓ Piper TTS already installed")
        return True
    
    try:
        # Download and install Piper
        piper_version = "1.2.0"
        piper_arch = "linux-x86_64"
        piper_url = f"https://github.com/rhasspy/piper/releases/download/v{piper_version}/piper_{piper_version}_{piper_arch}.tar.gz"
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            logger.info("Downloading Piper TTS...")
            urllib.request.urlretrieve(piper_url, "piper.tar.gz")
            
            logger.info("Extracting Piper...")
            subprocess.run(['tar', '-xzf', 'piper.tar.gz'], check=True)
            
            # Move to /usr/local/bin (requires sudo)
            logger.info("Installing Piper to /usr/local/bin...")
            subprocess.run(['sudo', 'mv', 'piper', '/usr/local/bin/'], check=True)
            subprocess.run(['sudo', 'chmod', '+x', '/usr/local/bin/piper'], check=True)
            
            logger.info("✓ Piper TTS installed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"✗ ERROR: Failed to install Piper TTS: {e}")
        logger.info("Please install Piper manually from: https://github.com/rhasspy/piper")
        return False

def download_vosk_model():
    """Download Vosk speech recognition model"""
    logger.info("Setting up Vosk speech recognition model...")
    
    vosk_model_dir = os.path.expanduser("~/Downloads")
    vosk_model_name = "vosk-model-small-en-us-0.15"
    vosk_model_path = os.path.join(vosk_model_dir, vosk_model_name)
    vosk_model_url = f"https://alphacephei.com/vosk/models/{vosk_model_name}.zip"
    
    if os.path.exists(vosk_model_path):
        logger.info("✓ Vosk model already exists")
        return True
    
    try:
        os.makedirs(vosk_model_dir, exist_ok=True)
        os.chdir(vosk_model_dir)
        
        logger.info("Downloading Vosk model...")
        urllib.request.urlretrieve(vosk_model_url, f"{vosk_model_name}.zip")
        
        logger.info("Extracting Vosk model...")
        with zipfile.ZipFile(f"{vosk_model_name}.zip", 'r') as zip_ref:
            zip_ref.extractall(vosk_model_dir)
        
        # Clean up zip file
        os.remove(f"{vosk_model_name}.zip")
        
        logger.info("✓ Vosk model installed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ ERROR: Failed to download Vosk model: {e}")
        logger.info("Please download manually from: https://alphacephei.com/vosk/models")
        logger.info(f"Extract to: {vosk_model_path}")
        return False

def main():
    logger.info("Setting up JarvisProject...")
    
    # Install system dependencies
    install_system_packages()
    
    # Install Piper TTS
    piper_installed = install_piper()
    
    # Download Vosk model
    vosk_installed = download_vosk_model()
    
    # Copy config template
    if not os.path.exists('config.py') and os.path.exists('config_template.py'):
        shutil.copy('config_template.py', 'config.py')
        logger.info("Copied config_template.py to config.py. Please edit it with your API keys.")

    # Copy contact template
    if not os.path.exists('contact.json') and os.path.exists('contact_template.json'):
        shutil.copy('contact_template.json', 'contact.json')
        logger.info("Copied contact_template.json to contact.json. Please edit it with your contacts.")

    # Check for face image
    dest_img = os.path.join('static', 'known_image.jpeg')
    if not os.path.exists(dest_img):
        logger.warning("WARNING: No face image found. Please add your face image as static/known_image.jpeg for face authentication.")

    # Verify critical dependencies
    logger.info("\nVerifying installation...")
    if piper_installed and check_command('piper'):
        logger.info("✓ Piper TTS is installed and available")
    else:
        logger.error("✗ ERROR: Piper TTS is not available. Please install manually.")
    
    if vosk_installed and os.path.exists(os.path.expanduser("~/Downloads/vosk-model-small-en-us-0.15")):
        logger.info("✓ Vosk model is installed")
    else:
        logger.error("✗ ERROR: Vosk model is missing. Please download manually.")
    
    if check_command('ffmpeg'):
        logger.info("✓ FFmpeg is installed")
    else:
        logger.warning("✗ WARNING: FFmpeg not found. Some features may not work.")
    
    if check_command('rofi'):
        logger.info("✓ Rofi is installed")
    else:
        logger.warning("✗ WARNING: Rofi not found. GUI selection features may not work.")
    
    if check_command('mpv'):
        logger.info("✓ MPV is installed")
    else:
        logger.warning("✗ WARNING: MPV not found. Media playback features may not work.")

    logger.info("\n==================================SETUP COMPLETE=================================================")
    logger.info("Next steps:")
    logger.info("1. Edit config.py with your API keys")
    logger.info("2. Edit contact.json with your contacts")
    logger.info("3. Add your face image as static/known_image.jpeg")
    logger.info("4. Download voice models: bash voice_models/voice_setup.sh")
    logger.info("5. Install Python dependencies: pip install -r requirements.txt")
    logger.info("6. Create virtual environment: python3 -m venv venv")
    logger.info("7. Activate your venv: source venv/bin/activate")
    logger.info("8. Run Jarvis: python main.py")
    logger.info("")
    logger.info("If you encounter any issues, check the troubleshooting section in README.md")

if __name__ == "__main__":
    main() 