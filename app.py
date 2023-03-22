from flask import Flask, jsonify
from flask_smorest import Api
import os
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from resources.developers import blp as DeveloperBlueprint
from resources.investments import blp as InvestmentBlueprint
from resources.flats import blp as FlatBlueprint
from resources.scrape_data import blp as ScrapeBlueprint
from resources.excel_data import blp as ExcelBlueprint
from resources.user import blp as UserBlueprint
from db import db
from blocklist import BLOCKLIST
import models


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
    migrate = Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "owsiej"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return BLOCKLIST.sismember("revoked tokens", jwt_payload['jti'])

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has been revoked.",
                "error": "token_revoked"
            }),
            401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callable(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token is not fresh.",
                "error": "fresh_token_required"
            })
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has expired",
                "error": "token_expired"
            }),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Invalid token.",
                "error": "token_invalid"
            }),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "message": "Request must contain an access token",
                "error": "token_missing"
            }),
            401
        )

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute('pragma foreign_keys=ON')

        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)

    api.register_blueprint(DeveloperBlueprint)
    api.register_blueprint(InvestmentBlueprint)
    api.register_blueprint(FlatBlueprint)
    api.register_blueprint(ScrapeBlueprint)
    api.register_blueprint(ExcelBlueprint)
    api.register_blueprint(UserBlueprint)
    return app
