from db import db


class InvestmentModel(db.Model):
    __tablename__ = "investments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String)
    developer_id = db.Column(db.Integer,
                             db.ForeignKey("developers.id", ondelete='RESTRICT', onupdate='CASCADE'),
                             unique=False, nullable=False)
    developer = db.relationship("DeveloperModel", back_populates="investments")
    flats = db.relationship("FlatModel", back_populates='investment',
                            foreign_keys="FlatModel.invest_name"
                            , lazy="dynamic", cascade="all,delete")
    flats_2 = db.relationship("FlatModel", back_populates='investment_2',
                              foreign_keys="FlatModel.investment_id"
                              , lazy="dynamic", cascade="all,delete")
