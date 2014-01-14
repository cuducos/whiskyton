#!flask/bin/python
from app import db, models
from itertools import imap

# our data

tastes = (
    'body',
    'sweetness',
    'smoky',
    'medicinal',
    'tobacco',
    'honey',
    'spicy',
    'winey',
    'nutty',
    'malty',
    'fruity',
    'floral')
whiskies = models.Whisky.query.all()

# helper functions


def pearsonr(x, y):
    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(map(lambda x: pow(x, 2), x))
    sum_y_sq = sum(map(lambda x: pow(x, 2), y))
    psum = sum(imap(lambda x, y: x * y, x, y))
    num = psum - (sum_x * sum_y/n)
    multiplier_1 = (sum_x_sq - pow(sum_x, 2) / n)
    multiplier_2 = (sum_y_sq - pow(sum_y, 2) / n)
    den = pow(multiplier_1 * multiplier_2, 0.5)
    if den == 0:
        return 0
    else:
        return num / den


def get_tastes(whisky):
    global tastes
    values = []
    for taste in tastes:
        eval('values.append(whisky.' + taste + ')')
    return values

# calc and add to db

for reference in whiskies:
    for whisky in whiskies:
        corr = pearsonr(get_tastes(reference), get_tastes(whisky))
        row = models.Correlation(
            reference=reference.id,
            whisky=whisky.id,
            r=corr)
        db.session.add(row)

db.session.commit()
