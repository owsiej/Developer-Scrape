from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.schema import DeveloperSchema, DeveloperUpdateSchema
from models import DeveloperModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("developers", __name__, description="Operations on developers")


@blp.route('/developers')
class DeveloperList(MethodView):
    @blp.response(200, DeveloperSchema(many=True),
                  description="Returns list of all developers in database.")
    def get(self):
        return DeveloperModel.query.all()

    @blp.arguments(DeveloperSchema)
    @blp.response(201,
                  DeveloperSchema,
                  description="Adds developers if developer with requested name doesn't exists.")
    @blp.alt_response(400,
                      description="Returned if developer with requested name exists.",
                      example={"message": "A developer with that name already exists."}, )
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "developer can't be added.")
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
    @blp.response(200, DeveloperSchema,
                  description="Returns a developer of given id if id is valid.")
    @blp.alt_response(404,
                      description="Developer not found.")
    def get(self, developerId):
        developer = db.get_or_404(DeveloperModel, developerId)
        return developer

    @blp.response(200,
                  description="Deletes a developer if that developer exists and there are no investments assigned to "
                              "it.",
                  example={"message": "Developer deleted."})
    @blp.alt_response(400,
                      description="Returned if developer has got any investments assigned to it. In this case "
                                  "developer can't be deleted.",
                      example={"message": "Delete failed. Make sure that developer doesnt have any investments "
                                          "assigned to it."})
    @blp.alt_response(404,
                      description="Developer not found.")
    def delete(self, developerId):
        developer = db.get_or_404(DeveloperModel, developerId)
        if not developer.investments.all():
            db.session.delete(developer)
            db.session.commit()
            return {"message": "Developer deleted."}
        abort(400, message="Delete failed. Make sure that developer doesnt have any investments assigned to it.")

    @blp.arguments(DeveloperUpdateSchema)
    @blp.response(200, DeveloperSchema,
                  description="Returns updated developer if that developer exists.")
    @blp.alt_response(404,
                      description="Developer not found.")
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "developer can't be updated.")
    def put(self, developer_data, developerId):
        developer = db.get_or_404(DeveloperModel, developerId)
        try:
            developer.name = developer_data['name']
        except KeyError:
            pass
        try:
            developer.url = developer_data['url']
        except KeyError:
            pass
        db.session.add(developer)
        db.session.commit()
        return developer
