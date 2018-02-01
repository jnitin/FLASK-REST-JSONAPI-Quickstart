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
http://flask-rest-jsonapi.readthedocs.io/en/latest/quickstart.html#classical-crud-operations
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
        """Adds 1 computer to the database
        Use this for the RUD tests."""

        url = '/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
                "type": "computer",
                "attributes": {
                    "serial": "Amstrad"
                }
            }
        }
        response = self.client().post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)

    def test_0_1_create_computer(self):
        """Test if API can register a new computer (POST request)"""

        url = '/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
                "type": "computer",
                "attributes": {
                    "serial": "Amstrad"
                }
            }
        }

        expected_status_code = 201
        expected_data = {
            "data": {
              "type": "computer",
              "id": "1",
              "attributes": {
                "serial": "Amstrad"
              },
              "relationships": {
                "owner": {
                  "links": {
                    "related": "/computers/1/owner",
                    "self": "/computers/1/relationships/owner"
                  }
                }
              },
              "links": {
                "self": "/computers/1"
              }
            },
            "links": {
              "self": "/computers/1"
            },
            "jsonapi": {
              "version": "1.0"
            }
          }

        response = self.client().post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))

    def test_0_2_read_computer(self):
        """Test if API can read a computer (GET request)"""

        # first register a computer
        self.populate_database()

        # then list it
        url = '/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = None

        expected_status_code = 200
        expected_data = {
            "data": [
                {
                  "type": "computer",
                  "id": "1",
                  "attributes": {
                    "serial": "Amstrad"
                  },
                  "relationships": {
                    "owner": {
                      "links": {
                        "related": "/computers/1/owner",
                        "self": "/computers/1/relationships/owner"
                      }
                    }
                  },
                  "links": {
                    "self": "/computers/1"
                  }
                }
              ],
              "meta": {
                "count": 1
              },
              "links": {
                "self": "/computers"
              },
              "jsonapi": {
                "version": "1.0"
              },
            }

        response = self.client().get(url,
                                      headers=headers)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))

    def test_0_3_update_computer(self):
        """Test if API can update a computer (PATCH request)"""

        # first register a computer
        self.populate_database()

        # then patch it
        url = '/computers/1'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
              "type": "computer",
              "id": "1",
              "attributes": {
                "serial": "Amstrad 2"
              }
            }
          }

        expected_status_code = 200
        expected_data = {
            "data": {
              "type": "computer",
              "id": "1",
              "attributes": {
                "serial": "Amstrad 2"
              },
              "relationships": {
                "owner": {
                  "links": {
                    "related": "/computers/1/owner",
                    "self": "/computers/1/relationships/owner"
                  }
                }
              },
              "links": {
                "self": "/computers/1"
              }
            },
            "links": {
              "self": "/computers/1"
            },
            "jsonapi": {
              "version": "1.0"
            }
          }

        response = self.client().patch(url,
                                       headers=headers,
                                       data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))

    def test_0_4_delete_computer(self):
        """Test if API can read a computer (DELETE request)"""

        # first register a computer
        self.populate_database()

        # then delete it
        url = '/computers/1'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = None

        expected_status_code = 200
        expected_data = {
            "meta": {
              "message": "Object successfully deleted"
            },
            "jsonapi": {
              "version": "1.0"
            }
          }

        response = self.client().delete(url,
                                        headers=headers)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))


if __name__ == '__main__':
    unittest.main(verbosity=2)

