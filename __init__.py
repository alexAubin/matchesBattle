from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    from .app import main, players
    from .settings import SQLALCHEMY_DATABASE_URI
    from flask_uploads import configure_uploads

    app = Flask(__name__)
    app.register_blueprint(main)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOADED_PLAYERS_DEST'] = '/var/www/allumette/app/players/'

    configure_uploads(app, (players,))

    db.init_app(app)

    return app
