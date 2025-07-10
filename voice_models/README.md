# Voice Models Directory

This directory is for storing Piper TTS voice models used by Jarvis Voice Assistant.

## Setup Instructions

### 1. Download Voice Models

Download Piper TTS voice models from the official repository:
- Visit: https://huggingface.co/rhasspy/piper-voices
- Download the `.onnx` and `.onnx.json` files for your preferred voices

### 2. Place Models in This Directory

Place the downloaded voice model files in this directory:
```
voice_models/
├── en_US-john-medium.onnx
├── en_US-john-medium.onnx.json
├── en_US-amy-medium.onnx
├── en_US-amy-medium.onnx.json
└── ... (other voice models)
```

### 3. Update Configuration

Update the voice model paths in `main.py` to point to this directory:

```python
# Example voice model paths
VOICE_MODELS = {
    "Jarvis": "voice_models/en_US-john-medium.onnx",
    "Samantha": "voice_models/en_US-amy-medium.onnx",
    "Male": "voice_models/en_US-bryce-medium.onnx",
    "Female": "voice_models/en_US-kristin-medium.onnx",
    # Add more voices as needed
}
```

## Recommended Voice Models

### English Voices
- `en_US-john-medium.onnx` - Male voice, good for Jarvis
- `en_US-amy-medium.onnx` - Female voice, clear and natural
- `en_US-kristin-medium.onnx` - Female voice, professional
- `en_US-bryce-medium.onnx` - Male voice, deep and clear

### Other Languages
- `ne_NP-google-medium.onnx` - Nepali voice
- `es_ES-google-medium.onnx` - Spanish voice
- `fr_FR-google-medium.onnx` - French voice
- `de_DE-google-medium.onnx` - German voice

## File Structure

Each voice model consists of two files:
- `.onnx` - The actual voice model file
- `.onnx.json` - Configuration file for the voice

Both files are required for the voice to work properly.

## Troubleshooting

### Voice Not Working
1. Ensure both `.onnx` and `.onnx.json` files are present
2. Check file permissions (should be readable)
3. Verify the path in `main.py` is correct
4. Test with a simple command: `echo "test" | piper --model voice_models/your-model.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -`

### Poor Audio Quality
1. Try different voice models
2. Ensure your audio system is properly configured
3. Check if your speakers/headphones are working

### Model Not Found
1. Verify the file path in `main.py`
2. Check if the model files are in the correct directory
3. Ensure the model name matches exactly (case-sensitive)

## Adding Custom Voices

To add your own custom voices:
1. Train a voice model using Piper's training tools
2. Place the `.onnx` and `.onnx.json` files in this directory
3. Update the `VOICE_MODELS` dictionary in `main.py`
4. Test the voice with a simple command

## Notes

- Voice models can be large (50-200MB each)
- Keep only the voices you plan to use to save space
- The `.gitignore` file excludes voice models from version control
- Consider using symbolic links if you have models in other locations 