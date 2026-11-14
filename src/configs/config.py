import numpy as np
import src.configs.comon as comon

# ========== КОНФИГУРАЦИЯ =======
# ================================

def create_parameters_config() -> dict:
    """Создание конфигурации"""
    comons = comon.init_comon_params()

    # ВЕКТОРЫ
    TIME_VECTOR = np.arange(comons["N"]) * comons["dt"]
    FREQ_VECTOR = np.fft.fftshift(np.fft.fftfreq(comons["N"], d=1 / comons["fs"]))
    PHI_VECTOR = np.linspace(0, 2 * np.pi, comons["amount_phi"], endpoint=False)
    # ДИАПАЗОНЫ
    SENSOR_VALUES = [1, 5, 7, 10, 12, 15, 17, 20]
    SNR_VALUES = np.linspace(0.5, 10, 10)
    NOISE_LEVEL_VALUES = comons["A"] / np.sqrt(SNR_VALUES)
    RADIUS_VALUES = np.linspace(0.1, 1, 10)
    SDN_VALUES = comons["A"] / np.sqrt(np.array(SNR_VALUES))
    PHI_VALUES = np.linspace(0, 2 * np.pi, 18, endpoint=True)
    FREQ_VALUES = np.linspace(1, 100, 25)

    return {
        "time_vector": TIME_VECTOR,
        "freq_vector": FREQ_VECTOR,
        "phi_vector": PHI_VECTOR,
        "sensor_values": SENSOR_VALUES,
        "snr_values": SNR_VALUES,
        "noise_level_values": NOISE_LEVEL_VALUES,
        "radius_values": RADIUS_VALUES,
        "sdn_values": SDN_VALUES,
        "phi_values": PHI_VALUES,
        "freq_values": FREQ_VALUES,
        "main_rng": np.random.default_rng(comons["main_seed"]),
        **comons
    }

# ========== ИНИЦИАЛИЗАЦИЯ =======
# ========================

def init_rng(main_seed: int = comon.init_comon_params()["main_seed"]):
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


def shake_rng(config_parametrs: dict) -> dict:
    """Случайное значение генератора"""
    import copy

    new_config = copy.deepcopy(config_parametrs)
    new_config["main_seed"] = None
    new_config["main_rng"] = np.random.default_rng(new_config["main_seed"])
    return new_config
