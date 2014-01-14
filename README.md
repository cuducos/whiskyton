Whiskython
==========

* **Oficial page**: [http://whiskyton.herokuapp.com/](http://whiskyton.herokuapp.com/)
* **Version**: 0.0.1 (Jan. 11h 2014)
* **Authors**: [Eduardo Cuducos](http://about.me/cuducos) and [Gabriel Vicente](http://about.me/gabrielvicente)

About
-----

This web based app uses [an open database about whisky](https://www.mathstat.strath.ac.uk/outreach/nessie/nessie_whisky.html) to help you find whiskys you'd probably like. It uses mathematics to run through the tastes classified in that database, and to find the best macthes. We were inspired by [this data visualization shared on Reddit](http://www.reddit.com/r/dataisbeautiful/comments/1u747v/flavor_profiles_for_86_scotch_whiskies/).

What really matters
-------------------

It is our very first project in Python (and we are not professional coders) -- so every feedback is important to help us through our learning process. **Don't hesitate to criticize our code and software design!** To be true, that is what we are expecting :)

Instalation
-----------

Get your [virtualenv](https://pypi.python.org/pypi/virtualenv) and [PostgreSQL](http://postgresql.org/) running.

Check if the access data to your local PostgreSQL server (user, password and database) is correct at `config.py` (first instance of the variable `SQLALCHEMY_DATABASE_URI`; the second instance is set to work under Heroku server).

Install the following extensions:

```
$ pip install Flask==0.9
$ pip install Flask-SQLAlchemy==0.16
$ pip install slimish-jinja==1.0.2
$ pip install SQLAlchemy==0.7.9
$ pip install sqlalchemy-citext==1.2-0
$ pip install sqlalchemy-migrate==0.7.2
```

If you already have an old version of Whiskython database, drop it:

```
$ ./db_drop_tables.py
```

Then run the following commands (you might have to give the right permissions to each file by typing `chmod a+x [filename]`, otherwise you won't be able to execiute them):

```
$ ./db_create.py
$ ./db_migrate.py
$ ./db_add_whisky_data.py
$ ./db_add_correlations.py
```

Finally `./run.py` to start your server.

Thanks
------

We had a lot of Python teachers, we are so glad we could count on you, guys:

* Joe Warren, Scott Rixner, John Greiner and Stephen Wong, from the [An Introduction to Interactive Programming in Python](https://www.coursera.org/course/interactivepython) course at [Coursera](https://www.coursera.org/)
* Allen B. Downey and Jeff Elkner, authors of [Think Python: How to Think Like a Computer Scientist](http://www.greenteapress.com/thinkpython/thinkpython.html)
* Miguel Grinberg and his [The Flask Mega-Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* Everyone who have ever contributed to [The Hitchhiker’s Guide to Python!](http://docs.python-guide.org/en/latest/)
* Everyone who helped at Reddit, mainly these guys [here](http://www.reddit.com/r/webdev/comments/1uec51/a_dinosaur_wants_to_code/) and [here](http://www.reddit.com/r/Python/comments/1rnfle/setting_up_a_web_development_environment/) 

In sum, we had the best teachers of the world in the Python. Any mistake here is completely our fault. 

License, copyright and shit
---------------------------

Do whatever you want with these code, but try to remember to mention the source.
