import numpy as np
from scipy.signal import hilbert
"""Преобразование гильберта возращает уже весь аналитический сигнал (real + imag)
hilbert(s(t)) = s(t) + h(s(t)) """
from src.functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_sin_signal, 
                       calculate_complex_stiring_matrix,
                       calculate_complex_stiring_vector,
                       calculate_full_bartlett_values, 
                       calculate_full_capon_values, 
                       get_analytical_sin_signal
                       )
import src.configs as cfg

config_parametrs = cfg.init_rng()
def test_bartlet_and_capon_for_hilbert_signal():

    for pseudospectrum in (calculate_full_bartlett_values, calculate_full_capon_values):
        tau_array = get_tau_array(config_parametrs)
        channel_real_matrix = get_channel_matrix(config_parametrs, tau_array, get_sin_signal)
        channel_complex_matrix = get_channel_matrix(config_parametrs, tau_array)

        w_real = get_covariation_matrix(channel_real_matrix, config_parametrs["N"])
        w_complex = get_covariation_matrix(channel_complex_matrix, config_parametrs["N"])
        dir_complex_matrix = calculate_complex_stiring_matrix(config_parametrs)



        bartlett_real = pseudospectrum(w_real, dir_complex_matrix)
        bartlett_complex = pseudospectrum(w_real, dir_complex_matrix)


        np.array_equal(bartlett_real, bartlett_complex)

