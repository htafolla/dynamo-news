#!/usr/bin/env python3
"""
Dynamo Governance Client (v2.1)
Handles calls to the external Dynamo Governance MCP endpoint.
"""

import requests
import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

GOVERNANCE_ENDPOINT = "https://mcp-production-80e2.up.railway.app/call_connected_tool"
TIMEOUT_SECONDS = 12

def _call_tool(tool_name: str, params: Dict[str, Any]) -> Optional[Dict]:
    """Generic caller for Dynamo governance tools."""
    payload = {
        "tool_name": tool_name,
        "params": params
    }

    try:
        response = requests.post(
            GOVERNANCE_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT_SECONDS
        )
        response.raise_for_status()
        data = response.json()
        return data.get("result")
    except Exception as e:
        print(f"[Dynamo Governance] Error calling {tool_name}: {e}")
        return None


def evaluate_governance(proposal_text: str, agent_reviews: list = None) -> Optional[Dict]:
    """
    Evaluates a post/proposal using the core governance model.
    Returns recommendation: PASS | NEEDS_REVISION | REJECT
    """
    proposal_id = f"post-{uuid.uuid4().hex[:8]}"

    params = {
        "proposalId": proposal_id,
        "proposalText": proposal_text,
        "agentReviews": agent_reviews or ["Signal relevance to AI × Web3 sovereignty and governance"]
    }

    result = _call_tool("evaluate_governance", params)
    return result


def govern_with_solar(proposal_text: str, base_vote_weight: float = 1.0) -> Optional[Dict]:
    """
    Runs governance with real-time solar context (NOAA GOES).
    Returns finalRecommendation and solarContext.
    """
    params = {
        "proposal": proposal_text,
        "baseVoteWeight": base_vote_weight
    }

    result = _call_tool("govern_with_solar", params)
    return result


def should_include_post(post_text: str, min_confidence: float = 0.75) -> bool:
    """
    Full governance check for a post.
    Returns True only if governance recommends PASS with sufficient confidence.
    """
    # First pass: core governance
    gov_result = evaluate_governance(post_text)

    if not gov_result:
        print("[Dynamo] Governance call failed — falling back to inclusion")
        return True  # Fail open for now

    recommendation = gov_result.get("recommendation", "REJECT")
    confidence = gov_result.get("confidence", 0.0)

    if recommendation != "PASS" or confidence < min_confidence:
        print(f"[Dynamo] Post rejected by governance: {recommendation} (conf={confidence})")
        return False

    # Second pass: solar-enhanced check (optional but recommended)
    solar_result = govern_with_solar(post_text)
    if solar_result:
        final_rec = solar_result.get("finalRecommendation", recommendation)
        if final_rec != "PASS":
            print(f"[Dynamo] Post rejected after solar adjustment: {final_rec}")
            return False

    return True


if __name__ == "__main__":
    # Quick test
    test_post = "Local LLMs give you free inference, complete privacy, offline access, model ownership, and fine-tuning capability."
    print("Testing governance on sample post...")
    result = evaluate_governance(test_post)
    print(json.dumps(result, indent=2))