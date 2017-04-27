from my_server.app import db, app

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

