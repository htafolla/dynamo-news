---
name: dynamo-news-daily-summary
description: "Cross-correlates X feeds on AI, agents, governance, sovereignty, local inference and Web3. Applies Dynamo Governance Layer to evaluate and validate findings. Generates structured daily briefings with trends, top insights, and governance verdicts."
---

# Dynamo News Daily Summary Skill

**Purpose:** Deliver high-signal daily briefings on the AI × Web3 / Sovereign AI intersection by intelligently querying X activity and applying the Dynamo Governance Layer.

## Core Workflow (execute in this order)

1. **Establish Time Window**
   Use current date. Search since: yesterday or last 48 hours.

2. **Execute Multi-Vector X Searches**
   - Personalized searches from @Blaze0x1 feed + interests (sovereignty, local AI, governance, Polymarket)
   - Use semantic + keyword searches with engagement filters

3. **Cross-Correlation & Ranking**
   - Rank by composite value score (engagement, credibility, depth, cross-link strength)

4. **Dynamo Governance Layer**
   - Use `evaluate_governance` — core governance (recommendation: PASS / NEEDS_REVISION / REJECT)
   - Use `govern_with_solar` — strategic proposals with real-time NOAA GOES solar context
   - Only keep items that pass governance (PASS + confidence >= 0.75)

5. **Synthesize Daily Briefing**
   - Include actual tweet text and direct links
   - Tag every post with Repertoire Category

6. **Quality Controls**
   - Always disclose search parameters and Dynamo results

## Repertoire Categories (Current)

- Agent Infra & Tooling
- Memory & Post-RAG Systems
- Local Inference & Models
- Local AI OS & Sovereignty Stacks
- Governance & Security
- Polymarket / Execution & Real-Money Agents
- Hybrid Architecture
- Meta-Curation / Ecosystem Directories
- Creative Sovereignty / Content Automation

## Next Priorities

- Expand full 230-item Master Repertoire table
- Add real X tool integration (x_search + xmcp)
- Automate daily cron runs
- Improve signal filtering and curation engine
