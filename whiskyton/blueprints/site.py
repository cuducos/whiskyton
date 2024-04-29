from random import choice

from flask import Blueprint, abort, current_app, redirect, render_template, request
from sqlalchemy import desc

from whiskyton.models import Correlation, Whisky, db

site = Blueprint("site", __name__)


@site.route("/")
def index():
    return render_template("home.html")


@site.route("/search", methods=["GET", "POST"])
def search():
    whisky = Whisky(distillery=request.args["s"])
    row = Whisky.query.filter_by(slug=whisky.get_slug()).first()
    if row is None:
        return render_template("404.html", slug=request.args["s"])
    else:
        return redirect("/" + str(row.slug))


@site.route("/<whisky_slug>")
def whisky_page(whisky_slug):
    # error page if whisky doesn't exist
    reference = Whisky.query.filter_by(slug=whisky_slug).first()
    if reference is None:
        return abort(404)

    # load correlations
    else:
        # query
        whiskies = (
            Correlation.query.add_entity(Whisky)
            .filter(Correlation.reference == reference.id)
            .filter(Correlation.r > 0.5)
            .join(Whisky, Correlation.whisky == Whisky.id)
            .order_by(desc(Correlation.r))
            .limit(9)
        )

        # if query succeeded
        if whiskies is not None:
            title = "Whiskies for %s lovers | %s" % (
                reference.distillery,
                current_app.config["MAIN_TITLE"],
            )
            return render_template(
                "whiskies.html",
                main_title=title,
                whiskies=whiskies,
                reference=reference,
                count=whiskies.count(),
                result_page=True,
            )

        # if queries fail, return 404
        else:
            return abort(404)


@site.route("/w/<whisky_id>")
def search_id(whisky_id):
    reference = Whisky.query.filter_by(id=whisky_id).first()
    if reference is None:
        return abort(404)
    else:
        return redirect("/" + reference.slug)


@site.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


@site.context_processor
def inject_main_vars():
    return {
        "main_title": current_app.config["MAIN_TITLE"],
        "headline": current_app.config["HEADLINE"],
        "random_one": choice(db.session.query(Whisky).all()),
    }
