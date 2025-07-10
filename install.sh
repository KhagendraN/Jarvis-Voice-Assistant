#!/bin/bash
set -e

# Setup JarvisProject

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

echo "\nSetup complete!"
echo "- Edit config.py and contact.json with your info."
echo "- Add your face image as static/known_image.jpeg."
echo "- Activate your venv: source venv/bin/activate"
echo "- Run: python main.py" 