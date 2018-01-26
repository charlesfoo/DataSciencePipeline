main: setup upload clean update
	
setup:
	python setup.py sdist

upload:
	twine upload dist/*

update:
	sudo pip3 install easyscrape --upgrade

clean:
	rm -rf dist easyscrape.egg-info
