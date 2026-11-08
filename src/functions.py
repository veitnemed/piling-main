import numpy as np
from numpy.random import Generator
from .configs import config as cfg


def filtering_spectrum(spectrum: np.ndarray, bandwidth: float, fs: float) -> np.ndarray:
    """Идеальный фильтр нижних частот.
    Оставляет составляющие в диапазоне от -bandwidth/2 до bandwidth/2.
    """

    local_freq_vector = np.fft.fftshift(np.fft.fftfreq(len(spectrum), d=1 / fs))
    mask = (local_freq_vector < -bandwidth / 2) | (local_freq_vector > bandwidth / 2)
    spectrum_copy = spectrum.copy()
    spectrum_copy[mask] = 0
    return spectrum_copy


def calculate_ifft(spectrum: np.ndarray) -> np.ndarray:
    """Обратное преобразование Фурье: комплексный спектр S(f) -> сигнал s(t)."""

    fft_back = np.fft.ifftshift(spectrum)
    complex_signal_back = np.fft.ifft(fft_back)
    return np.real(complex_signal_back)


def calculate_f_rms(spectrum: np.ndarray, config_parametrs: dict):
    "Расчёт среднеквадратической эффективной частоты."
    return np.abs(
        np.sqrt(
            np.trapezoid(
                y=(config_parametrs["freq_vector"] * np.abs(spectrum)) ** 2,
                x=config_parametrs["freq_vector"],
            )
            / (np.trapezoid(y=np.abs(spectrum) ** 2, x=config_parametrs["freq_vector"]))
        )
    )


def calculate_fft(signal: np.ndarray):
    """Вычисление комплексного амплитудного спектра с помощью БПФ."""

    fft_values = np.fft.fft(signal)
    fft_centred = np.fft.fftshift(fft_values)
    return fft_centred


def calculate_spectrum_energy(spectrum: np.ndarray):
    """Сумма мощностей выбранных отсчётов БПФ для расчёта SNR."""
    return np.sum(np.abs(spectrum) ** 2)


def calculate_spectrum_SNR(signal, noise, freq_vector, f):

    spectrum_signal = calculate_fft(signal)
    spectrum_noise = calculate_fft(noise)

    if (len(spectrum_signal) != len(spectrum_noise)) or (
        len(spectrum_signal) != len(freq_vector)
    ):
        raise ValueError("Все входные массивы должны быть одинаковой длины")

    mask = np.abs(freq_vector) >= f
    cut_signal = spectrum_signal[mask]
    cut_noise = spectrum_noise[mask]

    if len(cut_signal) == 0:
        raise ValueError(
            "Спектральная составляющая должна содержать хотя бы один отсчёт"
        )

    se_signal = calculate_spectrum_energy(cut_signal)
    se_noise = calculate_spectrum_energy(cut_noise)

    return se_signal / se_noise


def filering_signal(signal: np.ndarray, bandwidth: float, fs: float) -> np.ndarray:
    """Фильтрация сигнала во временной области с заданной шириной полосы."""

    freq_signal = calculate_fft(signal)
    filt_freq_signal = filtering_spectrum(freq_signal, bandwidth, fs)
    back_signal = calculate_ifft(filt_freq_signal)

    return back_signal


def calculate_99(freq_vector: np.ndarray, freq_signal: np.ndarray):
    """Расчёт односторонней ширины спектра, сохраняющей 99 % энергии.
    Полная ширина полосы фильтрации равна 2*B.
    """

    power = np.abs(freq_signal) ** 2
    order = np.argsort(np.abs(freq_vector))
    energy_1 = np.cumsum(power[order])
    energy_1 /= energy_1[-1]
    idx = np.searchsorted(energy_1, 0.99)
    res = np.abs(freq_vector[order[idx]])
    return res


def calculate_energy(signal: np.ndarray, time_vector: np.ndarray):
    """Расчёт энергии сигнала на интервале наблюдения от 0 до T."""
    return np.trapezoid(y=signal**2, x=time_vector)


def calculate_noise_level(
    energy_signal: np.ndarray, snr: float, duration_all: np.ndarray
):
    """Расчёт СКО шума из отношения энергии сигнала к средней энергии шума."""

    return np.sqrt(energy_signal / (duration_all * snr))


def get_noise(config_parametrs, rng: Generator, energy_signal: float) -> np.ndarray:
    """Генерация аддитивного белого гауссовского шума с нулевым средним."""

    noise_level = calculate_noise_level(
        energy_signal, config_parametrs["snr"], config_parametrs["duration_all"]
    )
    return rng.normal(loc=0, scale=noise_level, size=config_parametrs["N"])


def get_gamma_array(SENSOR_AMOUNT: int) -> np.ndarray:
    """Расчёт углов датчиков относительно оси x по их количеству."""

    return (2 * np.pi / SENSOR_AMOUNT) * np.arange(SENSOR_AMOUNT)


def get_tau_array(config_parametrs: dict) -> np.ndarray:
    """Расчёт задержек относительно каждого датчика."""

    return (config_parametrs["R"] / config_parametrs["c"]) * np.cos(
        config_parametrs["target_phi"] - get_gamma_array(config_parametrs["M"])
    )


def get_impulse_signal(config_params: dict) -> np.ndarray:
    """Расчёт импульса Лоренца по заданным параметрам."""
    tau = config_params["duration_pulse"]
    return (
        config_params["A"]
        * tau
        / (tau**2 + (config_params["time_vector"] - config_params["center_pulse"]) ** 2)
    )


def get_sin_signal(config_params: dict) -> np.ndarray:
    """Расчёт гармонического сигнала в каждый момент времени."""

    return config_params["A"] * np.sin(
        config_params["time_vector"] * (2 * np.pi * config_params["f0"])
    )


def get_avp_signals(
    p_t: np.ndarray, config_parametrs: dict, energy_signal: float
) -> dict:
    """Расчёт значений каналов y0, y1, y2 для АВП."""

    child_seeds = config_parametrs["main_rng"].bit_generator.seed_seq.spawn(3)

    rng1 = np.random.default_rng(child_seeds[0])
    rng2 = np.random.default_rng(child_seeds[1])
    rng3 = np.random.default_rng(child_seeds[2])

    y0 = p_t + get_noise(config_parametrs, rng1, energy_signal)  # Размер 1 x N.

    y1 = p_t * np.cos(config_parametrs["target_phi"]) + get_noise(
        config_parametrs, rng2, energy_signal
    )

    y2 = p_t * np.sin(config_parametrs["target_phi"]) + get_noise(
        config_parametrs, rng3, energy_signal
    )

    return {"y0": y0, "y1": y1, "y2": y2}


def get_channel_matrix(
    config_params: dict, tau_array: np.ndarray, signal_func
) -> np.ndarray:
    """Матрица 3M x N для трёх каналов каждого датчика АВП."""

    config_params_copy = config_params.copy()
    channel_matrix = np.zeros(
        (3 * config_params_copy["M"], config_params_copy["N"])
    )  # Создаём нулевую матрицу размера 3M x N.

    for idx, tau in enumerate(tau_array):
        """Сдвигаем временной вектор на задержку текущего датчика."""

        config_params_copy["time_vector"] = config_params["time_vector"] - tau
        p_t = signal_func(config_params_copy)
        energy_signal = calculate_energy(p_t, config_params_copy["time_vector"])
        signals = get_avp_signals(p_t, config_params_copy, energy_signal)

        sensor_matrix = np.vstack((signals["y0"], signals["y1"], signals["y2"]))
        channel_matrix[idx * 3 : idx * 3 + 3] = sensor_matrix

    return channel_matrix


def get_covariation_matrix(matrix: np.ndarray, N: int) -> np.ndarray:
    """Расчёт ковариационной матрицы для комплексных и вещественных данных."""

    return (matrix @ matrix.conj().T) / N


def calculate_complex_stiring_vector(
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


def calculate_complex_stiring_matrix(configs: dict) -> np.ndarray:
    """Рассчёт матрицы стиринг-векторов"""
    res = []

    for phi in configs["phis"]:
        config_copy = configs.copy()
        config_copy["target_phi"] = phi
        tau_array = get_tau_array(config_copy)
        res.append(
            calculate_complex_stiring_vector(
                phi, tau_array, configs["f0"], configs["M"]
            )
        )
    return np.array(res)


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
            for phi in config_params["phis"]
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
