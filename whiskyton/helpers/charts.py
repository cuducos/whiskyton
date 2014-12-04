# coding: utf-8

import math
from jinja2 import Template
from slimmer import xhtml_slimmer
from unipath import Path
from whiskyton import app


def cache_name(reference, comparison, full_path=False):
    reference_string = ''.join(reference)
    comparison_string = ''.join(comparison)
    filename = '%sx%s.svg' % (reference_string, comparison_string)
    if full_path:
        return Path(cache_path(), filename).absolute()
    else:
        return filename


def cache_path():
    path = app.config['BASEDIR'].child('whiskyton', 'static', 'charts')
    return path.absolute()


def create(reference, comparison):

    # basic variables for the chart
    sides = 12
    width = 330
    height = 260
    margin = 60
    scales = 4
    text_line_height = 11

    # variables for drawing
    polygon_coordinates = pol_coordinates(width, height, sides, scales, margin)
    text_coordinates = txt_coordinates(polygon_coordinates, text_line_height)
    reference_coordinates = area_coordinates(
        reference,
        width,
        height,
        polygon_coordinates)
    whisky_coordinates = area_coordinates(
        comparison,
        width,
        height,
        polygon_coordinates)

    # generate the svg
    basedir = app.config['BASEDIR']
    template = basedir.child('whiskyton', 'templates', 'chart.svg')
    with open(template, 'r') as file_handler:
        svg_template = Template(file_handler.read())
        svg_image = svg_template.render(
            polygon_coordinates=polygon_coordinates,
            text_coordinates=text_coordinates,
            reference_coordinates=reference_coordinates,
            whisky_coordinates=whisky_coordinates,
            center_x=(width / 2),
            center_y=(height / 2))
        svg_compressed = xhtml_slimmer(svg_image)

        # save the file
        Path(cache_path()).mkdir()
        file_path = cache_name(reference, comparison, True)
        file_path.write_file(svg_compressed)


def pol_coordinates(width, height, sides, scales, margin):

    # support
    polygon_coordinates = []
    center_x = width / 2
    center_y = height / 2
    angle_adjust = (2 * math.pi / sides) / 2
    radius = (width - (2 * margin)) / 2
    interval = radius / scales

    # calc
    for scale in range(0, scales):
        output = []
        for x in range(0, sides):
            angle = ((2 * math.pi / sides) * x) - angle_adjust
            r = radius - (scale * interval)
            a = center_x + (math.sin(angle) * r)
            b = center_y + (math.cos(angle) * r)
            output.append([int(a), int(b)])
        polygon_coordinates.append(output)

    return polygon_coordinates


def text_position(x, y, count, position, line_height):
    if count in position['top']:
        y -= line_height * 0.75
    if count in position['right']:
        x += line_height * 0.75
    if count in position['bottom']:
        y += line_height * 1.5
    if count in position['left']:
        x -= line_height * 0.75
    if count in position['diagonal_up']:
        y -= line_height * 0.5
    if count in position['diagonal_down']:
        y += line_height * 0.75
    if count in position['sub_diagonal_down']:
        y += line_height * 0.25
    return [x, y]


def text_alignment(count, position):
    text_anchor = 'start'
    if count in position['top'] or count in position['bottom']:
        text_anchor = 'middle'
    elif count in position['left']:
        text_anchor = 'end'
    return text_anchor


def text_content(count):
    taste = app.config['TASTES'][count]
    taste = taste[0].upper() + taste[1:]
    return taste


def txt_coordinates(polygon_coordinates, line_height):

    # support
    text_coordinates = []
    count = 0

    # adjust groups
    pos = {
        'bottom': [0, 1],
        'right': [2, 3, 4, 5],
        'top': [6, 7],
        'left': [8, 9, 10, 11],
        'diagonal_down': [2, 11],
        'diagonal_up': [5, 8],
        'sub_diagonal_down': [3, 10]}

    # calc
    for coordinates in polygon_coordinates[0]:

        # get coordinates
        x = coordinates[0]
        y = coordinates[1]

        # get values
        text_values = text_position(x, y, count, pos, line_height)
        text_values.append(text_alignment(count, pos))
        text_values.append(text_content(count))

        # save values
        text_coordinates.append(text_values)
        count += 1

    return text_coordinates


def area_coordinates(tastes, width, height, polygon_coordinates):

    # support
    lst = []
    center_x = width / 2
    center_y = height / 2
    taste_count = 0

    for taste in tastes:
        taste = abs(int(taste) - 4)
        if taste == 4:
            lst.append([center_x, center_y])
        else:
            polygon = polygon_coordinates[taste]
            point = polygon[taste_count]
            lst.append(point)
        taste_count += 1

    return lst
