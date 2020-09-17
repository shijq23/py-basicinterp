tests: clean-pyc
	pytest tests

tests-cov: clean-pyc
	pytest --cov=dashboard tests

clean:
	@rm -f .coverage
	@find . -maxdepth 2 -name .pytest_cache -type d -print0 | xargs -0 /bin/rm -rf
	@find . -maxdepth 2 -name __pycache__ -type d -print0 | xargs -0 /bin/rm -rf

clean-pyc:
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +
    name '*~' -exec rm --force  {}

clean-build:
    rm --force --recursive build/
    rm --force --recursive dist/
    rm --force --recursive *.egg-info

env:
	virtualenv env --python=python3
	#source env/bin/activate
	#pip3 install jira pytest pytest-cov
	#deactivate

isort:
    sh -c "isort --skip-glob=.tox --recursive . "

lint:
	#@find . -type f -name "*.py" | xargs autopep8 -i
	flake8 --exclude=.tox

help:
	python3 shell.py --help

run:
    python3 shell.py

package:
	python3 setup.py sdist

docker-run:
    docker build \
      --file=./Dockerfile \
      --tag=my_project ./
    docker run \
      --detach=false \
      --name=my_project \
      --publish=$(HOST):8080 \
      my_project

.PHONY: tests tests-cov clean help env