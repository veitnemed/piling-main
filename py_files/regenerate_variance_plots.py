"""Recalculate and save the variance plots used by report.ipynb.

Run from the repository root: python -m py_files.regenerate_variance_plots
Existing images are preserved; updated plots go to plots_image/updated.
"""

from pathlib import Path
import sys
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
import numpy as np

from py_files import config as cfg
from py_files.experiment_stats import var_vs_params
from py_files.functions import get_barlet_values, get_cap_values
from py_files.plot_scrip import plot_variance_vs_param


OUTPUT = Path(__file__).resolve().parents[1] / "plots_image" / "updated"
SEED = 20261019


def generate_one(name, parameter, values):
    started = perf_counter()
    curves = {}
    for label, energy in (("Бартлетт", get_barlet_values),
                          ("Кейпон", get_cap_values)):
        params = cfg.CONFIG_PARAMETRS.copy()
        params["main_rng"] = np.random.default_rng(SEED)
        curves[label] = var_vs_params(
            config_params=params,
            energy_func=energy,
            parametr_name=parameter,
            parametr_values=values,
        )

    if name == "azimuth":
        y_limits = (0, 3e-4)
    elif name == "alpha_1_10":
        y_limits = (0, 140e-5)
    elif name == "alpha_0_1_1":
        y_limits = (0, 4)
    else:
        y_limits = (0, 1.02 * max(max(curve) for curve in curves.values()))

    fig, _ = plot_variance_vs_param(
        dict_values=curves,
        config_params=cfg.CONFIG_PARAMETRS,
        parametr_name="phis" if parameter == "target_phi" else parameter,
        parametr_values=values,
        ylim=y_limits,
        delta_time=perf_counter() - started,
        save_path=OUTPUT / f"variance_{name}.png",
    )
    plt.close(fig)
    print(f"Saved {OUTPUT / f'variance_{name}.png'}", flush=True)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = [
        ("azimuth", "target_phi", cfg.PHI_VALUES),
        ("snr", "snr", np.linspace(0.1, 1, 10)),
        ("radius", "R", np.linspace(1, 10, 10)),
        ("sensors", "M", cfg.SENSOR_VALUES),
        ("alpha_1_10", "alpha", np.linspace(1, 10, 20)),
        ("alpha_0_1_1", "alpha", np.linspace(0.1, 1, 20)),
    ]
    selected = set(sys.argv[1:])
    for name, parameter, values in cases:
        if not selected or name in selected:
            generate_one(name, parameter, values)


if __name__ == "__main__":
    main()
