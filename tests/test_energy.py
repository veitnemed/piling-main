import numpy as np
from py_files.configs.config import DURATION_ALL
import py_files.configs.config as cfg
from py_files.functions import calculate_energy
import py_files.configs.comon as comon

def test_rectangular_pulse_energy():
    A = 2       # Амплитуда
    t_0 = comon.DURATION_ALL/2    # ЦЕНТР ИМПУЛЬСА (например, в точке t = 2)
    tau = comon.DURATION_ALL/10     # Полная длительность импульса (ширина)
    pulse = np.where((cfg.TIME_VECTOR>= t_0 - tau/2) & (cfg.TIME_VECTOR <= t_0 + tau/2), A, 0.0)
    x1 = calculate_energy(pulse, cfg.TIME_VECTOR)

    x2 = (A**2)*tau
    assert np.abs(x1-x2) < 1e-3
