import numpy as np
import src.configs.config as cfg
import src.spectrum as spectrum
from src.functions import (
    calculate_energy,
    spectrum.calculate_f_rms,
    spectrum.calculate_fft,
    get_impulse_signal,
    get_sin_signal,
    spectrum.filering_signal,
    spectrum.calculate_99,
)
import src.configs.comon as comon


def test_lorenth_freq_rms():
    """Сравнение численной среднеквадратической частоты импульса Лоренца
    с аналитическим значением для бесконечного интервала времени.
    """

    config_params = cfg.init_rng()
    config_params["duration_pulse"] = 0.01
    lorentz_pulse = get_impulse_signal(config_params)
    freq_lorentz_pulse = spectrum.calculate_fft(lorentz_pulse)
    freq_rms = spectrum.calculate_f_rms(freq_lorentz_pulse, config_params)

    analytical_rms = 1 / (2 * np.sqrt(2) * np.pi * config_params["duration_pulse"])
    assert np.abs(freq_rms - analytical_rms) < 1e-1


def test_sinus_freq_high_rms():
    """Сравнение среднеквадратической и центральной частот синусоиды."""

    config_params1 = cfg.init_rng()
    config_params1["f0"] = 1000
    sin_signal = get_sin_signal(config_params1)
    freq_sin_pulse = spectrum.calculate_fft(sin_signal)
    freq_rms = spectrum.calculate_f_rms(freq_sin_pulse, config_params1)
    target = config_params1["f0"] / freq_rms

    assert 0.99 < target and target < 1.01


def test_f99_for_gauss():
    sigma = 0.01
    t0 = comon.DURATION_ALL / 2
    gauss_pulse = np.exp(-(((cfg.TIME_VECTOR - t0) / sigma) ** 2))
    spectrum = spectrum.calculate_fft(gauss_pulse)
    E_gaus = calculate_energy(gauss_pulse, cfg.TIME_VECTOR)
    filt_rect = spectrum.filering_signal(gauss_pulse, 100, comon.FS)
    f99 = spectrum.calculate_99(cfg.FREQ_VECTOR, spectrum)

    filt_rect = spectrum.filering_signal(gauss_pulse, 2 * f99, comon.FS)

    E_rect_filt = calculate_energy(filt_rect, cfg.TIME_VECTOR)

    assert (E_rect_filt / E_gaus) * 100 >= 99
