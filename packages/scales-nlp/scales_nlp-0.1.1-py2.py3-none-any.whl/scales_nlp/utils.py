import os
from pathlib import Path
import json

CACHE_PATH = Path.home() / '.cache' / 'scales_nlp'
CACHE_PATH.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = CACHE_PATH / 'config.json'

CONFIG_KEYS = [
    'HUGGING_FACE_TOKEN',
    'LABEL_STUDIO_HOST',
    'LABEL_STUDIO_TOKEN',
]

DEVELOPER_CONFIG_KEYS = [
    'DOCKET_VIEWER_HOST',
    'DOCKET_VIEWER_API_KEY',
]

DEFAULT_TRAINING_ARGS = {
    'model_name': 'scales-okn/docket-language-model',
    'max_length': 256,
    'eval_split': 0.2,
    'epochs': 10,
    'train_batch_size': 2,
    'eval_batch_size': 8,
    'gradient_accumulation_steps': 4,
    'learning_rate': 3e-5,
    'warmup_ratio': 0.06,
    'weight_decay': 0.01,
    'save_steps': 100,
}

def load_json(path):
    with open(str(path), 'r') as f:
        return json.loads(f.read())

def setup_config():
    config = {}
    if CONFIG_PATH.exists():
        config = load_json(CONFIG_PATH)
    
    for key in CONFIG_KEYS + DEVELOPER_CONFIG_KEYS:
        value = os.environ.get(key, None)
        config[key] = value

    return config

def convert_default_binary_outputs(predictions):
    if isinstance(predictions[0], str):
        predictions = [prediction == 'LABEL_1' for prediction in predictions]
    elif isinstance(predictions[0], dict):
        predictions = [prediction['LABEL_1'] for prediction in predictions]
    return predictions


config = setup_config()


