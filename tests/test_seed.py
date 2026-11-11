import src.configs.config as config
from src.pseudospectrum import (
    approx_capon,
    approx_bartlett,
)
import numpy as np
from src.experement import stat_vs_params
import src.signals as signals
import src.model as model


def test_some_avp_signals():
    config_parametrs = config.init_rng(42)
    config_parametrs1 = config.init_rng(42)
    p_t = signals.sinus(config_parametrs)
    e_t = signals.calculate_energy(p_t, config.TIME_VECTOR)

    signals1 = model.avp_signals(p_t, config_parametrs, e_t)
    signals2 = model.avp_signals(p_t, config_parametrs1, e_t)
    assert all(np.array_equal(signals1[key], signals2[key]) for key in signals1)


def test_different_avp_signals():
    config_parametrs = config.init_rng(1)
    p_t = signals.sinus(config_parametrs)
    e_t = signals.calculate_energy(p_t, config.TIME_VECTOR)
    signals1 = model.avp_signals(p_t, config_parametrs, e_t)

    config_parametrs1 = config.init_rng(2)
    signals2 = model.avp_signals(p_t, config_parametrs1, e_t)
    assert any(not np.array_equal(signals1[key], signals2[key]) for key in signals1)


def test_full_experiment():
    config_parametrs1 = config.init_rng()
    config_parametrs2 = config.init_rng()
    config_parametrs1["realisation_count"] = 3
    config_parametrs2["realisation_count"] = 3
    var_bartlett_vs_snr1 = stat_vs_params(
        config_params=config_parametrs1,
        energy_func=approx_bartlett,
        signal_func=signals.sinus,
        parametr_name="snr",
        stiring_func=model.calculate_stiring_matrix,
        parametr_values=config.SNR_VALUES,
    )

    var_bartlett_vs_snr2 = stat_vs_params(
        config_params=config_parametrs2,
        energy_func=approx_bartlett,
        signal_func=signals.sinus,
        parametr_name="snr",
        stiring_func=model.calculate_stiring_matrix,
        parametr_values=config.SNR_VALUES,
    )
    assert np.array_equal(var_bartlett_vs_snr1, var_bartlett_vs_snr2)


def test_equality_rng():
    general_seed = 42
    original = config.init_rng(general_seed)

    config1 = config.restart_rng(original)
    config2 = config.restart_rng(original)

    p_t1 = signals.sinus(config1)
    e_t1 = signals.calculate_energy(p_t1, config.TIME_VECTOR)
    noise1 = signals.get_noise(config1, config1["main_rng"], e_t1)

    p_t2 = signals.sinus(config2)
    e_t2 = signals.calculate_energy(p_t2, config.TIME_VECTOR)
    noise2 = signals.get_noise(config2, config2["main_rng"], e_t2)

    assert np.array_equal(noise1, noise2)
