from functools import lru_cache

from crates import random_whisky, recommendations_for
from flask import Blueprint, abort, current_app, redirect, render_template, request

from whiskyton.models import Correlation, Whisky

site = Blueprint("site", __name__)


@lru_cache(maxsize=128)
def whiskies_for(slug):
    try:
        return tuple(Correlation(*args) for args in recommendations_for(slug))
    except ValueError:
        pass


@site.route("/")
def index():
    return render_template("home.html")


@site.route("/search")
def search():
    name = request.args["s"]
    correlations = whiskies_for(name)
    if not correlations:
        return render_template("404.html", slug=name)

    return redirect(f"/{correlations[0].reference.slug}")


@site.route("/<slug>")
def whisky_page(slug):
    correlations = whiskies_for(slug)
    if not correlations:
        return abort(404)

    reference = correlations[0].reference.distillery
    title = f"Whiskies for {reference} lovers | {current_app.config['MAIN_TITLE']}"
    return render_template(
        "whiskies.html",
        main_title=title,
        correlations=correlations,
        reference=reference,
        count=len(correlations),
        result_page=True,
    )


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
