# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
api = Api(version='1.0', title='Article API', description='A RESTful API for managing articles and comments')
