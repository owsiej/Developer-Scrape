from marshmallow import Schema, fields


class PlainDeveloperSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)


class PlainInvestmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)


class PlainFlatSchema(Schema):
    id = fields.Int(dump_only=True)
    floor_number = fields.Int(allow_none=True)
    rooms_number = fields.Int(allow_none=True)
    area = fields.Float(allow_none=True)
    price = fields.Float(allow_none=True)
    status = fields.Str(allow_none=True)


class DeveloperSchema(PlainDeveloperSchema):
    investments = fields.List(fields.Nested(PlainInvestmentSchema()), load_only=True)
    flats = fields.List(fields.Nested(PlainFlatSchema()), load_only=True)


class InvestmentSchema(PlainInvestmentSchema):
    developer_id = fields.Int(required=True, dump_only=True)
    developer = fields.Nested(PlainDeveloperSchema(), load_only=True)
    flats = fields.List(fields.Nested(PlainFlatSchema()), load_only=True)


class FlatSchema(PlainFlatSchema):
    investment_id = fields.Int(required=True, dump_only=True)
    investment = fields.Nested(PlainDeveloperSchema(), load_only=True)
    developer_id = fields.Int(required=True, dump_only=True)
    developer = fields.Nested(PlainDeveloperSchema(), load_only=True)
    invest_name = fields.Str(required=True)


class DeveloperUpdateSchema(Schema):
    name = fields.Str()
    url = fields.Str()


class InvestmentUpdateSchema(Schema):
    name = fields.Str()
    url = fields.Str()
    developer_id = fields.Int()


class InvestmentByDeveloperUpdateSchema(InvestmentUpdateSchema):
    name = fields.Str(required=True)


class FlatUpdateSchema(Schema):
    floor_number = fields.Int()
    rooms_number = fields.Int()
    area = fields.Float()
    price = fields.Float()
    status = fields.Str()


class FlatSearchQueryArgs(Schema):
    floor_number = fields.Int()
    floor_number__gt = fields.Int()
    floor_number__lt = fields.Int()
    rooms_number = fields.Int()
    rooms_number__gt = fields.Int()
    rooms_number__lt = fields.Int()
    area = fields.Float()
    area__gt = fields.Float()
    area__lt = fields.Float()
    price = fields.Float()
    price__gt = fields.Float()
    price__lt = fields.Float()
    status = fields.Str()
    status__ne = fields.Str()


class FlatSearchQueryByInvestment(FlatSearchQueryArgs):
    investment_id = fields.Int(required=True)


class FlatSearchQueryByDeveloper(FlatSearchQueryArgs):
    developer_id = fields.Int(required=True)


class PlainScrapeSchema(Schema):
    developer_id = fields.Int(required=True)


class ScrapeSchema(PlainScrapeSchema):
    developer_name = fields.Str(required=True)


class FinalResponseScrapeSchema(PlainDeveloperSchema):
    investments = fields.List(fields.Nested(PlainInvestmentSchema()), dump_only=True)
    flats = fields.List(fields.Nested(PlainFlatSchema()), dump_only=True)
