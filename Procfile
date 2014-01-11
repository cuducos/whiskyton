web: gunicorn runp-heroku:app
init: python db_create.py && python db_migrate.py && python db_add_whisky_data.py && python db_add_correlations.py
