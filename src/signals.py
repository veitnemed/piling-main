import numpy as np


def lorenth(config_params: dict) -> np.ndarray:
    """Расчёт импульса Лоренца по заданным параметрам."""
    tau = config_params["duration_pulse"]
    return (
        config_params["A"]
        * tau
        / (tau**2 + (config_params["time_vector"] - config_params["center_pulse"]) ** 2)
    )


def sinus(config_params: dict) -> np.ndarray:
    """Расчёт гармонического сигнала в каждый момент времени."""

    return config_params["A"] * np.sin(
        config_params["time_vector"] * (2 * np.pi * config_params["f0"])
    )
