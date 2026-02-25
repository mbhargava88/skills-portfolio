from app.domain.interfaces import GrafanaClient
from app.domain.entities import TrafficPattern
import random

class GrafanaClientImpl(GrafanaClient):
    def fetch_traffic(self, service: str, endpoint: str) -> TrafficPattern:
        # Mock implementation as per Agents.md
        return TrafficPattern(
            rps=250.0 + random.uniform(-50, 50),
            avg_latency_ms=120.0,
            p95_latency_ms=200.0,
            payload_size_bytes=2100,
            error_rate=0.02,
            raw_data={"service": service, "endpoint": endpoint, "source": "mock_grafana"}
        )
