"""Статистика экспериментов"""

import numpy as np
import py_files.config as cfg 
from collections.abc import Callable

from py_files.functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_est_phi,
                       get_direction_matrix)


def single_est(config_params: dict,
               dir_matrix: np.ndarray,
               target_func: Callable,
               signal_func) -> float:
    """Считаем оценку по одной ревлизации шума"""
    
    tau_array = get_tau_array(config_params)
    channel_matrix = get_channel_matrix(config_params = config_params,
                                        tau_array = tau_array,
                                        signal_func = signal_func)
    W = get_covariation_matrix(channel_matrix, config_params["N"])
    Energy_values = target_func(W, dir_matrix)
    est = get_est_phi(config_params["phis"], Energy_values)
    return est


def single_error(est, target_phi):
    """Считаем ошибку оценки по одной ревлизации шума"""
    return (est - target_phi + np.pi)%(2*np.pi) - np.pi

def list_errors(config_params: dict,
                energy_func: Callable,
                signal_func: Callable) -> float:
    """Формируем список ошибок для каждой реализации шума"""
    dir_matrix = get_direction_matrix(config_params["phis"], config_params["M"])
    
    return [single_error(single_est(config_params, dir_matrix, energy_func, signal_func), config_params["target_phi"]) 
            for _ in range(config_params["realisation_count"])]

def calculate_variance(list_errors: list) -> float:
    """Считаем дисперсию по списку ошибок"""
    
    var = 0
    K = len(list_errors)
    m_error = sum(list_errors)/K
    for error in list_errors:
        var += (m_error - error)**2
    return var/(K-1) 

def radius_from_alpha(config_params, alpha) -> float:
    """Значение радиуса по альфа при фиксированной частоте"""
    return config_params["c"] / (2 * config_params["f0"] * alpha)

def var_vs_params(config_params: dict,
                  energy_func: Callable,
                  signal_func: Callable,
                  parametr_name: str,
                  parametr_values: np.ndarray | list):
    """Универсальная фанкция для построения зависимость дисперссии от параметра моделирования"""
    result = []
    
    config_params = config_params.copy()
    for value in parametr_values:
        
        if parametr_name not in config_params:
            raise KeyError(F"Неизвестный параметр {parametr_name}")
        
        config_params[parametr_name] = value
        if parametr_name == "alpha":
            config_params["R"] = radius_from_alpha(config_params, value)
        lst = list_errors(config_params, energy_func,signal_func)
        result.append(calculate_variance(lst))
    return result








