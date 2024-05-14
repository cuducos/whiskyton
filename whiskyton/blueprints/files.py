from io import BytesIO

from crates import all_whiskies, asset, latest_changed_at
from flask import (
    Blueprint,
    abort,
    current_app,
    render_template,
    request,
    send_file,
)

files = Blueprint("files", __name__)


@files.route("/style.css")
@files.route("/app.js")
@files.route("/whiskyton.json")
@files.route("/robots.txt")
@files.route("/favicon.ico")
def assets():
    try:
        contents, mime = asset(request.path.removeprefix("/"))
    except ValueError:
        abort(404)

    return send_file(BytesIO(contents), mimetype=mime)


@files.route("/sitemap.xml")
def sitemap():
    return render_template(
        "sitemap.xml",
        whiskies=(slug for _, slug, _, _ in all_whiskies()),
        last_change=latest_changed_at(str(current_app.config["BASEDIR"])),
        url_root=request.url_root,
    )
