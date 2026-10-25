import numpy as np
from matplotlib import pyplot as plt


PI_AXIS = { "ticks": np.arange(9) * np.pi / 4,
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
                ]
        
    }
COLORS = ["red", "green", "blue"]
LINES = ["-", "--", "-.", ":"]
LABELS_DICT = {
    "snr": "SNR (c/ш)",
    "M": "количества датчиков",
    "R": "радиуса решетки",
    "alpha": r"$\alpha = \frac{\lambda}{2R} $",
    "phis": r"$\varphi_0$"
    
}
XLABELS_DICT = {
    "snr": "SNR (c/ш)",
    "M": "M (кол-во датчиков), шт",
    "R": "R (радиус решётки АВП), м",
    "alpha": r"$\alpha = \frac{\lambda}{2R} $",
    "phis": r"$\varphi_0, град$"
    
}
NAMING_DICT = {
    "snr": "SNR",
        "M": "M",
        "R": "R",
        "alpha": r"$\alpha$",
        "phis": r"$\varphi_0$"
}
TYPE_SIGNALS = ["garmonic", "pulse"]

def plot_variance_vs_param(dict_values: dict,
                           config_params: dict,
                           parametr_name: str,
                           parametr_values: np.ndarray | list,
                           delta_time : float = 0,
                           xlim: tuple = None,
                           ylim: tuple = None,
                           y_label: str = r"$s_{\varepsilon}^{2}$",
                           y_size: str = r", $град^2$",
                           type_signal: str = None
                           ):
    """Функция строит график зависимости дисперсии оценки от параметра моделирования
    для нескольких методов"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 11))
    fig.subplots_adjust(top=0.88, bottom=0.45)
    if parametr_name == "phis":
        parametr_values = np.degrees(parametr_values)
        
    info_for_plots = []
    for idx, (method, values) in enumerate(dict_values.items()):
        values = np.asarray(values) * (180 / np.pi)**2
        info_for_plots.append({"method": method, "stats": {"Max": np.max(values), "Min": np.min(values), "Mean": np.mean(values)}})
        ax.plot(parametr_values, values, color = COLORS[idx % len(COLORS)], label =  method, linestyle = LINES[idx % len(LINES)], linewidth = 3)

    ax.set_xlabel(XLABELS_DICT[parametr_name], fontsize=18)
    ax.set_ylabel(y_label+y_size, fontsize=18)

    fig.suptitle(
        "Зависимость " + y_label + f" от {LABELS_DICT[parametr_name]}",
        y=0.94, va="center", fontfamily="Times New Roman", fontsize=22
    )
    ax.grid(True)
    if ylim is not None:
        ax.set_ylim([
        value * (180 / np.pi)**2 if value is not None else None
        for value in ylim])
    if xlim is not None:
        ax.set_xlim([
        value if value is not None else None
        for value in xlim])
    ax.legend(fontsize=15)
    # Параметры под графиком
    methods = ", ".join(dict_values)
    info = f"Методы: {methods}\n"
    if type_signal is not None:
        info += f"Тип сигнала: {type_signal}"
        
    if type_signal == "garmonic":
        info += f"Частота сигнала: {config_params['f0']} Гц\n"
   
    if parametr_name != "R":
        info += f"Радиус решётки: {config_params['R']:.2f} м\n"
    if parametr_name != "M":
        info += f"Количество датчиков: {config_params['M']} шт.\n"
    if parametr_name != "snr":
        info += f"SNR: {config_params['snr']} (С/Ш)\n"
    info += (
        f"{NAMING_DICT[parametr_name]} от {parametr_values[0]:.2f} "
        f"до {parametr_values[-1]:.2f} ({len(parametr_values)} точек)\n"
    )
    info += f"Количество проверенных углов: {len(config_params['phis'])}\n"
    info += f"Количество реализаций шума: {config_params['realisation_count']}\n"
    info += f"SEED: {config_params['main_seed']}\n"
    info += f"Время расчёта: {delta_time:.2f} сек."

    ax.text(
        0, -0.20, info,
        transform=ax.transAxes,
        fontsize=14, linespacing=1.5,
        ha="left", va="top",
        bbox=dict(boxstyle="round",facecolor='none', alpha=1),
        clip_on=False
    )
    info2 = ""
    for info_obj in info_for_plots:
        info2 += info_obj["method"] + ":\n" + f"Max: {info_obj["stats"]["Max"]:.3f} град^2 \nMin: {info_obj["stats"]["Min"]:.3f} град^2\nAvg: {info_obj["stats"]["Mean"]:.3f} град^2\n"
    
    ax.text(
            0.5, -0.20, info2,
            transform=ax.transAxes,
            fontsize=14, linespacing=1.5,
            ha="left", va="top",
            bbox=dict(boxstyle="round",facecolor='none',alpha=1),
            clip_on=False
        )
    
    plt.savefig(fname = f"images/report/{parametr_name}", bbox_inches = 'tight', dpi = 300)
    return fig, ax
