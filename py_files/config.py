import numpy as np

GLOBAL_SEED = 10


# ПАРАМЕТРЫ МОДЕЛИ 
fs = 8800 # ЧАСТОТА ДИСКРЕТИЗАЦИИ
dt = 1/fs # ШАГ ДИСКРЕТИЗАЦИИ
N = 10000 # КОЛИЧЕСТВО ТОЧЕК 
t = np.arange(N)*dt #ВЕКТОР ВРЕМЕНИ
T = t[-1] - t[0] # окно наблюдения 

delta_phi = 0.001 # Шаг поиска угла 0.0003
N_phi = int(2*np.pi/delta_phi) # Количество значений угла 
phi_vector = np.linspace(0,2*np.pi,N_phi,endpoint= False) # Значения угла от 0 до 2П

# ПАРАМЕТРЫ АВП
M = 3 # КОЛИЧЕСТВО ДАТЧИКОВ
c = 343.26 # СКОРОСТЬ ЗВУКА


# ПАРАМЕТРЫ СИГНАЛА 
f = 10 # ЦЕНТРАЛЬНАЯ ЧАСТОТА СИГНАЛА 
A = 1 # АМПЛИТУДА СИГНАЛА 
alpha = 10
R = c / (2*f*alpha)
TARGET_PHI = np.pi/2 # АЗИМУТ ПОД КОТОРЫМ ПРИХОДИТ ИСГНАЛ (ТО ЧТО ОЦЕНИВАЕМ)

f1 = c/(2*R*alpha)
R1 = 1

# Параметры шумы

REALISATION_COUNT = 2

# ПАРАМЕТРЫ ЭКСПЕРИМЕНТА 

SENSOR_VALUES = [1, 5, 7, 10, 12, 15, 17, 20]

SNR_VALUES = np.linspace(0.5, 10, 10)
NOISE_LEVEL_VALUES = A/np.sqrt(SNR_VALUES)

ALPHA_VALUES_2 = np.arange(0,1, 0.01)
ALPHA_VALUES_1 = np.arange(1,10,1)
R_min = 0.1
R_max = 10.0
R_VALUES = np.linspace(R_min, R_max, 10)


STANDART_DIVIATONS_NOISE = A/np.sqrt(np.array(SNR_VALUES))

SNR = 2
NOISE_LEVEL = 0.3
TIME_LIMIT = {"left": 0,
        "right": 0.15}


PHI_VALUES = np.linspace(0,2*np.pi,10, endpoint = False)

CONFIG_PARAMETRS = {"snr": SNR,
        "M": M,
        "N": N,
        "R": R,
        "f0": f,
        "A": A,
        "c": c,
        "K": REALISATION_COUNT,
        "target_phi": TARGET_PHI,
        "alpha": alpha,
        "phis": phi_vector,
        "main_seed": GLOBAL_SEED}



def init_rng(main_seed: int = GLOBAL_SEED):
    """Инциализация стартового конфига"""
    parametrs = CONFIG_PARAMETRS.copy()
    parametrs["main_rng"] = np.random.default_rng(main_seed)
    parametrs["main_seed"] = main_seed
    return parametrs

def update_config():
    parametrs = CONFIG_PARAMETRS.copy()
    """Отдельная функция, чтобы случайно не передать в init_rng значенеи seed"""
    if "main_rng" not in parametrs:
        raise KeyError(f"Rng не иницализирован, сначала вызовоите init_rng")
    return parametrs
    