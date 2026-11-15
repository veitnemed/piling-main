import numpy as np
import src.model as model

def complex_stiring_vector(
    phi: float, tau_array: np.ndarray, f0: float, M: int
) -> np.ndarray:
    "Рассчет комплексного стиринг-вектора"

    return np.array(
        [
            x
            for i in range(M)
            for x in np.array([1, np.cos(phi), np.sin(phi)])
            * np.exp(-2j * np.pi * f0 * tau_array[i])
        ]
    ).T


def complex_stiring_matrix(configs: dict) -> np.ndarray:
    """Рассчёт матрицы стиринг-векторов"""
    res = []

    for phi in configs["phi_vector"]:
        config_copy = configs.copy()
        config_copy["target_phi"] = phi
        taus = model.tau_array(config_copy)
        res.append(complex_stiring_vector(phi, taus, configs["f0"], configs["M"]))
    return np.array(res)


def calculate_stiring_vector(phi: float, M: int) -> np.ndarray:
    """Направляющий вектор"""
    return np.array([1, np.cos(phi), np.sin(phi)] * M).T


def calculate_stiring_matrix(config_params: dict):
    """Рассчёт матрицы направляющих векторов"""
    return np.array(
        [
            calculate_stiring_vector(phi, config_params["M"])
            for phi in config_params["phi_vector"]
        ]
    )
