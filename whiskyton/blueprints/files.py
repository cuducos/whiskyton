from crates import all_whiskies, latest_changed_at
from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

files = Blueprint("files", __name__)


@files.route("/whiskyton.json")
def whisky_json():
    return jsonify(whiskies=tuple(distillery for distillery, _, _ in all_whiskies()))


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
    return render_template(
        "sitemap.xml",
        whiskies=(slug for _, slug, _ in all_whiskies()),
        last_change=latest_changed_at(str(current_app.config["BASEDIR"])),
        url_root=request.url_root,
    )
