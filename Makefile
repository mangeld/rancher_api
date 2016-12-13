test:
	py.test -v -s --cov-report term-missing --cov=rancher/ tests/
functional:
	py.test -v -s --cov-report term-missing --cov=rancher/ functional_tests/
publish:
	python setup.py register && python setup.py sdist upload
