APP_NAME=hini

# Save dependencies
freeze:
	pip freeze > requirements.txt

# Start the application
start_dev:
	export FLASK_ENV=development && export OAUTHLIB_INSECURE_TRANSPORT=1 && python main.py runserver

start:
	gunicorn -w 6 -b 0.0.0.0 main:app

install_deps:
	pip intall -r requirements.txt

db_prepare:
	python main.py db migrate && python main.py db upgrade
