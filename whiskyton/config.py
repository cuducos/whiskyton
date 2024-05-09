from os import getenv
from pathlib import Path

BASEDIR = Path(__file__).parent.parent
DEBUG = bool(getenv("DEBUG", False))

MAIN_TITLE = "Whiskyton"
HEADLINE = "Find whiskies that you like!"
TASTES = (
    "body",
    "sweetness",
    "smoky",
    "medicinal",
    "tobacco",
    "honey",
    "spicy",
    "winey",
    "nutty",
    "malty",
    "fruity",
    "floral",
)
