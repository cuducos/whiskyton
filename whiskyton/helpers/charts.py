import math
from pathlib import Path

from flask import current_app
from jinja2 import Template


class Chart(object):
    def __init__(
        self,
        reference=None,
        comparison=None,
        sides=12,
        width=330,
        height=260,
        margin=60,
        scales=4,
        text_line_height=11,
    ):
        """
        :param reference: whiskyton.models.Whisky or tastes (tuple of integers)
        :param comparison: whiskyton.models.Whisky or tastes (tuple of integers)
        :param width: (int) width of the SVG chart
        :param height: (int) width of the SVG chart
        :param sides: (int) number of sides the grid (polygon)
        :param scales: (int) number of steps (internal lines of the grid)
        :param margin: (int) margin between that edge of the SVG and the grid
        """

        # set whisky data
        if not isinstance(reference, (list, tuple)) and reference is not None:
            reference = tuple(str(taste) for taste in reference.get_tastes())
        if not isinstance(comparison, (list, tuple)) and comparison is not None:
            comparison = tuple(str(taste) for taste in comparison.get_tastes())

        self.reference = reference
        self.comparison = comparison

        # set chart data
        self.sides = sides
        self.width = width
        self.height = height
        self.margin = margin
        self.scales = scales
        self.text_line_height = text_line_height
        self.center_x = width / 2
        self.center_y = height / 2

    @staticmethod
    def cache_path():
        """
        Returns the directory where cached charts are saved.
        :return: (pathlib.Path) path of the directory where cache files are
        stored
        """
        path = current_app.config["BASEDIR"] / "whiskyton" / "static" / "charts"
        if not path.exists():
            path.mkdir()
        return path.absolute()

    def cache_name(self, full_path=False):
        """
        Returns the name of a cache file for a given chart.
        :param full_path: (boolean) return the file name only if True, or the
        full path with file name if false
        :return: (string or pathlib.Path) the file name of the cache for the
        chart comparing these both whiskies
        """
        reference_string = "".join(self.reference)
        comparison_string = "".join(self.comparison)
        filename = "%sx%s.svg" % (reference_string, comparison_string)
        if full_path:
            return Path(self.cache_path(), filename).absolute()
        else:
            return filename

    def create(self):
        """
        This method creates a SVG chart.
        :return: (string) contents of the SVG file
        """

        # variables for drawing
        grid = self.__grid_coordinates()
        objs = {
            "grid": grid,
            "labels": self.__txt_coordinates(grid),
            "reference": self.area_coordinates(self.reference, grid),
            "whisky": self.area_coordinates(self.comparison, grid),
            "center_x": self.center_x,
            "center_y": self.center_y,
        }

        # generate the svg
        basedir = current_app.config["BASEDIR"]
        template = basedir / "whiskyton" / "templates" / "chart.svg"
        with open(template, "r") as file_handler:
            # create SVG
            svg_template = Template(file_handler.read())
            return svg_template.render(**objs)

    def cache(self):
        """
        This method saves a SVG chart in the cache directory.
        :return: (pathlib.Path) the path of the cache file
        """
        svg = self.create()
        file_path = self.cache_name(True)
        if file_path.exists():
            file_path.unlink()
        file_path.write_text(svg)
        return file_path

    def __grid_coordinates(self):
        """
        Returns the coordinates for drawing the grid of the chart.
        :return: (list of lists of tuples of integers) list containing lists
        of tuples with the x, y coordinates of the grid of the chart
        """

        # support
        polygon_coordinates = list()
        angle_adjust = (2 * math.pi / self.sides) / 2
        radius = (self.width - (2 * self.margin)) / 2
        interval = radius / self.scales

        # calc
        for scale in range(0, self.scales):
            output = list()
            for x in range(0, self.sides):
                angle = ((2 * math.pi / self.sides) * x) - angle_adjust
                r = radius - (scale * interval)
                a = self.center_x + (math.sin(angle) * r)
                b = self.center_y + (math.cos(angle) * r)
                output.append((int(a), int(b)))
            polygon_coordinates.append(output)

        return polygon_coordinates

    def __txt_coordinates(self, grid):
        """
        Returns a map for drawing the text labels of a chart.
        :param grid: (list of lists of tuples of integers) list containing
        lists of tuples with the x, y coordinates of the grid of the chart
        :return: (list of dictionaries) list containing a dictionary for each
        label; the keys are 'coordinates' (tuple of integers - x, y position
        of the label), 'align' (string - value for the text align attribute)
        and 'content' (string - content of the text of the label)
        """

        # support
        text_info = list()
        count = 0

        # adjust groups
        pos = {
            "bottom": [0, 1],
            "right": [2, 3, 4, 5],
            "top": [6, 7],
            "left": [8, 9, 10, 11],
            "diagonal_down": [2, 11],
            "diagonal_up": [5, 8],
            "sub_diagonal_down": [3, 10],
        }

        # calc
        for coordinates in grid[0]:
            x = coordinates[0]
            y = coordinates[1]
            text_info.append(
                {
                    "coordinates": self.__text_position(x, y, count, pos),
                    "align": self.__text_alignment(count, pos),
                    "content": self.__text_content(count),
                }
            )
            count += 1

        return text_info

    def __text_position(self, x, y, count, position):
        """
        Returns the position of labels adjusted for a better visual harmony.
        :param x: (int) x coordinate of the original text label position
        :param y: (int) y coordinate of the original text label position
        :param count: (int) sequential position count
        :param position: (dictionary of lists) map of position sequential count
        to position class (string; e.g. right, bottom...)
        :return: (tuple of floats) adjusted x and y coordinates for a better
        placing of the text label
        """
        if count in position["top"]:
            y -= self.text_line_height * 0.75
        if count in position["right"]:
            x += self.text_line_height * 0.75
        if count in position["bottom"]:
            y += self.text_line_height * 1.5
        if count in position["left"]:
            x -= self.text_line_height * 0.75
        if count in position["diagonal_up"]:
            y -= self.text_line_height * 0.5
        if count in position["diagonal_down"]:
            y += self.text_line_height * 0.75
        if count in position["sub_diagonal_down"]:
            y += self.text_line_height * 0.25
        return x, y

    @staticmethod
    def __text_alignment(count, position):
        """
        Returns the alignment attribute for the text label.
        :param count: (int) sequential position count
        :param position: (dictionary of lists) map of position sequential count
        to position class (string; e.g. right, bottom, etc.)
        :return: (string) attribute for aligning the label (e.g. start, end...)
        """
        text_anchor = "start"
        if count in position["top"] or count in position["bottom"]:
            text_anchor = "middle"
        elif count in position["left"]:
            text_anchor = "end"
        return text_anchor

    @staticmethod
    def __text_content(count):
        """
        Return the name of the taste according to their position count.
        :param count: (int) sequential position count
        :return: (string) taste label
        """
        taste = current_app.config["TASTES"][count]
        return taste.title()

    def area_coordinates(self, tastes, grid):
        """
        Returns the coordinates of the chart representing a whisky.
        :param tastes: (list of strings) tastes of a whisky
        :param grid: (list of lists of tuples of integers) list containing
        lists of tuples with the x, y coordinates of the grid of the chart
        :return: (list of tuples of integers) sequence of x, y coordinates for
        drawing the area inside the chart representing the given whisky
        """
        output = list()
        taste_count = 0
        for taste in tastes:
            taste = abs(int(taste) - self.scales)
            if taste == self.scales:
                output.append((self.center_x, self.center_y))
            else:
                polygon = grid[taste]
                point = polygon[taste_count]
                output.append(point)
            taste_count += 1
        return output
