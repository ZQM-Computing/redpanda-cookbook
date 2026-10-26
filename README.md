# Redpanda Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A **Redpanda cookbook** — Kafka-compatible streaming for geospatial events. Redpanda is running on Node-1 and Node-3 from the Docker sets (broker :19092/:19644/:18081, console :18080). Patterns are drawn from those deployments. It is intended for Engineers who stream geospatial events between services. Validate each pattern against your own data, software versions, and operating environment before adopting it.

## Repository role and status

**Status:** Active, public — first pattern pass written (design-only, gate 1 target; runtime validation pending).

**What this repository is:** Redpanda patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Engineers who stream geospatial events between services.

## Prerequisites

- Redpanda via Docker
- A Kafka-compatible client (rpk ships with Redpanda)
- Bash or PowerShell

## Patterns

| # | Example | Status | What it demonstrates |
|---|---------|--------|----------------------|
| 01 | [01-topic-setup](examples/01-topic-setup/README.md) | Written | Topics, partitions, and retention for event streams |
| 02 | [02-produce-consume](examples/02-produce-consume/README.md) | Written | Producing and consuming geo events |
| 03 | [03-schema-notes](examples/03-schema-notes/README.md) | Written | Schema handling for evolving event shapes |
| 04 | [04-pipeline-pairing](examples/04-pipeline-pairing/README.md) | Written | Pairing streams with NiFi or Prefect consumers |

## Repository layout

```text
redpanda-cookbook/
├── examples/01-topic-setup/
├── examples/02-produce-consume/
├── examples/03-schema-notes/
├── examples/04-pipeline-pairing/
├── README.md
└── LICENSE
```

## Roadmap

- First pattern pass: the first two table rows
- Second pass: the remaining rows, from fleet-verified setups

## Contributing

A contributing guide lands with the first pattern pass. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [airflow-cookbook](https://github.com/ZQM-Computing/airflow-cookbook) — DAGs, schedules, and geospatial pipelines
- [nifi-cookbook](https://github.com/ZQM-Computing/nifi-cookbook) — Visual dataflow, ingestion, and feed-to-PostGIS pipelines
- [mosquitto-cookbook](https://github.com/ZQM-Computing/mosquitto-cookbook) — MQTT broker setup, listeners, and pub/sub patterns

