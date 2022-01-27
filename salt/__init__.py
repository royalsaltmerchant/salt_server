# Init Flask Server
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from salt.config import Config

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
mail = Mail()
cors = CORS() 
migrate = Migrate(compare_type=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate.init_app(app, db)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    from salt.users.routes import users
    from salt.main.routes import main
    from salt.projects.routes import projects
    from salt.packs.routes import packs
    from salt.tracks.routes import tracks
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(projects)
    app.register_blueprint(packs)
    app.register_blueprint(tracks)

    return app                