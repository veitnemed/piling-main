import numpy as np
import py_files.configs.comon as comon



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
ALPHA_VALUES = np.arange(10,20,1)
RADIUS_VALUES = np.linspace(0,1, 10, 10)
SDN_VALUES = comon.A / np.sqrt(np.array(SNR_VALUES))
PHI_VALUES = np.linspace(0,2*np.pi,120, endpoint = True) # Для построения пространства ошибок
ALPHA_RMS_VALUES = np.arange(10,20,1)


# ========== CONFIGURATION =======
# ================================

CONFIG_PARAMETRS = {"snr": comon.SNR,
        "M": comon.M,
        "time_vector": TIME_VECTOR,
        "freq_vector": FREQ_VECTOR,
        "duration_all": comon.DURATION_ALL,
        "N": comon.N,
        "fs": comon.FS,
        "R": comon.R,
        "f0": comon.F_GARMONIC,
        "A": comon.A,
        "c": comon.SPEED_ON_SOUND,
        "duration_pulse": comon.BETTA_PULSE,
        "realisation_count": comon.REALISATION_COUNT,
        "target_phi": comon.TARGET_PHI,
        "alpha": comon.ALPHA,
        "alpha_rms_values": ALPHA_RMS_VALUES,
        "alpha_rms": comon.ALPHA_RMS,
        "phis": PHI_VECTOR,
        "main_seed": comon.GLOBAL_SEED,
        "main_rng": np.random.default_rng(comon.GLOBAL_SEED),
        "center_pulse": comon.CENTER_PULSE}


# ========== INIT =======
# ========================

def init_rng(main_seed: int = comon.GLOBAL_SEED):
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
    