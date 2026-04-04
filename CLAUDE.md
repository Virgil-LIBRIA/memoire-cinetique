# Mémoire Cinétique — Mem0 local

## Quoi
Couche mémoire persistante locale basée sur [Mem0](https://github.com/mem0ai/mem0).
Extrait automatiquement des faits des conversations, les vectorise, les déduplique.

## Pourquoi
- **Mémoire du corpus** = Chambre Réverbérante (localhost:5002) — statique, indexe les fichiers
- **Mémoire des interactions** = Mémoire Cinétique (Mem0) — dynamique, retient les patterns, décisions, préférences

Dans le mapping INTemple : Mémoire Cinétique = la mémoire vivante du système.

## Stack
- **Mem0** (`pip install mem0ai ollama`) — extraction de faits + recherche sémantique
- **Ollama** — LLM local pour extraction (`qwen2.5:7b-instruct-q5_K_M`) + embeddings (`nomic-embed-text`)
- **Qdrant local** — stockage vecteurs en fichiers (pas de serveur, pas de Docker)
- **SQLite** — historique des opérations mémoire (`~/.mem0/history.db`)
- **FastMCP** — serveur MCP pour bridge avec Claude Code

## Fichiers
```
memoire_cinetique/
├── CLAUDE.md          ← ce fichier (contexte pour Claude Code)
├── README.md          ← documentation publique (GitHub)
├── config.py          ← configuration Mem0 (modèles, paths, vector store)
├── mcp_server.py      ← serveur MCP (4 outils : add, search, list, delete)
├── test_mem0.py       ← script de test minimal
├── requirements.txt   ← dépendances Python
└── qdrant_data/       ← données vectorielles (généré auto, gitignored)
```

## Serveur MCP
Le serveur MCP expose 4 outils à Claude Code :
- `memory_add` — ajouter un fait (extraction automatique par LLM)
- `memory_search` — recherche sémantique dans les souvenirs
- `memory_list` — lister toutes les mémoires
- `memory_delete` — supprimer une mémoire par ID

Configuration dans `Documents/.mcp.json` :
```json
{
  "mcpServers": {
    "memoire-cinetique": {
      "command": "python",
      "args": ["C:\\Users\\VISION\\Documents\\Projets\\memoire_cinetique\\mcp_server.py"]
    }
  }
}
```

## Utilisation directe (Python)
```bash
# Prérequis : Ollama doit tourner
ollama serve

# Test
cd Documents/Projets/memoire_cinetique
python test_mem0.py
```

```python
from mem0 import Memory
from config import MEM0_CONFIG

m = Memory.from_config(MEM0_CONFIG)
m.add("fait à retenir", user_id="vision")
m.search("recherche sémantique", user_id="vision")
m.get_all(user_id="vision")
```

## Dépendances
- `mem0ai` (1.0.10+)
- `ollama` (Python client)
- `fastmcp` (3.2.0+)
- Ollama server avec `qwen2.5:7b-instruct-q5_K_M` et `nomic-embed-text`

## À faire
- [ ] Prompt d'extraction personnalisé pour le contexte PZ (français, concepts philosophiques)
- [ ] Ingestion des mémoires Claude Code existantes
- [ ] Bridge avec la Chambre Réverbérante
