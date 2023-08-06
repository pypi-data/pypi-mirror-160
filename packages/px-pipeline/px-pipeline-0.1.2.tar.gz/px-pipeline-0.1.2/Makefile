package-publish:
	rm -rf ./dist
	python setup.py sdist
	twine upload dist/*

coverage:
	coverage run -m "pytest"
	coverage report
