from flask.views import MethodView
from flask_smorest import Blueprint
from schema import InvestmentSchema, InvestmentUpdateSchema
from models import InvestmentModel, DeveloperModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("investments", __name__, description="Operations on investments")


@blp.route('/investments')
class InvestmentList(MethodView):
    @blp.response(200, InvestmentSchema(many=True))
    def get(self):
        return InvestmentModel.query.all()


@blp.route('/investments/<int:investmentId>')
class Investment(MethodView):
    @blp.response(200, InvestmentSchema)
    def get(self, investmentId):
        investment = InvestmentModel.query.get_or_404(investmentId)
        return investment

    def delete(self, investmentId):
        investment = InvestmentModel.query.get_or_404(investmentId)
        db.session.delete(investment)
        db.session.commit()
        return {"message": "Investment deleted."}

    @blp.arguments(InvestmentUpdateSchema)
    @blp.response(200, InvestmentSchema)
    def put(self, investment_data, investmentId):
        investment = InvestmentModel.query.get_or_404(investmentId)
        investment.name = investment_data['name']
        investment.url = investment_data['url']

        db.session.add(investment)
        db.session.commit()
        return investment


@blp.route('/developers/<int:developerId>/investments')
class InvestmentListByDeveloper(MethodView):
    @blp.response(200, InvestmentSchema(many=True))
    def get(self, developerId):
        developer = DeveloperModel.query.get_or_404(developerId)
        return developer.investments.all()

    def delete(self, developerId):
        # investments = InvestmentModel.query.filter_by(developer_id=developerId)
        # db.session.delete(investments)
        developer = DeveloperModel.query.get_or_404(developerId).investments.all()
        for investment in developer:
            db.session.delete(investment)
        db.session.commit()
        return {"message": "Investments from developer deleted."}

    @blp.arguments(InvestmentUpdateSchema)
    @blp.response(201, InvestmentSchema)
    def put(self, investment_data, developerId):
        investment = InvestmentModel.query.filter_by(name=investment_data['name']).first()
        if investment:
            investment.name = investment_data['name']
            investment.url = investment_data['url']
        else:
            investment = InvestmentModel(developer_id=developerId, **investment_data)

        db.session.add(investment)
        db.session.commit()
        return investment
