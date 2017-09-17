# straverse

Straverse is a cross-platform static file [signature scanner](https://wiki.alliedmods.net/Signature_scanning).
>Sigscanning is a multi-step process involving extracting function signatures from a binary and then scanning for them at run-time to locate an otherwise-hidden function. 

Given a signature (i.e. an array of bytes) and an input file,
straverse tries to locate an address the said signature occurs,
be it one or multiple times.  

## Why?
I wanted something portable and cross platform.
Also, I find it very convenient to run a simple python program
as opposed to executing something like IDA and running a script against
a file.

## Requirements
Requirements are all included in `requirements.txt`
* Python 3 (tested with 3.6.2)
* [colorama](https://github.com/tartley/colorama)
* [pefile](https://pypi.python.org/pypi/pefile)

## Installation
It's recommended, as always, to use [virtualenv](https://docs.python.org/3/library/venv.html).
Assuming `python3` points to Python version 3:
```commandline
$ virtualenv --python=/usr/bin/python3 <directory>
$ source <directory>/bin/activate
$ pip install -r requirements.txt
$ cp config.example.json config.json
$ $EDITOR config.json
$ ./straverse.py --help
```

## Configuration
TBA

## Command line arguments
TBA

## Example use-case
TBA

## Tests
TBA

## Notes
Analyzing a Portable Executable where located bytes are not in `.text` will
most likely display wrong bytes. This can be manually fixed (`fixpe`).  
Note to self: do this properly one day.

## Reuse