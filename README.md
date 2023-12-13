# curve_parser
Python parser for curves to points graphs.

Парсит графики кривых из картинки в точки.

# INSTRUCTION
1. обрежьте фотографию графика по краям
2. приведите к черно-белому виду
3. сохраните в папке img
4. откройте и запустите [ноутбук](graph_reader.ipynb) (возможно потребуется установка pyenv, poetry)
5. введите в функцию get_points путь до картинки
6. выберите крайние точки и названия осей
7. сохраните в csv формате в папке data
8. сохраните в виде графика через интерфейс plotly или seaborn в папку output

# INSTALLATION

`poetry install --no-root`

# ENVIRONMENT ACTIVATION

`poetry shell`
# Linters

`pre-commit install`
`pre-commit run -a`
