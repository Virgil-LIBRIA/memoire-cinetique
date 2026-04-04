# Mémoire Cinétique

Couche mémoire persistante locale pour le système Point Zéro.

Basée sur [Mem0](https://github.com/mem0ai/mem0), elle extrait automatiquement des faits des conversations, les vectorise via embeddings locaux, et les rend interrogeables par similarité sémantique.

## Architecture

```
Claude Code ──MCP──> mcp_server.py ──> Mem0 ──> Ollama (LLM + embeddings)
                                         │
                                         └──> Qdrant local (vecteurs fichier)
```

**100% local.** Zéro cloud, zéro API payante. Survit sans abonnement.

## Prérequis

- Python 3.10+
- [Ollama](https://ollama.com) avec les modèles :
  - `qwen2.5:7b-instruct-q5_K_M` (extraction de faits)
  - `nomic-embed-text` (embeddings 768 dims)

```bash
ollama pull qwen2.5:7b-instruct-q5_K_M
ollama pull nomic-embed-text
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### En direct (Python)
```bash
ollama serve  # dans un terminal séparé
python test_mem0.py
```

### Via Claude Code (MCP)
Ajouter dans `.mcp.json` à la racine du projet :
```json
{
  "mcpServers": {
    "memoire-cinetique": {
      "command": "python",
      "args": ["chemin/vers/mcp_server.py"]
    }
  }
}
```

Outils MCP disponibles :
| Outil | Description |
|-------|-------------|
| `memory_add` | Ajouter un fait (extraction auto par LLM) |
| `memory_search` | Recherche sémantique |
| `memory_list` | Lister toutes les mémoires |
| `memory_delete` | Supprimer par ID |

## Contexte

Ce projet fait partie de l'écosystème [Point Zéro](https://github.com/Virgil-LIBRIA) :
- **Chambre Réverbérante** = mémoire du corpus (statique, embeddings sur fichiers)
- **Mémoire Cinétique** = mémoire des interactions (dynamique, faits extraits des conversations)

Dans le mapping INTemple OS : la Mémoire Cinétique est la mémoire vivante du système.

## Licence

MIT
