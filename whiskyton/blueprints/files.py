from crates import latest_changed_at
from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

from whiskyton import models
from whiskyton.helpers.charts import Chart

files = Blueprint("files", __name__)


@files.route("/charts/<reference_slug>-<whisky_slug>.svg")
def create_chart(reference_slug, whisky_slug):
    # get whisky objects form db
    reference_obj = models.Whisky.query.filter_by(slug=reference_slug).first()
    whisky_obj = models.Whisky.query.filter_by(slug=whisky_slug).first()

    # error page if whisky doesn't exist
    if reference_obj is None or whisky_obj is None:
        return abort(404)

    # if file does not exists, create it
    chart = Chart(reference=reference_obj, comparison=whisky_obj)
    filename = chart.cache_name(True)
    if not filename.exists():
        chart.cache()

    # return the chart to the user
    return Response(filename.read_text(), mimetype="image/svg+xml")


@files.route("/whiskyton.json")
def whisky_json():
    whiskies = models.Whisky.query.all()
    return jsonify(whiskies=[w.distillery for w in whiskies])


@files.route("/robots.txt")
def robots():
    basedir = current_app.config["BASEDIR"]
    return send_from_directory((basedir / "whiskyton" / "static"), "robots.txt")


@files.route("/favicon.ico")
def favicon():
    basedir = current_app.config["BASEDIR"]
    return send_from_directory((basedir / "whiskyton" / "static"), "favicon.ico")


@files.route("/sitemap.xml")
def sitemap():
    whiskies = models.Whisky.query.all()
    return render_template(
        "sitemap.xml",
        whiskies=whiskies,
        last_change=latest_changed_at(str(current_app.config["BASEDIR"])),
        url_root=request.url_root,
    )
