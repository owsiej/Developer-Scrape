from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import InvestmentSchema, InvestmentUpdateSchema, InvestmentByDeveloperUpdateSchema
from models import InvestmentModel, DeveloperModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("investments", __name__, description="Operations on investments")


@blp.route('/investments')
class InvestmentList(MethodView):
    @blp.response(200, InvestmentSchema(many=True),
                  description="Returns list of all investments in database.")
    def get(self):
        return InvestmentModel.query.all()


@blp.route('/investments/<int:investmentId>')
class Investment(MethodView):
    @blp.response(200, InvestmentSchema,
                  description="Returns investment of given id if id is valid.")
    @blp.alt_response(404,
                      description="Investment not found.")
    def get(self, investmentId):
        investment = db.get_or_404(InvestmentModel, investmentId)
        return investment

    @blp.response(200,
                  description="Deletes an investment with all flats attached to it if that investment exists.",
                  example={"message": "Investment with all flats attached deleted."})
    @blp.alt_response(404,
                      description="Investment not found.")
    def delete(self, investmentId):
        investment = db.get_or_404(InvestmentModel, investmentId)
        db.session.delete(investment)
        db.session.commit()
        return {"message": "Investment with all flats attached deleted."}

    @blp.arguments(InvestmentUpdateSchema)
    @blp.response(200, InvestmentSchema,
                  description="Returns updated investment if that investment exists.")
    @blp.alt_response(404,
                      description="Investment not found.")
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "investment can't be updated.")
    def put(self, investment_data, investmentId):
        investment = db.get_or_404(InvestmentModel, investmentId)
        try:
            investment.name = investment_data['name']
        except KeyError:
            pass
        try:
            investment.url = investment_data['url']
        except KeyError:
            pass
        db.session.add(investment)
        db.session.commit()
        return investment


@blp.route('/developers/<int:developerId>/investments')
class InvestmentListByDeveloper(MethodView):
    @blp.response(200, InvestmentSchema(many=True),
                  description="Returns all investments of chosen developer.")
    @blp.alt_response(404,
                      description="Developer not found.")
    def get(self, developerId):
        developer = db.get_or_404(DeveloperModel, developerId)
        return developer.investments.all()

    @blp.response(200,
                  description="Deletes all investments with flats attached of chosen developer if developer exists.",
                  example={"message": "All investments of chosen developer deleted."})
    @blp.alt_response(404,
                      description="Developer not found.")
    def delete(self, developerId):
        developer = db.get_or_404(DeveloperModel, developerId).investments.all()
        for investment in developer:
            db.session.delete(investment)
        db.session.commit()
        return {"message": "All investments of chosen developer deleted."}

    @blp.arguments(InvestmentByDeveloperUpdateSchema)
    @blp.response(201, InvestmentSchema,
                  description="Adds investment to chosen developer.")
    @blp.alt_response(400,
                      description="Returned if investment with requested name exists.",
                      example={"message": "An investment with that name already exists."}, )
    @blp.alt_response(404,
                      description="Developer not found.")
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "investment can't be updated.")
    def post(self, investment_data, developerId):
        developer = db.get_or_404(DeveloperModel, developerId)
        investment = InvestmentModel(**investment_data, developer_id=developer.id)
        try:
            db.session.add(investment)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An investment with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the developer.")
        return investment
