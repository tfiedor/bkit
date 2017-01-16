init:
	pip install -r requirements.txt

install:
	python setup.py install --force

.PHONY: init install
