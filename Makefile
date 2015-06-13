SRC_DIR = turingmarkov
GENERATED = build dist *.egg-info

all : test lint pep257

clean :
	rm -rf $(GENERATED)

dist :
	python setup.py sdist bdist_egg bdist_wheel

test :
	py.test $(SRC_DIR)

cov :
	py.test --cov $(SRC_DIR)

lint :
	pylint $(SRC_DIR)

pep257 :
	pep257 $(SRC_DIR)
