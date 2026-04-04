"""
Test minimal de Mem0 — Mémoire Cinétique locale.
Prérequis : ollama serve (avec qwen2.5:7b + nomic-embed-text)
"""

from mem0 import Memory
from config import MEM0_CONFIG

def main():
    print("Initialisation Mem0...")
    m = Memory.from_config(MEM0_CONFIG)

    # 1. Ajouter une mémoire
    print("\n--- Ajout d'une mémoire ---")
    result = m.add(
        "VISION travaille sur un corpus philosophique appelé Point Zéro, "
        "structuré en 6 piliers. Il utilise Obsidian et Google Drive.",
        user_id="vision"
    )
    print(f"Résultat: {result}")

    # 2. Rechercher
    print("\n--- Recherche sémantique ---")
    results = m.search("corpus philosophique", user_id="vision")
    for r in results:
        if isinstance(r, dict):
            score = r.get('score', '?')
            mem = r.get('memory', r)
            print(f"  [{score}] {mem}")
        else:
            print(f"  {r}")

    # 3. Lister tout
    print("\n--- Toutes les mémoires ---")
    all_mem = m.get_all(user_id="vision")
    items = all_mem.get("results", all_mem) if isinstance(all_mem, dict) else all_mem
    for mem in items:
        if isinstance(mem, dict):
            print(f"  - {mem.get('memory', mem)}")
        else:
            print(f"  - {mem}")

    print("\nMémoire Cinétique opérationnelle.")

if __name__ == "__main__":
    main()
