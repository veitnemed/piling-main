import pytest
import src.config as config
import src.pseudospectrum as pseudospectrum
import numpy as np
import src.experement as experement
import src.signals as signals
import src.model as model
import src.steerings as steerings

def test_raise_for_stat_vs_params():
    configs = config.init_rng()
    configs["realisation_count"] = 3
    with pytest.raises(KeyError):
        experement.stat_vs_params(
        config_params=configs,
        pseudospectrum_func=pseudospectrum.approx_bartlett,
        signal_func=signals.sinus,
        parametr_name="snr",
        stiring_func=steerings.calculate_stiring_matrix,
        parametr_values=configs["qwerty"],
    )

        