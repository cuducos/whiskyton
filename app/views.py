import json
import math
import os
from flask import render_template, redirect, Response, request, abort
from flask import make_response
from app import app, models
from slimmer import xhtml_slimmer
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


@app.route('/charts/<reference_slug>-<whisky_slug>.svg')
def create_chart(reference_slug, whisky_slug):

    # URL check
    cond1 = whisky_slug != whisky_slug.lower()
    cond2 = reference_slug != reference_slug.lower()
    if cond1 or cond2:
        return redirect('/' + whisky_slug.lower())

    reference_obj = models.Whisky.query.filter_by(slug=reference_slug).first()
    whisky_obj = models.Whisky.query.filter_by(slug=whisky_slug).first()

    # error page if whisky doesn't exist
    if reference_obj is None or whisky_obj is None:
        return abort(404)

    # get whisky data
    tastes_labels = (
        'spicy',
        'honey',
        'tobacco',
        'medicinal',
        'smoky',
        'sweetness',
        'body',
        'floral',
        'fruity',
        'malty',
        'nutty',
        'winey')
    reference = []
    comparison = []
    for taste in tastes_labels:
        reference.append(eval('reference_obj.' + taste))
        comparison.append(eval('whisky_obj.' + taste))

    # name for caching
    filename = ''
    for taste in reference:
        filename += str(taste)
    filename += 'x'
    for taste in comparison:
        filename += str(taste)
    filename += '.svg'

    # check if file exists
    basedir = os.path.abspath(os.path.dirname(__file__))
    charts_dir = basedir + '/static/charts/'
    try:
        os.stat(charts_dir)
    except:
        os.mkdir(charts_dir)
    filepath = charts_dir + filename

    # if file does not exists, create it
    if not os.path.isfile(filepath):

        # basic variables for the chart
        sides = 12
        width = 330
        height = 260
        margin = 60
        scales = 4

        # calc other basic values for the chart
        radius = (width-(2*margin))/2
        angle_adjust = ((2*math.pi/sides))/2
        interval = radius / scales

        # variables for drawing
        polygon_coordinates = []
        text_coordinates = []
        reference_coordinates = []
        whisky_coordinates = []
        center_x = width / 2
        center_y = height / 2

        # calculate the coordinates of the grid
        for scale in range(0, scales):
            output = []
            for x in range(0, sides):
                angle = ((2*math.pi/sides)*x) - angle_adjust
                r = radius - (scale * interval)
                a = center_x + (math.sin(angle)*r)
                b = center_y + (math.cos(angle)*r)
                output.append([int(a), int(b)])
            polygon_coordinates.append(output)

        # calculate the position of text
        text_count = 0
        text_line_height = 11

        for coordinates in polygon_coordinates[0]:

            a = coordinates[0]
            b = coordinates[1]

            top = [6, 7]
            right = [2, 3, 4, 5]
            bottom = [0, 1]
            left = [8, 9, 10, 11]
            diagonal_down = [2, 11]
            diagonal_up = [5, 8]
            sub_diagonal_down = [3, 10]

            if text_count in top:
                b -= text_line_height * 0.75
            if text_count in right:
                a += text_line_height * 0.75
            if text_count in bottom:
                b += text_line_height * 1.5
            if text_count in left:
                a -= text_line_height * 0.75
            if text_count in diagonal_up:
                b -= text_line_height * 0.5
            if text_count in diagonal_down:
                b += text_line_height * 0.75
            if text_count in sub_diagonal_down:
                b += text_line_height * 0.25

            text_anchor = 'start'
            if text_count in top or text_count in bottom:
                text_anchor = 'middle'
            if text_count in left:
                text_anchor = 'end'

            taste = tastes_labels[text_count]
            taste = taste[0].upper() + taste[1:]

            text_coordinates.append([int(a), int(b), text_anchor, taste])
            text_count += 1

            # calculate the coordinate of the reference data
            taste_count = 0
            for taste in reference:
                taste = abs(taste - 4)
                if taste == 4:
                    reference_coordinates.append([center_x, center_y])
                else:
                    polygon = polygon_coordinates[taste]
                    point = polygon[taste_count]
                    reference_coordinates.append(point)
                taste_count += 1

            # calculate the coordinate of the comparison data
            taste_count = 0
            for taste in comparison:
                taste = abs(taste - 4)
                if taste == 4:
                    whisky_coordinates.append([center_x, center_y])
                else:
                    polygon = polygon_coordinates[taste]
                    point = polygon[taste_count]
                    whisky_coordinates.append(point)
                taste_count += 1

            # generate the svg
            svg_image = render_template(
                'chart.svg',
                polygon_coordinates=polygon_coordinates,
                text_coordinates=text_coordinates,
                reference_coordinates=reference_coordinates,
                whisky_coordinates=whisky_coordinates,
                center_x=center_x,
                center_y=center_y)
            svg_compressed = xhtml_slimmer(svg_image)

            # save the file
            new_chart = open(filepath, 'w+')
            new_chart.write(svg_compressed)
            new_chart.close()

    # return the chart to the user
    content = open(filepath).read()
    return Response(content, mimetype='image/svg+xml')


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
