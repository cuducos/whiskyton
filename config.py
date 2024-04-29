from os import getenv
from pathlib import Path

BASEDIR = Path(__file__).parent
LOCAL_DEV_DATABASE = f"sqlite:///{BASEDIR}/app.db"
SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", LOCAL_DEV_DATABASE).replace(
    "postgres://", "postgresql://"
)
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
