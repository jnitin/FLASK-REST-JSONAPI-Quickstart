# FLASK-REST-JSONAPI: Quickstart Example

---
## Content

I took the quickstart example of FLASK-REST-JSONAPI, and build 3 variations:

- quickstart1: the original version, written as a single python module
- quickstart2: refactored into a python package
- quickstart3: refactored into a blueprint, with extensive tests, including filtering

quickstart3 is the final version, which you should use as the starter project.

#### Usage

The steps described here show how to run quickstart3 within a python virtual environment.
Development and testing was done on Ubuntu 16.04.


1. Clone the project repository
```bash
$ git clone https://github.com/ArjaanBuijk/FLASK-REST-JSONAPI-Quickstart
```

2. One time: prepare the python virtual environment
```bash
$ cd FLASK-REST-JSONAPI-Quickstart/quickstart3
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

 Alternatively, instead of installing the required python packages using the file <em>'requirements.txt'</em>, which installs the specific versions that were used during development and testing, one can also enter these commands, which I had used to install the actual packages:
```bash
$ cd FLASK-REST-JSONAPI-Quickstart/quickstart3
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install flask
(venv) $ pip install Flask-REST-JSONAPI
(venv) $ pip install flask-sqlalchemy
(venv) $ pip install requests
```

3. Activate the python virtual environment and start the application server
```bash
$ cd FLASK-REST-JSONAPI-Quickstart/quickstart3
$ source venv/bin/activate
(venv) $ export FLASK_APP=quickstart3.py
(venv) $ flask run
```

 You should see this output printed to the console:
 ```bash
 * Serving Flask app "quickstart3"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```