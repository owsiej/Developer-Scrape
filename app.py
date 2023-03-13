from flask import Flask
from flask_smorest import Api
from resources.developers import blp as DeveloperBlueprint
from resources.investments import blp as InvestmentBlueprint
from resources.flats import blp as FlatBlueprint
from resources.scrape_data import blp as ScrapeBlueprint
from db import db
import models
import os


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Developer Scrape REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", 'sqlite:///data.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute('pragma foreign_keys=ON')

        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)
            db.create_all()

    api.register_blueprint(DeveloperBlueprint)
    api.register_blueprint(InvestmentBlueprint)
    api.register_blueprint(FlatBlueprint)
    api.register_blueprint(ScrapeBlueprint)
    return app
