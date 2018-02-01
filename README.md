# FLASK-REST-JSONAPI: Quickstart Example

---
## Content

I took the [quickstart example of Flask-REST-JSONAPI](http://flask-rest-jsonapi.readthedocs.io/en/latest/quickstart.html#), and made 3 variations:

- quickstart1: the original version, written as a single python module
- quickstart2: refactored into a python package
- quickstart3: refactored into a blueprint, with unit tests.


## Filtering in Flask-REST-JSONAPI

The main reason I very much appreciate Flask-REST-JSONAPI is because of the build in [filtering capability](http://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html), and the fact it adheres strictly to the [JSON API 1.0 specification](http://jsonapi.org/format/).

I spent some time figuring out how to actually do the filtering for the quickstart example, and build some unittests for the flask test client. (See [here](https://github.com/ArjaanBuijk/FLASK-REST-JSONAPI-Quickstart/blob/master/quickstart3/test/test_filtering.py).)

For [example](https://github.com/ArjaanBuijk/FLASK-REST-JSONAPI-Quickstart/blob/master/quickstart3/test/test_filtering.py):
```bash
        # Get persons, filtered through a combination of their name or a
        # relationship to his/her computers
        # - find Mary & Dopey by their name
        # - find John, because he owns (ie. has the relationship with) the computer named Amstrad
        url = """/persons?filter=
            [{"or":[{"name":"name","op":"eq","val":"John"},
                    {"name":"name","op":"eq","val":"Dopey"},
                    {"name":"computers","op":"any","val": {
                          "name":"serial","op":"ilike","val":"%Amstrad%"}
                    }
                   ]
             }
            ]"""
        url = ''.join(url.split())  # get rid of all whitespace
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        expected_status_code = 200
        expected_count = 3
        response = self.client().get(url,
                                     headers=headers)
        response_data = json.loads(response.data.decode())
        response_count = response_data['meta']['count']
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_count, expected_count)
```

When you print the response_data of above request, you see something like this, when the filter finds 3 Persons:
```bash
response_data =
{'data':
 [
    {'attributes': {
        'display_name': 'JOHN <john@gmail.com>',
        'birth_date': '1990-12-18'
        },
     'id': '1',
     'relationships': {
         'computers': {
             'links': {
                 'self': '/persons/1/relationships/computers',
                 'related': '/persons/1/computers'
                 }
             }
         },
     'type': 'person',
     'links': {
         'self': '/persons/1'
         }
     },
    {'attributes': {
        'display_name': 'JOHN <john2@gmail.com>',
        'birth_date': '2010-12-18'
        },
     'id': '2',
     'relationships': {
         'computers': {
             'links': {
                 'self': '/persons/2/relationships/computers',
                 'related': '/persons/2/computers'
                 }
             }
         },
     'type': 'person',
     'links': {
         'self': '/persons/2'
         }
     },
    {'attributes': {
        'display_name': 'DOPEY <dopey@gmail.com>',
        'birth_date': '1931-01-12'
        },
     'id': '4',
     'relationships': {
         'computers': {
             'links': {
                 'self': '/persons/4/relationships/computers',
                 'related': '/persons/4/computers'
                 }
             }
         },
     'type': 'person',
     'links': {
         'self': '/persons/4'
         }
     }
 ],
 'jsonapi': {'version': '1.0'},
 'meta': {'count': 3},
 'links': {
    'self': '/persons?filter=%5B%7B%22or%22%3A%5B%7B%22name%22%3A%22name%22%2C%22op%22%3A%22eq%22%2C%22val%22%3A%22John%22%7D%2C%7B%22name%22%3A%22name%22%2C%22op%22%3A%22eq%22%2C%22val%22%3A%22Dopey%22%7D%2C%7B%22name%22%3A%22computers%22%2C%22op%22%3A%22any%22%2C%22val%22%3A%7B%22name%22%3A%22serial%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25Amstrad%25%22%7D%7D%5D%7D%5D'
 }
}

```

Development and testing was done on Ubuntu 16.04.

## Usage

The steps described here show how to run <b>quickstart3</b> within a python virtual environment.

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

 Alternatively, instead of installing the required python packages using the file <em>'requirements.txt'</em>, which installs the specific versions that were used during development and testing, you can also enter these commands, which I had used to install the actual packages:
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