from kano_ring.config import KanoRingConfig


def test_default_config_matches_working_half_of_ring() -> None:
    cfg = KanoRingConfig()
    assert cfg.led_count == 5
    assert cfg.led_pin == 18
    assert cfg.led_dma == 10
    assert cfg.led_freq_hz == 800_000
    assert cfg.led_brightness == 150


def test_from_env_overrides_count_pin_and_brightness(monkeypatch) -> None:
    monkeypatch.setenv("KANO_RING_COUNT", "10")
    monkeypatch.setenv("KANO_RING_PIN", "21")
    monkeypatch.setenv("KANO_RING_BRIGHTNESS", "40")
    monkeypatch.setenv("KANO_RING_STRIP_TYPE", "rgb")
    cfg = KanoRingConfig.from_env()
    assert cfg.led_count == 10
    assert cfg.led_pin == 21
    assert cfg.led_brightness == 40
    assert cfg.strip_type == "rgb"
    assert cfg.led_dma == 10
