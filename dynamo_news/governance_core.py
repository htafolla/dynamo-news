"""PHI/TAU decision matrix — ported from StringRay governance-core.ts.

Pure logic, no side effects. Applied client-side to the raw metrics
returned by the Dynamo governance endpoint.
"""

PHI = 1.666
TAU = 0.865


def apply_decision_matrix(
    *,
    resonance: float,
    isotopic_ratio: float,
    vortex_volume: float | None = None,
    historical_coherence: float | None = None,
    solar_activity: str = "quiet",
) -> dict:
    """Apply the PHI/TAU matrix to derive recommendation, confidence, voteWeight
    and structured reasons from raw Dynamo metrics. Mirrors StringRay's
    applyDecisionMatrix() in governance-core.ts.
    """
    reasons: list[str] = []
    recommendation = "NEEDS_REVISION"
    confidence = 0.75
    vote_weight = 1.0

    # Tiers (PHI/TAU thresholds)
    if resonance >= 0.92 and isotopic_ratio >= 0.95:
        recommendation = "PASS"
        confidence = 0.97
        vote_weight = 1.4
        reasons.append("High symbiotic resonance (PHI-aligned)")
    elif resonance >= 0.82 and isotopic_ratio >= 0.88:
        recommendation = "PASS"
        confidence = 0.89
        vote_weight = 1.15
        reasons.append("Solid alignment above TAU threshold")
    elif resonance < 0.75 or isotopic_ratio < 0.80:
        recommendation = "REJECT"
        confidence = 0.84
        reasons.append("Signal below critical threshold (1 - TAU)")
    else:
        reasons.append("Moderate resonance - requires refinement")

    # Vortex volume — low inertia demotes PASS to needs_revision
    if vortex_volume is not None and vortex_volume < 2.5e25:
        reasons.append("Low inertial mass (W x M = V)")
        if recommendation == "PASS":
            recommendation = "NEEDS_REVISION"

    # Historical coherence
    if historical_coherence is not None:
        if historical_coherence < 0.70:
            reasons.append("Weak historical alignment with past decisions")
            if recommendation == "PASS":
                recommendation = "NEEDS_REVISION"
        elif historical_coherence > 0.90:
            reasons.append("Strong continuity with previous governance")
            vote_weight *= 1.1

    # Solar adjustment
    if solar_activity in ("active", "storm"):
        vote_weight *= 0.92
        reasons.append("Elevated solar activity - increased caution applied")

    return {
        "recommendation": recommendation,
        "confidence": max(0.5, min(0.99, confidence)),
        "voteWeight": round(max(0.5, min(1.8, vote_weight)), 2),
        "reasons": reasons,
    }
