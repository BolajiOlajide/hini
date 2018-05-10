APP_NAME=hini

# Save dependencies
save_deps:
	pip freeze > requirements.txt

# Start the application
start_dev:
	export FLASK_ENV=development && python main.py runserver

start:
	python main.py runserver

install_deps:
	pip intall -r requirements.txt
