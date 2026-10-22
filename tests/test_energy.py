import numpy as np
from py_files.config import T
import py_files.config as cfg
from py_files.functions import calculate_energy


def test_rectangular_pulse_energy():
    A = 2       # Амплитуда
    t_0 = T/2    # ЦЕНТР ИМПУЛЬСА (например, в точке t = 2)
    tau = T/10     # Полная длительность импульса (ширина)
    pulse = np.where((cfg.t>= t_0 - tau/2) & (cfg.t <= t_0 + tau/2), A, 0.0)
    x1 = calculate_energy(pulse, cfg.t)

    x2 = (A**2)*tau
    assert np.abs(x1-x2) < 1e-6
