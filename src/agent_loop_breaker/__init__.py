"""agent_loop_breaker -- detect repeated agent steps and stop runaway loops.

Public API:
    detect_loop(events, *, window=4, repeat_threshold=3) -> LoopDetection
    should_stop(events, *, window=4, repeat_threshold=3) -> bool
"""

from dataclasses import dataclass
from typing import Any, Iterable, Optional


@dataclass(frozen=True)
class LoopDetection:
    looping: bool
    pattern: Optional[str] = None
    count: int = 0


def _signature(event: Any) -> str:
    """Pick the most descriptive identifier for an event.

    Mirrors the JS heuristic: `event.tool ?? event.name ?? event.type`.
    """
    if isinstance(event, dict):
        for key in ("tool", "name", "type"):
            if event.get(key) is not None:
                return str(event[key])
        return "<unknown>"
    return str(event)


def detect_loop(
    events: Iterable[Any],
    *,
    window: int = 4,
    repeat_threshold: int = 3,
) -> LoopDetection:
    """Scan events for a repeating window of length `window`.

    Returns the first detection (a window seen `repeat_threshold` or more times).
    The pattern is the joined signature with ``>`` between steps.
    """
    sigs = [_signature(e) for e in events]
    if window <= 0 or repeat_threshold <= 1 or len(sigs) < window:
        return LoopDetection(looping=False)

    counts: dict[str, int] = {}
    for i in range(0, len(sigs) - window + 1):
        key = ">".join(sigs[i : i + window])
        counts[key] = counts.get(key, 0) + 1
        if counts[key] >= repeat_threshold:
            return LoopDetection(looping=True, pattern=key, count=counts[key])
    return LoopDetection(looping=False)


def should_stop(
    events: Iterable[Any],
    *,
    window: int = 4,
    repeat_threshold: int = 3,
) -> bool:
    """Convenience: ``True`` when ``detect_loop`` reports a loop."""
    return detect_loop(events, window=window, repeat_threshold=repeat_threshold).looping


__version__ = "0.1.0"
__all__ = ["detect_loop", "should_stop", "LoopDetection"]
