from flask import (
    Blueprint,
    Response,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

import whiskyton.helpers.sitemap as whiskyton_sitemap
from whiskyton import app, models
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
    return Response(filename.read_file(), mimetype="image/svg+xml")


@files.route("/whiskyton.json")
def whisky_json():
    whiskies = models.Whisky.query.all()
    return jsonify(whiskies=[w.distillery for w in whiskies])


@files.route("/robots.txt")
def robots():
    basedir = app.config["BASEDIR"]
    return send_from_directory(basedir.child("whiskyton", "static"), "robots.txt")


@files.route("/favicon.ico")
def favicon():
    basedir = app.config["BASEDIR"]
    return send_from_directory(basedir.child("whiskyton", "static"), "favicon.ico")


@files.route("/sitemap.xml")
def sitemap():
    whiskies = models.Whisky.query.all()
    last_change = whiskyton_sitemap.most_recent_update()
    return render_template(
        "sitemap.xml",
        whiskies=whiskies,
        last_change=last_change,
        url_root=request.url_root,
    )
