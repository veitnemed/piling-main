import numpy as np
import src.configs.config as config
import src.signals as signals
import src.configs.comon as comon


def test_rectangular_pulse_energy():
    """Сравнение энергии сигнала с аналитической формулой."""
    A = 2  # Амплитуда
    t_0 = comon.DURATION_ALL / 2  # Центр импульса.
    tau = comon.DURATION_ALL / 10  # Полная длительность импульса.
    pulse = np.where(
        (config.TIME_VECTOR >= t_0 - tau / 2) & (config.TIME_VECTOR <= t_0 + tau / 2),
        A,
        0.0,
    )
    x1 = signals.calculate_energy(pulse, config.TIME_VECTOR)

    x2 = (A**2) * tau
    assert np.abs(x1 - x2) < 1e-3
