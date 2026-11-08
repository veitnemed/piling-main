import src.configs.config as cfg
from src.functions import (
    get_avp_signals,
    get_sin_signal,
    calculate_capon_values,
    calculate_bartlett_values,
    calculate_energy,
    get_impulse_signal,
    get_noise,
    calculate_stiring_matrix,
)
import numpy as np
from src.experiments import stat_vs_params


def test_some_avp_signals():
    config_parametrs = cfg.init_rng(42)
    config_parametrs1 = cfg.init_rng(42)
    p_t = get_sin_signal(config_parametrs)
    e_t = calculate_energy(p_t, cfg.TIME_VECTOR)

    signals1 = get_avp_signals(p_t, config_parametrs, e_t)
    signals2 = get_avp_signals(p_t, config_parametrs1, e_t)
    assert all(np.array_equal(signals1[key], signals2[key]) for key in signals1)


def test_different_avp_signals():
    config_parametrs = cfg.init_rng(1)
    p_t = get_sin_signal(config_parametrs)
    e_t = calculate_energy(p_t, cfg.TIME_VECTOR)
    signals1 = get_avp_signals(p_t, config_parametrs, e_t)

    config_parametrs1 = cfg.init_rng(2)
    signals2 = get_avp_signals(p_t, config_parametrs1, e_t)
    assert any(not np.array_equal(signals1[key], signals2[key]) for key in signals1)


def test_full_experiment():
    config_parametrs1 = cfg.init_rng()
    config_parametrs2 = cfg.init_rng()
    config_parametrs1["realisation_count"] = 3
    config_parametrs2["realisation_count"] = 3
    var_bartlett_vs_snr1 = stat_vs_params(
        config_params=config_parametrs1,
        energy_func=calculate_bartlett_values,
        signal_func=get_sin_signal,
        parametr_name="snr",
        stiring_func=calculate_stiring_matrix,
        parametr_values=cfg.SNR_VALUES)
        

    var_bartlett_vs_snr2 = stat_vs_params(
        config_params=config_parametrs2,
        energy_func=calculate_bartlett_values,
        signal_func=get_sin_signal,
        parametr_name="snr",
        stiring_func=calculate_stiring_matrix,
        parametr_values=cfg.SNR_VALUES,
    )
    assert np.array_equal(var_bartlett_vs_snr1, var_bartlett_vs_snr2)


def test_equality_rng():
    general_seed = 42
    original = cfg.init_rng(general_seed)

    config1 = cfg.restart_rng(original)
    config2 = cfg.restart_rng(original)

    p_t1 = get_sin_signal(config1)
    e_t1 = calculate_energy(p_t1, cfg.TIME_VECTOR)
    noise1 = get_noise(config1, config1["main_rng"], e_t1)

    p_t2 = get_sin_signal(config2)
    e_t2 = calculate_energy(p_t2, cfg.TIME_VECTOR)
    noise2 = get_noise(config2, config2["main_rng"], e_t2)

    assert np.array_equal(noise1, noise2)
