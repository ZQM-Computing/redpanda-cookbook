# 04 — Pairing streams with NiFi or Prefect consumers

> **Design-only, gate 1 target** — drafted from fleet evidence, not runtime-validated. Run it against your own stack before adopting it.

Two consumer pairings for a Redpanda topic: a NiFi flow that drains the topic continuously, and a Prefect flow that polls it on a schedule. Both sketches are labeled as sketches — their property spellings are validation items, not asserted fleet facts.

## Files

- `prefect_consumer.py` — Prefect flow sketch: poll `geo-events` via `rpk consume --num 10`, parse JSON lines, print a per-kind count.
- `nifi-notes.md` — NiFi ConsumeKafka sketch: processor settings, offset behavior, and the auth gate.

## NiFi pairing (sketch)

- Processor: ConsumeKafka (Kafka 2.x/3.x consumer API family) pointed at the broker listener (placeholder `localhost:19092`; replace with the fleet's Kafka API listener).
- Topic: `geo-events`; consumer group: a dedicated group per flow (never share a group between two flows — they would split the partitions).
- Offset reset: `earliest` for a first run that must see history, `latest` for live-only tailing. The choice is per-flow, not global.
- Failure behavior: a poison record (unparseable JSON) must route to a dead-letter relationship, never block the topic. NiFi's route-on-attribute pattern from nifi-cookbook 02 applies here.

## Prefect pairing (sketch)

- The flow runs on a schedule (see prefect-cookbook 02), polls with a capped consume (`--num 10`), and exits — it never holds a long-lived consumer open.
- State: the flow prints counts only; persisting offsets or results is a separate decision (a destination table or object, not assumed here).
- Failure behavior: a failed poll (broker unreachable) fails the flow run and retries per the flow's retry policy; a malformed record is counted as skipped, not fatal, and logged.

## Versions note

- Fleet evidence: Redpanda broker :19092 (Kafka API assumption) with console :18080; NiFi 2.12.0 on Node-1 (NSSM direct-JVM route) and Node-4 (installed, localhost-probe rule); Prefect 3.9.0 with the MODULE_PATH-enum deployment rule (see prefect-cookbook 03).
- NiFi processor property names and the Prefect deployment spelling are validation items — the sketches use illustrative names, not verbatim fleet definitions.

## Failure behavior

- Two consumers sharing one group split partitions and each sees only part of the stream — the classic "missing events" bug. One group per consumer flow.
- A consumer that never commits offsets replays the whole topic on restart. Decide the commit strategy before the first production run.

## To confirm at validation

- Verbatim NiFi ConsumeKafka property spellings on NiFi 2.12.0 (bootstrap servers, group id, offset reset, security protocol).
- The fleet's real broker listener for Kafka clients (19092 assumed; 19644/18081 roles flagged in 01).
- Whether the fleet's Prefect server (:4300 Node-1, :4200 Node-3 per the seed note) is the deployment target for the consumer flow, or a standalone run.
