from my_server.app import db

class Hub(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    hub_id = db.Column(db.String(40))
    hub_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')