import os
import urllib.request

MODELS = {
    "en_US-john-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/john/en_US-john-medium.onnx",
    "en_US-john-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/john/en_US-john-medium.onnx.json",
    "en_US-amy-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/en_US-amy-medium.onnx",
    "en_US-amy-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/en_US-amy-medium.onnx.json",
    "en_US-bryce-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/bryce/en_US-bryce-medium.onnx",
    "en_US-bryce-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/bryce/en_US-bryce-medium.onnx.json",
    "en_US-hfc_female-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/hfc_female/en_US-hfc_female-medium.onnx",
    "en_US-hfc_female-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/hfc_female/en_US-hfc_female-medium.onnx.json",
    "en_US-kristin-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/kristin/en_US-kristin-medium.onnx",
    "en_US-kristin-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/kristin/en_US-kristin-medium.onnx.json",
    "en_US-lessac-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/en_US-lessac-medium.onnx",
    "en_US-lessac-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/en_US-lessac-medium.onnx.json",
    "en_US-arctic-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/arctic/en_US-arctic-medium.onnx",
    "en_US-arctic-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/arctic/en_US-arctic-medium.onnx.json",
    "ne_NP-google-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ne/ne_NP/google/ne_NP-google-medium.onnx",
    "ne_NP-google-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ne/ne_NP/google/ne_NP-google-medium.onnx.json",
}

def download_file(url, dest):
    print(f"Downloading {dest} ...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Downloaded {dest}")
    except Exception as e:
        print(f"Failed to download {dest}: {e}")

def main():
    os.makedirs("voice_models", exist_ok=True)
    for fname, url in MODELS.items():
        dest = os.path.join("voice_models", fname)
        if not os.path.exists(dest):
            download_file(url, dest)
        else:
            print(f"{fname} already exists, skipping.")
    print("\nAll voice models downloaded to voice_models/")

if __name__ == "__main__":
    main() 