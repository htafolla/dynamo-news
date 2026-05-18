import json
import os
import time
import uuid
from typing import Any, Optional

import requests

from dynamo_news.governance_core import apply_decision_matrix

CALIBRATE = os.environ.get("DYNAMO_NEWS_CALIBRATE") == "1"

GOVERNANCE_ENDPOINT = (
    "https://mcp-production-80e2.up.railway.app/call_connected_tool"
)
TIMEOUT_SECONDS = 12
MAX_RETRIES = 3
RETRY_DELAY = 1.0


def _call_tool(tool_name: str, params: dict[str, Any]) -> Optional[dict]:
    """Generic caller with exponential backoff."""
    payload = {"tool_name": tool_name, "params": params}

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                GOVERNANCE_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT_SECONDS,
            )
            resp.raise_for_status()
            return resp.json().get("result")
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2**attempt)
                print(
                    f"[Dynamo] Retry {attempt + 1}/{MAX_RETRIES} "
                    f"for {tool_name} in {delay:.1f}s: {e}"
                )
                time.sleep(delay)

    print(
        f"[Dynamo] All {MAX_RETRIES} retries failed "
        f"for {tool_name}: {last_error}"
    )
    return None


def evaluate_governance(
    proposal_text: str, agent_reviews: list[str] | None = None
) -> Optional[dict]:
    proposal_id = f"post-{uuid.uuid4().hex[:8]}"
    params = {
        "proposalId": proposal_id,
        "proposalText": proposal_text,
        "agentReviews": agent_reviews or [
            "Signal relevance to AI \u00d7 Web3 sovereignty and governance"
        ],
    }
    return _call_tool("evaluate_governance", params)


def govern_with_solar(proposal_text: str, base_vote_weight: float = 1.0) -> Optional[dict]:
    params = {"proposal": proposal_text, "baseVoteWeight": base_vote_weight}
    return _call_tool("govern_with_solar", params)


def evaluate_post(post_text: str) -> dict:
    """Run full governance and return structured result with matrix output.

    Returns dict with keys: passed, matrix, raw_metrics, solar_activity, error.
    """
    gov_result = evaluate_governance(post_text)
    if not gov_result:
        return {"passed": False, "error": "governance_unreachable", "matrix": None}

    resonance = gov_result.get("resonanceScore")
    isotopic_ratio = gov_result.get("isotopicRatio")

    if resonance is not None and isotopic_ratio is not None:
        solar_activity = "quiet"
        solar_result = govern_with_solar(post_text)
        if solar_result:
            sc = solar_result.get("solarContext", {})
            solar_activity = sc.get("solarActivityLevel", "quiet")

        matrix = apply_decision_matrix(
            resonance=resonance,
            isotopic_ratio=isotopic_ratio,
            vortex_volume=gov_result.get("vortexVolume"),
            historical_coherence=gov_result.get("historicalCoherence"),
            solar_activity=solar_activity,
        )

        row = f"resonance={resonance:.3f} ratio={isotopic_ratio:.3f}"
        print(f"  [PHI/TAU] {row} → {matrix['recommendation']} "
              f"(conf={matrix['confidence']} w={matrix['voteWeight']})")
        for r in matrix["reasons"]:
            print(f"    • {r}")

        return {
            "passed": matrix["recommendation"] == "PASS" and matrix["confidence"] >= 0.75,
            "matrix": matrix,
            "raw_metrics": {
                "resonanceScore": resonance,
                "isotopicRatio": isotopic_ratio,
                "vortexVolume": gov_result.get("vortexVolume"),
                "historicalCoherence": gov_result.get("historicalCoherence"),
            },
            "solar_activity": solar_activity,
        }

    recommendation = gov_result.get("recommendation", "REJECT")
    confidence = gov_result.get("confidence", 0.0)
    passed = recommendation == "PASS" and confidence >= 0.75
    return {
        "passed": passed,
        "matrix": {"recommendation": recommendation, "confidence": confidence},
        "raw_metrics": None,
    }


def should_include_post(post_text: str) -> bool:
    """High-level gate. In calibration mode, always returns True and logs matrix."""
    result = evaluate_post(post_text)
    if CALIBRATE:
        if not result.get("passed"):
            m = result.get("matrix", {})
            print(f"  [CALIBRATE] Would have REJECTED — {m.get('recommendation')} "
                  f"(conf={m.get('confidence')})")
        return True
    return result.get("passed", False)


if __name__ == "__main__":
    test = (
        "Local LLMs give you free inference, complete privacy, "
        "offline access, model ownership, and fine-tuning capability."
    )
    print("Testing governance on sample post...\n")
    print(f"Include post? {should_include_post(test)}")
