# configure env
env:
	python3 -m venv ~/DareData/.pod6

# install pip and requirements
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# format the code using python black
format:
	black *.py

# Lint
lint:
	# pylint --disable=R,C hello.py

# Testing
test:
	# python -m pytest -vv --cov=hello test_hello.py

all: format lint test