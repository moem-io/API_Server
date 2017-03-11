from my_server.app import db

class Hub(db.Model):
    hub_id = db.Column(db.String(40), primary_key=True)
    hub_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')