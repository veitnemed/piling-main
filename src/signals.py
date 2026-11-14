import numpy as np
from numpy.random import Generator


def lorenth(config_params: dict) -> np.ndarray:
    """Расчёт импульса Лоренца по заданным параметрам."""
    tau = config_params["duration_pulse"]
    return config_params["p_max"] * (
        tau**2
        / (tau**2 + (config_params["time_vector"] - config_params["center_pulse"]) ** 2)
    )


def sinus(config_params: dict) -> np.ndarray:
    """Расчёт гармонического сигнала в каждый момент времени."""

    return config_params["A"] * np.sin(
        config_params["time_vector"] * (2 * np.pi * config_params["f0"])
    )


def calculate_energy(signal: np.ndarray, time_vector: np.ndarray):
    """Расчёт энергии сигнала на интервале наблюдения от 0 до T."""
    return np.trapezoid(y=np.abs(signal) ** 2, x=time_vector)


def noise_level(
    energy_signal: np.ndarray, snr: float, duration_all: np.ndarray
):
    """Расчёт СКО шума из отношения энергии сигнала к средней энергии шума."""

    return np.sqrt(energy_signal / (duration_all * snr))


def noise(config_parametrs: dict, rng: Generator, energy_signal: float) -> np.ndarray:
    """Генерация аддитивного белого гауссовского шума с нулевым средним."""

    sigma = noise_level(
        energy_signal, config_parametrs["snr"], config_parametrs["duration_all"]
    )
    return rng.normal(loc=0, scale=sigma, size=config_parametrs["N"])
