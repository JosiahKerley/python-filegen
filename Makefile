upload: clean
	python setup.py sdist upload
register: clean
	python setup.py register
clean:
	rm -rf FileGenerator.egg-info dist

