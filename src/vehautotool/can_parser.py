"""CAN log parsing utilities supporting multiple formats."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional


@dataclass
class CANFrame:
    """Simple representation of a CAN frame."""

    timestamp: Optional[float]
    can_id: int
    data: bytes

    @property
    def dlc(self) -> int:
        return len(self.data)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "can_id": self.can_id,
            "dlc": self.dlc,
            "data_hex": self.data.hex().upper(),
        }


class CANLogParser:
    """Parser that handles a variety of CAN log formats."""

    def __init__(self) -> None:
        self.parsers: List[Callable[[str], Optional[CANFrame]]] = [
            self._parse_candump,
            self._parse_canutils,
            self._parse_json,
        ]

    def parse_line(self, line: str) -> Optional[CANFrame]:
        normalized = line.strip()
        if not normalized or normalized.startswith("#"):
            return None
        for parser in self.parsers:
            result = parser(normalized)
            if result:
                return result
        return None

    def parse_file(self, path: Path) -> List[CANFrame]:
        frames: List[CANFrame] = []
        for raw_line in path.read_text().splitlines():
            frame = self.parse_line(raw_line)
            if frame:
                frames.append(frame)
        return frames

    @staticmethod
    def _parse_candump(line: str) -> Optional[CANFrame]:
        """Parse lines in the candump style.

        Example: ``(1606406475.123456) can0 123#11223344``
        """

        match = re.match(r"\((?P<ts>\d+\.\d+)\)\s+\w+\s+(?P<id>[0-9A-Fa-f]+)#(?P<data>[0-9A-Fa-f]*)", line)
        if not match:
            return None
        timestamp = float(match.group("ts"))
        can_id = int(match.group("id"), 16)
        data = bytes.fromhex(match.group("data"))
        return CANFrame(timestamp=timestamp, can_id=can_id, data=data)

    @staticmethod
    def _parse_canutils(line: str) -> Optional[CANFrame]:
        """Parse ``candump -L`` style or bare ``CANID#DATA`` frames."""

        match = re.match(r"(?:(?P<ts>\d+\.\d+)\s+)?(?P<id>[0-9A-Fa-f]{1,8})#(?P<data>[0-9A-Fa-f]*)", line)
        if not match:
            return None
        timestamp = float(match.group("ts")) if match.group("ts") else None
        can_id = int(match.group("id"), 16)
        data = bytes.fromhex(match.group("data"))
        return CANFrame(timestamp=timestamp, can_id=can_id, data=data)

    @staticmethod
    def _parse_json(line: str) -> Optional[CANFrame]:
        """Parse JSON objects like {""can_id"": "0x123", ""data"": "11223344"}."""

        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return None

        if not isinstance(payload, dict):
            return None

        if "can_id" not in payload or "data" not in payload:
            return None

        raw_id = payload["can_id"]
        can_id = int(str(raw_id), 0)
        data = bytes.fromhex(str(payload["data"]))
        timestamp = float(payload["timestamp"]) if "timestamp" in payload else None
        return CANFrame(timestamp=timestamp, can_id=can_id, data=data)


__all__ = ["CANFrame", "CANLogParser"]
