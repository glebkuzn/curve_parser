from math import fabs

import pandas as pd
from PIL import Image


def check_pixel_colour(pixel, colour, delta=(0, 0, 0)):
    """сравниваем цвет пиксиля с эталонным цветом с погрешностью дельта"""
    return (
        (colour[0] - delta[0]) <= pixel[0] <= (colour[0] + delta[0])
        and (colour[1] - delta[1]) <= pixel[1] <= (colour[1] + delta[1])
        and (colour[2] - delta[2]) <= pixel[2] <= (colour[2] + delta[2])
    )


def better_colour_value(pixels, colour):
    """из списка цветов выбираем более подходящий эталонному цвету"""
    delta = 1024
    better_pixel = None
    for pixel in pixels:
        current_delta = (
            fabs(pixel[0] - colour[0])
            + fabs(pixel[1] - colour[1])
            + fabs(pixel[2] - colour[2])
        )
        if current_delta < delta:
            delta = current_delta
            better_pixel = pixel
    return better_pixel


def get_border_grids(image, grid_colour):
    """
    получаем номера пиксилей по оси x первой и последней линий сетки, по оси y верхней и нижней
    данные пиксили соответствуют переданным граничным значениям сетки
    """
    width, height = image.size
    x1, x2, y1, y2 = 0, width, 0, height
    for x in range(width):
        if check_pixel_colour(image.getpixel((x, 0)), grid_colour):
            x1 = x
            break
    for x in range(width - 1, -1, -1):
        if check_pixel_colour(image.getpixel((x, 0)), grid_colour):
            x2 = x
            break
    for y in range(height - 1, -1, -1):
        if check_pixel_colour(image.getpixel((0, y)), grid_colour):
            y1 = y
            break
    for y in range(height):
        if check_pixel_colour(image.getpixel((0, y)), grid_colour):
            y2 = y
            break
    return x1, x2, y1, y2


def get_linear_value(x, x1, x2, x1_value, x2_value):
    """получаем значение для текущего пикселя с учетом граничных значений сетки для линейной оси"""
    k = (x2 - x1) / (x2_value - x1_value)
    b = x1 - x1_value * k
    return (x - b) / k


def process_graph(
    image_path, x1_value, x2_value, y1_value, y2_value, colour, delta, grid_colour
):
    """получаем список координат графика на изображении"""
    image = Image.open(image_path)
    width, height = image.size
    x1, x2, y1, y2 = get_border_grids(image, grid_colour)
    coordinates = []
    y_list = []
    for x in range(width):
        pixels = {}
        for y in range(height):
            pixel = image.getpixel((x, y))
            if check_pixel_colour(pixel, colour, delta):
                pixels[pixel] = y
        if len(pixels) > 0:
            y = pixels[better_colour_value(pixels.keys(), colour)]
            x_value = get_linear_value(x, x1, x2, x1_value, x2_value)
            y_value = get_linear_value(height - y, y1, y2, y1_value, y2_value)
            coordinates.append((x_value, y_value))
            y_list.append(y)

    return coordinates


def get_points(
    img_path: str,
    x_col_name: str = "x",
    y_col_name: str = "y",
    x_min_value: float = 0.0,
    x_max_value: float = 1.0,
    y_min_value: float = 0.0,
    y_max_value: float = 1.0,
    grid_val: int = 256,
    line_val: int = 30,
    fon_val: int = 256,
) -> pd.DataFrame:
    """Если график плохо читается, то стоит покрутить значения grid_val, line_val, fon_val.

    Args:
        img_path (str): путь до изображения

        x_col_name (str, optional): название оси x. Defaults to 'x'.

        y_col_name (str, optional): название оси y. Defaults to 'y'.

        x_min_value (float, optional): значение крайней левой точки по оси х. Defaults to 0.0.

        x_max_value (float, optional): значение крайней правой точки по оси х. Defaults to 1.0.

        y_min_value (float, optional): значение крайней нижней точки по оси y. Defaults to 0.0.

        y_max_value (float, optional): значение крайней верхней точки по оси y. Defaults to 1.0.

        grid_val (int, optional): яркость сетки. 256 - сетка прозрачная. 0 - черная. Defaults to 256.

        line_val (int, optional): яркость кривой. 256 - линия прозрачная. 0 - черная. Defaults to 30.

        fon_val (int, optional): яркость фона. 256 - линия прозрачная. 0 - черная. Defaults to 256.

    Raises:
        ValueError: Минимальные значения должны быть меньше максимальных!

    Returns:
        pd.DataFrame: табличка из 2х колонок в пандасе. Первая это ось x, а вторая y.
    """
    if (x_max_value <= x_min_value) or (y_max_value <= y_min_value):
        raise ValueError("Минимальные значения должны быть меньше максимальных!")
    return pd.DataFrame(
        process_graph(
            img_path,
            x_min_value,
            x_max_value,
            y_min_value,
            y_max_value,
            (line_val, line_val, line_val),
            (fon_val, fon_val, fon_val),
            (grid_val, grid_val, grid_val),
        ),
        columns=[x_col_name, y_col_name],
    )
