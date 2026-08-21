from app.schemas.security_event import SecurityEvent
from app.services.risk_engine import calculate_risk


def test_normal_https_event_is_low_risk():
    event = SecurityEvent(
        source_ip="192.168.1.10",
        destination_ip="10.0.0.5",
        source_port=49152,
        destination_port=443,
        protocol="TCP",
        bytes_sent=5240
    )

    result = calculate_risk(event)

    assert result["risk_score"] == 10
    assert result["severity"] == "LOW"


def test_rdp_large_transfer_is_high_risk():
    event = SecurityEvent(
        source_ip="192.168.1.10",
        destination_ip="10.0.0.5",
        source_port=49152,
        destination_port=3389,
        protocol="TCP",
        bytes_sent=2500000
    )

    result = calculate_risk(event)

    assert result["risk_score"] == 55
    assert result["severity"] == "HIGH"