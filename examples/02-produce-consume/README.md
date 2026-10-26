# 02 — Producing and consuming geo events

> **Design-only, gate 1 target** — drafted from fleet evidence, not runtime-validated. Run it against your own Redpanda before adopting it.

Produce three synthetic geo events to `geo-events`, then consume exactly three back. The round trip proves the topic, the broker address, and the event shape in one pass.

## Files

- `events.jsonl` — 3 synthetic geo events (NDJSON, one object per line; no real place, no real data).
- `produce.sh` — pipes the file into `rpk topic produce`.
- `consume.sh` — consumes exactly 3 records.

## Run

```bash
REDPANDA_BROKER=localhost:19092 bash produce.sh
REDPANDA_BROKER=localhost:19092 bash consume.sh
```

## Expected output (stated, not yet run against the fleet)

- Produce exits 0 with no error output.
- Consume prints exactly the 3 events from `events.jsonl`, in offset order, then exits (the `--num 3` cap prevents a hanging consumer).
- Each event carries `event_id`, `lon`, `lat`, `ts`, and `kind` fields.

## Versions note

- Fleet evidence: Redpanda broker :19092 (Kafka API assumption, see 01) with console :18080; `rpk topic create/list/delete` verified on Node-1.
- `rpk topic produce` reads records from stdin; `rpk topic consume --num N` caps the read — both spellings flagged to confirm on the fleet's rpk version.

## Failure behavior

- Consume without `--num` hangs waiting for more records — always cap demo consumes.
- Producing to a nonexistent topic fails fast; create the topic first (see 01-topic-setup).
- A malformed JSON line in the input file fails that record's produce; the file's NDJSON shape (not a JSON array) is deliberate — one object per line.

## To confirm at validation

- Exact `rpk topic produce` / `consume` flag spellings on the fleet's rpk version.
- Whether the fleet's broker requires TLS/SASL (the scripts assume a plaintext local listener, as in the fleet's Docker setup).
- Consumer-group behavior for repeated consumes (the demo uses a fresh implicit group each run; offset commits are a validation item).
