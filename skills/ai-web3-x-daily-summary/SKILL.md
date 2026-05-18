---
name: ai-web3-x-daily-summary
description: "Cross-correlates X feeds on AI and Web3 to surface the highest-value posts, discussions, and linked articles at their intersection. Applies Dynamo Governance Layer (evaluate_governance + govern_with_solar + PHI/TAU matrix) to validate findings before inclusion. Generates a structured daily summary with trends, top insights, and governance verdicts."
---

# AI × Web3 X Daily Summary Skill (v2.1)

**Purpose**: Deliver high-signal, low-noise daily briefings on the AI-Web3 convergence by intelligently querying, filtering, synthesizing X activity, and applying Dynamo Governance to validate the highest-value findings.

## Core Workflow (execute in this order)

1. **Establish Time Window**
   - Use current date. Set since: to yesterday or 48 hours ago.

2. **Execute Multi-Vector X Searches**
   - Use real X search via Hermes runtime
   - Include sovereignty, local AI, governance, Polymarket, and agent-related vectors
   - Prioritize @Blaze0x1 interests where relevant

3. **Cross-Correlation & Ranking**
   - Rank by composite value score (engagement, credibility, depth, timeliness, isotopic ratio)

4. **Dynamo Governance Layer**
   - Call `evaluate_governance` on each candidate
   - Apply `govern_with_solar` for strategic context
   - Use PHI/TAU decision matrix client-side
   - Only keep items with strong PASS or high NEEDS_REVISION scores

5. **Synthesize Daily Briefing**
   - Include actual tweet text, likes, replies, and direct links
   - Tag every post with Repertoire Category
   - Rank by governance score

6. **Quality Controls**
   - Always disclose search parameters and governance results
   - Fail closed if governance is unreachable

## Output Format

Clean, scannable daily briefing with:
- Ranked list by governance strength
- Direct X links
- Governance scores (resonance, isotopic ratio, recommendation)
- Repertoire category tags

## Trigger Conditions

- Daily AI-Web3 briefing
- Best X posts on decentralized AI / Web3 AI
- Latest crypto AI trends
- Top influencers AI x blockchain
- "summarize AI Web3 today"

## Version

- Skill: ai-web3-x-daily-summary v2.1
- Governance: Dynamo MCP + PHI/TAU matrix
- Date: May 2026