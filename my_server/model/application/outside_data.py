from my_server.app import db, app
from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text

class Weather(db.Model):
    __bind_key__ = app.config.get('EX_DB')
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    baseDate = db.Column(db.Integer)
    baseTime = db.Column(db.Integer)
    category = db.Column(db.String(20))
    nx = db.Column(db.Integer)
    ny = db.Column(db.Integer)
    obsrValue = db.Column(db.Integer)
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )
    def __init__(self, baseDate, baseTime, category, nx, ny, obsrValue):
        self.baseDate = baseDate
        self.baseTime = baseTime
        self.category = category
        self.nx = nx
        self.ny = ny
        self.obsrValue = obsrValue

    def __repr__(self):
        return "<Weather('%s', '%s', '%s')>" % (self.baseDate, self.baseTime, self.category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'baseDate': self.baseDate,
            'baseTime': self.baseTime,
            'category': self.category,
            'nx': self.nx,
            'ny': self.ny,
            'obsrValue': self.obsrValue,
        }


class Mise(db.Model):
    __bind_key__ = app.config.get('EX_DB')

    __tablename__ = 'mise'

    id = db.Column(db.Integer, primary_key=True)
    MSRDT_DE = db.Column(db.String(20))  # 측정 일시
    SO2 = db.Column(db.Float)  # 아황산가서ppm
    NO2 = db.Column(db.Float)  # 이산화질소농도(ppm)
    PM25 = db.Column(db.Float)  # 초미세먼지(㎍/㎥)
    MSRSTE_NM = db.Column(db.String(20))  # 측정소명
    CO = db.Column(db.Float)  # 일산화탄소농도(ppm)
    PM10 = db.Column(db.Float)  # 미세먼지(㎍/㎥)
    O3 = db.Column(db.Float)  # 오존농도(ppm)
    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )
    def __init__(self, MSRDT_DE, SO2, NO2, PM25, MSRSTE_NM, CO, PM10, O3):
        self.MSRDT_DE = MSRDT_DE
        self.SO2 = SO2
        self.NO2 = NO2
        self.PM25 = PM25
        self.MSRSTE_NM = MSRSTE_NM
        self.CO = CO
        self.PM10 = PM10
        self.O3 = O3

    def __repr__(self):
        return "<Mise('%s', '%s', '%s')>" % (self.MSRDT_DE, self.PM10, self.PM25)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'MSRDT_DE': self.MSRDT_DE,
            'SO2': self.SO2,
            'NO2': self.NO2,
            'PM25': self.PM25,
            'MSRSTE_NM': self.MSRSTE_NM,
            'CO': self.CO,
            'PM10': self.PM10,
            'O3': self.O3,
        }