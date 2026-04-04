"""
Mémoire Cinétique — Configuration Mem0 locale
Tout tourne sur Ollama, zéro cloud, zéro API payante.
"""

import os

_HERE = os.path.dirname(os.path.abspath(__file__))

MEM0_CONFIG = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "qwen2.5:7b-instruct-q5_K_M",
            "ollama_base_url": "http://localhost:11434",
            "temperature": 0.1,
            "max_tokens": 2000,
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            "ollama_base_url": "http://localhost:11434",
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "memoire_cinetique",
            "path": os.path.join(_HERE, "qdrant_data"),
            "embedding_model_dims": 768,
        }
    },
    "version": "v1.1"
}
