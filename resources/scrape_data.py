from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from schemas.schema import PlainScrapeSchema, FinalResponseScrapeSchema
from services.scrape_logic.scrape_request import get_info_from_scrape, get_developer_list_to_scrape
from models import DeveloperModel, InvestmentModel, FlatModel

blp = Blueprint("scrape_data", __name__, description="Operations on data strict from scraping.")


@blp.route('/scrape')
class ScrapeData(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200,
                  description="Returns list of developers available to scrape.")
    def get(self):
        return get_developer_list_to_scrape()

    @jwt_required(fresh=True)
    @blp.arguments(PlainScrapeSchema)
    @blp.response(201, FinalResponseScrapeSchema,
                  description="Adds developer from scrape with investments and flats attached. If that developer "
                              "already exists, updates it.")
    @blp.alt_response(404,
                      description="Developer not found.")
    def put(self, scrape_choice):
        userChoice = scrape_choice['developer_id']
        try:
            scrape_data = get_info_from_scrape(userChoice)
        except IndexError:
            abort(404, message="Developer not found.")
        developer_data = DeveloperModel.query.filter_by(name=scrape_data[0]['name']).first()

        if developer_data:
            developerInvestments = developer_data.investments.all()
            for developerInvestment in developerInvestments:
                db.session.delete(developerInvestment)
            db.session.commit()
        else:
            developer_data = DeveloperModel(**scrape_data[0])
            db.session.add(developer_data)
            db.session.commit()
        investments_data = [
            InvestmentModel(developer_id=developer_data.id, **investment_data)
            for investment_data in scrape_data[1]
        ]
        for investment in investments_data:
            db.session.add(investment)
        db.session.commit()
        flats_data = [
            FlatModel(developer_id=developer_data.id,
                      investment_id=list(filter(lambda invest: invest.name == flat_data['invest_name'],
                                                investments_data))[0].id,
                      **flat_data)
            for flat_data in scrape_data[2]
        ]
        for flat in flats_data:
            db.session.add(flat)
        db.session.commit()
        return developer_data
