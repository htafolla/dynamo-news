# Dynamo News

High-signal daily briefings on AI × Web3, local/sovereign AI, and agentic systems — filtered through the Dynamo Governance Layer.

## Overview

Dynamo News automatically pulls recent X activity, cross-correlates it against a curated Master Index, and runs every post through the **Dynamo Governance Layer** (`evaluate_governance` + `govern_with_solar`) before inclusion.

Only posts that receive a clear **PASS** after governance evaluation are included in the final briefing.

## Features

- Real-time X search with personalized vectors
- Master Index cross-correlation (200+ curated entries)
- Full Dynamo Governance integration (evaluate_governance + solar context)
- Clean, scannable daily briefings
- Scheduled runs at 4am and 1pm CST

## Project Structure

```
dynamo-news/
├── dynamo_news/
│   ├── daily_correlator.py      # Main engine
│   ├── x_search_client.py       # X data ingestion
│   └── dynamo_governance.py     # Dynamo MCP governance calls
├── references/
│   └── master_index.csv         # Curated signal index
├── artifacts/                   # Generated briefings
├── scripts/
├── skills/
│   └── ai-web3-x-daily-summary/ # Hermes skill definition
└── README.md
```

## Quick Start

```bash
cd /opt/dynamo-news
PYTHONPATH=/opt/dynamo-news python dynamo_news/daily_correlator.py
```

## Governance Layer

Every candidate post is evaluated using:

- `evaluate_governance` — technical validation
- `govern_with_solar` — strategic + real-time solar context

Only posts with `recommendation: "PASS"` are surfaced.

## Schedule

The system runs automatically twice daily via cron:
- 04:00 CST
- 13:00 CST

## Version

- Skill: `ai-web3-x-daily-summary` v2.1
- Governance: Dynamo MCP (evaluate_governance + govern_with_solar)
- Date: May 2026

---

*Built with Hermes Agent + Dynamo Governance*