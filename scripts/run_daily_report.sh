#!/bin/bash
# Dynamo News - Daily Report Runner
# Runs at 4am and 1pm CST

cd /opt/dynamo-news

echo "=== Dynamo News Daily Run: $(date) ===" >> /opt/dynamo-news/logs/daily.log

# Future: Call Python script that uses x_search tool via Hermes
# For now, this is the execution hook

echo "Daily report generation triggered at $(date)" >> /opt/dynamo-news/logs/daily.log
