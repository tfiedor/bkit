init:
	pip install -r requirements.txt

install:
	python setup.py install

.PHONY: init install
