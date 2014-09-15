import math
from whiskyton import app
from flask import render_template
from slimmer import xhtml_slimmer
from unipath import Path


def tastes2list(whisky):
    tastes = app.config['TASTES']
    return [str(eval('whisky.' + taste)) for taste in tastes]


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

    # text
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
    svg_image = render_template(
        'chart.svg',
        polygon_coordinates=polygon_coordinates,
        text_coordinates=text_coordinates,
        reference_coordinates=reference_coordinates,
        whisky_coordinates=whisky_coordinates,
        center_x=(width / 2),
        center_y=(height / 2))
    svg_compressed = xhtml_slimmer(svg_image)

    # save the file
    filepath = cache_name(reference, comparison, True)
    filepath.write_file(svg_compressed)


def pol_coordinates(width, height, sides, scales, margin):

    # support
    polygon_coordinates = []
    center_x = width / 2
    center_y = height / 2
    angle_adjust = ((2 * math.pi / sides)) / 2
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


def txt_coordinates(polygon_coordinates, text_line_height):

    # support
    text_coordinates = []
    text_count = 0

    # calc
    for coordinates in polygon_coordinates[0]:

        a = coordinates[0]
        b = coordinates[1]

        # adjusts
        top = [6, 7]
        right = [2, 3, 4, 5]
        bottom = [0, 1]
        left = [8, 9, 10, 11]
        diagonal_down = [2, 11]
        diagonal_up = [5, 8]
        sub_diagonal_down = [3, 10]

        if text_count in top:
            b -= text_line_height * 0.75
        if text_count in right:
            a += text_line_height * 0.75
        if text_count in bottom:
            b += text_line_height * 1.5
        if text_count in left:
            a -= text_line_height * 0.75
        if text_count in diagonal_up:
            b -= text_line_height * 0.5
        if text_count in diagonal_down:
            b += text_line_height * 0.75
        if text_count in sub_diagonal_down:
            b += text_line_height * 0.25

        text_anchor = 'start'
        if text_count in top or text_count in bottom:
            text_anchor = 'middle'
        if text_count in left:
            text_anchor = 'end'

        taste = app.config['TASTES'][text_count]
        taste = taste[0].upper() + taste[1:]

        text_coordinates.append([int(a), int(b), text_anchor, taste])
        text_count += 1

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
