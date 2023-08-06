.PHONY: clean sdist bdist all

.DEFAULT_GOAL := all

all:
	$(MAKE) sdist
	$(MAKE) bdist

minicapy/minica.dll:
	cd minicapy && go get -d github.com/bjornsnoen/minica \
		&& go build -o minica.dll --buildmode=c-shared github.com/bjornsnoen/minica
	rm minicapy/minica.h

bdist: minicapy/minica.dll
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

clean:
	rm -rf minicapy/minica.h minicapy/minica.dll
	rm -rf minica-key.pem minica.pem
	rm -rf minicapy/__pycache__ __pycache__
	rm -rf build dist minicapy.egg-info
	rm -rf build
