import numpy as np



GLOBAL_SEED = 10
SPEED_ON_SOUND = 343.26 # СКОРОСТЬ ЗВУКА
FS = 8800 # ЧАСТОТА ДИСКРЕТИЗАЦИИ
DT = 1/FS # ШАГ ДИСКРЕТИЗАЦИИ
CONST_RADIAN = (np.pi/180)**2


# ПАРАМЕТРЫ МОДЕЛИ 
N = 10000 # КОЛИЧЕСТВО ТОЧЕК 

TIME_VECTOR = np.arange(N)*DT #ВЕКТОР ВРЕМЕНИ
DURATION_ALL = TIME_VECTOR[-1] - TIME_VECTOR[0] # ДЛИТЕЛЬНОСТЬ ИМПУЛЬСА
CENTER_PULSE = DURATION_ALL/2 # Центр импульсного сигнала 
PHI_STEP = 0.001 # Шаг поиска угла 0.0003
FREQ_VECTOR = np.fft.fftshift(np.fft.fftfreq(N, d=1/FS))
N_PHI = int(2*np.pi/PHI_STEP) # Количество значений угла 
PHI_VECTOR = np.linspace(0, 2*np.pi, N_PHI, endpoint= False) # Значения угла от 0 до 2П

# ПАРАМЕТРЫ АВП
M = 1 # КОЛИЧЕСТВО ДАТЧИКОВ



# ПАРАМЕТРЫ СИГНАЛА 
F_GARMONIC = 10 # ЦЕНТРАЛЬНАЯ ЧАСТОТА СИГНАЛА 
A = 1 # АМПЛИТУДА СИГНАЛА 
ALPHA = 10
R = SPEED_ON_SOUND / (2*F_GARMONIC*ALPHA)
TARGET_PHI = np.pi/4 # АЗИМУТ ПОД КОТОРЫМ ПРИХОДИТ ИСГНАЛ (ТО ЧТО ОЦЕНИВАЕМ)

f1 = SPEED_ON_SOUND/(2*R*ALPHA)
R1 = 1

# Параметры шумы
REALISATION_COUNT = 200

# ПАРАМЕТРЫ ЭКСПЕРИМЕНТА 
SENSOR_VALUES = [1, 5, 7, 10, 12, 15, 17, 20]
SNR_VALUES = np.linspace(0.5, 10, 10)
NOISE_LEVEL_VALUES = A/np.sqrt(SNR_VALUES)
ALPHA_VALUES_2 = np.arange(0,1, 0.01)
ALPHA_VALUES_1 = np.arange(10,20,1)
RADIUS_VALUES = np.linspace(0,1, 10, 10)


STANDART_DIVIATONS_NOISE = A/np.sqrt(np.array(SNR_VALUES))

SNR = 2
TIME_LIMIT = {"left": 0,
        "right": 0.15}

BETTA_PULSE = 0.05
PHI_VALUES = np.linspace(0,np.pi,120, endpoint = True) # Для построения пространства ошибок

CONFIG_PARAMETRS = {"snr": SNR,
        "M": M,
        "time_vector": TIME_VECTOR,
        "freq_vector": FREQ_VECTOR,
        "duration_all": DURATION_ALL,
        "N": N,
        "fs": FS,
        "R": R,
        "f0": F_GARMONIC,
        "A": A,
        "c": SPEED_ON_SOUND,
        "duration_pulse": BETTA_PULSE,
        "realisation_count": REALISATION_COUNT,
        "target_phi": TARGET_PHI,
        "alpha": ALPHA,
        "phis": PHI_VECTOR,
        "main_seed": GLOBAL_SEED,
        "main_rng": np.random.default_rng(GLOBAL_SEED),
        "center_pulse": CENTER_PULSE}



def init_rng(main_seed: int = GLOBAL_SEED):
    """Инциализация стартового конфига"""
  
    parametrs = CONFIG_PARAMETRS.copy()
    parametrs["main_rng"] = np.random.default_rng(main_seed)
    parametrs["main_seed"] = main_seed
    return parametrs

def restart_rng(config_parametrs: dict) -> dict:
    """Сброс генератора"""
    import copy
    new_config = copy.deepcopy(config_parametrs)
    new_config["main_rng"] = np.random.default_rng(new_config["main_seed"])
    return new_config
    