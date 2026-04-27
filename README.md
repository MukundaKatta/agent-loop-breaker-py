# agent-loop-breaker-py

Detect repeated agent steps and stop runaway loops. Pure Python, zero deps. Python port of [`@mukundakatta/agent-loop-breaker`](https://www.npmjs.com/package/@mukundakatta/agent-loop-breaker).

```bash
pip install agent-loop-breaker-py
```

```python
from agent_loop_breaker import detect_loop, should_stop

events = [{"tool": "search"}, {"tool": "fetch"}] * 4
res = detect_loop(events, window=2, repeat_threshold=3)
# LoopDetection(looping=True, pattern="search>fetch", count=4)

if should_stop(events):
    raise RuntimeError("agent stuck in a loop")
```

## API

### `detect_loop(events, *, window=4, repeat_threshold=3) -> LoopDetection`

Scans `events` for a repeating window of length `window`. Returns the first window seen `repeat_threshold` times or more.

Each event is reduced to a signature via `event.get("tool") or event.get("name") or event.get("type")` (or `str(event)` for non-dicts).

### `should_stop(events, *, window=4, repeat_threshold=3) -> bool`

Convenience wrapper returning the `looping` flag.

## License

MIT
