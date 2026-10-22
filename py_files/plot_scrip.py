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
    "phis": r"$\varphi_0, рад$"
    
}
NAMING_DICT = {
    "snr": "SNR",
        "M": "M",
        "R": "R",
        "alpha": r"$\alpha$",
        "phis": r"$\varphi_0$"
}
def plot_variance_vs_param(dict_values: dict,
                           config_params: dict,
                           parametr_name: str,
                           ylim: tuple,
                           parametr_values: dict,
                           delta_time : float = 0,
                           y_label: str = r"$s_{\varepsilon}^{2}$",
                           y_size: str = r", $рад^2$"
                           ):
    """Функция строит график зависимости дисперсии оценки от параметра моделирования
    для неескольких методов"""
    
    _, ax = plt.subplots(1, 1, figsize=(14, 7), constrained_layout=True)
    for idx, (method, values) in enumerate(dict_values.items()):
        ax.plot(parametr_values, values, color = COLORS[idx], label =  method, linestyle = LINES[idx], linewidth = 3)

    ax.set_xlabel(XLABELS_DICT[parametr_name], fontsize=18)
    ax.set_ylabel(y_label+y_size, fontsize=18)
    ax.set_title("Зависимость " + y_label + f" от {LABELS_DICT[parametr_name]} ", fontsize=24)
    ax.grid(True)
    ax.set_ylim(ylim)
    ax.legend(fontsize=15)
    s = ""
    for key in list(dict_values.keys()):
        s += key + " "
        
    info = ""
    
    info += f"Методы: {s}\n\n"
    info += f"Частота сигнала: {config_params['f0']} Гц\n"
    if parametr_name != "R":
        info += f"Радиус решетки: {round(config_params['R'], 2)} м\n"
    if parametr_name != "M":
        info += f"Количество датчиков: {config_params['M']} шт\n"
    if parametr_name != "SNR":
        info += f"SNR: {config_params["snr"]} (С/Ш)\n"   
    info += f"{NAMING_DICT[parametr_name]} от {round(parametr_values[0],2)} до {round(parametr_values[-1],2)} ({len(parametr_values)} точек)\n\n"
    info +=   f"Кол-во реализаций шума: {config_params["K"]}\n"
    info += f"Время рассчёта: {round(delta_time,2)} сек."


    ax.text(0.7, 0.96, info, transform=ax.transAxes, fontsize=17, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=1))

  