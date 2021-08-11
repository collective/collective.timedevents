#!/usr/bin/make
.PHONY: buildout run cleanall test
all: buildout

bin/buildout: bin/pip buildout.cfg
	bin/pip install -I -r requirements.txt

buildout: bin/instance

bin/instance: bin/buildout
	bin/buildout

bin/pip:
	python3 -m venv .

run: bin/instance
	bin/instance fg

test: bin/instance
	bin/test

cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib lib64 include bin .mr.developer.cfg local/
