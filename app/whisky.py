import models
import re
from sqlalchemy.sql.expression import func


def random_whisky():
    random_one = models.Whisky.query.order_by(func.random()).first()
    return random_one


def slugfy(string):
    regex = re.compile('[^a-zA-Z]+')
    string = regex.sub('', string)
    return string.lower()
