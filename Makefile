init:
	pip install pipenv
	pipenv install --dev
	pipenv install codecov


test:
	pipenv run isort --recursive --check-only --diff charcoallog
	pipenv run flake8 .
	pipenv run coverage_all
	pipenv run coverage_report

