"""Build and execute an isolated research notebook using the user's original cells."""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import hashlib
import json
from pathlib import Path
import sys
import nbformat as nbf
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/lorentz_study'
OUT.mkdir(exist_ok=True)
sources = [ROOT / n for n in ['notebook.ipynb', 'report.ipynb']]
sources += sorted((ROOT / 'py_files').glob('*.py'))
sources += sorted((ROOT / 'tests').glob('*.py'))
sources += [ROOT / 'reports/dox/info_snr_supplement.docx', ROOT / 'reports/report_avp_template_v6.docx']
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
original = nbf.read(ROOT / 'notebook.ipynb', as_version=4)
report = nbf.read(ROOT / 'report.ipynb', as_version=4)
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))

md('''# Исследование импульса Лоренца и сравнение с синусоидой
Рабочая копия расчёта. Исходные ноутбуки и модули не редактируются.
Ячейки формирования сигналов и диаграмм перенесены из `notebook.ipynb`,
схема эксперимента по SNR — из `report.ipynb`.
Дополнения: сохранение рисунков, аналитические проверки, независимая
инициализация генератора для каждого метода и статистики ошибок.
Используются текущие параметры `py_files/config.py`, включая τ = 0,05 с.
''')
code('''from pathlib import Path
import sys, os, json, csv
ROOT = Path.cwd()
if not (ROOT / 'py_files').exists():
    ROOT = Path.cwd().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'reports/lorentz_study'
FIG = OUT / 'figures'
FIG.mkdir(parents=True, exist_ok=True)
import matplotlib
matplotlib.use('Agg')
from IPython.display import Image
''')
code(original.cells[1].source)
code(original.cells[2].source + '\n' + original.cells[3].source)
md('## Воспроизведение графиков исходного ноутбука')
for i, name in [(5,'01_pulse'), (6,'02_fft_original'), (8,'03_noise'), (9,'04_sensors'), (10,'05_channels')]:
    src = original.cells[i].source
    # Saving and explicit closing are the only changes to these original plotting cells.
    code(src.replace('plt.show()', f"fig.savefig(FIG / '{name}.png', dpi=180, bbox_inches='tight')\nfrom IPython.display import display\ndisplay(Image(filename=str(FIG / '{name}.png')))\nplt.close(fig)"))
code(original.cells[11].source)
for i, name in [(12,'06_bartlett_original'),(13,'07_capon_original')]:
    code(original.cells[i].source.replace('plt.show()', f"fig.savefig(FIG / '{name}.png', dpi=180, bbox_inches='tight')\ndisplay(Image(filename=str(FIG / '{name}.png')))\nplt.close(fig)"))
md('## Аналитическая энергия и спектр; проверки нормировки')
code(r'''
T = config_parametrs['duration_all']
tau = config_parametrs['duration_pulse']
A = config_parametrs['A']
tc = config_parametrs['center_pulse']
def primitive(x):
    return A*A/2 * (x/(x*x+tau*tau) + np.arctan(x/tau)/tau)
E_analytic = primitive(T-tc)-primitive(-tc)
E_infinite = np.pi*A*A/(2*tau)
nu = E_analytic/E_infinite
E_sin = calculate_energy(sin_signal, config_parametrs['time_vector'])
sigma_imp = calculate_noise_level(en_signal, config_parametrs['snr'], T)
sigma_sin = calculate_noise_level(E_sin, config_parametrs['snr'], T)
assert np.isclose(en_signal,E_analytic,rtol=1e-8)
assert np.isclose(sigma_imp**2*T*config_parametrs['snr'],en_signal)
f = cfg.FREQ_VECTOR
F_infinite = np.pi*A*np.exp(-2*np.pi*tau*np.abs(f))
fig, axs = plt.subplots(1,2,figsize=(11.3,4.2))
for ax in axs:
    ax.plot(f,freq_signal,label='ДПФ конечной записи',lw=2)
    ax.plot(f,F_infinite,'--',label='Полная временная ось',lw=1.5)
    ax.set_xlim(-30,30); ax.set_xlabel('Частота f, Гц'); ax.grid(True,alpha=.35)
axs[0].set_ylabel(r'$|\widetilde P(f)|$, Па·с')
axs[1].set_yscale('log'); axs[1].set_ylim(1e-5,5)
axs[1].set_ylabel(r'$|\widetilde P(f)|$, Па·с (лог. шкала)')
axs[0].legend(fontsize=9)
fig.tight_layout(); fig.savefig(FIG/'08_spectrum_comparison.png',dpi=200)
display(Image(filename=str(FIG/'08_spectrum_comparison.png'))); plt.close(fig)
assert np.allclose(pulse_signal,pulse_signal[::-1])
tau_array = get_tau_array(config_parametrs)
energies_channels = []
for delay in tau_array:
    cp = config_parametrs.copy(); cp['time_vector'] = config_parametrs['time_vector']-delay
    energies_channels.append(calculate_energy(get_impulse_signal(cp),cp['time_vector']))
checks = dict(T=T,tc=tc,tau=tau,A=A,peak=A/tau,E_imp_numeric=en_signal,
              E_imp_analytic=E_analytic,E_infinite=E_infinite,nu=nu,
              E_sin=E_sin,sigma_imp=sigma_imp,sigma_sin=sigma_sin,
              fft_zero=float(freq_signal[np.argmin(np.abs(f))]),
              area_exact=float(2*A*np.arctan(T/(2*tau))),
              fft_df=cfg.FS/cfg.N,angular_step=2*np.pi/len(cfg.PHI_VECTOR),
              delays=tau_array.tolist(),energies_channels=energies_channels,
              energy_relative_error=abs(en_signal/E_analytic-1),
              f_99_energy=np.log(100)/(4*np.pi*tau),
              low_frequency_alpha_at_f99=cfg.SPEED_ON_SOUND/(2*cfg.R*(np.log(100)/(4*np.pi*tau))))
print(json.dumps(checks,ensure_ascii=False,indent=2))
''')
md('''## Сравнение методов на одной реализации
Для каждого типа сигнала генератор заново инициализируется seed = 10.
Бартлетт и Кейпон работают с одной и той же матрицей наблюдений.
Для обоих сигналов задан энергетический SNR = 2.
''')
code(r'''
from py_files.experiment_stats import list_errors, calculate_variance, var_vs_params
methods = {'Бартлетт':get_barlet_values,'Кейпон':get_cap_values}
signals_to_compare = {'Лоренц':get_impulse_signal,'Синусоида':get_sin_signal}
single_results = []
fig, axs = plt.subplots(1,2,figsize=(11.3,4.4))
for signal_name, signal_func in signals_to_compare.items():
    cp = cfg.init_rng(10)
    X = get_channel_matrix(cp,get_tau_array(cp),signal_func)
    W0 = get_covariation_matrix(X,cp['N'])
    D = get_direction_matrix(cp['phis'],cp['M'])
    for ax,(method,func) in zip(axs,methods.items()):
        val = func(W0,D)
        estimate = get_est_phi(cp['phis'],val)
        error = (estimate-cp['target_phi']+np.pi)%(2*np.pi)-np.pi
        single_results.append(dict(signal=signal_name,method=method,estimate_deg=float(np.degrees(estimate)),error_deg=float(np.degrees(error))))
        ax.plot(np.degrees(cp['phis']),val/np.max(val),label=signal_name)
        ax.set_title(method); ax.set_xlabel('Проверяемый азимут, град.'); ax.grid(True,alpha=.35)
        ax.set_xlim(0,360)
for ax in axs:
    ax.axvline(45,color='black',ls=':',label='Истинный азимут 45°')
    ax.legend(fontsize=9); ax.set_ylabel('Диаграмма / максимум')
fig.tight_layout(); fig.savefig(FIG/'09_direction_comparison.png',dpi=200)
display(Image(filename=str(FIG/'09_direction_comparison.png'))); plt.close(fig)
print(single_results)
''')
md('''## Дисперсия ошибки в зависимости от SNR
Схема соответствует ячейке 3 `report.ipynb`: `var_vs_params` →
`list_errors` → `single_est`. Здесь `list_errors` вызывается явно, чтобы
сохранить индивидуальные ошибки и дополнительно вычислить смещение и RMSE.
Сетка SNR исходной ячейки 0,1…1 дополнена базовой точкой SNR = 2.
На каждую точку и метод приходится 100 реализаций, как в конфигурации.
Генераторы методов независимы как объекты, но инициализируются одинаково,
что обеспечивает сравнение на одинаковых стандартизованных шумах.
''')
code(r'''
SNR_VALUES = np.r_[np.linspace(0.1,1,10),cfg.SNR]
rows = []; raw_errors = {}
for signal_name, signal_func in signals_to_compare.items():
    for method,func in methods.items():
        cp = cfg.init_rng(10)
        for snr in SNR_VALUES:
            cp['snr'] = float(snr)
            errors = np.asarray(list_errors(cp,func,signal_func))
            key = f'{signal_name}|{method}|{snr:.12g}'
            raw_errors[key] = errors.tolist()
            rows.append(dict(signal=signal_name,method=method,snr=float(snr),K=len(errors),
                             bias_rad=float(np.mean(errors)),variance_rad2=float(calculate_variance(errors)),
                             rmse_rad=float(np.sqrt(np.mean(errors**2)))))
        print(signal_name,method,'готово')
with (OUT/'statistics.csv').open('w',encoding='utf-8-sig',newline='') as fp:
    writer=csv.DictWriter(fp,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(OUT/'errors.json').write_text(json.dumps(raw_errors,ensure_ascii=False,indent=2),encoding='utf-8')
# Verify the explicitly expanded loop against the original notebook's helper.
cp = cfg.init_rng(10)
expected = var_vs_params(cp,get_barlet_values,get_impulse_signal,'snr',SNR_VALUES[:2])
actual = [r['variance_rad2'] for r in rows if r['signal']=='Лоренц' and r['method']=='Бартлетт'][:2]
assert np.array_equal(expected,actual)
fig,axs=plt.subplots(1,2,figsize=(11.3,4.3))
styles = {'Лоренц':'-','Синусоида':'--'}
colors = {'Бартлетт':'#2056a0','Кейпон':'#bd3a32'}
for signal_name in signals_to_compare:
    for method in methods:
        data=[r for r in rows if r['signal']==signal_name and r['method']==method]
        x=[r['snr'] for r in data]
        axs[0].plot(x,[r['variance_rad2'] for r in data],styles[signal_name],color=colors[method],marker='.',label=f'{signal_name}: {method}')
        axs[1].plot(x,np.degrees([r['rmse_rad'] for r in data]),styles[signal_name],color=colors[method],marker='.')
for ax in axs:
    ax.set_xlabel('Энергетический SNR, линейная шкала');ax.grid(True,alpha=.35)
axs[0].set_ylabel(r'$s_\varepsilon^2$, рад$^2$');axs[0].set_yscale('log')
axs[1].set_ylabel('RMSE, град.');axs[0].legend(fontsize=8)
fig.tight_layout();fig.savefig(FIG/'10_statistics_comparison.png',dpi=200)
display(Image(filename=str(FIG/'10_statistics_comparison.png')));plt.close(fig)
summary=dict(checks=checks,single=single_results,statistics=rows,
             parameters={k:config_parametrs[k] for k in ['M','N','fs','R','c','f0','snr','main_seed','realisation_count','alpha','target_phi']},
             versions=dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__))
(OUT/'results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
''')
nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python (project environment)','language':'python','name':'python3'}})
path=OUT/'lorentz_research.ipynb'
nbf.write(nb,path)
km=KernelManager(kernel_name='python3')
km.kernel_spec.argv[0]=sys.executable
client=NotebookClient(nb,km=km,timeout=600,resources={'metadata':{'path':str(ROOT)}})
try:
    client.execute()
finally:
    nbf.write(nb,path)
    after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    audit={'before':before,'after':after,'all_unchanged':before==after}
    (OUT/'source_integrity.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    assert before==after,'Original source files changed during execution'
print('Notebook complete; original sources unchanged:',path)
