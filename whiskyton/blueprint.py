from functools import lru_cache
from io import BytesIO

from crates import (
    asset,
    random_whisky,
    recommendations_for,
    render_sitemap,
)
from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    send_file,
)

from whiskyton.models import Whisky

site = Blueprint("site", __name__)


@lru_cache(maxsize=128)
def whiskies_for(slug):
    try:
        data = recommendations_for(slug)
    except ValueError:
        return
    return Whisky(*data)


@site.route("/")
def index():
    return render_template("home.html")


@site.route("/search")
def search():
    name = request.args["s"]
    whisky = whiskies_for(name)
    if not whisky:
        return render_template("404.html", slug=name)
    return redirect(f"/{whisky.slug}")


@site.route("/<slug>")
def whisky_page(slug):
    whisky = whiskies_for(slug)
    if not whisky:
        return abort(404)
    return render_template("whiskies.html", whisky=whisky, result_page=True)


@site.route("/style.css")
@site.route("/app.js")
@site.route("/whiskyton.json")
@site.route("/robots.txt")
@site.route("/favicon.ico")
def assets():
    try:
        contents, mime = asset(request.path.removeprefix("/"))
    except ValueError:
        abort(404)

    return send_file(BytesIO(contents), mimetype=mime)


@site.route("/sitemap.xml")
def sitemap():
    contents = render_sitemap(request.url_root, str(current_app.config["BASEDIR"]))
    return send_file(BytesIO(contents), mimetype="application/xml")


@site.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


@site.context_processor
def inject_main_vars():
    whisky = Whisky(*random_whisky())
    return {
        "main_title": current_app.config["MAIN_TITLE"],
        "headline": current_app.config["HEADLINE"],
        "random_one": whisky,
    }
