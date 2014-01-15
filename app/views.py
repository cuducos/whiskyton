import random
import json
from flask import Flask, render_template, redirect, Response, request, abort
from slimish_jinja import SlimishExtension
from app import app, models
from sqlalchemy import desc


class MyApp(Flask):
    jinja_options = Flask.jinja_options
    jinja_options = jinja_options['extensions'].append(SlimishExtension)


@app.route('/')
def index():
    rand = random.randrange(1, 87)
    random_one = models.Whisky.query.filter_by(id=rand).first()
    return render_template(
        'home.slim',
        main_title=app.config['MAIN_TITLE'],
        headline=app.config['HEADLINE'],
        ga=app.config['GOOGLE_ANALYTICS'],
        random_one=random_one)


@app.route('/<whisky_slug>')
def whisky_page(whisky_slug):
    if whisky_slug != whisky_slug.lower():
        return redirect('/' + whisky_slug.lower())
    reference = models.Whisky.query.filter_by(ci_index=whisky_slug).first()
    # error page if whisky doesn't exist
    if reference is None:
        return abort(404)
    # load correlations
    else:
        # query
        correlations = models.Correlation.query\
            .filter(
                models.Correlation.reference == reference.id,
                models.Correlation.whisky != reference.id)\
            .order_by(desc('r'))\
            .limit(9)
        # if query succeeded
        whiskies = []
        if correlations is not None:
            for w in correlations:
                # query each whisky
                whisky = models.Whisky.query.filter_by(id=w.whisky).first()
                if whisky is not None:
                    whiskies.append(whisky)
            main_title = 'Whiskies for ' + reference.distillery + ' lovers | '
            main_title = main_title + app.config['MAIN_TITLE']
            return render_template(
                'whiskies.slim',
                main_title=main_title,
                headline=app.config['HEADLINE'],
                ga=app.config['GOOGLE_ANALYTICS'],
                whiskies=whiskies,
                reference=reference)
        # if queries fail, return 404
        else:
            return abort(404)


@app.route('/w/int:whiskyID')
def search(whiskyID):
    reference = models.Whisky.query.filter_by(id=whiskyID).first()
    if reference is None:
        return abort(404)
    else:
        return redirect('/' + reference.ci_index)


@app.route('/search', methods=['GET', 'POST'])
def findID():
    s = request.form['s'].lower()
    whisky = models.Whisky.query.filter_by(ci_index=s).first()
    if whisky is None:
        return abort(404)
    else:
        return redirect('/' + str(whisky.ci_index))


@app.route('/whiskyton.json')
def whisky_list():
    whiskies = models.Whisky.query.all()
    wlist = json.dumps([whisky.distillery for whisky in whiskies])
    resp = Response(
        response=wlist,
        status=200,
        mimetype='application/json')
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.slim',
        main_title=app.config['MAIN_TITLE'],
        headline=app.config['HEADLINE'],
        ga=app.config['GOOGLE_ANALYTICS']), 404
