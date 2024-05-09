import math

from flask import current_app
from jinja2 import Template


class Whisky:
    def __init__(self, distillery, slug, tastes):
        self.distillery = distillery
        self.slug = slug
        self.tastes = tastes


class Correlation:
    def __init__(self, reference, other, value):
        self.reference = Whisky(*reference)
        self.other = Whisky(*other)
        self.value = value

    @property
    def chart(self):
        chart = Chart(self.reference.tastes, self.other.tastes)
        return chart.create()


class Chart:
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
        :param reference: (tuple of integers) tastes
        :param comparison: (tuple of integers) tastes
        :param width: (int) width of the SVG chart
        :param height: (int) width of the SVG chart
        :param sides: (int) number of sides the grid (polygon)
        :param scales: (int) number of steps (internal lines of the grid)
        :param margin: (int) margin between that edge of the SVG and the grid
        """
        self.reference = reference
        self.comparison = comparison
        self.sides = sides
        self.width = width
        self.height = height
        self.margin = margin
        self.scales = scales
        self.text_line_height = text_line_height
        self.center_x = width / 2
        self.center_y = height / 2

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
            return svg_template.render(**objs).strip()

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
        :param tastes: (tuple of integers) tastes of a whisky
        :param grid: (list of lists of tuples of integers) list containing
        lists of tuples with the x, y coordinates of the grid of the chart
        :return: (list of tuples of integers) sequence of x, y coordinates for
        drawing the area inside the chart representing the given whisky
        """
        output = list()
        taste_count = 0
        for value in tastes:
            taste = abs(value - self.scales)
            if taste == self.scales:
                output.append((self.center_x, self.center_y))
            else:
                polygon = grid[taste]
                point = polygon[taste_count]
                output.append(point)
            taste_count += 1
        return output
