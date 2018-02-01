from application import app, api
from application.resource_managers import \
     PersonList, PersonDetail, PersonRelationship,\
     ComputerList, ComputerDetail, ComputerRelationship
from flask_rest_jsonapi import Api


# Flask-REST-JSONAPI: Create endpoints
def create_api_endpoints():
    #http://flask-rest-jsonapi.readthedocs.io/en/latest/flask-rest-jsonapi.html
    #
    #Parameters given to api.route:
    #
    # resource (Resource) – a resource class inherited from
    #                       flask_rest_jsonapi.resource.Resource
    #                       -> see resource_managers.py
    # view (str) – the view name
    #              -> used eg. in check_permissions
    # urls (list) – the urls of the view
    #               -> used by clients in CRUD requests
    # kwargs (dict) – additional options of the route

    api.route(PersonList, 'person_list',
              '/persons')

    api.route(PersonDetail, 'person_detail',
              '/persons/<int:id>',
              '/computers/<int:computer_id>/owner')

    api.route(PersonRelationship, 'person_computers',
              '/persons/<int:id>/relationships/computers')

    api.route(ComputerList, 'computer_list',
              '/computers',
              '/persons/<int:id>/computers')

    api.route(ComputerDetail, 'computer_detail',
              '/computers/<int:id>')

    api.route(ComputerRelationship, 'computer_person',
              '/computers/<int:id>/relationships/owner')

