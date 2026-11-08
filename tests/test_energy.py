import numpy as np
import src.configs.config as cfg
from src.functions import calculate_energy
import src.configs.comon as comon


def test_rectangular_pulse_energy():
    """Тестируем энергию signalа, проверяем с аналитичеstandart divationй формулой"""
    A = 2  # Амплитуда
    t_0 = comon.DURATION_ALL / 2  # center pulseА (например, в точке t = 2)
    tau = comon.DURATION_ALL / 10  # Полная длительность pulseа (ширина)
    pulse = np.where(
        (cfg.TIME_VECTOR >= t_0 - tau / 2) & (cfg.TIME_VECTOR <= t_0 + tau / 2), A, 0.0
    )
    x1 = calculate_energy(pulse, cfg.TIME_VECTOR)

    x2 = (A**2) * tau
    assert np.abs(x1 - x2) < 1e-3
