import json
import os
import subprocess
from typing import List, Dict, Any


def search_x(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Production-only X search.
    Requires running inside Hermes runtime with HERMES_RUNTIME=1.
    No sample data or fallbacks allowed.
    """
    if not os.environ.get("HERMES_RUNTIME"):
        raise RuntimeError(
            "Production mode only. Real X search requires HERMES_RUNTIME=1. "
            "No sample data or development fallbacks are permitted."
        )

    try:
        result = subprocess.run(
            ["hermes", "tool", "x_search", query],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return (data or [])[:limit]
        else:
            print(f"[x_search] Hermes tool failed: {result.stderr}")
            return []
    except Exception as e:
        print(f"[x_search] Error calling Hermes x_search: {e}")
        return []


def fetch_recent_posts_for_clusters(
    clusters: List[str] | None = None, days_back: int = 1
) -> List[Dict]:
    """
    Production X search using multiple targeted queries.
    Returns real posts only.
    """
    clusters = clusters or []

    queries = clusters if clusters else [
        'sovereignty OR "local AI" OR "self-hosted" OR offline OR "edge AI"',
        'governance OR "self-healing" OR "agent harness" OR "tri-judge"',
        'Polymarket agent OR "execution layer" OR "real-money agent"',
        'agent OR orchestration OR "local inference" OR "multi-agent"',
        '"local model" OR quantization OR GGUF OR "on-device"',
        'sovereign OR airgap OR "zero telemetry" OR "private AI"',
        '"memory" OR RAG OR "knowledge graph" OR "agent memory"',
    ]

    all_posts = []
    for q in queries:
        posts = search_x(q, limit=12)
        all_posts.extend(posts)

    # Deduplicate by URL
    seen = set()
    unique = []
    for p in all_posts:
        url = p.get("url") or p.get("id", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(p)

    return unique[:50]