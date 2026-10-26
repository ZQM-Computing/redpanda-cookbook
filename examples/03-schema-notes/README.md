# 03 — Schema handling for evolving event shapes

> **Design-only, gate 1 target** — drafted from fleet evidence, not runtime-validated. Run it against your own Redpanda before adopting it.

Geo events evolve: a new field arrives, an old producer keeps sending the old shape, and consumers must not break. This pattern states the evolution rules and shows a v1 → v2 pair that follows them.

## Files

- `v1_event.json` — the original event shape (5 required fields).
- `v2_event.json` — the evolved shape: same 5 fields, plus 2 optional fields.

## Rules (the whole pattern in five lines)

1. New fields are always OPTIONAL — old producers never break new consumers, and new producers never break old consumers.
2. Never rename a field; never change a field's type. Add a new field instead.
3. Never remove a field; mark it deprecated and stop writing it, then remove it only after every consumer has migrated.
4. Consumers ignore unknown fields — a consumer that fails on an unexpected key will break on every evolution.
5. Carry a `schema_version` only if consumers branch on it; the v2 example does not need one, because the new fields are optional and ignored by old readers.

## Expected output (stated, not yet run against the fleet)

- A v1-only consumer reads `v2_event.json` and uses the 5 original fields, ignoring `accuracy_m` and `source`.
- A v2 consumer reads `v1_event.json` and treats the 2 missing fields as absent (null / default), not as an error.

## Versions note

- Fleet evidence: Redpanda broker :19092 with console :18080 (Node-1 and Node-3); no Schema Registry is mentioned in the fleet record used here.
- This pattern therefore assumes plain JSON events with no registry. Whether a registry (pandaproxy/schema on :18081) is enabled on the fleet is a validation item — do not assume it from the port mapping.

## Failure behavior

- A renamed field silently splits one logical field into two (old readers see nulls, new readers see the new name) — the hardest evolution bug to notice, which is why rule 2 exists.
- A type change (string → number) breaks strict consumers at parse time; treat it as a new field, never an edit.

## To confirm at validation

- Whether the fleet enables a schema registry, and if so which one (Redpanda's built-in vs an external registry).
- The fleet's real event-shape conventions (field names, timestamp format) — the example's names are illustrative, not fleet policy.
- Consumer-group offset behavior when a consumer restarts mid-evolution (see 02-produce-consume).
