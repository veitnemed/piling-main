import numpy as np
import src.configs.comon as comon

# ========== ВЕКТОРЫ =============
# ================================

TIME_VECTOR = np.arange(comon.N) * comon.DT  # ВЕКТОР ВРЕМЕНИ
FREQ_VECTOR = np.fft.fftshift(np.fft.fftfreq(comon.N, d=1 / comon.FS))
PHI_VECTOR = np.linspace(
    0, 2 * np.pi, comon.AMOUNT_PHI, endpoint=False
)  # Значения угла от 0 до 2П


# ========== ЗНАЧЕНИЯ =============
# ===============================

SENSOR_VALUES = [1, 5, 7, 10, 12, 15, 17, 20]
SNR_VALUES = np.linspace(0.5, 10, 10)
NOISE_LEVEL_VALUES = comon.A / np.sqrt(SNR_VALUES)

RADIUS_VALUES = np.linspace(0.1, 1, 10)
SDN_VALUES = comon.A / np.sqrt(np.array(SNR_VALUES))
PHI_VALUES = np.linspace(
    0, 2 * np.pi, 18, endpoint=True
)  # Для построения пространства ошибок
FREQ_VALUES = np.linspace(1, 100, 25)
# НА ДАННЫЙ МОМЕНТ ОТНОШЕНИЕ АЛЬФА ПОД ВОПРОСОМ, НУЖНО ЛИ ИМЕННО ЕГО ИССЛЕДОВАТЬ
# ПОЭТОМУ Я РЕШИЛ ПОКА УБРАТЬ АЛЬФА-ЗАВИСИМОСТЬ
# ALPHA_VALUES = np.arange(10,20,1)
# ALPHA_RMS_VALUES = np.arange(10,20,1)


# ========== КОНФИГУРАЦИЯ =======
# ================================


def create_parameters_config() -> dict:
    """Создание конфигурации"""
    comons = comon.init_comon_params()

    TIME_VECTOR = np.arange(comons["N"]) * comons["dt"]
    FREQ_VECTOR = np.fft.fftshift(np.fft.fftfreq(comons["N"], d=1 / comons["fs"]))
    PHI_VECTOR = np.linspace(0, 2 * np.pi, comons["amount_phi"], endpoint=False)

    return {
        "time_vector": TIME_VECTOR,
        "freq_vector": FREQ_VECTOR,
        "phi_vector": PHI_VECTOR,
        "main_rng": np.random.default_rng(comons["main_seed"]),
        **comons
        # "alpha": comon.ALPHA,
        # "alpha_rms": comon.RMS_ALPHA,
    }

# ========== ИНИЦИАЛИЗАЦИЯ =======
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


def shake_rng(config_parametrs: dict) -> dict:
    """Случайное значение генератора"""
    import copy

    new_config = copy.deepcopy(config_parametrs)
    new_config["main_seed"] = None
    new_config["main_rng"] = np.random.default_rng(new_config["main_seed"])
    return new_config
