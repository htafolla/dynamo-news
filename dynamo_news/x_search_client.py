import json
import os
import subprocess
from typing import List, Dict, Any


def search_x(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Search X via the Hermes x_search tool when available.

    Falls back to a clear error when not running inside Hermes.
    """
    if os.environ.get("HERMES_RUNTIME"):
        try:
            result = subprocess.run(
                ["hermes", "tool", "x_search", query],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return (data or [])[:limit]
        except Exception as e:
            print(f"[x_search] Hermes tool call failed: {e}")
    else:
        print(
            "[x_search] Not running inside Hermes runtime. "
            "Set HERMES_RUNTIME=1 or implement your own x_search integration."
        )
    return []


def fetch_recent_posts_for_clusters(
    clusters: List[str] | None = None, days_back: int = 1
) -> List[Dict]:
    """Fetch posts relevant to the key clusters in the Master Index."""
    clusters = clusters or []
    all_posts = []

    queries = clusters if clusters else [
        "sovereignty OR \"local AI\" OR \"self-hosted\" OR offline",
        "governance OR \"self-healing\" OR agent harness",
        "Polymarket agent OR execution layer",
        "agent OR orchestration OR local inference",
    ]

    for q in queries:
        posts = search_x(q, limit=6)
        all_posts.extend(posts)

    seen = set()
    unique = []
    for p in all_posts:
        url = p.get("url") or p.get("id", "")
        if url not in seen:
            seen.add(url)
            unique.append(p)
    return unique[:15]
