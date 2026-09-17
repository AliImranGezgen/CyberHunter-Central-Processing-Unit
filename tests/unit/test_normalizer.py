from cyberhunter_cpu.normalizer import normalize_cowrie, normalize_event, normalize_smtp


def test_cowrie_command_is_mapped_and_preserved() -> None:
    event = {
        "eventid": "cowrie.command.input",
        "timestamp": "2026-01-01T00:00:00Z",
        "session": "session-1",
        "src_ip": "192.0.2.10",
        "input": "whoami",
    }

    result = normalize_cowrie(event)

    assert result["event_type"] == "command.executed"
    assert result["details"]["command"] == "whoami"
    assert result["network"]["destination_port"] == 22


def test_event_id_is_deterministic() -> None:
    event = {
        "eventid": "cowrie.session.connect",
        "timestamp": "2026-01-01T00:00:00Z",
        "session": "same-session",
    }

    assert normalize_cowrie(event)["event_id"] == normalize_cowrie(event)["event_id"]


def test_smtp_event_is_normalized() -> None:
    result = normalize_smtp(
        {
            "event_type": "mail_from",
            "timestamp": "2026-01-01T00:00:00Z",
            "source_ip": "192.0.2.20",
            "source_port": 40123,
            "mail_from": "sender@example.invalid",
        }
    )

    assert result["event_type"] == "smtp.sender.declared"
    assert result["network"]["destination_port"] == 2525


def test_unknown_source_is_rejected() -> None:
    try:
        normalize_event("unknown-source", {})
    except ValueError as exc:
        assert "Desteklenmeyen kaynak" in str(exc)
    else:
        raise AssertionError("ValueError bekleniyordu")

