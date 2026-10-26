"""Prefect flow sketch: poll geo-events and count by kind.

SKETCH, not a verbatim fleet deployment (see README). Polls with a capped
rpk consume, parses JSON lines, prints per-kind counts. Malformed lines
are counted as skipped, not fatal. No state is persisted by this sketch.
"""
import json
import subprocess

from prefect import flow, task

BROKER = "localhost:19092"  # Placeholder: the fleet's Kafka API listener.
TOPIC = "geo-events"


@task(retries=2)
def poll_events():
    """Consume up to 10 records; return (events, skipped) counts."""
    proc = subprocess.run(
        ["rpk", "--brokers", BROKER, "topic", "consume", TOPIC, "--num", "10"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    events = []
    skipped = 0
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            skipped += 1
    return events, skipped


@task
def summarize(poll_result):
    """Print per-kind counts for the polled events."""
    events, skipped = poll_result
    kinds = {}
    for event in events:
        kinds[event.get("kind", "unknown")] = kinds.get(event.get("kind", "unknown"), 0) + 1
    print(f"Polled {len(events)} events, skipped {skipped} malformed lines")
    print(f"Counts by kind: {kinds}")


@flow(name="redpanda-geo-consumer")
def redpanda_geo_consumer():
    summarize(poll_events())


if __name__ == "__main__":
    redpanda_geo_consumer()
