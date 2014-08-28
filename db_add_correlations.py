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


def corr_exists(id1, id2):
    attempt1 = models.Correlation.query\
        .filter_by(reference=id1, whisky=id2).first()
    if attempt1 is not None:
        return True
    else:
        attempt2 = models.Correlation.query\
            .filter_by(reference=id2, whisky=id1).first()
        if attempt2 is None:
            return False
        else:
            return True


# calc and add to db
correlations_list = []

for reference in whiskies:

    for whisky in whiskies:

        item = str(whisky.id) + 'x' + str(reference.id)
        cond1 = item in correlations_list
        cond2 = reference.id == whisky.id

        if not cond1 and not cond2:
            corr = pearsonr(get_tastes(reference), get_tastes(whisky))
            row = models.Correlation(reference=reference.id,
                                     whisky=whisky.id,
                                     r=corr)
            db.session.add(row)
            correlations_list.append(item)

db.session.commit()
