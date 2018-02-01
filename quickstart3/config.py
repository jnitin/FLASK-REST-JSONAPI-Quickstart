"""Contains non-sensitive configurations for application"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # do NOT define secret information here.
    # Define those in ./instance/config.py

    # During development, use sqlite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

