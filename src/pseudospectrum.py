import numpy as np


def exact_bartlett(W: np.ndarray, complex_stiring_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Бартлетта с комплексным вектором."""
    return np.sum(
        (np.conj(complex_stiring_matrix) @ W) * complex_stiring_matrix, axis=1
    )


def excact_capon(W: np.ndarray, complex_dir_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Кейпона с комплексным вектором."""
    W_inv = np.linalg.pinv(W)

    return 1 / (
        np.sum((np.conj(complex_dir_matrix) @ W_inv) * complex_dir_matrix, axis=1)
    )


def approx_capon(W: np.ndarray, dir_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Кейпона."""
    W_inv = np.linalg.inv(W)

    return 1 / (np.sum((dir_matrix @ W_inv) * dir_matrix, axis=1))



def approx_bartlett(W: np.ndarray, dir_matrix: np.ndarray) -> list:
    """Расчёт энергетического спектра Бартлетта."""
    return np.sum((dir_matrix @ W) * dir_matrix, axis=1)
