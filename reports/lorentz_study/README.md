# Исследование импульса Лоренца

Итоговый отчёт: `lorentz_research_report_final.docx` и одноимённый PDF.
Выполненный ноутбук с рисунками: `lorentz_research.ipynb`.

Команды из корня проекта в PowerShell:

```powershell
.env/Scripts/python.exe -m pip install -r reports/lorentz_study/requirements.txt
.env/Scripts/python.exe reports/lorentz_study/run_study.py
.env/Scripts/python.exe reports/lorentz_study/build_report.py
```

`run_study.py` использует текущие версии исходных ноутбуков и модулей,
создаёт отдельный рабочий ноутбук и проверяет сохранность исходников по SHA-256.
При повторном запуске результаты в этой папке перезаписываются.
Во время подготовки отчёта после завершения расчётов обнаружены внешние
изменения `notebook.ipynb` и `py_files/functions.py`; они сохранены.
Контрольные суммы использованной версии находятся в `source_integrity.json`,
последующая проверка — в `source_postcheck.json`.

Для сборки формул требуется `MML2OMML.XSL` по указанному в `build_report.py`
пути Microsoft Office. PDF экспортирован из Word и проверен отдельно.

Текущие параметры: τ = 0,05 с, T = 1,13625 с, M = 3, K = 100, seed = 10.
Сравнение с синусоидой выполнено при одинаковом энергетическом SNR.
Все индивидуальные ошибки сохранены в `errors.json`, статистики —
в `statistics.csv`. Bootstrap-интервалы воспроизводятся сборщиком отчёта.
