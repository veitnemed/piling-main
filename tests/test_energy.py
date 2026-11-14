import numpy as np
import src.configs.config as config
import src.signals as signals


def test_rectangular_pulse_energy():
    """Сравнение энергии сигнала с аналитической формулой."""
    params = config.create_parameters_config()
    A = 2  # Амплитуда
    t_0 = params["duration_all"] / 2  # Центр импульса.
    tau = params["duration_all"] / 10  # Полная длительность импульса.
    pulse = np.where(
        (params["time_vector"] >= t_0 - tau / 2) & (params["time_vector"] <= t_0 + tau / 2),
        A,
        0.0,
    )
    x1 = signals.calculate_energy(pulse, params["time_vector"])

    x2 = (A**2) * tau
    assert np.abs(x1 - x2) < 1e-3
