import src.configs.config as config
import src.pseudospectrum as pseudospectrum
import numpy as np
import scipy.signal as signal
import src.experement as experement
import src.signals as signals
import src.model as model


def test_some_avp_signals():
    config_parametrs = config.init_rng(42)
    config_parametrs1 = config.init_rng(42)
    p_t = signals.sinus(config_parametrs)
    e_t = signals.calculate_energy(p_t, config_parametrs["time_vector"])

    signals1 = model.avp_signals(p_t, config_parametrs, e_t)
    signals2 = model.avp_signals(p_t, config_parametrs1, e_t)
    assert all(np.array_equal(signals1[key], signals2[key]) for key in signals1)


def test_different_avp_signals():
    config_parametrs = config.init_rng(1)
    p_t = signals.sinus(config_parametrs)
    e_t = signals.calculate_energy(p_t, config_parametrs["time_vector"])
    signals1 = model.avp_signals(p_t, config_parametrs, e_t)

    config_parametrs1 = config.init_rng(2)
    signals2 = model.avp_signals(p_t, config_parametrs1, e_t)
    assert any(not np.array_equal(signals1[key], signals2[key]) for key in signals1)


def test_full_experiment():
    config_parametrs1 = config.init_rng()
    config_parametrs2 = config.init_rng()
    config_parametrs1["realisation_count"] = 3
    config_parametrs2["realisation_count"] = 3
    var_bartlett_vs_snr1 = experement.stat_vs_params(
        config_params=config_parametrs1,
        energy_func=pseudospectrum.approx_bartlett,
        signal_func=signals.sinus,
        parametr_name="snr",
        stiring_func=model.calculate_stiring_matrix,
        parametr_values=config_parametrs1["snr_values"],
    )

    var_bartlett_vs_snr2 = experement.stat_vs_params(
        config_params=config_parametrs2,
        energy_func=pseudospectrum.approx_bartlett,
        signal_func=signals.sinus,
        parametr_name="snr",
        stiring_func=model.calculate_stiring_matrix,
        parametr_values=config_parametrs2["snr_values"],
    )
    assert np.array_equal(var_bartlett_vs_snr1, var_bartlett_vs_snr2)


def test_equality_rng():
    general_seed = 42
    original = config.init_rng(general_seed)

    config1 = config.restart_rng(original)
    config2 = config.restart_rng(original)

    p_t1 = signals.sinus(config1)
    e_t1 = signals.calculate_energy(p_t1, config1["time_vector"])
    noise1 = signals.get_noise(config1, config1["main_rng"], e_t1)

    p_t2 = signals.sinus(config2)
    e_t2 = signals.calculate_energy(p_t2, config2["time_vector"])
    noise2 = signals.get_noise(config2, config2["main_rng"], e_t2)

    assert np.array_equal(noise1, noise2)


def test_hilbert_channel_matrix():
    config_parametrs = config.init_rng(42)
    config_parametrs["realisation_count"] = 1
    taus = model.tau_array(config_parametrs)
    channels = model.channel_matrix(config_parametrs, taus, signals.sinus)
    expected = model.covariation_matrix(
        signal.hilbert(channels.real, axis=1), config_parametrs["N"]
    )

    matrices = []

    def capture_matrix(W, dir_matrix):
        matrices.append(W)
        return np.zeros(len(dir_matrix))

    experement.stat_vs_params(
        config_params=config.init_rng(42),
        energy_func=capture_matrix,
        signal_func=signals.sinus,
        stiring_func=model.complex_stiring_matrix,
        parametr_name="realisation_count",
        parametr_values=[1],
        stat_func=np.mean,
        is_hilbert=True,
    )
    assert np.allclose(matrices[0], expected)
