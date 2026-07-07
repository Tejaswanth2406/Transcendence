"""
Persistence — save and restore Transcendence state to/from JSON.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .exceptions import DeserializeError, SerializeError

_SCHEMA_VERSION = "2.0.0"


def _checksum(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def save(intelligence: Any, path: Union[str, Path], *, pretty: bool = True, include_checksum: bool = True) -> Path:
    path = Path(path)

    try:
        payload = _serialize_intelligence(intelligence)
    except Exception as exc:
        raise SerializeError(f"Failed to serialize: {exc}") from exc

    envelope: Dict[str, Any] = {
        "schema_version": _SCHEMA_VERSION,
        "created_at": time.time(),
        "payload": payload,
    }

    raw = json.dumps(envelope, indent=2 if pretty else None, ensure_ascii=False)

    if include_checksum:
        envelope["checksum"] = _checksum(raw)
        raw = json.dumps(envelope, indent=2 if pretty else None, ensure_ascii=False)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(raw, encoding="utf-8")
    return path.resolve()


def load(path: Union[str, Path], *, verify_checksum: bool = True) -> Any:
    path = Path(path)
    if not path.exists():
        raise DeserializeError(f"File not found: {path}")

    try:
        raw = path.read_text(encoding="utf-8")
        envelope = json.loads(raw)
    except Exception as exc:
        raise DeserializeError(f"Cannot read file: {exc}") from exc

    if verify_checksum and "checksum" in envelope:
        stored_checksum = envelope.pop("checksum")
        verification_raw = json.dumps(envelope, indent=2, ensure_ascii=False)
        if _checksum(verification_raw) != stored_checksum:
            raise DeserializeError("Checksum verification failed.")

    return _deserialize_intelligence(envelope.get("payload", {}))


def _serialize_intelligence(ti: Any) -> Dict[str, Any]:
    return {"name": ti.name, "created_at": ti.created_at, "log": list(ti._log)}


def _deserialize_intelligence(data: Dict[str, Any]) -> Any:
    from .intelligence import TranscendentIntelligence
    ti = TranscendentIntelligence(data.get("name", "TIA-Loaded"))
    ti.created_at = data.get("created_at", time.time())
    ti._log = data.get("log", [])
    return ti
