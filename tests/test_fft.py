import numpy as np
import py_files.configs.config as cfg
from py_files.functions import (calculate_energy, 
                                calculate_f_rms, 
                                calculate_fft, 
                                get_impulse_signal,
                                get_sin_signal,
                                filering_signal,
                                calculate_99)
import py_files.configs.comon as comon

def test_lorenth_freq_rms():
    """Тест сранивает численное вычисление f rms для испульса Лоренца от O до T 
    и аналтическую формула на бесконечном интревале времени """

    config_params = cfg.init_rng()
    config_params["duration_pulse"] = 0.01
    lorentz_pulse = get_impulse_signal(config_params)
    freq_lorentz_pulse = calculate_fft(lorentz_pulse)
    freq_rms = calculate_f_rms(freq_lorentz_pulse, config_params)

    analytical_rms = 1 / (2*np.sqrt(2)*np.pi*config_params["duration_pulse"])
    assert np.abs(freq_rms - analytical_rms) < 1e-1

def test_sinus_freq_high_rms():
    """Тест сранивает численное вычисление f rms для синусоиду 
    и центральную частоту """


    config_params1 = cfg.init_rng()
    config_params1["f0"] = 1000
    sin_signal = get_sin_signal(config_params1)
    freq_sin_pulse = calculate_fft(sin_signal)
    freq_rms = calculate_f_rms(freq_sin_pulse, config_params1)
    target = config_params1["f0"] / freq_rms

    assert 0.99 < target and target < 1.01

def test_f99_for_gauss():
    sigma = 0.01
    t0 = comon.DURATION_ALL / 2
    gauss_pulse = np.exp(-((cfg.TIME_VECTOR - t0)/ sigma)**2)
    spectrum = calculate_fft(gauss_pulse)
    E_gaus = calculate_energy(gauss_pulse,cfg.TIME_VECTOR)
    filt_rect = filering_signal(gauss_pulse, 100, comon.FS)
    f99 = calculate_99(cfg.FREQ_VECTOR, spectrum)

    filt_rect = filering_signal(gauss_pulse, 2*f99, comon.FS)

    E_rect_filt = calculate_energy(filt_rect,cfg.TIME_VECTOR)



    assert (E_rect_filt/E_gaus)*100 >= 99
