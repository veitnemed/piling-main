"""В данном модуле используются функци, связанные со спектральными преобразованием """
import numpy as np


def cut_spectrum(spectrum: np.ndarray, bandwidth: float, fs: float) -> np.ndarray:
    """Идеальный фильтр нижних частот.
    Оставляет составляющие в диапазоне от -bandwidth/2 до bandwidth/2. +
    """

    local_freq_vector = np.fft.fftshift(np.fft.fftfreq(len(spectrum), d=1 / fs))
    mask = (local_freq_vector < -bandwidth / 2) | (local_freq_vector > bandwidth / 2)
    spectrum_copy = spectrum.copy()
    spectrum_copy[mask] = 0
    return spectrum_copy


def ifft(spectrum: np.ndarray) -> np.ndarray:
    """Обратное преобразование Фурье: комплексный спектр S(f) -> сигнал s(t)."""

    fft_back = np.fft.ifftshift(spectrum)
    complex_signal_back = np.fft.ifft(fft_back)
    return np.real(complex_signal_back)


def f_rms(spectrum: np.ndarray, config_parametrs: dict):
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


def fft(signal: np.ndarray):
    """Вычисление комплексного амплитудного спектра с помощью БПФ."""

    fft_values = np.fft.fft(signal)
    fft_centred = np.fft.fftshift(fft_values)
    return fft_centred


def spectrum_energy(spectrum: np.ndarray):
    """Сумма мощностей выбранных отсчётов БПФ для расчёта SNR."""
    return np.sum(np.abs(spectrum) ** 2)


def spectrum_SNR(signal, noise, freq_vector, f):

    spectrum_signal = fft(signal)
    spectrum_noise = fft(noise)

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

    se_signal = spectrum_energy(cut_signal)
    se_noise = spectrum_energy(cut_noise)

    return se_signal / se_noise


def cut_signal(signal: np.ndarray, bandwidth: float, fs: float) -> np.ndarray:
    """Фильтрация сигнала во временной области с заданной шириной полосы."""

    freq_signal = fft(signal)
    filt_freq_signal = cut_spectrum(freq_signal, bandwidth, fs)
    back_signal = ifft(filt_freq_signal)

    return back_signal


def f_99(freq_vector: np.ndarray, freq_signal: np.ndarray):
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
