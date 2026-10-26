#!/bin/bash
# Create and configure the geo-events topic.
# Broker: ${REDPANDA_BROKER:-localhost:19092} (Kafka API listener; see README
# for the port-mapping assumption, flagged to confirm at validation).
# Retention flag spelling is flagged to confirm on the fleet's rpk version.
set -euo pipefail
BROKER="${REDPANDA_BROKER:-localhost:19092}"
TOPIC="geo-events"

rpk --brokers "$BROKER" topic create "$TOPIC" --partitions 3
# 7-day retention in milliseconds (example choice, not fleet policy).
rpk --brokers "$BROKER" topic alter-config "$TOPIC" --set retention.ms=604800000
rpk --brokers "$BROKER" topic list
rpk --brokers "$BROKER" topic describe "$TOPIC"
