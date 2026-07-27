#!/usr/bin/env bash

LOG_FILE="/Users/mac/a1/q1-deploy-monitor/monitor.log"

# Ensure log file exists
mkdir -p "$(dirname "$LOG_FILE")"
: > "$LOG_FILE"

while true; do
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code} %{time_total}" http://localhost:8080/health)
  echo "$TIMESTAMP $RESPONSE" >> "$LOG_FILE"
  sleep 30
done
