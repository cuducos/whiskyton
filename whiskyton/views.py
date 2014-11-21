# coding: utf-8

import charts
import json
import sitemap as whiskyton_sitemap
import whisky
from flask import abort, redirect, render_template, Response, request, send_from_directory
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from whiskyton import app, models


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    slug = whisky.slugfy(request.args['s'])
    w = models.Whisky.query.filter_by(slug=slug).first()
    if w is None:
        return render_template('404.html', slug=slug)
    else:
        return redirect('/' + str(w.slug))


@app.route('/<whisky_slug>')
def whisky_page(whisky_slug):

    slugfied = whisky.slugfy(whisky_slug)
    if whisky_slug != slugfied:
        return redirect('/' + slugfied)

    reference = models.Whisky.query.filter_by(slug=whisky_slug).first()

    # error page if whisky doesn't exist
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
            return render_template(
                'whiskies.html',
                main_title=title,
                whiskies=whiskies,
                reference=reference,
                count=whiskies.count(),
                result_page=True)

        # if queries fail, return 404
        else:
            return abort(404)


@app.route('/w/<whisky_id>')
def search_id(whisky_id):
    reference = models.Whisky.query.filter_by(id=whisky_id).first()
    if reference is None:
        return abort(404)
    else:
        return redirect('/' + reference.slug)


@app.route('/charts/<reference_slug>-<whisky_slug>.svg')
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
    reference = charts.tastes2list(reference_obj)
    comparison = charts.tastes2list(whisky_obj)
    filename = charts.cache_name(reference, comparison, True)
    if not filename.exists():
        charts.create(reference, comparison)

    # return the chart to the user
    return Response(filename.read_file(), mimetype='image/svg+xml')


@app.route('/whiskyton.json')
def whisky_json():
    whiskies = models.Whisky.query.all()
    distilleries = json.dumps([w.distillery for w in whiskies])
    resp = Response(
        response=distilleries,
        status=200,
        mimetype='application/json')
    return resp


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.config['BASEDIR'], 'robots.txt')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.config['BASEDIR'], 'favicon.ico')


@app.route('/sitemap.xml')
def sitemap():
    whiskies = models.Whisky.query.all()
    last_change = whiskyton_sitemap.most_recent_update()
    return render_template(
        'sitemap.xml',
        whiskies=whiskies,
        last_change=last_change,
        url_root=request.url_root)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.context_processor
def inject_main_vars():
    return {
        'main_title': app.config['MAIN_TITLE'],
        'headline': app.config['HEADLINE'],
        'remote_scripts': app.config['GOOGLE_ANALYTICS'],
        'random_one': models.Whisky.query.order_by(func.random()).first()
    }