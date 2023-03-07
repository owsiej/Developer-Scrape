from db import db


class DeveloperModel(db.Model):
    __tablename__ = "developers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String)
    investments = db.relationship("InvestmentModel", back_populates="developer", lazy="dynamic")
    flats = db.relationship("FlatModel", back_populates="developer", lazy="dynamic")
