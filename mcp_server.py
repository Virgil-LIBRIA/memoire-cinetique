"""
Mémoire Cinétique — Serveur MCP local
Bridge entre Claude Code et Mem0 (mémoire vectorielle locale).

Lancement : python mcp_server.py
Ou via Claude Code settings.json (mcpServers)
"""

import json
from fastmcp import FastMCP
from mem0 import Memory
from config import MEM0_CONFIG

mcp = FastMCP("memoire-cinetique")

# Initialisation lazy (évite de charger Ollama au démarrage si pas utilisé)
_memory = None

def get_memory():
    global _memory
    if _memory is None:
        _memory = Memory.from_config(MEM0_CONFIG)
    return _memory


@mcp.tool()
def memory_add(text: str, user_id: str = "vision") -> str:
    """Ajouter un fait, une observation ou une préférence à la Mémoire Cinétique.
    Mem0 extrait automatiquement les faits pertinents du texte.

    Args:
        text: Le texte contenant les informations à mémoriser
        user_id: Identifiant utilisateur (défaut: vision)
    """
    m = get_memory()
    result = m.add(text, user_id=user_id)
    entries = result.get("results", [])
    if not entries:
        return "Aucun fait nouveau extrait."
    facts = [e.get("memory", str(e)) for e in entries if isinstance(e, dict)]
    return f"{len(facts)} fait(s) mémorisé(s) :\n" + "\n".join(f"- {f}" for f in facts)


@mcp.tool()
def memory_search(query: str, user_id: str = "vision", limit: int = 5) -> str:
    """Rechercher dans la Mémoire Cinétique par similarité sémantique.

    Args:
        query: La requête de recherche
        user_id: Identifiant utilisateur (défaut: vision)
        limit: Nombre max de résultats (défaut: 5)
    """
    m = get_memory()
    raw = m.search(query, user_id=user_id, limit=limit)
    # Mem0 peut retourner une liste ou un dict {"results": [...]}
    if isinstance(raw, dict):
        results = raw.get("results", [])
    elif isinstance(raw, list):
        results = raw
    else:
        results = []
    if not results:
        return "Aucun souvenir trouvé."
    lines = []
    for r in results:
        if isinstance(r, dict):
            score = r.get("score", "?")
            mem = r.get("memory", str(r))
            lines.append(f"[{score:.3f}] {mem}" if isinstance(score, float) else f"[{score}] {mem}")
        else:
            lines.append(str(r))
    return f"{len(lines)} souvenir(s) trouvé(s) :\n" + "\n".join(lines)


@mcp.tool()
def memory_list(user_id: str = "vision") -> str:
    """Lister toutes les mémoires stockées pour un utilisateur.

    Args:
        user_id: Identifiant utilisateur (défaut: vision)
    """
    m = get_memory()
    all_mem = m.get_all(user_id=user_id)
    items = all_mem.get("results", all_mem) if isinstance(all_mem, dict) else all_mem
    if not items:
        return "Mémoire vide."
    lines = []
    for mem in items:
        if isinstance(mem, dict):
            lines.append(f"- [{mem.get('id', '?')[:8]}] {mem.get('memory', str(mem))}")
        else:
            lines.append(f"- {mem}")
    return f"{len(lines)} souvenir(s) en mémoire :\n" + "\n".join(lines)


@mcp.tool()
def memory_delete(memory_id: str) -> str:
    """Supprimer une mémoire spécifique par son ID.

    Args:
        memory_id: L'ID de la mémoire à supprimer
    """
    m = get_memory()
    m.delete(memory_id)
    return f"Mémoire {memory_id} supprimée."


if __name__ == "__main__":
    mcp.run()
