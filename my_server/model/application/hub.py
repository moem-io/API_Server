from my_server.app import db, app

class Hub(db.Model):
    __bind_key__ = app.config.get('DB_NAME')

    id = db.Column(db.Integer, primary_key=True)

    hub_id = db.Column(db.String(40))
    hub_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

class node(db.Model):
    __bind_key__ = app.config.get('EX_DB')

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(40))
    radius = db.Column(db.String(40))
    rgb = db.Column(db.String(40))

    def __init__(self, name, radius, rgb):
        self.name = name
        self.radius = radius
        self.rgb = rgb

class link(db.Model):
    __bind_key__ = app.config.get('EX_DB')

    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.Integer)
    target = db.Column(db.Integer)
    length = db.Column(db.Integer)

    def __init__(self, source, target, length):
        self.source = source
        self.target = target
        self.length = length
