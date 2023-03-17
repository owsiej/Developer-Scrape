from flask.views import MethodView
from flask_smorest import Blueprint
from flask import send_file
from schemas.schema import FlatSearchQueryArgs
from models import FlatModel, DeveloperModel
from db import db
from schemas.flat_query_search_filter import find_filters
from itertools import groupby
from services.data_to_excel.create_excel import create_memory_excel_file
from sqlalchemy import or_

blp = Blueprint("data_to_excel", __name__, description="Saving flats data to an Excel file.")


@blp.route('/flats_to_excel')
class FlatList(MethodView):
    @blp.arguments(FlatSearchQueryArgs, location="query")
    @blp.response(200,
                  description="Returns list of flats of given parameters in an Excel file. If any not supported "
                              "parameter is going to be used, it will be ignored without raising any error.")
    @blp.alt_response(422,
                      description="Returned if user passed parameters of invalid data type. In this case "
                                  "flats won't be searched.")
    def get(self, search_args):
        filters = find_filters(search_args)

        data = FlatModel.query.filter(or_(*filters[0])).filter(*filters[1]).all()

        flats = [dict(filter(lambda x: not x[0].startswith("_"), flat.__dict__.items()))
                 for flat in data]
        sorted_flats_by_developer = [{db.get_or_404(DeveloperModel, x).name: list(y)}
                                     for x, y in groupby(flats, lambda z: z["developer_id"])]

        excelFile = create_memory_excel_file(sorted_flats_by_developer)
        return send_file(excelFile,
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True,
                         download_name="All flats.xlsx")
