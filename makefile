deploy:
	python setup.py bdist_wheel
	python -m twine upload --repository pypi --skip-existing dist/*