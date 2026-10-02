#!/usr/bin/env python3
"""CyberHunter dokümantasyon ve kanıt bütünlüğünü salt okunur denetler."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

STAGE_COUNT = 19
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REMOTE_PREFIXES = ("http://", "https://", "mailto:", "#")
IMAGE_SIGNATURES = {
    ".jpeg": (b"\xff\xd8\xff",),
    ".jpg": (b"\xff\xd8\xff",),
    ".png": (b"\x89PNG\r\n\x1a\n",),
}


def stage_documents(root: Path) -> dict[int, Path]:
    documents: dict[int, Path] = {}
    for path in (root / "docs" / "stages").glob("[0-9][0-9]-*.md"):
        documents[int(path.name[:2])] = path
    return documents


def evidence_counts(root: Path) -> Counter[int]:
    counts: Counter[int] = Counter()
    pattern = re.compile(r"stage-(\d{2})_")
    for path in (root / "evidence").rglob("*"):
        if not path.is_file():
            continue
        match = pattern.search(path.name)
        if match:
            counts[int(match.group(1))] += 1
    return counts


def audit(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    documents = stage_documents(root)

    missing_stages = sorted(set(range(1, STAGE_COUNT + 1)) - set(documents))
    if missing_stages:
        errors.append(f"Eksik stage belgeleri: {missing_stages}")

    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if text.count("```") % 2:
            errors.append(f"Kapanmamış kod bloğu: {path.relative_to(root)}")

        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(REMOTE_PREFIXES):
                continue
            destination = (path.parent / target).resolve()
            if not destination.exists():
                errors.append(
                    f"Kırık yerel bağlantı: {path.relative_to(root)} -> {raw_target}"
                )

    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Geçersiz JSON: {path.relative_to(root)} ({exc})")

    for extension, signatures in IMAGE_SIGNATURES.items():
        for path in (root / "evidence").rglob(f"*{extension}"):
            header = path.read_bytes()[:8]
            if not any(header.startswith(signature) for signature in signatures):
                errors.append(
                    f"Görsel uzantısı/içeriği uyumsuz: {path.relative_to(root)}"
                )

    counts = evidence_counts(root)
    for stage in range(1, STAGE_COUNT + 1):
        if counts[stage] == 0:
            warnings.append(f"Stage {stage:02d} için tarihli kanıt dosyası yok")

    return errors, warnings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    errors, warnings = audit(root)
    counts = evidence_counts(root)

    print(f"Stage belgeleri: {len(stage_documents(root))}/{STAGE_COUNT}")
    print(f"Tarihli kanıt dosyaları: {sum(counts.values())}")
    print("Stage kanıt dağılımı: " + ", ".join(f"{n:02d}={counts[n]}" for n in range(1, 20)))

    for warning in warnings:
        print(f"UYARI: {warning}")
    for error in errors:
        print(f"HATA: {error}")

    if errors:
        print(f"SONUÇ: başarısız ({len(errors)} hata, {len(warnings)} uyarı)")
        return 1
    print(f"SONUÇ: başarılı ({len(warnings)} uyarı)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
