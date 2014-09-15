import charts
import datetime
import json
import os
import whisky
from flask import render_template, redirect, Response, request, abort
from flask import make_response
from sqlalchemy import desc
from whiskyton import app, models


@app.route('/')
def index():
    random_one = whisky.random_whisky()
    return render_template(
        'home.html',
        main_title=app.config['MAIN_TITLE'],
        headline=app.config['HEADLINE'],
        remote_scripts=app.config['GOOGLE_ANALYTICS'],
        random_one=random_one)


@app.route('/search', methods=['GET', 'POST'])
def search():
    slug = whisky.slugfy(request.args['s'])
    w = models.Whisky.query.filter_by(slug=slug).first()
    if w is None:
        random_one = whisky.random_whisky()
        return render_template(
            '404.html',
            main_title=app.config['MAIN_TITLE'],
            headline=app.config['HEADLINE'],
            remote_scripts=app.config['GOOGLE_ANALYTICS'],
            slug=slug,
            random_one=random_one)
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
                headline=app.config['HEADLINE'],
                remote_scripts=app.config['GOOGLE_ANALYTICS'],
                whiskies=whiskies,
                reference=reference,
                count=whiskies.count(),
                result_page=True)

        # if queries fail, return 404
        else:
            return abort(404)


@app.route('/w/<whiskyID>')
def searchID(whiskyID):
    reference = models.Whisky.query.filter_by(id=whiskyID).first()
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
    distilleries = json.dumps([whisky.distillery for whisky in whiskies])
    resp = Response(
        response=distilleries,
        status=200,
        mimetype='application/json')
    return resp


@app.route('/robots.txt', methods=['GET'])
def robots():
    robots = app.config['BASEDIR'].child('robots.txt').read_file()
    response = make_response(robots)
    response.headers["Content-type"] = "text/plain"
    return response


@app.route('/sitemap.xml')
def sitemap():
    whiskies = models.Whisky.query.all()
    ref_file = 'whiskyton/views.py'
    dt_unix = int(os.path.getmtime(ref_file))
    last_change = datetime.datetime.fromtimestamp(dt_unix).strftime('%Y-%m-%d')
    return render_template(
        'sitemap.xml',
        whiskies=whiskies,
        last_change=last_change,
        url_root=request.url_root)


@app.errorhandler(404)
def page_not_found(e):
    random_one = whisky.random_whisky()
    return render_template(
        '404.html',
        main_title=app.config['MAIN_TITLE'],
        headline=app.config['HEADLINE'],
        remote_scripts=app.config['GOOGLE_ANALYTICS'],
        random_one=random_one), 404
