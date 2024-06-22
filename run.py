# run.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.routes import api_bp
from extensions import db, api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    migrate = Migrate(app, db)
    from api.models import Article, Comment
    # Initialize extensions
    db.init_app(app)
    api.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
