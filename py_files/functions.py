import numpy as np
from numpy.random import Generator

def get_gamma_array(M: int) -> np.ndarray:
    """Рассчет углов датчиков относительно оси x
    Функция принимает на вход число датчиков и возвращает 
    массив углов для каждого датчика"""
    
    return (2*np.pi/M)*np.arange(M)

def get_tau_array(config_parametrs: dict) -> np.ndarray:
    """Рассчёт задержек относительно каждого датчика"""
    
    return (config_parametrs["R"]/config_parametrs["c"])*np.cos(config_parametrs["target_phi"] - get_gamma_array(config_parametrs["M"]))

def get_impulse_signal(time_vector: np.ndarray, 
                    tau: float,
                    A: float = 1.0) -> np.ndarray:
    
    return A*tau / (tau**2 + time_vector**2)
    
def get_sin_signal(time_vector: np.ndarray, 
                    f: float,
                    A: float = 1.0,) -> np.ndarray:
    """Считаем значение гармончиеского сигнала в каждый момент времени"""
    
    return  A*np.sin(time_vector*(2*np.pi*f))

def get_noise(config_parametrs, rng: Generator) -> np.ndarray:
    """Генрация помех"""

    noise_level = config_parametrs["A"]/np.sqrt(config_parametrs["snr"])
    return rng.normal(loc = 0, scale = noise_level, size = config_parametrs["N"])

def get_avp_signals(p_t: np.ndarray,
                    config_parametrs) -> dict:
    """Рассчёт значений каналов y0 y1 y2 для АВП"""
    child_seeds = config_parametrs["main_rng"].bit_generator.seed_seq.spawn(3)
    
    rng1 = np.random.default_rng(child_seeds[0])
    rng2 = np.random.default_rng(child_seeds[1])
    rng3 = np.random.default_rng(child_seeds[2])
    
    y0 = p_t + get_noise(config_parametrs, rng1) # size (1 x N)
    y1 = p_t*np.cos(config_parametrs["target_phi"]) + get_noise(config_parametrs, rng2)
    y2 = p_t*np.sin(config_parametrs["target_phi"]) + get_noise(config_parametrs, rng3)
        
    return {"y0": y0,"y1": y1,"y2": y2}

def get_channel_matrix(config_params: dict,
                       tau_array,
                       t: np.ndarray, 
                    ) -> np.ndarray:
    """Функция возращает матрицу 3M x N со значениями для каждого из трёх каналов датчика АВП"""
    
    channel_matrix = np.zeros((3*config_params["M"], config_params["N"])) # Создаём нулевую матрицу размера M x N
    
    for idx, tau in enumerate(tau_array):
        p_t = get_sin_signal(t - tau, config_params["f0"], config_params["A"])
        signals = get_avp_signals(p_t, config_params)

    
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