from agent_loop_breaker import detect_loop, should_stop, LoopDetection


def test_no_loop_for_short_history():
    assert detect_loop([{"tool": "a"}, {"tool": "b"}]).looping is False


def test_no_loop_when_unique_steps():
    events = [{"tool": x} for x in "abcdefgh"]
    assert detect_loop(events, window=2, repeat_threshold=2).looping is False


def test_detects_repeating_window():
    events = (
        [{"tool": "search"}, {"tool": "fetch"}, {"tool": "search"}, {"tool": "fetch"}] * 3
    )
    res = detect_loop(events, window=2, repeat_threshold=3)
    assert res.looping is True
    assert res.pattern == "search>fetch"
    assert res.count >= 3


def test_should_stop_returns_bool():
    looping = [{"tool": "x"}] * 10
    assert should_stop(looping, window=1, repeat_threshold=3) is True
    assert should_stop([{"tool": "a"}, {"tool": "b"}], window=2, repeat_threshold=2) is False


def test_signature_falls_back_to_name_then_type():
    events = [
        {"name": "edit"},
        {"type": "tool_call"},
        {"name": "edit"},
        {"type": "tool_call"},
    ]
    res = detect_loop(events, window=2, repeat_threshold=2)
    assert res.looping is True
    assert "edit>tool_call" == res.pattern


def test_window_larger_than_history_no_match():
    assert detect_loop([{"tool": "a"}], window=4).looping is False


def test_loop_detection_dataclass_fields():
    d = LoopDetection(looping=True, pattern="x>x", count=3)
    assert d.looping is True
    assert d.pattern == "x>x"
    assert d.count == 3
