from whiskyton.helpers.charts import Chart
from whiskyton.models import Whisky

from flask import Blueprint

charts = Blueprint("charts", __name__)


@charts.cli.command("delete")
def delete():
    """Delete all cached charts"""
    folder_path = (Chart()).cache_path()
    if not folder_path.exists():
        folder_path.mkdir()
    folder = tuple(f for f in folder_path.glob("*") if f.is_file())
    count = 0
    total_size = 0
    total = float(len(folder))
    for f in folder:
        size = f.stat().st_size
        print(
            "%s Deleting %s (%s)"
            % (percent((count / total)), f.absolute(), file_size(size))
        )
        count += 1
        total_size += size
        f.unlink()
    print("%s cached charts deleted (%s)" % (count, file_size(total_size)))


@charts.cli.command("create")
def create():
    """Create all charts as cache"""

    # support vars
    different_tastes = set()
    count = 0
    total_size = 0

    # get whiskies
    whiskies = Whisky.query.all()
    for whisky in whiskies:
        tastes = tuple(whisky.get_tastes())
        different_tastes.add(tastes)
    total = len(different_tastes) * (len(different_tastes) - 1.0)

    # combination
    for reference in different_tastes:
        for whisky in different_tastes:
            if whisky != reference:
                chart = Chart(reference=reference, comparison=whisky)
                file_name = chart.cache_name(True)
                if file_name.exists():
                    file_name.unlink()
                chart.cache()
                size = file_name.stat().st_size
                total_size += size
                count += 1
                print(
                    "%s Created %s (%s)"
                    % (
                        percent(count / total),
                        file_name.absolute(),
                        file_size(size),
                    )
                )
    print("%s charts created (%s)" % (count, file_size(total)))


@charts.cli.command("list")
def cache():
    """List cached charts"""
    folder_path = (Chart()).cache_path()
    if not folder_path.exists():
        folder_path.mkdir()
    folder = folder_path.glob("*")
    count = 0
    total = 0
    for f in folder:
        if f.is_file():
            size = f.stat().st_size
            print("%s (%s)" % (f.absolute(), file_size(size)))
            count += 1
            total += size
    print("%s cached files (%s)" % (count, file_size(total)))


def file_size(size):
    sizes = {9: "Gb", 6: "Mb", 3: "Kb", 0: "bytes"}
    for i in [9, 6, 3, 0]:
        if size >= 10**i:
            return "{:.1f}".format(size / (10.0**i)) + sizes[i]
    return "0 %s" % sizes[0]


def percent(number):
    return "{:.1f}%".format(number * 100)
