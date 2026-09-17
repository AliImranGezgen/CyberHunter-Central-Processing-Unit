import pytest

from cyberhunter_cpu.inbox_worker import REQUIRED_FIELDS, validate_event


def valid_event() -> dict[str, object]:
    return {
        "event_id": "evt-test-001",
        "timestamp": "2026-01-01T00:00:00Z",
        "source_ip": "192.0.2.10",
        "destination_port": 22,
        "protocol": "ssh",
        "event_type": "command_executed",
        "command": "whoami",
        "tactic": "discovery",
        "risk_score": 40,
    }


def test_valid_event_passes() -> None:
    event = valid_event()
    assert set(event) == REQUIRED_FIELDS
    assert validate_event(event) == event


@pytest.mark.parametrize("risk", [-1, 101])
def test_risk_score_range_is_enforced(risk: int) -> None:
    event = valid_event()
    event["risk_score"] = risk
    with pytest.raises(ValueError, match="out-of-range"):
        validate_event(event)


def test_extra_field_is_rejected() -> None:
    event = valid_event()
    event["unexpected"] = True
    with pytest.raises(ValueError, match="schema mismatch"):
        validate_event(event)

