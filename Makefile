test:
	py.test -v -s --cov-report term-missing --cov=rancher/ tests/
functional:
	py.test -v -s --cov-report term-missing --cov=rancher/ functional_tests/
release:
	python make_release.py --patch
release_minor:
	python make_release.py --minor
release_major:
	python make_release.py --major
publish:
	python setup.py register && python setup.py sdist upload
clean:
	rm -rf rancher.egg-info dist
