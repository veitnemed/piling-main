"""Plots for the AVP bearing estimation experiments."""

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter


PI_AXIS = {
    "ticks": np.arange(9) * np.pi / 4,
    "labels": ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$",
               r"$5\pi/4$", r"$3\pi/2$", r"$7\pi/4$", r"$2\pi$"],
}
COLORS = ["red", "green", "blue"]
LINES = ["-", "--", "-.", ":"]
LABELS_DICT = {
    "snr": "отношения сигнал/шум",
    "M": "количества датчиков",
    "R": "радиуса решётки",
    "alpha": r"$\alpha = \lambda/(2R)$",
    "phis": "истинного азимута",
}
XLABELS_DICT = {
    "snr": "С/Ш",
    "M": "Количество датчиков M, шт.",
    "R": "Радиус решётки R, м",
    "alpha": r"$\alpha = \lambda/(2R)$",
    "phis": r"Истинный азимут $\varphi_0$, рад",
}
NAMING_DICT = {
    "snr": "С/Ш",
    "M": "M",
    "R": "R",
    "alpha": r"$\alpha$",
    "phis": r"$\varphi_0$",
}


def plot_variance_vs_param(
    dict_values: dict,
    config_params: dict,
    parametr_name: str,
    ylim: tuple | None,
    parametr_values: np.ndarray | list,
    delta_time: float = 0,
    y_label: str = r"$s_{\varepsilon}^{2}$",
    y_size: str = r", рад$^2$",
    save_path: str | Path | None = None,
):
    """Plot estimation variance and optionally save a sharp PNG.

    ``ylim=None`` selects a readable vertical range from the data. An explicit
    ``ylim`` is respected for comparisons with a fixed scale.
    """
    if parametr_name not in XLABELS_DICT:
        raise ValueError(f"Неизвестный параметр: {parametr_name}")
    if not dict_values:
        raise ValueError("Нет данных для построения графика")

    x = np.asarray(parametr_values, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("parametr_values должен быть непустым конечным вектором")
    for method, values in dict_values.items():
        y = np.asarray(values, dtype=float)
        if y.shape != x.shape or not np.all(np.isfinite(y)):
            raise ValueError(f"Некорректные значения метода {method}")

    style = {
        "font.family": "Times New Roman",
        "font.size": 14,
        "mathtext.fontset": "stix",
        "axes.titlesize": 16,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "savefig.dpi": 220,
    }
    with plt.rc_context(style):
        fig = plt.figure(figsize=(9, 5.5), layout="constrained")
        grid = fig.add_gridspec(2, 1, height_ratios=(5, 0.9))
        ax = fig.add_subplot(grid[0])
        info_ax = fig.add_subplot(grid[1])

        for index, (method, values) in enumerate(dict_values.items()):
            ax.plot(x, values, color=COLORS[index % len(COLORS)],
                    linestyle=LINES[index % len(LINES)], linewidth=2.3,
                    marker="o", markersize=4, label=method)

        ax.set_xlabel(XLABELS_DICT[parametr_name])
        ax.set_ylabel(y_label + y_size)
        ax.set_title("Зависимость дисперсии оценки от " + LABELS_DICT[parametr_name])
        ax.grid(True, which="major", color="0.75", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.legend(loc="best", fontsize=12, framealpha=0.95)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_powerlimits((-3, 3))
        ax.yaxis.set_major_formatter(formatter)

        if parametr_name == "phis":
            ax.set_xticks(PI_AXIS["ticks"], PI_AXIS["labels"])
            ax.set_xlim(0, 2 * np.pi)
        elif parametr_name == "M":
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        if ylim is not None:
            ax.set_ylim(ylim)
            above = False
            for index, values in enumerate(dict_values.values()):
                y = np.asarray(values, dtype=float)
                outside = y > ylim[1]
                if np.any(outside):
                    above = True
                    ax.scatter(x[outside], np.full(np.count_nonzero(outside),
                                                  ylim[1] * 0.97),
                               marker="^", s=55, color=COLORS[index % len(COLORS)],
                               edgecolors="black", linewidths=0.5, zorder=5)
            if above:
                ax.text(0.36, 0.95, "▲ Значения выше выбранной шкалы",
                        transform=ax.transAxes, ha="left", va="top", fontsize=10,
                        bbox={"facecolor": "white", "edgecolor": "0.7"})
        else:
            y_min = min(float(np.min(v)) for v in dict_values.values())
            y_max = max(float(np.max(v)) for v in dict_values.values())
            spread = y_max - y_min
            if spread > 0:
                margin = 0.12 * spread
                ax.set_ylim(max(0, y_min - margin), y_max + margin)
            else:
                ax.set_ylim(0, y_max * 1.12 if y_max > 0 else 1)

        details = [f"f = {config_params['f0']} Гц"]
        if parametr_name != "R":
            details.append(f"R = {config_params['R']:.2f} м")
        if parametr_name != "M":
            details.append(f"M = {config_params['M']}")
        if parametr_name != "snr":
            details.append(f"С/Ш = {config_params['snr']}")
        details.append(f"K = {config_params['K']}")
        details.append(f"t = {delta_time:.2f} с")
        range_text = (f"{NAMING_DICT[parametr_name]}: "
                      f"{x[0]:.2f}–{x[-1]:.2f} ({x.size} точек)")
        info_ax.axis("off")
        info_ax.text(0.5, 0.5, "   ·   ".join(details) + "\n" + range_text,
                     transform=info_ax.transAxes, ha="center", va="center",
                     fontsize=11, bbox={"boxstyle": "round,pad=0.45",
                                        "facecolor": "#f4e2bd", "edgecolor": "0.5"})

        if save_path is not None:
            path = Path(save_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
        return fig, ax
