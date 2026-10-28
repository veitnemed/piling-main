import numpy as np
from numpy.random import Generator
from .configs import config as cfg

def spectrum_filtering(freq_spectr: np.ndarray,
                       bandwidth: float) -> np.ndarray:
    """Идеальный полосовой фильтр 
    Оставляет частотные составляющие в диапазоне от - bandwidth до bandwidth"""

    mask = (cfg.FREQ_VECTOR < -bandwidth/2) | (cfg.FREQ_VECTOR > bandwidth/2)
    freq_spectr_copy = freq_spectr.copy()
    freq_spectr_copy[mask] = 0
    return freq_spectr_copy

def calculate_ifft(freq_spectr):
    fft_back = np.fft.ifftshift(freq_spectr)
    complex_signal_back = np.fft.ifft(fft_back)
    return np.real(complex_signal_back)
    

def calculate_f_rms(freq_spectr: np.ndarray,
                    config_parametrs: dict):
    "Рассчёт среднеквадратической частоты"
    return np.abs(np.sqrt(np.trapezoid(y = (config_parametrs["freq_vector"]*freq_spectr)**2, 
                                x = config_parametrs["freq_vector"]) 
                                / (np.trapezoid(y = freq_spectr**2, 
                                                x = config_parametrs["freq_vector"]))))
    
def calculate_fft(signal: np.ndarray, 
                  fs: float):
    """Вычиление амплитудного спектра (БПФ)"""
    fft_values = np.fft.fft(signal)
    fft_centred = np.fft.fftshift(fft_values)
    return fft_centred
    
def calculate_99(freq_vector, freq_signal):
    
    power = freq_signal**2
    order = np.argsort(np.abs(freq_vector))

    energy_1 = np.cumsum(power[order])
    energy_1  /= energy_1[-1]
    idx = np.searchsorted(energy_1, 0.99)
    res = np.abs(freq_vector[order[idx]])
    return res

def calculate_energy(signal: np.ndarray, 
                     time_vector: np.ndarray):
    """ Рассчёт энергии сигнала на интервале наблюдения от 0 до T """
    
    return np.trapezoid(y = signal**2, x = time_vector)

def calculate_noise_level(energy_signal: np.ndarray, 
                          snr: float, 
                          duration_all: np.ndarray):
    """Рассчёт СКО шума из опредения SNR: отношения энергии сигнала к средней энергии шума"""

    return np.sqrt(energy_signal/(duration_all*snr))

def get_noise(config_parametrs, 
              rng: Generator,
              energy_signal: float) -> np.ndarray:
    """Генрация АЬГШ с мат ожиданием 0"""

    noise_level = calculate_noise_level(energy_signal, config_parametrs["snr"], config_parametrs["duration_all"])
    return rng.normal(loc = 0, scale = noise_level, size = config_parametrs["N"])

def get_gamma_array(SENSOR_AMOUNT: int) -> np.ndarray:
    """Рассчет углов датчиков относительно оси x
    Функция принимает на вход число датчиков и возвращает 
    массив углов для каждого датчика"""
    
    return (2*np.pi/SENSOR_AMOUNT)*np.arange(SENSOR_AMOUNT)

def get_tau_array(config_parametrs: dict) -> np.ndarray:
    """Рассчёт задержек относительно каждого датчика"""
    
    return (config_parametrs["R"] / config_parametrs["c"])*np.cos(config_parametrs["target_phi"] - get_gamma_array(config_parametrs["M"]))

def get_impulse_signal(config_params) -> np.ndarray:
    """Тут используется приблтжение чтобы у функций был один"""
    tau = config_params["duration_pulse"]
    return config_params["A"]*tau / (tau**2 + (config_params["time_vector"] - config_params["center_pulse"])**2)
    
def get_sin_signal(config_params) -> np.ndarray:
    """Считаем значение гармончиеского сигнала в каждый момент времени"""
    
    return  config_params["A"]*np.sin(config_params["time_vector"]*(2*np.pi*config_params["f0"]))



def get_avp_signals(p_t: np.ndarray,
                    config_parametrs,
                    energy_signal) -> dict:
    """Рассчёт значений каналов y0 y1 y2 для АВП"""

    child_seeds = config_parametrs["main_rng"].bit_generator.seed_seq.spawn(3)
    
    rng1 = np.random.default_rng(child_seeds[0])
    rng2 = np.random.default_rng(child_seeds[1])
    rng3 = np.random.default_rng(child_seeds[2])
    
    
    y0 = p_t + get_noise(config_parametrs, rng1, energy_signal) # size (1 x N)
    y1 = p_t*np.cos(config_parametrs["target_phi"]) + get_noise(config_parametrs, rng2, energy_signal)
    y2 = p_t*np.sin(config_parametrs["target_phi"]) + get_noise(config_parametrs, rng3, energy_signal)
        
    return {"y0": y0, "y1": y1, "y2": y2}

def get_channel_matrix(config_params: dict,
                       tau_array: np.ndarray,
                       signal_func) -> np.ndarray:
    """Функция возращает матрицу 3M x N со значениями для каждого из трёх каналов датчика АВП"""

    config_params_copy = config_params.copy()
    channel_matrix = np.zeros((3*config_params_copy["M"], config_params_copy["N"])) # Создаём нулевую матрицу размера M x N

    for idx, tau in enumerate(tau_array):
        """На каждой итерации для текущей кофигурации присваем параметру time_vector  - исодный 
        time минус текущий тау"""

        config_params_copy["time_vector"] = config_params["time_vector"] - tau 
        p_t = signal_func(config_params_copy)
        energy_signal = calculate_energy(p_t, config_params_copy["time_vector"])
        signals = get_avp_signals(p_t, config_params_copy, energy_signal)

    
        sensor_matrix = np.vstack((signals["y0"], signals["y1"], signals["y2"])) 
        channel_matrix[idx*3:idx*3+3] = sensor_matrix
        
    return channel_matrix

def get_covariation_matrix(matrix: np.ndarray,
                           N: int) -> np.ndarray:
    """Рассчёт ковариационной матрицы"""
    return (matrix @ matrix.T) / N

def get_direction_vector(phi: float, M: int) -> np.ndarray:
    """Направляющий вектор"""
    return np.array([1,np.cos(phi),np.sin(phi)]*M).T

def get_direction_matrix(phis: np.ndarray, M: int):
    """Рассчёт матрицы направляющих векторов"""
    return np.array([get_direction_vector(phi, M) for phi in phis])

def get_cap_values(
                 W: np.ndarray,
                 dir_matrix: np.ndarray) -> list:
    """Рассчёт значений энергетического спектра  Кейпона"""
    W_inv = np.linalg.inv(W)
    
    return 1/( np.sum((dir_matrix @ W_inv ) * dir_matrix, axis=1))


def get_est_phi(phi_vector: np.ndarray, e_values: np.ndarray) -> float:
    """Определяем угол по максимум аргумента Барлета"""
    return phi_vector[np.argmax(e_values)]

def get_barlet_values(
                 W: np.ndarray,
                 dir_matrix: np.ndarray) -> list:
    """Рассчёт значений энергетического спектра  Барлета"""
    return np.sum((dir_matrix @ W ) * dir_matrix, axis=1)
