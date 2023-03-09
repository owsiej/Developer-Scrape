from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import InvestmentSchema, InvestmentUpdateSchema
from models import InvestmentModel, DeveloperModel
from db import db

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
        investment = InvestmentModel.query.get_or_404(investmentId)
        return investment

    @blp.response(200,
                  description="Deletes an investment with all flats attached to it if that investment exists.",
                  example={"message": "Investment with all flats attached deleted."})
    @blp.alt_response(404,
                      description="Investment not found.")
    def delete(self, investmentId):
        investment = InvestmentModel.query.get_or_404(investmentId)
        db.session.delete(investment)
        db.session.commit()
        return {"message": "Investment with all flats attached deleted."}

    @blp.arguments(InvestmentUpdateSchema)
    @blp.response(200, InvestmentSchema,
                  description="Returns updated investment if that investment exists.")
    @blp.alt_response(400,
                      description="Returned if user didn't passed all required arguments. In this case "
                                  "investment can't be updated.",
                      example={"message": "Invalid request. Make sure you have passed all arguments needed to update an"
                                          "investment."})
    @blp.alt_response(404,
                      description="Investment not found.")
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "investment can't be updated.")
    def put(self, investment_data, investmentId):
        investment = InvestmentModel.query.get_or_404(investmentId)
        try:
            investment.name = investment_data['name']
            investment.url = investment_data['url']
        except KeyError:
            abort(400, message="Invalid request. Make sure you have passed all arguments needed to update an "
                               "investment.")
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
        developer = DeveloperModel.query.get_or_404(developerId)
        return developer.investments.all()

    @blp.response(200,
                  description="Deletes all investments with flats attached of chosen developer if developer exists.",
                  example={"message": "All investments of chosen developer deleted."})
    @blp.alt_response(404,
                      description="Developer not found.")
    def delete(self, developerId):
        developer = DeveloperModel.query.get_or_404(developerId).investments.all()
        for investment in developer:
            db.session.delete(investment)
        db.session.commit()
        return {"message": "All investments of chosen developer deleted."}

    @blp.arguments(InvestmentUpdateSchema)
    @blp.response(201, InvestmentSchema,
                  description="Updates investment of chosen developer. If that investment doesn't exists, "
                              "adds investment to chosen developer.")
    @blp.alt_response(400,
                      description="Returned if user didn't passed all required arguments. In this case "
                                  "investment can't be updated or added.",
                      example={
                          "message": "Invalid request. Make sure you have passed all arguments needed to update an "
                                     "investment."})
    @blp.alt_response(404,
                      description="Developer not found.")
    @blp.alt_response(422,
                      description="Returned if user passed arguments of invalid data type. In this case "
                                  "investment can't be updated.")
    def put(self, investment_data, developerId):

        try:
            investment = InvestmentModel.query.filter_by(name=investment_data['name']).first()
            if investment:
                investment.name = investment_data['name']
                investment.url = investment_data['url']
            else:
                investment = InvestmentModel(developer_id=developerId, **investment_data)

            db.session.add(investment)
            db.session.commit()
            return investment
        except KeyError:
            abort(400,
                  message="Invalid request. Make sure you have passed all arguments needed to update an "
                          "investment.")


