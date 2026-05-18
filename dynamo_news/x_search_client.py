import json
import os
import subprocess
from typing import List, Dict, Any


def search_x(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Production X search.
    Requires HERMES_RUNTIME=1 to use real Hermes x_search tool.
    """
    if not os.environ.get("HERMES_RUNTIME"):
        raise RuntimeError(
            "Production mode only. Real X search requires HERMES_RUNTIME=1. "
            "No sample data or development fallbacks are permitted."
        )

    try:
        result = subprocess.run(
            ["hermes", "tool", "x_search", query],
            capture_output=True, text=True, timeout=45,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return (data or [])[:limit]
    except Exception as e:
        print(f"[x_search] Hermes tool failed: {e}")

    return []


def fetch_recent_posts_for_clusters(
    clusters: List[str] | None = None, days_back: int = 1
) -> List[Dict]:
    """
    Fetch a large volume of relevant posts.
    Uses broad + targeted queries to maximize high-signal results.
    """
    queries = [
        # Core sovereignty & local AI
        'sovereignty OR "local AI" OR "self-hosted" OR offline OR airgap',
        '"on-device" OR "edge AI" OR "local inference" OR quantized',
        '"air gapped" OR "air-gapped" OR "no cloud" OR "zero telemetry"',
        
        # Governance & agents
        'governance OR "self-healing" OR "agent harness" OR "multi-agent"',
        'Polymarket OR "execution layer" OR "real money agent"',
        
        # Infrastructure & tooling
        'Hermes OR "local LLM" OR "sovereign stack" OR "local OS"',
        'Raspberry Pi OR "on-prem" OR "private inference"',
        
        # Broader high-signal
        'agent OR orchestration OR "local model" OR "self hosted"',
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

    return unique[:40]  # Allow up to 40 posts before governance