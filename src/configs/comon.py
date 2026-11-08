import numpy as np

# ====== parametrs МОДЕЛИ ======
# =====================================

N = 10000  # КОЛИЧЕСТВО ОТСЧЁТОВ
FS = 8800  # frequency ДИСКРЕТИЗАЦИИ

DT = 1 / FS  # ШАГ ДИСКРЕТИЗАЦИИ
DF = FS / N  # ШАГ ПО ЧАСТОНОЙ ОСИ

GLOBAL_SEED = 1  # НАЧАЛЬНОЕ СОСТОЯНИЕ ГЕНЕРАТОРА СЛУЧАЙНЫХ ЧИСЕЛ

DURATION_ALL = (N - 1) * DT  # ДЛИТЕЛЬНОСТЬ pulseА
SPEED_ON_SOUND = 343.26  # standart divationРОСТЬ ЗВУКА


# ====== parametrs КОНФИГУРАЦИИИ ======
# =====================================

REALISATION_COUNT = 50  # КОЛИЧЕСТВО РЕАЛИЗАЦИЙ noise
M = 3  # КОЛИЧЕСТВО SensorОВ
SNR = 2  # ОТНОШЕНИЕ signal/noise
BETTA_PULSE = 0.02  # ДЛИТЕЛЬНОСТЬ pulseНОГО signalА
F_GARMONIC = 10  # centerАЛЬНАЯfrequency ГАРМОНИЧЕstandart divationГО signalА
CENTER_PULSE = DURATION_ALL / 2  # center pulseного signalа

A = 1  # АМПЛИТУДА signalА

PHI_STEP = 0.001  # Шаг поиска угла 0.0003
K = 0.5  # коэффицент для полосы решетки

RADIUS = 0.4  # Radius array AVS

TARGET_PHI = np.pi / 3  # АЗИМУТ ПОД КОТОРЫМ ПРИХОДИТ ИСГНАЛ (ТО ЧТО ОЦЕНИВАЕМ)
AMOUNT_PHI = int(2 * np.pi / PHI_STEP)  # Количество значений угла
CONST_RADIAN = (np.pi / 180) ** 2

FIG_SIZE = (14, 6)
# ALPHA = 10
# RMS_ALPHA = 10
