import py_files.config as cfg
from py_files.functions import (get_avp_signals, get_sin_signal, get_noise)
import numpy as np

def some_avp_signals():
    config_parametrs = cfg.init_rng()
    p_t = get_sin_signal(cfg.t,cfg.f,cfg.A)
    signals1 = get_avp_signals(p_t, config_parametrs)

    config_parametrs1 = cfg.init_rng()
    signals2 = get_avp_signals(p_t, config_parametrs1)
    return all(np.array_equal(signals1[key], signals2[key]) for key in signals1)

def different_avp_signals():
    config_parametrs = cfg.init_rng(1)
    p_t = get_sin_signal(cfg.t,cfg.f,cfg.A)
    signals1 = get_avp_signals(p_t, config_parametrs)
    
    config_parametrs1 = cfg.init_rng(2)
    signals2 = get_avp_signals(p_t, config_parametrs1)
    return any(not np.array_equal(signals1[key], signals2[key]) for key in signals1)
if __name__ == "__main__":
    print(some_avp_signals())
    print(different_avp_signals())
