Whiskython
==========

* **Official page**: [http://whiskyton.herokuapp.com/](http://whiskyton.herokuapp.com/)
* **Authors**: [Eduardo Cuducos](http://cuducos.me) and [Gabriel Vicente](http://about.me/gabrielvicente)

About
-----

This web based app uses [an open database about whisky](https://www.mathstat.strath.ac.uk/outreach/nessie/nessie_whisky.html) to help you find whiskys you'd probably like. It uses mathematics to run through the tastes classified in that database, and to find the best matches. We were inspired by [this data visualization shared on Reddit](http://www.reddit.com/r/dataisbeautiful/comments/1u747v/flavor_profiles_for_86_scotch_whiskies/).

What really matters
-------------------

This is our very first project in Python (and we are not professional coders) -- so all feedback is important to help us through our learning process. **Don't hesitate to criticize our code and software design!** To be true, that is what we are expecting :)

Installation
------------

1. Clone the repository: `$ git clone git@github.com:cuducos/whiskyton.git`.

2. Go to the repository folder: `$ cd whiskyton` (if you want, get your [virtualenv](https://pypi.python.org/pypi/virtualenv) running there).

4. Install the dependencies: `$ pip install -r requirements.txt`.

5. You should have the `coffee` command line tool working: probably `$ apt-get install nodejs` and `$ npm install coffee-script` should do the job.  

5. Create and feed the database: `$ python manage.py db upgrade`.

6. Run the server: `$ python manage.py runserver`.

If you wanna deploy to [Heroku](http://heroku.com), you need to use [heroku-buildpack-multi](https://github.com/heroku/heroku-buildpack-multi).


Tests
-----

To run tests:

```
$ nosetests
```

[Nose](https://nose.readthedocs.org/en/latest/) does not run tests in executable files. If that is the case, run:

```
$ chmod -x $(find whiskyton/tests/ -name '*.py')
```

Managing the charts cache
-------------------------

If you want to get rid of all the cached SVG charts: `$ python manage.py charts delete`.

If you want to create all possible charts and cache the SVG files: `$ python manage.py charts create` (it is not necessary, the app creates and caches them on the fly; however pre-caching them can optimize page loading time).


Thanks
------

We had a lot of Python teachers, we are so glad we could count on you, guys:

* Joe Warren, Scott Rixner, John Greiner and Stephen Wong, from the [An Introduction to Interactive Programming in Python](https://www.coursera.org/course/interactivepython) course at [Coursera](https://www.coursera.org/)
* Allen B. Downey and Jeff Elkner, authors of [Think Python: How to Think Like a Computer Scientist](http://www.greenteapress.com/thinkpython/thinkpython.html)
* Miguel Grinberg and his [The Flask Mega-Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* Everyone who have ever contributed to [The Hitchhiker’s Guide to Python!](http://docs.python-guide.org/en/latest/)
* Everyone who helped at Reddit, mainly these guys [here](http://www.reddit.com/r/webdev/comments/1uec51/a_dinosaur_wants_to_code/) and [here](http://www.reddit.com/r/Python/comments/1rnfle/setting_up_a_web_development_environment/)

In sum, we had the best teachers of the world in Python. Any mistake here is completely our fault.

License
-------
Copyright (c) 2014 Eduardo Cuducos and Gabriel Vicente

Licensed under the MIT license (see [MIT-LICENSE file](https://github.com/cuducos/whiskyton/raw/master/MIT-LICENSE))
