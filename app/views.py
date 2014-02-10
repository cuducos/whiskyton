import json
from flask import Flask, render_template, redirect, Response, request, abort
from app import app, models
from sqlalchemy import desc
from sqlalchemy.sql.expression import func, select

@app.route('/')
def index():
    random_one = random_whisky()
    return render_template(
        'home.html',
        main_title=app.config['MAIN_TITLE'],
        headline=app.config['HEADLINE'],
        remote_scripts=app.config['GOOGLE_ANALYTICS'],
        random_one=random_one)


@app.route('/<whisky_slug>')
def whisky_page(whisky_slug):
    if whisky_slug != whisky_slug.lower():
        return redirect('/' + whisky_slug.lower())
    reference = models.Whisky.query.filter_by(slug=whisky_slug).first()
    # error page if whisky doesn't exist
    if reference is None:
        return abort(404)
    # load correlations
    else:
        # query
        correlations = models.Correlation.query\
            .filter(
                models.Correlation.reference == reference.id,
                models.Correlation.whisky != reference.id,
                models.Correlation.r > 0.5)\
            .order_by(desc('r'))\
            .limit(9)
        # if query succeeded
        whiskies = []
        if correlations is not None:
            for w in correlations:
                # query each whisky
                whisky = models.Whisky.query.filter_by(id=w.whisky).first()
                if whisky is not None:
                    whisky.r = '{0:.0f}'.format(w.r * 100) + '%'
                    whiskies.append(whisky)
            main_title = 'Whiskies for ' + reference.distillery + ' lovers | '
            main_title = main_title + app.config['MAIN_TITLE']
            return render_template(
                'whiskies.html',
                main_title=main_title,
                headline=app.config['HEADLINE'],
                remote_scripts=app.config['GOOGLE_ANALYTICS'],
                whiskies=whiskies,
                reference=reference,
                count=str(len(whiskies)),
                result_page=True)
        # if queries fail, return 404
        else:
            return abort(404)


@app.route('/w/int:whiskyID')
def search(whiskyID):
    reference = models.Whisky.query.filter_by(id=whiskyID).first()
    if reference is None:
        return abort(404)
    else:
        return redirect('/' + reference.slug)


@app.route('/search', methods=['GET', 'POST'])
def findID():
    slug = request.form['s'].lower().replace(' ','').replace('/','')
    whisky = models.Whisky.query.filter_by(slug=slug).first()
    if whisky is None:
        return abort(404)
    else:
        return redirect('/' + str(whisky.slug))


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
    random_one = random_whisky()
    return render_template(
        '404.html',
        main_title=app.config['MAIN_TITLE'],
        headline=app.config['HEADLINE'],
        remote_scripts=app.config['GOOGLE_ANALYTICS'],
        random_one=random_one), 404

def random_whisky():
    random_one = models.Whisky.query.order_by(func.random()).first()
    return random_one
