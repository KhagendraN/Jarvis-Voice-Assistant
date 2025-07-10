import os, shutil

print("Setting up JarvisProject...")

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

print("\nSetup complete!")
print("- Edit config.py and contact.json with your info.")
print("- Add your face image as static/known_image.jpeg.")
print("- Install dependencies: pip install -r requirements.txt")
print("- Activate your venv: source venv/bin/activate")
print("- Run: python main.py") 