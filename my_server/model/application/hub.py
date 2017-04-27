from my_server.app import db, app

class Hub(db.Model):
    __bind_key__ = app.config.get('DB_NAME')

    id = db.Column(db.Integer, primary_key=True)

    hub_id = db.Column(db.String(40))
    hub_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')