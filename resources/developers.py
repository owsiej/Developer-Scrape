from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import DeveloperSchema, DeveloperUpdateSchema
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
        developer = DeveloperModel.query.get_or_404(developerId)
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
        developer = DeveloperModel.query.get_or_404(developerId)
        if not developer.investments:
            db.session.delete(developer)
            db.session.commit()
            return {"message": "Developer deleted."}
        abort(400, message="Delete failed. Make sure that developer doesnt have any investments assigned to it.")

    @blp.arguments(DeveloperUpdateSchema)
    @blp.response(200, DeveloperSchema,
                  description="Returns updated developer if that developer exists.")
    @blp.alt_response(400,
                      description="Returned if user didn't passed all required arguments. In this case "
                                  "developer can't be updated.",
                      example={"message": "Invalid request. Make sure you have passed all arguments needed to update a "
                                          "developer."})
    @blp.alt_response(404,
                      description="Developer not found.")
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "developer can't be updated.")
    def put(self, developer_data, developerId):
        developer = DeveloperModel.query.get_or_404(developerId)
        try:
            developer.name = developer_data['name']
            developer.url = developer_data['url']
        except KeyError:
            abort(400, message="Invalid request. Make sure you have passed all arguments needed to update a developer.")
        db.session.add(developer)
        db.session.commit()
        return developer
