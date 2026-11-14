"""Статистика экспериментов"""

import numpy as np
import scipy.signal as signal
import src.configs.config as config
from collections.abc import Callable
import src.model as model

def estimate_athimut(phi_vector: np.ndarray, pseudospectrum: np.ndarray) -> float:
    """Определяем угол по максимум аргумента бартлета"""
    return phi_vector[np.argmax(pseudospectrum)]

def single_est(
    config_params: dict,
    dir_matrix: np.ndarray,
    target_func: Callable,
    signal_func: Callable,
    is_hilbert: bool = False,
) -> float:
    """Расчёт оценки по одной реализации шума."""


    taus = model.tau_array(config_params)
    channel_matrix = model.channel_matrix(
        config_params=config_params, tau_array=taus, signal_func=signal_func
    )
    if is_hilbert is True:
        channel_matrix = signal.hilbert(channel_matrix.real, axis=1)

    W = model.covariation_matrix(channel_matrix, config_params["N"])
    Energy_values = target_func(W, dir_matrix)
    est = estimate_athimut(config_params["phi_vector"], Energy_values)
    return est


def single_error(est, target_phi):
    """Расчёт ошибки оценки по одной реализации шума."""
    return (est - target_phi + np.pi) % (2 * np.pi) - np.pi


def list_errors(
    config_params: dict,
    target_func: Callable,
    signal_func: Callable,
    stiring_func: Callable,
    is_hilbert: bool = False,
) -> list:
    """Формирование списка ошибок для каждой реализации шума."""

    dir_matrix = stiring_func(config_params)

    return [
        single_error(
            single_est(config_params, dir_matrix, target_func, signal_func, is_hilbert),
            config_params["target_phi"],
        )
        for _ in range(config_params["realisation_count"])
    ]


def calculate_variance(list_errors: list) -> float:
    """Считаем дисперсию по списку ошибок"""
    return np.var(list_errors, ddof=1)


def stat_vs_params(
    config_params: dict,
    energy_func: Callable,
    signal_func: Callable,
    stiring_func: Callable,
    parametr_name: str,
    parametr_values: np.ndarray | list,
    stat_func: Callable = calculate_variance,
    is_CRN: bool = True,
    is_random_start: bool = False,
    is_hilbert: bool = False,
):
    """Расчёт статистики ошибки для набора значений параметра моделирования."""
    from copy import deepcopy

    result = []
    new_config = (
        config.shake_rng(config_params)
        if is_random_start is True
        else deepcopy(config_params)
    )

    for value in parametr_values:

        if is_CRN is True:
            new_config = config.restart_rng(new_config.copy())

        if parametr_name not in new_config:
            raise KeyError(f"Неизвестный параметр {parametr_name}")

        new_config[parametr_name] = value

        lst = list_errors(new_config, energy_func, signal_func, stiring_func, is_hilbert)
        result.append(stat_func(lst))
    return result
