from kano_ring.config import KanoRingConfig


def test_default_config_matches_kano_ring() -> None:
    cfg = KanoRingConfig()
    assert cfg.led_count == 10
    assert cfg.led_pin == 18
    assert cfg.led_dma == 10
    assert cfg.led_freq_hz == 800_000
