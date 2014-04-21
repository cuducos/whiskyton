import json
from flask import render_template, redirect, Response, request, abort
from flask import make_response
from app import app, models
from sqlalchemy import desc, or_
from sqlalchemy.sql.expression import func


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
                or_(models.Correlation.reference == reference.id,
                    models.Correlation.whisky == reference.id),              
                models.Correlation.r > 0.5)\
            .order_by(desc('r'))\
            .limit(9)

        # if query succeeded
        whiskies = []
        if correlations is not None:

            # query each whisky
            for corr in correlations:
                
                # check if whisky or reference holds the correlated ID
                search_for = corr.whisky
                if reference.id == corr.whisky:
                    search_for = corr.reference
                
                # query
                whisky = models.Whisky.query.filter_by(id=search_for).first()
                if whisky is not None:
                    whisky.r = '{0:.0f}'.format(corr.r * 100) + '%'
                    whiskies.append(whisky)
            
            # build result
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
    slug = request.form['s'].lower().replace(' ', '').replace('/', '')
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


@app.route('/robots.txt', methods=['GET'])
def sitemap():
    response = make_response(open('robots.txt').read())
    response.headers["Content-type"] = "text/plain"
    return response


def random_whisky():
    random_one = models.Whisky.query.order_by(func.random()).first()
    return random_one
