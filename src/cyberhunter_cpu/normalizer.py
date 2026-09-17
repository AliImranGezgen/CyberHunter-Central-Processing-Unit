"""Cowrie ve SMTP olaylarını CyberHunter ortak şemasına dönüştürür."""

from __future__ import annotations

import hashlib
import uuid
from typing import Any

COWRIE_EVENT_MAP = {
    "cowrie.session.connect": "connection.opened",
    "cowrie.session.closed": "connection.closed",
    "cowrie.client.version": "client.version.detected",
    "cowrie.client.kex": "ssh.key_exchange",
    "cowrie.client.fingerprint": "ssh.key.detected",
    "cowrie.client.size": "terminal.size.detected",
    "cowrie.session.params": "session.parameters.detected",
    "cowrie.login.failed": "authentication.failed",
    "cowrie.login.success": "authentication.success",
    "cowrie.command.input": "command.executed",
    "cowrie.log.closed": "session.recording.closed",
}

SMTP_EVENT_MAP = {
    "ehlo": "smtp.greeting",
    "helo": "smtp.greeting",
    "mail_from": "smtp.sender.declared",
    "rcpt_to": "smtp.recipient.declared",
    "message_received": "smtp.message.received",
}


def _event_id(
    source: str,
    raw_event_type: str,
    timestamp: str,
    session_id: str,
) -> str:
    """Aynı olay için tekrar üretilebilir benzersiz kimlik oluşturur."""

    seed = "|".join((source, raw_event_type, timestamp, session_id))
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def _smtp_session_id(event: dict[str, Any]) -> str:
    """SMTP bağlantısını IP ve geçici kaynak portundan ilişkilendirir."""

    value = f"{event.get('source_ip', 'unknown')}:{event.get('source_port', 'unknown')}"
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"smtp-{digest}"


def normalize_cowrie(event: dict[str, Any]) -> dict[str, Any]:
    """Tek bir Cowrie olayını ortak şemaya dönüştürür."""

    raw_event_type = str(event.get("eventid", "unknown"))
    timestamp = str(event.get("timestamp", "unknown"))
    session_id = str(event.get("session", "unknown"))

    credential_present = (
        event.get("password") is not None
        or event.get("key") is not None
        or event.get("fingerprint") is not None
    )

    if event.get("password") is not None:
        credential_type = "password"
    elif event.get("key") is not None:
        credential_type = str(event.get("type", "public_key"))
    else:
        credential_type = "unknown"

    details: dict[str, Any] = {}
    for field in (
        "duration",
        "version",
        "arch",
        "width",
        "height",
        "hassh",
        "size",
        "shasum",
    ):
        if field in event:
            details[field] = event[field]

    if raw_event_type == "cowrie.command.input" and "input" in event:
        details["command"] = str(event["input"])

    return {
        "schema_version": "1.0",
        "event_id": _event_id("cowrie", raw_event_type, timestamp, session_id),
        "timestamp": timestamp,
        "sensor": str(event.get("sensor", "cyberhunter-pi")),
        "source": "cowrie",
        "raw_event_type": raw_event_type,
        "event_type": COWRIE_EVENT_MAP.get(raw_event_type, "unknown"),
        "session_id": session_id,
        "network": {
            "source_ip": event.get("src_ip", "unknown"),
            "source_port": event.get("src_port", "unknown"),
            "destination_ip": event.get("dst_ip", "unknown"),
            "destination_port": event.get("dst_port", 22),
            "protocol": event.get("protocol", "ssh"),
        },
        "identity": {
            "username": event.get("username", "unknown"),
            "credential_type": credential_type,
            "credential_present": credential_present,
        },
        "details": details,
    }


def normalize_smtp(event: dict[str, Any]) -> dict[str, Any]:
    """Tek bir SMTP honeypot olayını ortak şemaya dönüştürür."""

    raw_event_type = str(event.get("event_type", "unknown"))
    timestamp = str(event.get("timestamp", "unknown"))
    session_id = _smtp_session_id(event)

    details: dict[str, Any] = {}
    for field in (
        "hostname",
        "mail_from",
        "rcpt_to",
        "recipients",
        "message_size",
        "sha256",
        "options",
    ):
        if field in event:
            details[field] = event[field]

    return {
        "schema_version": "1.0",
        "event_id": _event_id("smtp", raw_event_type, timestamp, session_id),
        "timestamp": timestamp,
        "sensor": "cyberhunter-pi",
        "source": "smtp",
        "raw_event_type": raw_event_type,
        "event_type": SMTP_EVENT_MAP.get(raw_event_type, "unknown"),
        "session_id": session_id,
        "network": {
            "source_ip": event.get("source_ip", "unknown"),
            "source_port": event.get("source_port", "unknown"),
            "destination_ip": "127.0.0.1",
            "destination_port": 2525,
            "protocol": "smtp",
        },
        "identity": {
            "username": "unknown",
            "credential_type": "none",
            "credential_present": False,
        },
        "details": details,
    }


def normalize_event(source: str, event: dict[str, Any]) -> dict[str, Any]:
    """Kaynak adına göre doğru normalleştiriciyi seçer."""

    if not isinstance(event, dict):
        raise TypeError("Olay bir JSON nesnesi olmalıdır.")
    if source == "cowrie":
        return normalize_cowrie(event)
    if source == "smtp":
        return normalize_smtp(event)
    raise ValueError(f"Desteklenmeyen kaynak: {source}")

