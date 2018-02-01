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

    def populate_database_with_4_computers(self):
        """Adds 4 computer to the database."""

        url = '/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        for serial in ["Amstrad", "Halo", "Nestor", "Comodor"]:
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

    def test_1_1_CRUD_person_with_relationship(self):
        """Test all CRUD operations for a person"""

        # First, populate the database with 4 computers
        self.populate_database_with_4_computers()

        # Then, create a person that owns the first computer (Amstrad)
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
                      }
                    ]
                  }
                }
              }
            }

        expected_status_code = 201
        expected_data = {
            "data": {
              "type": "person",
              "id": "1",
              "attributes": {
                "display_name": "JOHN <john@gmail.com>",
                "birth_date": "1990-12-18"
              },
              "links": {
                "self": "/persons/1"
              },
              "relationships": {
                "computers": {
                  "data": [
                    {
                      "id": "1",
                      "type": "computer"
                    }
                  ],
                  "links": {
                    "related": "/persons/1/computers",
                    "self": "/persons/1/relationships/computers"
                  }
                }
              },
            },
            "included": [
              {
                "type": "computer",
                "id": "1",
                "attributes": {
                  "serial": "Amstrad"
                },
                "links": {
                  "self": "/computers/1"
                },
                "relationships": {
                  "owner": {
                    "links": {
                      "related": "/computers/1/owner",
                      "self": "/computers/1/relationships/owner"
                    }
                  }
                }
              }
            ],
            "jsonapi": {
              "version": "1.0"
            },
            "links": {
              "self": "/persons/1"
            }
          }

        response = self.client().post(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))

        # Then, update information for this person:
        # - computer 1 is removed
        # - computer 3 is added
        # - add a change to the email address
        url = '/persons/1?include=computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": {
              "type": "person",
              "id": "1",
              "attributes": {
                "birth_date": "1990-10-18"
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

        expected_status_code = 200
        expected_data = {
            "data": {
              "type": "person",
              "id": "1",
              "attributes": {
                "display_name": "JOHN <john@gmail.com>",
                "birth_date": "1990-10-18",
              },
              "links": {
                "self": "/persons/1"
              },
              "relationships": {
                "computers": {
                  "data": [
                    {
                      "id": "3",
                      "type": "computer"
                    }
                  ],
                  "links": {
                    "related": "/persons/1/computers",
                    "self": "/persons/1/relationships/computers"
                  }
                }
              },
            },
            "included": [
              {
                "type": "computer",
                "id": "3",
                "attributes": {
                  "serial": "Nestor"
                },
                "relationships": {
                  "owner": {
                    "links": {
                      "related": "/computers/3/owner",
                      "self": "/computers/3/relationships/owner"
                    }
                  }
                },
                "links": {
                  "self": "/computers/3"
                }
              }
            ],
            "links": {
              "self": "/persons/1"
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

        # Then, create a new relationship for this person:
        # - computer 4 is added
        url = '/persons/1/relationships/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": [
              {
                "type": "computer",
                "id": "4"
              }
            ]
          }

        expected_status_code = 200
        expected_data = {
            "data": {
              "type": "person",
              "id": "1",
              "attributes": {
                "display_name": "JOHN <john@gmail.com>",
                "birth_date": "1990-10-18"
              },
              "relationships": {
                "computers": {
                  "data": [
                    {
                      "id": "3",
                      "type": "computer"
                    },
                    {
                      "id": "4",
                      "type": "computer"
                    }
                  ],
                  "links": {
                    "related": "/persons/1/computers",
                    "self": "/persons/1/relationships/computers"
                  }
                }
              },
              "links": {
                "self": "/persons/1"
              }
            },
            "included": [
              {
                "type": "computer",
                "id": "3",
                "attributes": {
                  "serial": "Nestor"
                },
                "relationships": {
                  "owner": {
                    "links": {
                      "related": "/computers/3/owner",
                      "self": "/computers/3/relationships/owner"
                    }
                  }
                },
                "links": {
                  "self": "/computers/3"
                }
              },
              {
                "type": "computer",
                "id": "4",
                "attributes": {
                  "serial": "Comodor"
                },
                "relationships": {
                  "owner": {
                    "links": {
                      "related": "/computers/4/owner",
                      "self": "/computers/4/relationships/owner"
                    }
                  }
                },
                "links": {
                  "self": "/computers/4"
                }
              }
            ],
            "links": {
              "self": "/persons/1/relationships/computers"
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


        # Then, delete an existing relationship for this person:
        # - computer 3 is removed from the relationship
        url = '/persons/1/relationships/computers'
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
            }
        data = {
            "data": [
              {
                "type": "computer",
                "id": "3"
              }
            ]
          }

        expected_status_code = 200
        expected_data = {
            "data": {
              "type": "person",
              "id": "1",
              "attributes": {
                "display_name": "JOHN <john@gmail.com>",
                "birth_date": "1990-10-18"
              },
              "relationships": {
                "computers": {
                  "data": [
                    {
                      "id": "4",
                      "type": "computer"
                    }
                  ],
                  "links": {
                    "related": "/persons/1/computers",
                    "self": "/persons/1/relationships/computers"
                  }
                }
              },
              "links": {
                "self": "/persons/1"
              }
            },
            "included": [
              {
                "type": "computer",
                "id": "4",
                "attributes": {
                  "serial": "Comodor"
                },
                "relationships": {
                  "owner": {
                    "links": {
                      "related": "/computers/4/owner",
                      "self": "/computers/4/relationships/owner"
                    }
                  }
                },
                "links": {
                  "self": "/computers/4"
                }
              }
            ],
            "links": {
                "self": "/persons/1/relationships/computers"
            },
            "jsonapi": {
                "version": "1.0"
            }
          }


        response = self.client().delete(url,
                                      headers=headers,
                                      data=json.dumps(data))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, expected_status_code)
        self.assertListEqual(ordered(response_data),
                             ordered(expected_data))


if __name__ == '__main__':
    unittest.main(verbosity=2)


