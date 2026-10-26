#!/bin/bash
# Produce the synthetic events file to geo-events (reads from stdin).
set -euo pipefail
BROKER="${REDPANDA_BROKER:-localhost:19092}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
rpk --brokers "$BROKER" topic produce geo-events < "$SCRIPT_DIR/events.jsonl"
echo "Produced events.jsonl to geo-events"
