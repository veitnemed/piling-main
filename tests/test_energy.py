import numpy as np
import src.configs.config as cfg
import src.spectrum as spectrum
from src.functions import calculate_energy
import src.configs.comon as comon


def test_rectangular_pulse_energy():
    """Сравнение энергии сигнала с аналитической формулой."""
    A = 2  # Амплитуда
    t_0 = comon.DURATION_ALL / 2  # Центр импульса.
    tau = comon.DURATION_ALL / 10  # Полная длительность импульса.
    pulse = np.where(
        (cfg.TIME_VECTOR >= t_0 - tau / 2) & (cfg.TIME_VECTOR <= t_0 + tau / 2), A, 0.0
    )
    x1 = calculate_energy(pulse, cfg.TIME_VECTOR)

    x2 = (A**2) * tau
    assert np.abs(x1 - x2) < 1e-3
