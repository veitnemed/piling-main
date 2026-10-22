import py_files.config as cfg
from py_files.functions import (get_avp_signals, get_sin_signal, get_cap_values, get_barlet_values, calculate_energy)
import numpy as np
from py_files.experiment_stats import (var_vs_params, )

def test_some_avp_signals():
    config_parametrs = cfg.init_rng(42)
    config_parametrs1 = cfg.init_rng(42)
    p_t = get_sin_signal(cfg.time_vector,cfg.f,cfg.A)
    e_t = calculate_energy(p_t,cfg.time_vector)
    
    signals1 = get_avp_signals(p_t, config_parametrs,e_t)
    signals2 = get_avp_signals(p_t, config_parametrs1, e_t)
    assert all(np.array_equal(signals1[key], signals2[key]) for key in signals1)

def test_different_avp_signals():
    config_parametrs = cfg.init_rng(1)
    p_t = get_sin_signal(cfg.time_vector,cfg.f,cfg.A)
    e_t = calculate_energy(p_t,cfg.time_vector)
    signals1 = get_avp_signals(p_t, config_parametrs,e_t)
    
    config_parametrs1 = cfg.init_rng(2)
    signals2 = get_avp_signals(p_t, config_parametrs1,e_t)
    assert any(not np.array_equal(signals1[key], signals2[key]) for key in signals1)
    

def test_full_experiment():
    config_parametrs1 = cfg.init_rng()
    config_parametrs2 = cfg.init_rng()
    config_parametrs1["realisation_count"] = 3
    config_parametrs2["realisation_count"] = 3
    var_barlett_vs_snr1 = var_vs_params(config_params=config_parametrs1,
                                   energy_func=get_barlet_values,
                                   parametr_name = "snr",
                                   parametr_values = cfg.SNR_VALUES,
                                   )
    var_barlett_vs_snr2 = var_vs_params(config_params=config_parametrs2,
                                       energy_func=get_barlet_values,
                                       parametr_name = "snr",
                                       parametr_values = cfg.SNR_VALUES,
                                       )
    assert np.array_equal(var_barlett_vs_snr1, var_barlett_vs_snr2)
    
    