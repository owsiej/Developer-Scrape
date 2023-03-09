from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import FlatSchema, FlatUpdateSchema, PlainFlatSchema, FlatSearchQueryByInvestment, \
    FlatSearchQueryByDeveloper, FlatSearchQueryArgs
from models import FlatModel, DeveloperModel, InvestmentModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flat_query_search_filter import find_filters

blp = Blueprint("flats", __name__, description="Operations on flats")


@blp.route('/flats')
class FlatList(MethodView):
    @blp.arguments(FlatSearchQueryArgs, location="query")
    @blp.response(200, FlatSchema(many=True))
    def get(self, search_args):
        filters = find_filters(search_args)
        return FlatModel.query.filter(*filters).all()


@blp.route('/flats/<int:flatId>')
class Flat(MethodView):
    @blp.response(200, FlatSchema)
    def get(self, flatId):
        flat = FlatModel.query.get_or_404(flatId)
        return flat

    def delete(self, flatId):
        developer = FlatModel.query.get_or_404(flatId)
        db.session.delete(developer)
        db.session.commit()
        return {"message": "Flat deleted."}

    @blp.arguments(FlatUpdateSchema)
    @blp.response(200, FlatSchema)
    def put(self, flat_data, flatId):
        flat = FlatModel.query.get_or_404(flatId)
        flat.floor_number = flat_data['floor_number']
        flat.rooms_number = flat_data['rooms_number']
        flat.area = flat_data['area']
        flat.price = flat_data['price']
        flat.status = flat_data['status']

        db.session.add(flat)
        db.session.commit()
        return flat


@blp.route('/investments/flats')
class FlatListByInvestment(MethodView):
    @blp.arguments(FlatSearchQueryByInvestment, location="query")
    @blp.response(200, FlatSchema(many=True))
    def get(self, search_args):
        investment = InvestmentModel.query.filter_by(id=search_args['investment_id']).first()
        filters = find_filters(search_args)
        return investment.flats.filter(*filters).all()


@blp.route('/investments/<int:investmentId>/flats')
class FlatListByInvestment(MethodView):
    def delete(self, investmentId):
        investment = InvestmentModel.query.get_or_404(investmentId).flats.all()
        for flat in investment:
            db.session.delete(flat)
        db.session.commit()
        return {"message": "Flats from investment deleted."}

    @blp.arguments(PlainFlatSchema)
    @blp.response(201, FlatSchema)
    def post(self, flat_data, investmentId):
        investment = InvestmentModel.query.filter_by(id=investmentId).first()
        print(investment)
        flat = FlatModel(investment_id=investmentId, invest_name=investment.name,
                         developer_id=investment.developer_id, **flat_data)
        try:
            db.session.add(flat)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the flat.")
        return flat


@blp.route('/developers/flats')
class FlatListByDeveloper(MethodView):
    @blp.arguments(FlatSearchQueryByDeveloper, location="query")
    @blp.response(200, FlatSchema(many=True))
    def get(self, search_args):
        developer = DeveloperModel.query.filter_by(id=search_args['developer_id']).first()
        filters = find_filters(search_args)
        return developer.flats.filter(*filters).all()


@blp.route('/developers/<int:developerId>/flats')
class FlatListByDeveloper(MethodView):
    def delete(self, developerId):
        developer = DeveloperModel.query.get_or_404(developerId).flats.all()
        for flat in developer:
            db.session.delete(flat)
        db.session.commit()
        return {"message": "Flats from developer deleted."}
