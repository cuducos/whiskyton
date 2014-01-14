import random, json
from flask import Flask, render_template, redirect, Response, request
from slimish_jinja import SlimishExtension
from app import app, models
from sqlalchemy import desc

class MyApp(Flask):
  jinja_options = Flask.jinja_options
  jinja_options = jinja_options['extensions'].append(SlimishExtension)

@app.route('/')
def index():
  rand = random.randrange(1,87) 
  random_one = models.Whisky.query.filter_by(id = rand).first()
  return render_template('home.slim',
    main_title = app.config['MAIN_TITLE'],
    headline = app.config['HEADLINE'],
    ga = app.config['GOOGLE_ANALYTICS'],
    random_one = random_one)
    
@app.route('/404')
def page_not_found():
  return render_template('404.slim',
    main_title = app.config['MAIN_TITLE'],
    headline = app.config['HEADLINE'],
        ga = app.config['GOOGLE_ANALYTICS'])

@app.route('/w/<whiskyID>')
def search(whiskyID): 
  # check if whisky exists
  whiskyID = int(whiskyID)
  reference = models.Whisky.query.filter_by(id = whiskyID).first()
  # error page if whisky doesn't exist
  if reference == None :
    return redirect('/404')
  # loag correlations
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
    if correlations != None: 
      for w in correlations:
        # query each whisky
        whisky = models.Whisky.query.filter_by(id = w.whisky).first()
        if whisky != None:
          whiskies.append(whisky)
      return render_template('whiskies.slim',
        main_title = 'Whiskies for ' + reference.distillery + ' lovers | ' + app.config['MAIN_TITLE'],
        headline = app.config['HEADLINE'],
        ga = app.config['GOOGLE_ANALYTICS'],
        whiskies = whiskies,
        reference = reference)        
    # if queries fail, return 404
    else:
      return redirect('/404')

@app.route('/search', methods = ['GET', 'POST'])
def findID():
  s = request.form['s'].lower()
  whisky = models.Whisky.query.filter_by(ci_index = s).first()
  if whisky == None:
    return redirect('/404')
  else:
    return redirect('/w/' + str(whisky.id))

@app.route('/whiskyton.json')
def whisky_list():
  whiskies = models.Whisky.query.all()
  wlist = json.dumps([whisky.distillery for whisky in whiskies])
  resp = Response( response = wlist, status = 200, mimetype='application/json')
  return resp
