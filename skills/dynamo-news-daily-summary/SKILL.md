---
name: dynamo-news-daily-summary
description: "Generates daily AI × Web3 / Sovereign AI briefings using real X data and the Dynamo Governance Layer."
---

# Dynamo News Daily Summary Skill

**Purpose:** Produce high-signal daily briefings by searching X, applying Dynamo governance, and synthesizing the best posts.

## How to Run

When this skill is triggered, it executes:

```bash
python dynamo_news/skill_runner.py
```

This runner:
1. Uses the native `x_search` tool available inside the Hermes agent
2. Fetches recent high-signal posts
3. Runs every post through the full Dynamo Governance Layer (evaluate_governance + PHI/TAU matrix)
4. Ranks results and generates the standard report
5. Saves the report to `artifacts/`
6. Prints the report to screen

## Governance Rules

- Posts are evaluated using resonance + isotopic ratio
- Only strong signals (PASS or high-confidence NEEDS_REVISION) are prioritized
- Reports include governance scores for transparency

## Schedule

Recommended cron triggers:
- 04:00 CST
- 13:00 CST

## Output Format

The skill produces the standard Dynamo News report format with:
- Author + engagement stats
- Post summary
- Governance result + confidence
- Direct X link

## Version

v3.0 — Fully integrated skill with native x_search support
