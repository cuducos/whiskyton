web: gunicorn runp-heroku:app
init: python db_create.py
upgrade: python db_upgrade.py && python db_add_whisky_data.py && python db_add_correlations.py
