# coding: utf-8

import whiskyton.helpers.sitemap as whiskyton_sitemap
from flask import (
    abort, Blueprint, jsonify, redirect, render_template,
    request, Response, send_from_directory
)
from whiskyton import app, models
from whiskyton.helpers import charts, whisky

files_blueprint = Blueprint('files', __name__)


@files_blueprint.route('/charts/<reference_slug>-<whisky_slug>.svg')
def create_chart(reference_slug, whisky_slug):

    # URL check
    slug1 = whisky.slugfy(whisky_slug)
    slug2 = whisky.slugfy(reference_slug)
    if slug1 != whisky_slug or slug2 != reference_slug:
        return redirect('/charts/%s-%s.svg' % (slug1, slug2))

    # get whisky objects form db
    reference_obj = models.Whisky.query.filter_by(slug=reference_slug).first()
    whisky_obj = models.Whisky.query.filter_by(slug=whisky_slug).first()

    # error page if whisky doesn't exist
    if reference_obj is None or whisky_obj is None:
        return abort(404)

    # if file does not exists, create it
    reference = whisky.get_tastes(reference_obj)
    comparison = whisky.get_tastes(whisky_obj)
    filename = charts.cache_name(reference, comparison, True)
    if not filename.exists():
        charts.create(reference, comparison)

    # return the chart to the user
    return Response(filename.read_file(), mimetype='image/svg+xml')


@files_blueprint.route('/static/fonts/glyphicons-halflings-regular.<extension>')
def bootstrap_fonts(extension=None):
    basedir = app.config['BASEDIR']
    path = basedir.child('whiskyton', 'bower', 'bootstrap', 'dist', 'fonts')
    filename = 'glyphicons-halflings-regular.{}'.format(extension)
    if path.child(filename).exists():
        return send_from_directory(path, filename)
    else:
        abort(404)


@files_blueprint.route('/whiskyton.json')
def whisky_json():
    whiskies = models.Whisky.query.all()
    return jsonify(whiskies=[w.distillery for w in whiskies])


@files_blueprint.route('/robots.txt')
def robots():
    basedir = app.config['BASEDIR']
    return send_from_directory(
        basedir.child('whiskyton', 'static'),
        'robots.txt'
    )


@files_blueprint.route('/favicon.ico')
def favicon():
    basedir = app.config['BASEDIR']
    return send_from_directory(
        basedir.child('whiskyton', 'static'),
        'favicon.ico'
    )


@files_blueprint.route('/sitemap.xml')
def sitemap():
    whiskies = models.Whisky.query.all()
    last_change = whiskyton_sitemap.most_recent_update()
    return render_template(
        'sitemap.xml',
        whiskies=whiskies,
        last_change=last_change,
        url_root=request.url_root)
