test:
	py.test -v -s --cov-report term-missing --cov=rancher/ tests/
functional:
	py.test -v -s --cov-report term-missing --cov=rancher/ functional_tests/
