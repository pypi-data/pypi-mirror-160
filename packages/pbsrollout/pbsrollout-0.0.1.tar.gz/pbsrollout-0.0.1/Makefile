clean:
	rm -rf dist/

build:
	python3 -m build
publish: build
	python3 -m twine upload --repository pypi dist/*
