from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_repository_documentation_and_evidence_integrity() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "scripts/validation/audit_repository.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Stage belgeleri: 19/19" in result.stdout
    assert "Stage 19 için tarihli kanıt dosyası yok" in result.stdout
