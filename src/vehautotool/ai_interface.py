"""AI-facing stubs to enable future intelligent analysis."""
from __future__ import annotations

from typing import Iterable, List

from .can_parser import CANFrame


class AIInsights:
    """Placeholder for future AI-enhanced diagnostics."""

    def summarize(self, frames: Iterable[CANFrame]) -> str:
        frame_list: List[CANFrame] = list(frames)
        if not frame_list:
            return "未检测到可用的CAN帧。"

        ids = {frame.can_id for frame in frame_list}
        timestamps = [f.timestamp for f in frame_list if f.timestamp is not None]
        summary_parts = [
            f"采集帧数: {len(frame_list)}",
            f"涉及ID数量: {len(ids)}",
        ]
        if timestamps:
            summary_parts.append(
                f"时间范围: {min(timestamps):.6f}s -> {max(timestamps):.6f}s"
            )
        else:
            summary_parts.append("未提供时间戳")

        summary_parts.append(
            "AI接口预留：可接入大模型完成故障诊断、模式发现等高级分析。"
        )
        return " | ".join(summary_parts)


__all__ = ["AIInsights"]
