
# configure env
env:
	python3 -m venv ~/pyenvs/pod6

# activate the environemnt (it does not work. Here just to remember)
activate:
	# source ~/pyenvs/pod6/bin/activate

# install pip and requirements
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# install dev
install_dev:
	pip install -e '.[dev]'

# format the code using python black
format:
	# black *.py

# Lint
lint:
	pylint life_expectancy.life_expectancy
	#life_expectancy.cleaning_with_class
	# pylint --disable=R,C hello.py

# Testing
test:
	pytest life_expectancy --cov --cov-report term-missing
	# python -m pytest -vv --cov=hello ./life_expectancy/tests/*.py

all: format lint test