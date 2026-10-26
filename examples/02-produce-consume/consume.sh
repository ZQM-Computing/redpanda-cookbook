#!/bin/bash
# Consume exactly 3 records from geo-events, then exit (never hang).
set -euo pipefail
BROKER="${REDPANDA_BROKER:-localhost:19092}"
rpk --brokers "$BROKER" topic consume geo-events --num 3
