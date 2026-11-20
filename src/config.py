import numpy as np

def init_comon_params():
    # ====== ПАРАМЕТРЫ МОДЕЛИ ======
    # =====================================

    N = 10000  # КОЛИЧЕСТВО ОТСЧЁТОВ
    FS = 8800  # ЧАСТОТА ДИСКРЕТИЗАЦИИ

    DT = 1 / FS  # ШАГ ДИСКРЕТИЗАЦИИ
    DF = FS / N  # ШАГ ПО ЧАСТОНОЙ ОСИ

    GLOBAL_SEED = 1  # НАЧАЛЬНОЕ СОСТОЯНИЕ ГЕНЕРАТОРА СЛУЧАЙНЫХ ЧИСЕЛ

    DURATION_ALL = (N - 1) * DT  # ДЛИТЕЛЬНОСТЬ НА ВСЕЙ ОСИ ВРЕМЕНИ
    SPEED_ON_SOUND = 343.26  # СКОРОСТЬ ЗВУКА


    # ====== ПАРАМЕТРЫ КОНФИГУРАЦИИ ======
    # =====================================

    REALISATION_COUNT =  500 # КОЛИЧЕСТВО РЕАЛИЗАЦИЙ ШУМА
    M = 3  # КОЛИЧЕСТВО ДАТЧИКОВ
    SNR = 0.5  # ОТНОШЕНИЕ СИГНАЛ/ШУМ
    BETTA_PULSE = 0.05  # ДЛИТЕЛЬНОСТЬ ИМПУЛЬСНОГО СИГНАЛА
    F_GARMONIC =40# ЦЕНТРАЛЬНАЯ ЧАСТОТА ГАРМОНИЧЕСКОГО СИГНАЛА
    CENTER_PULSE = DURATION_ALL / 2  # ЦЕНТР ИМПУЛЬСНОГО СИГНАЛА

    A = 0.1  # АМПЛИТУДА СИГНАЛА
    LORENTZ_P_MAX = 0.1 # параметр импульса
    PHI_STEP = 0.001  # Шаг поиска угла 0.0003
    K = 0.5  # коэффицент для полосы решетки

    RADIUS = 1  # РАДИУС РЕШЁТКИ АВП

    TARGET_PHI = np.pi / 3  # АЗИМУТ ПОД КОТОРЫМ ПРИХОДИТ ИСГНАЛ (ТО ЧТО ОЦЕНИВАЕМ)
    AMOUNT_PHI = int(2 * np.pi / PHI_STEP)  # Количество значений угла
    CONST_RADIAN = (np.pi / 180) ** 2
    return {
            "dt": DT,
            "df": DF,
            "snr": SNR,
            "M": M,
            "duration_all": DURATION_ALL,
            "N": N,
            "fs": FS,
            "R": RADIUS,
            "f0": F_GARMONIC,
            "A": A,
            "p_max": LORENTZ_P_MAX,
            "c": SPEED_ON_SOUND,
            "duration_pulse": BETTA_PULSE,
            "realisation_count": REALISATION_COUNT,
            "target_phi": TARGET_PHI,
            "main_seed": GLOBAL_SEED,
            "center_pulse": CENTER_PULSE,
            "amount_phi": AMOUNT_PHI,
            "const_radian": CONST_RADIAN,
            "k": K,
            "fig_size": (14, 6),
        }

# ALPHA = 10
# RMS_ALPHA = 10

# ========== КОНФИГУРАЦИЯ =======
# ================================


def create_parameters_config() -> dict:
    """Создание конфигурации"""
    comons = init_comon_params()

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
    PHI_VALUES = np.linspace(0, 2 * np.pi, 9, endpoint=True)
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
        **comons,
    }


# ========== ИНИЦИАЛИЗАЦИЯ =======
# ========================


def init_rng(main_seed: int = init_comon_params()["main_seed"]):
    """Инциализация стартового конфига"""

    parametrs = create_parameters_config()
    parametrs["main_rng"] = np.random.default_rng(main_seed)
    parametrs["main_seed"] = main_seed
    return parametrs


def restart_rng(configs: dict) -> dict:
    """Сброс генератора"""
    import copy

    new_config = copy.deepcopy(configs)
    new_config["main_rng"] = np.random.default_rng(new_config["main_seed"])
    return new_config


def shake_rng(configs: dict) -> dict:
    """Случайное значение генератора"""
    import copy

    new_config = copy.deepcopy(configs)
    new_config["main_seed"] = None
    new_config["main_rng"] = np.random.default_rng(new_config["main_seed"])
    return new_config
