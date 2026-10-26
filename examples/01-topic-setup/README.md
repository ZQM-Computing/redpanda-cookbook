# 01 — Topic setup: partitions and retention

> **Design-only, gate 1 target** — drafted from fleet evidence, not runtime-validated. Run it against your own Redpanda before adopting it.

Create a geo-event topic with an explicit partition count, then set retention and verify with describe. Partition count is a creation-time decision; retention is a config you can change later.

## Files

- `topics.sh` — create, configure, list, describe (broker overridable via `REDPANDA_BROKER`).

## Run

```bash
REDPANDA_BROKER=localhost:19092 bash topics.sh
```

## Expected output (stated, not yet run against the fleet)

- `rpk topic create` reports the `geo-events` topic created with 3 partitions.
- `rpk topic list` shows `geo-events` among the topics.
- `rpk topic describe geo-events` shows 3 partitions and the retention setting applied by the script.

## Versions note

- Fleet evidence: Redpanda broker on :19092/:19644/:18081 with console on :18080 (Node-1 and Node-3); broker flags `--overprovisioned --smp 1 --memory 1G` on Node-1; `rpk topic create/list/delete` verified working on Node-1.
- Port mapping assumption (to confirm at validation): 19092 is the Kafka API listener (standard 9092 offset by 10000); 19644 is the admin API; 18081 is the proxy/schema listener. The scripts default to 19092.
- Redpanda image tag / rpk version: not in the fleet record used here — to confirm at validation, never guessed.

## Failure behavior

- Creating an already-existing topic fails with an already-exists error — the script is not idempotent by design; delete first (`rpk topic delete geo-events`) or pick a new name.
- If `rpk` cannot reach the broker, check the listener port first (see the mapping note above) before suspecting the topic command.

## To confirm at validation

- Exact `rpk topic alter-config --set` spelling on the fleet's rpk version.
- The fleet's real topic-naming, partition-count, and retention conventions (the script's 3 partitions / 7-day retention are example choices, not fleet policy).
- Whether Schema Registry / pandaproxy is enabled on the fleet (the schema pattern assumes no registry; see 03-schema-notes).
