from my_server.app import db, app
from my_server.app import bcrypt

class User(db.Model):
    __bind_key__ = app.config.get('DB_NAME')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    ps = db.Column(db.String(200))
    name = db.Column(db.String(40))
    belong = db.Column(db.String(40))

    def is_valid_password(self, in_val):
        return bcrypt.check_password_hash(self.ps, in_val)