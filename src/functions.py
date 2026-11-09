import numpy as np
from numpy.random import Generator
from .configs import config as cfg
import 

def calculate_energy(signal: np.ndarray, time_vector: np.ndarray):
    """Расчёт энергии сигнала на интервале наблюдения от 0 до T."""
    return np.trapezoid(y=np.abs(signal) ** 2, x=time_vector)


def calculate_noise_level(
    energy_signal: np.ndarray, snr: float, duration_all: np.ndarray
):
    """Расчёт СКО шума из отношения энергии сигнала к средней энергии шума."""

    return np.sqrt(energy_signal / (duration_all * snr))


def get_noise(
    config_parametrs: dict, rng: Generator, energy_signal: float
) -> np.ndarray:
    """Генерация аддитивного белого гауссовского шума с нулевым средним."""

    noise_level = calculate_noise_level(
        energy_signal, config_parametrs["snr"], config_parametrs["duration_all"]
    )
    return rng.normal(loc=0, scale=noise_level, size=config_parametrs["N"])






def calculate_full_bartlett_values(
    W: np.ndarray, complex_stiring_matrix: np.ndarray
) -> list:
    """Расчёт энергетического спектра Бартлетта с комплексным вектором."""
    return np.sum(
        (np.conj(complex_stiring_matrix) @ W) * complex_stiring_matrix, axis=1
    )


def calculate_stiring_vector(phi: float, M: int) -> np.ndarray:
    """Направляющий вектор"""
    return np.array([1, np.cos(phi), np.sin(phi)] * M).T


def calculate_full_capon_values(W: np.ndarray, complex_dir_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Кейпона с комплексным вектором."""
    W_inv = np.linalg.pinv(W)

    return 1 / (
        np.sum((np.conj(complex_dir_matrix) @ W_inv) * complex_dir_matrix, axis=1)
    )


def calculate_stiring_matrix(config_params: dict):
    """Рассчёт матрицы направляющих векторов"""
    return np.array(
        [
            calculate_stiring_vector(phi, config_params["M"])
            for phi in config_params["phi_vector"]
        ]
    )


def calculate_capon_values(W: np.ndarray, dir_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Кейпона."""
    W_inv = np.linalg.inv(W)

    return 1 / (np.sum((dir_matrix @ W_inv) * dir_matrix, axis=1))


def get_est_phi(phi_vector: np.ndarray, e_values: np.ndarray) -> float:
    """Определяем угол по максимум аргумента бартлета"""
    return phi_vector[np.argmax(e_values)]


def calculate_bartlett_values(W: np.ndarray, dir_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Бартлетта."""
    return np.sum((dir_matrix @ W) * dir_matrix, axis=1)
