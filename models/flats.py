from db import db


class FlatModel(db.Model):
    __tablename__ = "flats"

    id = db.Column(db.Integer, primary_key=True)

    invest_name = db.Column(db.String, db.ForeignKey("investments.name", ondelete='CASCADE', onupdate='CASCADE'),
                            unique=False, nullable=False)

    floor_number = db.Column(db.Integer)
    rooms_number = db.Column(db.Integer)
    area = db.Column(db.Float(precision=2))
    price = db.Column(db.Float(precision=2))
    status = db.Column(db.String)
    investment_id = db.Column(db.Integer, db.ForeignKey("investments.id", ondelete='CASCADE', onupdate='CASCADE'),
                              unique=False, nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey("developers.id", ondelete='RESTRICT', onupdate='CASCADE'),
                             unique=False)

    investment = db.relationship("InvestmentModel", back_populates="flats", foreign_keys="FlatModel.invest_name")

    investment_2 = db.relationship("InvestmentModel",
                                   back_populates="flats_2", foreign_keys="FlatModel.investment_id")
    developer = db.relationship("DeveloperModel", back_populates="flats")
