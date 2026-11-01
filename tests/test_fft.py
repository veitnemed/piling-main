import numpy as np
import py_files.configs.config as cfg
from py_files.functions import (calculate_energy, 
                                calculate_f_rms, 
                                calculate_fft, 
                                get_impulse_signal,
                                get_sin_signal)
import py_files.configs.comon as comon

def test_lorenth_freq_rms():
    """Тест сранивает численное вычисление f rms для испульса Лоренца от O до T 
    и аналтическую формула на бесконечном интревале времени """

    config_params = cfg.init_rng()
    lorentz_pulse = get_impulse_signal(config_params)
    freq_lorentz_pulse = calculate_fft(lorentz_pulse, config_params["fs"])
    freq_rms = calculate_f_rms(freq_lorentz_pulse, config_params)

    analytical_rms = 1 / (2*np.sqrt(2)*np.pi*config_params["duration_pulse"])
    assert np.abs(freq_rms - analytical_rms) < 1e-3

def test_sinus_freq_rms():
    """Тест сранивает численное вычисление f rms для синусоиду 
    и центральную частоту """

    
    config_params = cfg.init_rng()
    sin_signal = get_sin_signal(config_params)
    freq_sin_pulse = calculate_fft(sin_signal, config_params["fs"])
    freq_rms = calculate_f_rms(freq_sin_pulse, config_params)


    assert np.abs(freq_rms - config_params["f0"]) < 1e-3
