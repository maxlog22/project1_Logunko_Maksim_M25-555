install:
	poetry install

build:
	poetry build

package-install:
	python -m pip install dist/*.whl

publish:
	poetry publish --dry-run

project:
	poetry run project
