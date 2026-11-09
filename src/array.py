import numpy as np
import src.functions as functions


def gamma_array(sensor_amount: int) -> np.ndarray:
    """Расчёт углов датчиков относительно оси x по их количеству."""

    return (2 * np.pi / sensor_amount) * np.arange(sensor_amount)


def tau_array(config_parametrs: dict) -> np.ndarray:
    """Расчёт задержек относительно каждого датчика."""

    return (config_parametrs["R"] / config_parametrs["c"]) * np.cos(
        config_parametrs["target_phi"] - gamma_array(config_parametrs["M"])
    )


def avp_signals(p_t: np.ndarray, config_parametrs: dict, energy_signal: float) -> dict:
    """Расчёт значений каналов y0, y1, y2 для АВП."""

    child_seeds = config_parametrs["main_rng"].bit_generator.seed_seq.spawn(3)

    rng1 = np.random.default_rng(child_seeds[0])
    rng2 = np.random.default_rng(child_seeds[1])
    rng3 = np.random.default_rng(child_seeds[2])

    y0 = p_t + functions.get_noise(
        config_parametrs, rng1, energy_signal
    )  # Размер 1 x N.

    y1 = p_t * np.cos(config_parametrs["target_phi"]) + functions.get_noise(
        config_parametrs, rng2, energy_signal
    )

    y2 = p_t * np.sin(config_parametrs["target_phi"]) + functions.get_noise(
        config_parametrs, rng3, energy_signal
    )

    return {"y0": y0, "y1": y1, "y2": y2}


def channel_matrix(
    config_params: dict, tau_array: np.ndarray, signal_func
) -> np.ndarray:
    """Матрица 3M x N для трёх каналов каждого датчика АВП."""

    config_params_copy = config_params.copy()
    channel_matrix = np.zeros(
        (3 * config_params_copy["M"], config_params_copy["N"]), dtype=complex
    )  # Создаём нулевую матрицу размера 3M x N.

    for idx, tau in enumerate(tau_array):
        """Сдвигаем временной вектор на задержку текущего датчика."""

        config_params_copy["time_vector"] = config_params["time_vector"] - tau
        p_t = signal_func(config_params_copy)
        energy_signal = functions.calculate_energy(
            p_t, config_params_copy["time_vector"]
        )
        signals = avp_signals(p_t, config_params_copy, energy_signal)

        sensor_matrix = np.vstack((signals["y0"], signals["y1"], signals["y2"]))
        channel_matrix[idx * 3 : idx * 3 + 3] = sensor_matrix

    return channel_matrix


def covariation_matrix(matrix: np.ndarray, N: int) -> np.ndarray:
    """Расчёт ковариационной матрицы для комплексных и вещественных данных."""

    return (matrix @ matrix.conj().T) / N


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
        tau_array = tau_array(config_copy)
        res.append(complex_stiring_vector(phi, tau_array, configs["f0"], configs["M"]))
    return np.array(res)
