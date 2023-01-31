from flask import *
from flask_sqlalchemy import SQLAlchemy

"""
Initialization / app context.
"""

# Make this a singleton instance then associate below.
db = SQLAlchemy()
app = Flask("python_api")

def init_app():
    app = get_internal_app()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://example:example@localhost/example'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Split the db and app initialization
    # Set here instead of above
    db.init_app(app) 

    # Must associate handlers with app context on initialization with this factoring style
    with app.app_context():
        from domain import prepopulate
        prepopulate()

        from .dbapi import app
        from .mlapi import app
        from .testapi import app

        return app

# Bit awkward but should avoid circularity.
# Must app wrapped in return app_context()
def get_app():
    with app.app_context():
        return app

def get_internal_app():
    return app

"""
These are effectively singletons that can be imported like so:

from init import app
from init import app,db
from init import db
"""