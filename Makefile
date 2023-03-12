pip-install-poetry:
		pip install poetry

poetry-config:
		poetry config virtualenvs.create false
		poetry install --no-root

flake:
	flake8 -v ./

isort:
	isort --check-only --diff ./

bandit:
	bandit -x './styles/*,settings/local.py,settings/test.py' -r ./ --skip B311

black:
	black --check ./

isort-inplace:
	isort ./

black-inplace:
	black ./

test:
	python manage.py test

linters:
	make flake
	make isort
	make bandit
	make black