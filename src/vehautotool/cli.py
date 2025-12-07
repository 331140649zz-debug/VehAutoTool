"""Command line interface for VehAutoTool CAN parsing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from .ai_interface import AIInsights
from .can_parser import CANLogParser
from .data_viz import plot_byte_series


def _export_frames(frames: Iterable, output: Path) -> None:
    records = [frame.to_dict() for frame in frames]
    output.write_text(json.dumps(records, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CAN报文解析与可视化工具")
    parser.add_argument("log", type=Path, help="输入的CAN日志文件")
    parser.add_argument("--plot-byte", type=int, help="需要展示的字节索引(0-based)")
    parser.add_argument("--plot-output", type=Path, default=Path("can_byte_series.png"))
    parser.add_argument("--export", type=Path, help="解析结果导出为JSON的路径")
    parser.add_argument("--summary", action="store_true", help="输出AI风格摘要")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    parser = CANLogParser()
    frames = parser.parse_file(args.log)

    if not frames:
        print("未从日志中解析到CAN帧。")
        return 1

    print(f"解析到 {len(frames)} 条CAN帧，涉及 {len({f.can_id for f in frames})} 个ID。")

    if args.export:
        _export_frames(frames, args.export)
        print(f"已导出解析结果到 {args.export}")

    if args.plot_byte is not None:
        output_path = plot_byte_series(frames, args.plot_byte, output=args.plot_output)
        print(f"已输出图像到 {output_path}")

    if args.summary:
        summary = AIInsights().summarize(frames)
        print(summary)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
