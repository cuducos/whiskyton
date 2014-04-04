#!venv/bin/python
from app import db, models

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
    sum_x_sq = sum(i**2 for i in x)
    sum_y_sq = sum(i**2 for i in y)
    psum = sum(i * j for i, j in zip(x, y))
    num = psum - ((sum_x * sum_y)/n)
    multiplier_1 = sum_x_sq - ((sum_x ** 2) / n)
    multiplier_2 = sum_y_sq - ((sum_y ** 2) / n)
    den = (multiplier_1 * multiplier_2) ** 0.5
    try:
        return num / den
    except ZeroDivisionError:
        return 0


def get_tastes(whisky):
    return [getattr(whisky, taste) for taste in tastes]

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
