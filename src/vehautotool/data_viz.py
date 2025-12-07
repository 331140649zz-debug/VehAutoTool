"""Lightweight plotting helpers for CAN data."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional

try:
    import matplotlib.pyplot as plt
except Exception as exc:  # pragma: no cover - matplotlib is optional
    plt = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

from .can_parser import CANFrame


def _require_matplotlib() -> None:
    if plt is None:
        raise RuntimeError(
            "matplotlib is required for plotting. Install it with 'pip install matplotlib'."
        ) from _IMPORT_ERROR


def plot_byte_series(
    frames: Iterable[CANFrame],
    byte_index: int,
    *,
    output: Optional[Path] = None,
    title: Optional[str] = None,
) -> Path:
    """Plot the value of a specific byte across a set of frames.

    Args:
        frames: CAN frames to plot.
        byte_index: Which byte (0-based) to visualize.
        output: File path to save the plot. Defaults to ``can_byte_series.png``.
        title: Optional plot title.

    Returns:
        Path to the saved image file.
    """

    _require_matplotlib()
    frames_list: List[CANFrame] = list(frames)
    if not frames_list:
        raise ValueError("No frames to plot.")

    y_values: List[int] = []
    x_values: List[int] = list(range(len(frames_list)))

    for frame in frames_list:
        if byte_index >= frame.dlc:
            y_values.append(0)
        else:
            y_values.append(frame.data[byte_index])

    plt.figure(figsize=(8, 4))
    plt.plot(x_values, y_values, marker="o")
    plt.xlabel("Frame Index")
    plt.ylabel(f"Byte[{byte_index}] Value")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.title(title or f"CAN Byte {byte_index} Trend")

    output_path = output or Path("can_byte_series.png")
    plt.tight_layout()
    plt.savefig(output_path)
    return output_path


__all__ = ["plot_byte_series"]
