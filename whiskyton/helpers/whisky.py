# coding: utf-8

import re
from whiskyton import app


def get_tastes(whisky, integers=False):
    return [str(getattr(whisky, taste)) for taste in app.config['TASTES']]


def slugfy(string):
    regex = re.compile('[^a-zA-Z]+')
    string = regex.sub('', string)
    return string.lower()


def get_correlation(reference, whisky):
    r = pearsonr(get_tastes(reference), get_tastes(whisky))
    row = {
        'reference': reference.id,
        'whisky': whisky.id,
        'r': r}
    return row


def pearsonr(x, y):
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
