#!/bin/bash
set -e

mkdir -p voice_models
cd voice_models

# List of models and URLs (Hugging Face official links)
declare -A MODELS
MODELS["en_US-john-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/john/en_US-john-medium.onnx"
MODELS["en_US-john-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/john/en_US-john-medium.onnx.json"
MODELS["en_US-amy-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/en_US-amy-medium.onnx"
MODELS["en_US-amy-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/en_US-amy-medium.onnx.json"
MODELS["en_US-bryce-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/bryce/en_US-bryce-medium.onnx"
MODELS["en_US-bryce-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/bryce/en_US-bryce-medium.onnx.json"
MODELS["en_US-hfc_female-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/hfc_female/en_US-hfc_female-medium.onnx"
MODELS["en_US-hfc_female-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/hfc_female/en_US-hfc_female-medium.onnx.json"
MODELS["en_US-kristin-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/kristin/en_US-kristin-medium.onnx"
MODELS["en_US-kristin-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/kristin/en_US-kristin-medium.onnx.json"
MODELS["en_US-lessac-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/en_US-lessac-medium.onnx"
MODELS["en_US-lessac-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/en_US-lessac-medium.onnx.json"
MODELS["en_US-arctic-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/arctic/en_US-arctic-medium.onnx"
MODELS["en_US-arctic-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/arctic/en_US-arctic-medium.onnx.json"
MODELS["ne_NP-google-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/ne/ne_NP/google/ne_NP-google-medium.onnx"
MODELS["ne_NP-google-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/ne/ne_NP/google/ne_NP-google-medium.onnx.json"

for file in "${!MODELS[@]}"; do
  url="${MODELS[$file]}"
  if [ ! -f "$file" ]; then
    echo "Downloading $file ..."
    curl -L -o "$file" "$url"
  else
    echo "$file already exists, skipping."
  fi
done

echo "\nAll voice models downloaded to voice_models/" 