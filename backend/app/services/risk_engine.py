from app.schemas.security_event import SecurityEvent


def calculate_risk(event: SecurityEvent) -> dict:
    score = 0
    reasons = []

    # High-risk destination ports
    high_risk_ports = {
        21: "FTP",
        23: "Telnet",
        3389: "RDP",
        445: "SMB"
    }

    if event.destination_port in high_risk_ports:
        score += 30
        reasons.append(
            f"Connection targets {high_risk_ports[event.destination_port]} "
            f"port {event.destination_port}"
        )

    # Unusually large transfer
    if event.bytes_sent > 1_000_000:
        score += 25
        reasons.append("Large amount of data transferred")

    # Suspiciously low destination port
    if event.destination_port < 1024:
        score += 10
        reasons.append("Connection targets a privileged port")

    # Cap score at 100
    score = min(score, 100)

    if score >= 70:
        severity = "CRITICAL"
    elif score >= 40:
        severity = "HIGH"
    elif score >= 20:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "risk_score": score,
        "severity": severity,
        "reasons": reasons
    }