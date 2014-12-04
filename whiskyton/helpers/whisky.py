# coding: utf-8

import re
from whiskyton import app


def get_tastes(whisky, integers=False):
    return [str(getattr(whisky, taste)) for taste in app.config['TASTES']]


def slugfy(string):
    """
    Returns a slug, a lower case string with only letters.
    string: (string) any given text
    return: (string) the inputed string converted to lower case and deleting any
        non-letter character
    """
    regex = re.compile('[^a-z]+')
    return regex.sub('', string.lower())


def get_correlation(reference, whisky):
    """
    Returns the id of the two whiskies and the index of correlation
    reference: (whiskyton.models.Whisky) object of the reference whisky
    whisky: (whiskyton.models.Whisky) object of the comparison whisky
    return: (dictionary) contains the id (int) of each whisky (whisky and reference)
        and the index of correlation (r) between them (float)
    """
    return {
        'reference': reference.id,
        'whisky': whisky.id,
        'r': pearsonr(get_tastes(reference), get_tastes(whisky))
    }


def pearsonr(x, y):
    """
    Returns the index of correlation between two whiskies.
    x: (list of strings) tastes of a whisky
    y: (list of strings) tastes of a whisky
    return: (float) index of correlation
    """
    x = [float(n) for n in x]
    y = [float(n) for n in y]
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(i ** 2 for i in x)
    sum_y_sq = sum(i ** 2 for i in y)
    psum = sum(i * j for i, j in zip(x, y))
    num = psum - ((sum_x * sum_y) / n)
    multiplier_1 = sum_x_sq - ((sum_x ** 2) / n)
    multiplier_2 = sum_y_sq - ((sum_y ** 2) / n)
    den = (multiplier_1 * multiplier_2) ** 0.5
    try:
        return num / den
    except ZeroDivisionError:
        return 0
