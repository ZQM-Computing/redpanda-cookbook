# NiFi ConsumeKafka sketch (property names illustrative, not verbatim)

- Processor: ConsumeKafka
- Kafka Brokers: `<BROKER_LIST>` (placeholder; the fleet's Kafka API listener — 19092 assumed, see 01)
- Topic Names: `geo-events`
- Consumer Group ID: `geonode-or-flow-specific-group` (one group per flow — never share a group between flows)
- Auto Offset Reset: `earliest` for first runs needing history, `latest` for live-only tailing
- Security Protocol: PLAINTEXT assumed for the fleet's local Docker listener (to confirm at validation — never assume it for a non-local broker)
- Downstream: RouteOnAttribute on parse success/failure; failures go to a dead-letter relationship, never block the topic
- Validation items: verbatim NiFi 2.12.0 property spellings, the fleet's real broker listener, and whether SASL/TLS is enabled anywhere in the fleet's Redpanda setup
