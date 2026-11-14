import numpy as np
import src.configs.config as config
import src.spectrum as spectrum
import src.signals as signals


def test_lorenth_freq_rms():
    """Сравнение численной среднеквадратической частоты импульса Лоренца
    с аналитическим значением для бесконечного интервала времени.
    """

    config_params = config.init_rng()
    config_params["duration_pulse"] = 0.01
    lorentz_pulse = signals.lorenth(config_params)
    freq_lorentz_pulse = spectrum.fft(lorentz_pulse)
    freq_rms = spectrum.f_rms(freq_lorentz_pulse, config_params)

    analytical_rms = 1 / (2 * np.sqrt(2) * np.pi * config_params["duration_pulse"])
    assert np.abs(freq_rms - analytical_rms) < 1e-1


def test_sinus_freq_high_rms():
    """Сравнение среднеквадратической и центральной частот синусоиды."""

    config_params1 = config.init_rng()
    config_params1["f0"] = 1000
    sin_signal = signals.sinus(config_params1)
    freq_sin_pulse = spectrum.fft(sin_signal)
    freq_rms = spectrum.f_rms(freq_sin_pulse, config_params1)
    target = config_params1["f0"] / freq_rms

    assert 0.99 < target and target < 1.01


def test_f99_for_gauss():
    params = config.create_parameters_config()
    sigma = 0.01
    t0 = params["duration_all"] / 2
    gauss_pulse = np.exp(-(((params["time_vector"] - t0) / sigma) ** 2))
    spectr = spectrum.fft(gauss_pulse)
    E_gaus = signals.calculate_energy(gauss_pulse, params["time_vector"])
    filt_rect = spectrum.cut_spectrum(gauss_pulse, 100, params["fs"])
    f99 = spectrum.f_99(params["freq_vector"], spectr)

    filt_rect = spectrum.cut_signal(gauss_pulse, 2 * f99, params["fs"])

    E_rect_filt = signals.calculate_energy(filt_rect, params["time_vector"])

    assert (E_rect_filt / E_gaus) * 100 >= 99
