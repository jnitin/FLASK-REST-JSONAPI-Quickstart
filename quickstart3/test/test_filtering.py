#!/usr/bin/env python3
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from config import Config
from application import create_app, db
from application.models import Computer, Person
import requests
import json
from base64 import b64encode
from my_utils import ordered

"""All tests are based on:
http://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html  # NOQA
"""

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # initialize the test client
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_database(self):
        """Adds 4 computers and 2 persons to the database."""
        computers = ["Amstrad", "Halo", "Nestor", "Comodor"]

        url = '/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        for serial in computers:
            data = {
                "data": {
                    "type": "computer",
                    "attributes": {
                        "serial": "{}".format(serial)
                    }
                }
            }
            response = self.client().post(url,
                                          headers=headers,
                                          data=json.dumps(data))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)


        # Create a person named John that owns the first 2 computers
        url = '/persons?include=computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
                "type": "person",
                "attributes": {
                  "name": "John",
                  "email": "john@gmail.com",
                  "birth_date": "1990-12-18"
                },
                "relationships": {
                  "computers": {
                    "data": [
                      {
                        "type": "computer",
                        "id": "1"
                      },
                          {
                          "type": "computer",
                        "id": "2"
                      }
                    ]
                  }
                }
              }
            }
        expected_status_code = 201
        response = self.client().post(url,
                                          headers=headers,
                                          data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)

        # Create a 2nd person, also named John that owns the 3rd computer
        url = '/persons?include=computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
                "type": "person",
                "attributes": {
                  "name": "John",
                  "email": "john2@gmail.com",
                  "birth_date": "2010-12-18"
                },
                "relationships": {
                  "computers": {
                    "data": [
                      {
                        "type": "computer",
                        "id": "3"
                      }
                    ]
                  }
                }
              }
            }
        expected_status_code = 201
        response = self.client().post(url,
                                          headers=headers,
                                          data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)

        # Create a 3rd person, named Mary that owns the 4th computer
        url = '/persons?include=computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
                "type": "person",
                "attributes": {
                  "name": "Mary",
                  "email": "mary@gmail.com",
                  "birth_date": "1964-03-21"
                },
                "relationships": {
                  "computers": {
                    "data": [
                      {
                        "type": "computer",
                        "id": "4"
                      }
                    ]
                  }
                }
              }
            }
        expected_status_code = 201
        response = self.client().post(url,
                                          headers=headers,
                                          data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)

        # Create a 4th person, named Dopey that owns no computers
        url = '/persons'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
                "type": "person",
                "attributes": {
                  "name": "Dopey",
                  "email": "dopey@gmail.com",
                  "birth_date": "1931-01-12"
                }
              }
            }
        expected_status_code = 201
        response = self.client().post(url,
                                          headers=headers,
                                          data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)

    def test_2_1_filter1(self):
        """Test some filters..."""

        # First, populate the database with 4 computers
        self.populate_database()

        # Get all the persons, no filters applied
        url = '/persons'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        expected_status_code = 200
        expected_count = 4
        response = self.client().get(url,
                                     headers=headers)
        response_data = json.loads(response.data.decode())
        response_count = response_data['meta']['count']
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_count, expected_count)

        # Get the persons, filltered by name=John
        url = '/persons?filter=[{"name":"name","op":"eq","val":"John"}]'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        expected_status_code = 200
        expected_count = 2  # We populated with two Johns
        response = self.client().get(url,
                                     headers=headers)
        response_data = json.loads(response.data.decode())
        response_count = response_data['meta']['count']
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_count, expected_count)

        # Get the persons, filltered by name=John or name=Dopey
        url = """/persons?filter=
        [{"or":[{"name":"name","op":"eq","val":"John"},
                {"name":"name","op":"eq","val":"Dopey"}
               ]
         }
        ]"""
        url = ''.join(url.split())  # get rid of all whitespace
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        expected_status_code = 200
        expected_count = 3  # We populated with two Johns and 1 Dopey
        response = self.client().get(url,
                                     headers=headers)
        response_data = json.loads(response.data.decode())
        response_count = response_data['meta']['count']
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_count, expected_count)

        # Get a person, filtered through a relationship to his/her computers
        # - John owns Amstrad
        url = """/persons?filter=[
            {
              "name": "computers",
              "op": "any",
              "val": {
                "name": "serial",
                "op": "ilike",
                "val": "%Amstrad%"
              }
            }
          ]"""
        url = ''.join(url.split())  # get rid of all whitespace
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        expected_status_code = 200
        expected_count = 1  # Only 1 person owns Amstrad
        response = self.client().get(url,
                                     headers=headers)
        response_data = json.loads(response.data.decode())
        response_count = response_data['meta']['count']
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_count, expected_count)

        # Get persons, filtered through a combination of their name or a
        # relationship to his/her computers
        # - find Mary & Dopey by their name
        # - find John, because he owns Amstrad
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
        expected_data = \
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
        response = self.client().get(url,
                                         headers=headers)
        response_data = json.loads(response.data.decode())
        response_count = response_data['meta']['count']
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_count, expected_count)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))


if __name__ == '__main__':
    unittest.main(verbosity=2)



