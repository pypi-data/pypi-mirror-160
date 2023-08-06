# Minicapy, python bindings for minica, a mini CA 
A small python library for using minica to create ssl certificates

## Installation
This package is pip installable, simply

`pip install minicapy`

You will need to have a fairly recent version of `go` and `make` installed
in order to build the library, because I can't figure out manylinux to provide
binary dist wheels.

## Usage
```python
from minicapy import minica

success = minica.create_domain_cert("somedomain.com")
if success > 0:
    print("Something went wrong")

# Or
success = minica.create_ip_cert("10.0.0.25")
if success > 0:
    print("Something went wrong")
```

## Return codes
The functions return ints, which have the following meanings

| Return code | Meaning                                                   |
|-------------|-----------------------------------------------------------|
| 0           | Success                                                   |
| 1           | Couldn't create root cert files minica.pem/minica-key.pem |
| 2           | Couldn't create domain/ip cert, probably already exist    |
