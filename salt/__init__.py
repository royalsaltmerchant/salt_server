# Init Flask Server
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from salt.config import Config
import os
import sqlite3

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
mail = Mail()
migrate = Migrate(compare_type=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate.init_app(app, db)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    ma.init_app(app)

    from salt.users.routes import users
    from salt.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)

    return app                