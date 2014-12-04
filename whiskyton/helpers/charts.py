# coding: utf-8

import math
from jinja2 import Template
from slimmer import xhtml_slimmer
from unipath import Path
from whiskyton import app


def cache_name(reference, comparison, full_path=False):
    """
    Returns the name of a cache file for a given chart.
    reference: (list of strings) tastes of one of the whiskies
    comparison: (list of strings) tastes of the other whisky
    full_path: (boolean) return the file name onli if True, or the full path
        with file name if false
    return: (string or unipath.Path) the file name of the cache for the chart
        comparing these both whiskies
    """
    reference_string = ''.join(reference)
    comparison_string = ''.join(comparison)
    filename = '%sx%s.svg' % (reference_string, comparison_string)
    if full_path:
        return Path(cache_path(), filename).absolute()
    else:
        return filename


def cache_path():
    """
    Returns the directory where cached charts are saved.
    return: (unipath.Path) path of the directory where cache files are stored
    """
    path = app.config['BASEDIR'].child('whiskyton', 'static', 'charts')
    return path.absolute()


def create(reference, comparison):
    """
    This method creates a SVG chart and save it in the cache directory.
    reference: (list of strings) tastes of one of the whiskies
    comparison: (list of strings) tastes of the other whisky
    return: (unipath.Path) the file name of the cache for the chart created
    """

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
        return file_path


def pol_coordinates(width, height, sides, scales, margin):
    """
    Returns the coordinates for drawing the grid of the chart.
    width: (int) width of the SVG chart
    height: (int) width of the SVG chart
    sides: (int) number of sides the grid (polygon)
    scales: (int) number of steps (internal reference lines of the grid)
    margin: (int) margin betwwen tha edge of the SVG and the chart grid
    return: (list of lists of tuples of integers) list cointaining lists of
        tuples with the x, y coordinates of the grid of the chart
    """

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
            output.append((int(a), int(b)))
        polygon_coordinates.append(output)

    return polygon_coordinates


def text_position(x, y, count, position, line_height):
    """
    Returns the position of text labels adjusted for a better visual hamrony.
    x: (int) x coordinate of the original position for the text label
    y: (int) y coordinate of the original position for the text label
    count: (int) sequencial position count
    position: (dictionary of lists) map of position sequential counts to
        position class (string; e.g. right, bottom...)
    line_height: (int) height of the text line
    return: (tuple of floats) adjusted x and y coordinates for a better placing
        of the text label
    """
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
    return (x, y)


def text_alignment(count, position):
    """
    Returns the aligment attribute for the text label.
    count: (int) sequencial position count
    position: (dictionary of lists) map of position sequential counts to
        position class (string; e.g. right, bottom, etc.)
    return: (string) attribute for aligning the text label (e.g. start, end...)
    """
    text_anchor = 'start'
    if count in position['top'] or count in position['bottom']:
        text_anchor = 'middle'
    elif count in position['left']:
        text_anchor = 'end'
    return text_anchor


def text_content(count):
    """
    Return the label of the tasted according to the position sequencial count.
    count: (int) sequencial position count
    return: (string) taste label
    """
    taste = app.config['TASTES'][count]
    return taste.title()


def txt_coordinates(polygon_coordinates, line_height):
    """
    Returns a map for drawing the text labels of a chart.
    polygon_coordinates: (list of lists of tuples of integers) list cointaining
        lists of tuples with the x, y coordinates of the grid of the chart
    line_height: (int) height of the text line
    return: (list of dictionaried) list containing a dicionary for each label:
        * coordinates: (tuple of integers) x, y position of the label
        * align: (string) value for the text align attribute
        * content: (string) content of the text of the label
    """

    # support
    text_info = []
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
        text_info.append({
            'coordinates': text_position(x, y, count, pos, line_height),
            'align': text_alignment(count, pos),
            'content': text_content(count)
        })
        count += 1

    return text_info


def area_coordinates(tastes, width, height, polygon_coordinates):
    """
    Returns the coordinates of the chart representing a whisky.
    tastes: (list of strings) tastes of a whisky
    width: (int) width of the SVG chart
    height: (int) width of the SVG chart
    polygon_coordinates: (list of lists of tuples of integers) list cointaining
        lists of tuples with the x, y coordinates of the grid of the chart
    retrun: (list of tuples of integers) sequence of x, y coordinates for
        drawing the area inside the chart represenitng the given whisky
    """

    # support
    output = list()
    center_x = width / 2
    center_y = height / 2
    taste_count = 0

    for taste in tastes:
        taste = abs(int(taste) - 4)
        if taste == 4:
            output.append((center_x, center_y))
        else:
            polygon = polygon_coordinates[taste]
            point = polygon[taste_count]
            output.append(point)
        taste_count += 1

    return output
