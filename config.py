from os import getenv
from pathlib import Path

BASEDIR = Path(__file__).parent
SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", f"sqlite:///{BASEDIR}/app.db")
DEBUG = bool(getenv("DEBUG", False))

MAIN_TITLE = "Whiskyton"
HEADLINE = "Find whiskies that you like!"
TASTES = (
    "spicy",
    "honey",
    "tobacco",
    "medicinal",
    "smoky",
    "sweetness",
    "body",
    "floral",
    "fruity",
    "malty",
    "nutty",
    "winey",
)
