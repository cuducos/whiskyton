# Whiskython

By [Eduardo Cuducos](http://cuducos.me) and [Gabriel Vicente](https://g4brielvs.me).

## About

This was our very first project in Python, back in 2014. 10 years later, the idea is to use that as a playground to explore Rust bindings in Python projetcs.

<details>

This web based app uses [an open database about whisky](https://www.mathstat.strath.ac.uk/outreach/nessie/nessie_whisky.html) to help you find whiskys you'd probably like. It uses mathematics to run through the tastes classified in that database, and to find the best matches. We were inspired by [this data visualization shared on Reddit](http://www.reddit.com/r/dataisbeautiful/comments/1u747v/flavor_profiles_for_86_scotch_whiskies/).

### Thanks

We had a lot of Python teachers, we are so glad we could count on you, guys:

* Joe Warren, Scott Rixner, John Greiner and Stephen Wong, from the [An Introduction to Interactive Programming in Python](https://www.coursera.org/course/interactivepython) course at [Coursera](https://www.coursera.org/)
* Allen B. Downey and Jeff Elkner, authors of [Think Python: How to Think Like a Computer Scientist](http://www.greenteapress.com/thinkpython/thinkpython.html)
* Miguel Grinberg and his [The Flask Mega-Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* Everyone who have ever contributed to [The Hitchhiker’s Guide to Python!](http://docs.python-guide.org/en/latest/)
* Everyone who helped at Reddit, mainly these guys [here](http://www.reddit.com/r/webdev/comments/1uec51/a_dinosaur_wants_to_code/) and [here](http://www.reddit.com/r/Python/comments/1rnfle/setting_up_a_web_development_environment/)

In sum, we had the best teachers of the world in Python. Any mistake here is completely our fault.

Also we are glad to have contributions from [Henrique Bastos](http://github.com/henriquebastos), [Lucretiel](http://github.com/Lucretiel), [Justin Velluppillai](http://github.com/justinvelluppillai) and [Chris Loverchio](http://github.com/cloverchio).

</details>

## Installation

Depends on [Python](https://python.org) 3.12 (or newer), [Poetry](https://python-poetry.org) and [Rust](https://www.rust-lang.org).

### Install the Python dependencies

```console
$ poetry install
```

### Install the Rust `crates`

```console
$ poetry run pip install .
```

## Web server

```console
$ poetry run flask --app whiskyton run
```

## Tests

To run tests:

```console
$ cargo test --no-default-features
$ poetry run pytest
```

Some tests use your local [Firefox](http://mozilla.org/firefox/) through [Selenium](http://www.seleniumhq.org/). So get the server running before running tests. If you do not want to run UI tests, use `-k 'not ui'`.
