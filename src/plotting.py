import numpy as np
from matplotlib import pyplot as plt

from src.configs import config

PI_AXIS = {
    "ticks": np.arange(9) * np.pi / 4,
    "labels": [
        "0",
        r"$\frac{\pi}{4}$",
        r"$\frac{\pi}{2}$",
        r"$\frac{3\pi}{4}$",
        r"$\pi$",
        r"$\frac{5\pi}{4}$",
        r"$\frac{3\pi}{2}$",
        r"$\frac{7\pi}{4}$",
        r"$2\pi$",
    ],
}
COLORS = ("red", "green", "blue")
LINES = ("-", "--", "-.", ":")
MARKERS = ["o", "s", "D", "x"]
LABELS_DICT = {
    "snr": "SNR",
    "M": "sensor count",
    "R": "array radius",
    "target_phi": r"source azimuth $\varphi_0$",
    "f0": r"signal frequency $f_0$",
    # "alpha": r"$\alpha = \frac{\lambda}{2R} $",
}
XLABELS_DICT = {
    "snr": "SNR (linear)",
    "M": "Sensor count $M$",
    "R": "Array radius $R$, m",
    "target_phi": r"Source azimuth $\varphi_0$, deg",
    "f0": r"Signal frequency $f_0$, Hz",
    # "alpha": r"$\alpha = \frac{\lambda}{2R} $",
}
NAMING_DICT = {
    "snr": "SNR",
    "M": "M",
    "R": "R",
    "target_phi": r"$\varphi_0$",
    "f0": "f0",
    # "alpha": r"$\alpha$",
}
TYPE_SIGNALS = ["garmonic", "pulse"]


def plot_mean_vs_param(
    dict_values: dict,
    config_params: dict,
    parametr_name: str,
    parametr_values: np.ndarray | list,
    delta_time: float = 0,
    xlim: tuple | None = None,
    ylim: tuple | None = None,
    y_label: str = r"$\mathbb{E}[\varepsilon]$",
    y_size: str = ", deg",
    type_signal: str | None = None,
    save: bool = False,
):
    """График среднего значения ошибки оценки для нескольких методов."""

    fig, ax = plt.subplots(1, 1, figsize=(14, 11))
    fig.subplots_adjust(top=0.88, bottom=0.45)
    if parametr_name == "target_phi":
        parametr_values = np.degrees(parametr_values)

    info_for_plots = []
    for idx, (method, values) in enumerate(dict_values.items()):
        values = np.asarray(values) * (180 / np.pi)
        info_for_plots.append(
            {
                "method": method,
                "stats": {
                    "Max": np.max(values),
                    "Min": np.min(values),
                    "Mean": np.mean(values),
                },
            }
        )
        ax.plot(
            parametr_values,
            values,
            color=COLORS[idx % len(COLORS)],
            label=method,
            linestyle=LINES[idx % len(LINES)],
            linewidth=3,
            marker = MARKERS[idx % len(MARKERS)]
        )

    ax.set_xlabel(XLABELS_DICT[parametr_name], fontsize=18)
    ax.set_ylabel(y_label + y_size, fontsize=18)

    fig.suptitle(
        "Mean bearing error " + y_label + f" vs. {LABELS_DICT[parametr_name]}",
        y=0.94,
        va="center",
        fontfamily="Times New Roman",
        fontsize=22,
    )
    ax.grid(True)
    if ylim is not None:
        ax.set_ylim(
            [value * (180 / np.pi) if value is not None else None for value in ylim]
        )
    if xlim is not None:
        ax.set_xlim([value if value is not None else None for value in xlim])
    ax.legend(fontsize=15)
    # Параметры под графиком.
    methods = ", ".join(dict_values)
    info = ""
    if type_signal is not None:
        info += f"Signal type: {type_signal.replace('garmonic', 'harmonic')}\n"

    if type_signal == "garmonic":
        info += f"Signal frequency: {config_params['f0']} Hz\n"

    if parametr_name != "R":
        info += f"Array radius: {config_params['R']:.2f} m\n"
    if parametr_name != "M":
        info += f"Sensor count: {config_params['M']}\n"
    if parametr_name != "snr":
        info += f"SNR: {config_params['snr']} (linear)\n"
    info += (
        f"{NAMING_DICT[parametr_name]}: {parametr_values[0]:.2f} "
        f"to {parametr_values[-1]:.2f} ({len(parametr_values)} points)\n"
    )
    info += f"Search angles: {len(config_params['phi_vector'])}\n"
    info += f"Noise realizations: {config_params['realisation_count']}\n"
    info += f"Seed: {config_params['main_seed']}\n"
    info += f"Computation time: {delta_time:.2f} s"

    ax.text(
        0,
        -0.20,
        info,
        transform=ax.transAxes,
        fontsize=14,
        linespacing=1.5,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round", facecolor="none", alpha=1),
        clip_on=False,
    )
    info2 = ""
    for info_obj in info_for_plots:
        info2 += (
            info_obj["method"]
            + ":\n"
            + f"Max: {info_obj["stats"]["Max"]:.3f} deg\nMin: {info_obj["stats"]["Min"]:.3f} deg\nMean: {info_obj["stats"]["Mean"]:.3f} deg\n"
        )

    ax.text(
        0.5,
        -0.20,
        info2,
        transform=ax.transAxes,
        fontsize=14,
        linespacing=1.5,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round", facecolor="none", alpha=1),
        clip_on=False,
    )
    if save is True:
        plt.savefig(
            fname=f"attachment/images/report/mean_{parametr_name}_{config_params['realisation_count']}",
            bbox_inches="tight",
            dpi=300,
    )
    return fig, ax


def plot_variance_vs_param(
    dict_values: dict,
    config_params: dict,
    parametr_name: str,
    parametr_values: np.ndarray | list,
    delta_time: float = 0,
    xlim: tuple = None,
    ylim: tuple = None,
    y_label: str = r"$s_{\varepsilon}^{2}$",
    y_size: str = r", deg$^2$",
    type_signal: str = None,
    save: bool = False,
):
    """График дисперсии ошибки оценки для нескольких методов."""

    fig, ax = plt.subplots(1, 1, figsize=(14, 11))
    fig.subplots_adjust(top=0.88, bottom=0.45)
    if parametr_name == "target_phi":
        parametr_values = np.degrees(parametr_values)

    info_for_plots = []
    for idx, (method, values) in enumerate(dict_values.items()):
        values = np.asarray(values) * (180 / np.pi) ** 2
        info_for_plots.append(
            {
                "method": method,
                "stats": {
                    "Max": np.max(values),
                    "Min": np.min(values),
                    "Mean": np.mean(values),
                },
            }
        )
        ax.plot(
            parametr_values,
            values,
            color=COLORS[idx % len(COLORS)],
            label=method,
            linestyle=LINES[idx % len(LINES)],
            linewidth=3,
            marker = MARKERS[idx % len(MARKERS)]
        )

    ax.set_xlabel(XLABELS_DICT[parametr_name], fontsize=18)
    ax.set_ylabel(y_label + y_size, fontsize=18)

    fig.suptitle(
        "Bearing error variance " + y_label + f" vs. {LABELS_DICT[parametr_name]}",
        y=0.94,
        va="center",
        fontfamily="Times New Roman",
        fontsize=22,
    )
    ax.grid(True)
    if ylim is not None:
        ax.set_ylim(
            [
                value * (180 / np.pi) ** 2 if value is not None else None
                for value in ylim
            ]
        )
    if xlim is not None:
        ax.set_xlim([value if value is not None else None for value in xlim])
    ax.legend(fontsize=15)
    # Параметры под графиком.
    methods = ", ".join(dict_values)
    info = ""
    if type_signal is not None:
        info += f"Signal type: {type_signal.replace('garmonic', 'harmonic')}\n"

    if type_signal == "garmonic":
        info += f"Signal frequency: {config_params['f0']} Hz\n"

    if parametr_name != "R":
        info += f"Array radius: {config_params['R']:.2f} m\n"
    if parametr_name != "M":
        info += f"Sensor count: {config_params['M']}\n"
    if parametr_name != "snr":
        info += f"SNR: {config_params['snr']} (linear)\n"
    info += (
        f"{NAMING_DICT[parametr_name]}: {parametr_values[0]:.2f} "
        f"to {parametr_values[-1]:.2f} ({len(parametr_values)} points)\n"
    )
    info += f"Search angles: {len(config_params['phi_vector'])}\n"
    info += f"Noise realizations: {config_params['realisation_count']}\n"
    info += f"Seed: {config_params['main_seed']}\n"
    info += f"Computation time: {delta_time:.2f} s"

    ax.text(
        0,
        -0.20,
        info,
        transform=ax.transAxes,
        fontsize=14,
        linespacing=1.5,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round", facecolor="none", alpha=1),  # noqa: C408
        clip_on=False,
    )
    info2 = ""
    for info_obj in info_for_plots:
        info2 += (
            info_obj["method"]
            + ":\n"
            + f"Max: {info_obj["stats"]["Max"]:.3f} deg²\nMin: {info_obj["stats"]["Min"]:.3f} deg²\nMean: {info_obj["stats"]["Mean"]:.3f} deg²\n"
        )

    ax.text(
        0.5,
        -0.20,
        info2,
        transform=ax.transAxes,
        fontsize=14,
        linespacing=1.5,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round", facecolor="none", alpha=1),
        clip_on=False,
    )
    if save is True:
        plt.savefig(
        fname=f"attachment/images/report/var_{parametr_name}_{config_params['realisation_count']}",
        bbox_inches="tight",
        dpi=300,
    )
    return fig, ax


def create_and_save_table(rows: list, columns: list, filename: str, save: bool = True):
    """Таблица значений параметров графика"""
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.axis("off")
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        colWidths=[0.55, 0.25, 0.20],
        cellLoc="center",
        loc="center",
    )
    for cell in table.get_celld().values():
        cell.get_text().set_fontfamily("Times New Roman")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)  # Масштаб ячеек по ширине и высоте

    fig.tight_layout()
    fig.canvas.draw()

    bbox = table.get_window_extent(fig.canvas.get_renderer())
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    if save is False:
        fig.savefig(
            filename, bbox_inches=bbox, pad_inches=0, dpi=300, facecolor="white"
        )

    plt.show()


def create_config_table(
    config_params: np.ndarray,
):
    """Таблица значений параметров графика"""

    def round_n(number, k):
        """Округление числа до n значящих цифр"""
        return round(number, int(np.log10(1 / number)) + k)

    columns = ["Parameter", "Value"]
    rows = [
        [key, round_n(value, 2)]
        for key, value in sorted(config_params.items())
        if isinstance(value, (int, float, np.integer, np.floating))
        and not isinstance(value, (bool, np.bool_))
    ]

    fig, ax = plt.subplots(figsize=(8, max(2, 0.35 * (len(rows) + 1))))
    ax.axis("off")
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        colWidths=[0.55, 0.45],
        cellLoc="center",
        bbox=[0, 0, 1, 1],
    )
    for cell in table.get_celld().values():
        cell.get_text().set_fontfamily("Times New Roman")

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)  # Масштаб ячеек по ширине и высоте

    fig.tight_layout()
    fig.canvas.draw()

    bbox = table.get_window_extent(fig.canvas.get_renderer())
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    plt.show()


def show_geometry_avp(configs: dict):
    """Построение геометрии акустической векторной решётки."""

    from src.functions import get_gamma_array, get_tau_array

    r = configs["R"]

    x = r * np.sin(2 * np.pi * configs["time_vector"])
    y = r * np.cos(2 * np.pi * configs["time_vector"])

    gamma_arr = get_gamma_array(configs["M"])
    tau_arr = list(get_tau_array(configs) * 1e3)  # Миллисекунды.
    tau_mks = [round(float(tau), 1) for tau in tau_arr]

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))

    ax.plot(x, y, linestyle="-", color="black")
    ax.grid(False)
    ax.set_xlim(-1.65 * r, 1.65 * r)
    ax.set_ylim(-1.65 * r, 1.65 * r)

    ax.axline((0, 0), (1, 0), color="black", linestyle="-")
    ax.plot(0, 0, marker="o", markersize=10, color="black")

    d = r / 12
    for idx, value in enumerate(gamma_arr):

        x1 = r * np.cos(value)
        y1 = r * np.sin(value)
        ax.plot(x1, y1, marker="o", markersize=10, color="blue")
        ax.set_title("AVS array geometry", fontsize=15)
        plt.text(
            x1 + d / 2, y1 + d / 2, rf"$M_{{{idx+1}}}$", fontsize=15, color="black"
        )
        v = int(value * (180 / np.pi))
        plt.text(
            x1 + 2.8 * d,
            y1 + 1.5 * d,
            rf"$\gamma_{idx+1}$ = ${v}^\circ$"
            + "\n"
            + rf"$\tau_{idx+1}$ = {tau_mks[idx]} ms",
            fontsize=9,
            color="black",
            bbox={
                "facecolor": "white",  # Белый цвет фона
                "edgecolor": "black",  # Без рамки вокруг текста (или 'black' для рамки)
                "boxstyle": "round,pad=0.5",  # Скругленные углы и отступы вокруг текста
                "alpha": 0.65,  # Прозрачность фона (1.0 — полностью непрозрачный)
            },
        )

    x2 = r * np.cos(configs["target_phi"])
    y2 = r * np.sin(configs["target_phi"])
    x3 = r * np.cos(3.3)
    y3 = r * np.sin(3.3)
    x4 = 0.5 * r * np.cos(3.3)
    y4 = 0.5 * r * np.sin(3.3) - d
    plt.text(0, -0.15 * r, "O", fontsize=20, color="black")
    ax.plot(
        x2 * 1.6,
        y2 * 1.6,
        marker="o",
        markersize=15,
        color="black",
    )
    ax.text(
        x2 * 1.6,
        y2 * 1.52 + 2 * d,
        rf"Source (${(configs["target_phi"]*180/np.pi):.0f}^\circ$)",
        fontsize=14,
        color="black",
    )
    ax.plot([0, x2 * 1.6], [0, y2 * 1.6], color="purple", linestyle="--", linewidth=2)
    ax.plot([0, x3], [0, y3], color="black", linestyle="-", linewidth=1.5)
    ax.plot(x3, y3, marker="o", markersize=8, color="black")
    ax.text(x4, y4, f"R = {r:.1f}", fontsize=12, color="black")
    ax.set_ylim(-1.7 * r, 1.7 * r)
    plt.gca().set_aspect("equal", adjustable="box")
