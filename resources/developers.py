from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import DeveloperSchema, DeveloperUpdateSchema
from models import DeveloperModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("developers", __name__, description="Operations on developers")


@blp.route('/developers')
class DeveloperList(MethodView):
    @blp.response(200, DeveloperSchema(many=True))
    def get(self):
        return DeveloperModel.query.all()

    @blp.arguments(DeveloperSchema)
    @blp.response(201, DeveloperSchema)
    def post(self, developer_data):
        developer = DeveloperModel(**developer_data)
        try:
            db.session.add(developer)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A developer with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the developer.")
        return developer


@blp.route('/developers/<int:developerId>')
class Developer(MethodView):
    @blp.response(200, DeveloperSchema)
    def get(self, developerId):
        developer = DeveloperModel.query.get_or_404(developerId)
        return developer

    def delete(self, developerId):
        developer = DeveloperModel.query.get_or_404(developerId)

        db.session.delete(developer)
        db.session.commit()
        return {"message": "Developer deleted."}

    @blp.arguments(DeveloperUpdateSchema)
    @blp.response(200, DeveloperSchema)
    def put(self, developer_data, developerId):
        developer = DeveloperModel.query.get_or_404(developerId)
        developer.name = developer_data['name']
        developer.url = developer_data['url']

        db.session.add(developer)
        db.session.commit()
        return developer
