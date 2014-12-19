# coding: utf-8

from re import compile
from whiskyton import app, db


class Whisky(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    distillery = db.Column(db.String(64), index=True, unique=True)
    slug = db.Column(db.String(64), index=True, unique=True)
    body = db.Column(db.Integer)
    sweetness = db.Column(db.Integer)
    smoky = db.Column(db.Integer)
    medicinal = db.Column(db.Integer)
    tobacco = db.Column(db.Integer)
    honey = db.Column(db.Integer)
    spicy = db.Column(db.Integer)
    winey = db.Column(db.Integer)
    nutty = db.Column(db.Integer)
    malty = db.Column(db.Integer)
    fruity = db.Column(db.Integer)
    floral = db.Column(db.Integer)
    postcode = db.Column(db.String(16))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    views = db.Column(db.Integer)

    def __repr__(self):
        return '<Distillery: {}>'.format(self.distillery)

    def get_tastes(self):
        """
        Return a list of tastes of the whisky.
        :return: (list of strings) tastes of the whisky
        """
        tastes = app.config['TASTES']
        return [str(getattr(self, taste, None)) for taste in tastes]

    def get_slug(self):
        """
        Returns a slug, a lower case string with only letters.
        :return: (string) the inputted string converted to lower case and
        deleting any non-letter character
        """
        regex = compile('[^a-z]+')
        return regex.sub('', self.distillery.lower())

    def get_correlation(self, comparison):
        """
        Returns the id of the two whiskies and the index of correlation
        :param comparison: (whiskyton.models.Whisky) whisky for comparison
        :return: (dictionary) contains the id (int) of each whisky (whisky and
        reference) and the index of correlation (r) between them (float)
        """
        return {
            'reference': self.id,
            'whisky': comparison.id,
            'r': self.__pearson_r(self.get_tastes(), comparison.get_tastes())
        }

    @staticmethod
    def __pearson_r(x, y):
        """
        Returns the index of correlation between two whiskies.
        :param x: (list of strings) tastes of a whisky
        :param y: (list of strings) tastes of a whisky
        :return: (float) index of correlation
        """
        x = [float(n) for n in x]
        y = [float(n) for n in y]
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_x_sq = sum(i ** 2 for i in x)
        sum_y_sq = sum(i ** 2 for i in y)
        p_sum = sum(i * j for i, j in zip(x, y))
        num = p_sum - ((sum_x * sum_y) / n)
        multiplier_1 = sum_x_sq - ((sum_x ** 2) / n)
        multiplier_2 = sum_y_sq - ((sum_y ** 2) / n)
        den = (multiplier_1 * multiplier_2) ** 0.5
        try:
            return num / den
        except ZeroDivisionError:
            return 0


class Correlation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.Integer, index=True)
    whisky = db.Column(db.Integer, db.ForeignKey('whisky.id'))
    r = db.Column(db.Float, index=True)

    def __repr__(self):
        return '<Correlation: {}>'.format(self.r)