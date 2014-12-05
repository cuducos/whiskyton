# coding: utf-8

from flask import abort, Blueprint, redirect, render_template, request
from htmlmin.minify import html_minify
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from whiskyton import app, models

site_blueprint = Blueprint('site', __name__)


@site_blueprint.route('/')
def index():
    return html_minify(render_template('home.html'))


@site_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    whisky = models.Whisky(distillery=request.args['s'])
    row = models.Whisky.query.filter_by(slug=whisky.get_slug()).first()
    if row is None:
        return render_template('404.html', slug=whisky)
    else:
        return redirect('/' + str(row.slug))


@site_blueprint.route('/<whisky_slug>')
def whisky_page(whisky_slug):

    # error page if whisky doesn't exist
    reference = models.Whisky.query.filter_by(slug=whisky_slug).first()
    if reference is None:
        return abort(404)

    # load correlations
    else:

        # query
        whiskies = models.Correlation.query\
            .add_entity(models.Whisky)\
            .filter(models.Correlation.reference == reference.id)\
            .filter(models.Correlation.r > 0.5)\
            .join(models.Whisky, models.Correlation.whisky == models.Whisky.id)\
            .order_by(desc(models.Correlation.r))\
            .limit(9)

        # if query succeeded
        if whiskies is not None:

            # build result
            title = 'Whiskies for %s lovers | %s' % (reference.distillery,
                                                     app.config['MAIN_TITLE'])
            return html_minify(render_template(
                'whiskies.html',
                main_title=title,
                whiskies=whiskies,
                reference=reference,
                count=whiskies.count(),
                result_page=True
            ))

        # if queries fail, return 404
        else:
            return abort(404)


@site_blueprint.route('/w/<whisky_id>')
def search_id(whisky_id):
    reference = models.Whisky.query.filter_by(id=whisky_id).first()
    if reference is None:
        return abort(404)
    else:
        return redirect('/' + reference.slug)


@site_blueprint.errorhandler(404)
def page_not_found(error):
    return html_minify(render_template('404.html', error=error)), 404


@site_blueprint.context_processor
def inject_main_vars():
    return {
        'main_title': app.config['MAIN_TITLE'],
        'headline': app.config['HEADLINE'],
        'remote_scripts': app.config['GOOGLE_ANALYTICS'],
        'random_one': models.Whisky.query.order_by(func.random()).first()
    }