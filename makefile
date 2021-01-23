deploy:
	python setup.py sdist bdist_wheel
	python -m twine upload --repository pypi --skip-existing dist/*