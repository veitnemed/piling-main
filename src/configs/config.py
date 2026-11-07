import numpy as np
import src.configs.comon as comon


# ========== VECTORS =============
# ================================

TIME_VECTOR = np.arange(comon.N)*comon.DT #ВЕКТОР ВРЕМЕНИ
FREQ_VECTOR = np.fft.fftshift(np.fft.fftfreq(comon.N, d=1/comon.FS))
PHI_VECTOR = np.linspace(0, 2*np.pi, comon.AMOUNT_PHI, endpoint= False) # Значения угла от 0 до 2П


# ========== VALUES =============
# ===============================

SENSOR_VALUES = [1, 5, 7, 10, 12, 15, 17, 20]
SNR_VALUES = np.linspace(0.5, 10, 10)
NOISE_LEVEL_VALUES = comon.A/np.sqrt(SNR_VALUES)

RADIUS_VALUES = np.linspace(0.1, 1, 10)
SDN_VALUES = comon.A / np.sqrt(np.array(SNR_VALUES))
PHI_VALUES = np.linspace(0, 2*np.pi, 30, endpoint = True) # Для построения пространства ошибок
FREQ_VALUES = np.linspace(1,250,25)
# НА ДАННЫЙ МОМЕНТ ОТНОШЕНИЕ АЛЬФА ПОД ВОПРОСОМ, НУЖНО ЛИ ИМЕННО ЕГО ИССЛЕДОВАТЬ
# ПОЭТОМУ Я РЕШИЛ ПОКА УБРАТЬ АЛЬФА-ЗАВИСИМОСТЬ 
#ALPHA_VALUES = np.arange(10,20,1)
#ALPHA_RMS_VALUES = np.arange(10,20,1)


# ========== CONFIGURATION =======
# ================================

def create_parameters_config() -> dict:
    """Создание конфигурации"""
    TIME_VECTOR = np.arange(comon.N)*comon.DT
    FREQ_VECTOR = np.fft.fftshift(np.fft.fftfreq(comon.N, d=1/comon.FS))
    PHI_VECTOR = np.linspace(0, 2*np.pi, comon.AMOUNT_PHI, endpoint= False)

    return {"dt": comon.DT,
            "df": comon.DF,
            "snr": comon.SNR,
            "M": comon.M,
            "time_vector": TIME_VECTOR,
            "freq_vector": FREQ_VECTOR,
            "duration_all": comon.DURATION_ALL,
            "N": comon.N,
            "fs": comon.FS,
            "R": comon.RADIUS,
            "f0": comon.F_GARMONIC,
            "A": comon.A,
            "c": comon.SPEED_ON_SOUND,
            "duration_pulse": comon.BETTA_PULSE,
            "realisation_count": comon.REALISATION_COUNT,
            "target_phi": comon.TARGET_PHI,
            "phis": PHI_VECTOR,
            "main_seed": comon.GLOBAL_SEED,
            "main_rng": np.random.default_rng(comon.GLOBAL_SEED),
            "center_pulse": comon.CENTER_PULSE,
         #"alpha": comon.ALPHA,
        #"alpha_rms": comon.RMS_ALPHA,
    }


# ========== INIT =======
# ========================
def init_rng(main_seed: int = comon.GLOBAL_SEED):
    """Инциализация стартового конфига"""
  
    parametrs = create_parameters_config()
    parametrs["main_rng"] = np.random.default_rng(main_seed)
    parametrs["main_seed"] = main_seed
    return parametrs

def restart_rng(config_parametrs: dict) -> dict:
    """Сброс генератора"""
    import copy
    new_config = copy.deepcopy(config_parametrs)
    new_config["main_rng"] = np.random.default_rng(new_config["main_seed"])
    return new_config

