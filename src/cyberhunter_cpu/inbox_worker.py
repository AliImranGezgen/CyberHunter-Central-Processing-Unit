#!/usr/bin/env python3
"""Consume one CyberHunter bridge inbox event and deliver it through ESP32."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

BRIDGE_ROOT = Path("/var/lib/cyberhunter/bridge")
INBOX = BRIDGE_ROOT / "inbox"
PROCESSING = BRIDGE_ROOT / "processing"
ARCHIVE = BRIDGE_ROOT / "archive"
REJECTED = BRIDGE_ROOT / "rejected"
STATE = BRIDGE_ROOT / "state"

ACK_CLIENT_DIR = Path("/opt/cyberhunter/apps/bridge/esp32_tests")
ACK_CLIENT_FILE = ACK_CLIENT_DIR / "esp32_client.py"

MAX_ATTEMPTS = 3
RESPONSE_TIMEOUT_SECONDS = 45.0

REQUIRED_FIELDS = {
    "event_id",
    "timestamp",
    "source_ip",
    "destination_port",
    "protocol",
    "event_type",
    "command",
    "tactic",
    "risk_score",
}


def emit(status: str, **fields: Any) -> None:
    record = {
        "status": status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **fields,
    }
    print(json.dumps(record, ensure_ascii=False, separators=(",", ":")), flush=True)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temporary, 0o640)
    os.replace(temporary, path)


def unique_destination(directory: Path, source: Path) -> Path:
    destination = directory / source.name
    if not destination.exists():
        return destination

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    candidate = directory / f"{source.stem}.{stamp}{source.suffix}"
    counter = 1
    while candidate.exists():
        candidate = directory / f"{source.stem}.{stamp}.{counter}{source.suffix}"
        counter += 1
    return candidate


def select_and_claim() -> Path | None:
    processing_files = sorted(
        PROCESSING.glob("*.json"), key=lambda path: path.stat().st_mtime
    )
    if processing_files:
        claimed = processing_files[0]
        emit("resume", file=claimed.name)
        return claimed

    inbox_files = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    if not inbox_files:
        return None

    source = inbox_files[0]
    claimed = PROCESSING / source.name
    os.replace(source, claimed)
    emit("claimed", file=claimed.name)
    return claimed


def validate_event(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("event must be a JSON object")
    if set(event) != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - set(event))
        extra = sorted(set(event) - REQUIRED_FIELDS)
        raise ValueError(f"schema mismatch missing={missing} extra={extra}")

    for key in ("event_id", "timestamp", "source_ip", "protocol", "event_type", "command", "tactic"):
        if not isinstance(event[key], str) or not event[key]:
            raise ValueError(f"invalid string field: {key}")

    for key, minimum, maximum in (
        ("destination_port", 1, 65535),
        ("risk_score", 0, 100),
    ):
        value = event[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"invalid integer field: {key}")
        if value < minimum or value > maximum:
            raise ValueError(f"out-of-range field: {key}")

    if len(event["event_id"]) > 40:
        raise ValueError("event_id is longer than 40 characters")
    if len(event["command"]) > 256:
        raise ValueError("command is longer than 256 characters")
    return event


def state_path_for(file_path: Path) -> Path:
    digest = hashlib.sha256(file_path.name.encode("utf-8")).hexdigest()
    return STATE / f"inbox-worker-{digest}.json"


def read_previous_attempts(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle).get("attempts", 0)
        return value if isinstance(value, int) and value >= 0 else 0
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return 0


def move_after_failure(claimed: Path, attempts: int) -> tuple[str, Path]:
    if attempts >= MAX_ATTEMPTS:
        target = unique_destination(REJECTED, claimed)
        os.replace(claimed, target)
        return "rejected", target

    target = INBOX / claimed.name
    os.replace(claimed, target)
    return "retry_scheduled", target


def load_ack_client():
    sys.path.insert(0, str(ACK_CLIENT_DIR))
    import esp32_client  # type: ignore

    loaded = Path(esp32_client.__file__).resolve()
    if loaded != ACK_CLIENT_FILE.resolve():
        raise RuntimeError(f"wrong ESP32 client loaded: {loaded}")
    return esp32_client


def process_one() -> int:
    for directory in (INBOX, PROCESSING, ARCHIVE, REJECTED, STATE):
        if not directory.is_dir():
            raise RuntimeError(f"required directory is missing: {directory}")

    lock_path = STATE / "inbox-worker.lock"
    with lock_path.open("a+", encoding="utf-8") as lock_handle:
        try:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            emit("already_running")
            return 0

        claimed = select_and_claim()
        if claimed is None:
            emit("empty")
            return 0

        state_path = state_path_for(claimed)
        attempts = read_previous_attempts(state_path) + 1
        event_id = "unknown"

        try:
            with claimed.open("r", encoding="utf-8") as handle:
                event = validate_event(json.load(handle))
            event_id = event["event_id"]

            atomic_write_json(
                state_path,
                {
                    "status": "sending",
                    "attempts": attempts,
                    "event_id": event_id,
                    "file": claimed.name,
                },
            )

            client = load_ack_client()
            client.send_event_to_esp32(event)
            response = client.read_esp32_response(
                event_id,
                timeout=RESPONSE_TIMEOUT_SECONDS,
            )

            if response.get("event_id") != event_id:
                raise RuntimeError("ESP32 response event_id mismatch")
            if response.get("processed") is not True:
                raise RuntimeError(f"ESP32 processed is not true: {response}")

            target = unique_destination(ARCHIVE, claimed)
            os.replace(claimed, target)
            atomic_write_json(
                state_path,
                {
                    "status": "success",
                    "attempts": attempts,
                    "event_id": event_id,
                    "file": target.name,
                    "response": response,
                },
            )
            emit(
                "success",
                event_id=event_id,
                attempts=attempts,
                archive=str(target),
            )
            return 0

        except (json.JSONDecodeError, ValueError) as exc:
            target = unique_destination(REJECTED, claimed)
            os.replace(claimed, target)
            atomic_write_json(
                state_path,
                {
                    "status": "rejected",
                    "attempts": attempts,
                    "event_id": event_id,
                    "file": target.name,
                    "error": f"{type(exc).__name__}: {exc}",
                },
            )
            emit("rejected", event_id=event_id, error=str(exc), file=target.name)
            return 0

        except Exception as exc:
            status, target = move_after_failure(claimed, attempts)
            atomic_write_json(
                state_path,
                {
                    "status": status,
                    "attempts": attempts,
                    "event_id": event_id,
                    "file": target.name,
                    "error": f"{type(exc).__name__}: {exc}",
                },
            )
            emit(
                status,
                event_id=event_id,
                attempts=attempts,
                error=f"{type(exc).__name__}: {exc}",
                file=target.name,
            )
            return 0


if __name__ == "__main__":
    try:
        raise SystemExit(process_one())
    except Exception as exc:
        emit("fatal", error=f"{type(exc).__name__}: {exc}")
        raise
