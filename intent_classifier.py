from sentence_transformers import SentenceTransformer, util
import torch
import logging
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("IntentClassifier")

# Load intents from a JSON file for maintainability
INTENTS_PATH = os.path.join(os.path.dirname(__file__), 'intents.json')
with open(INTENTS_PATH, 'r') as f:
    intents = json.load(f)

embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Flatten intents into phrases and labels
intent_phrases = []
intent_labels = []

for intent, phrases in intents.items():
    for phrase in phrases:
        intent_phrases.append(phrase.lower().strip())  # Normalize
        intent_labels.append(intent)

# Precompute embeddings once
phrase_embeddings = embedder.encode(intent_phrases, convert_to_tensor=True)

def detect_intent(text, confidence_threshold=0.55):
    """Returns (intent, confidence) using semantic similarity"""
    text = text.lower().strip()
    query_embedding = embedder.encode(text, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(query_embedding, phrase_embeddings)[0]

    top_score, top_idx = float(cosine_scores.max()), int(cosine_scores.argmax())
    if top_score >= confidence_threshold:
        return intent_labels[top_idx], top_score
    else:
        logger.warning(f"Unrecognized or ambiguous command: '{text}' (score={top_score:.2f})")
        return None, top_score
      
#this is primary classifier 
# this has been used to determine user intent ( defined only )