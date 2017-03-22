from my_server.app import db
from my_server.app import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    ps = db.Column(db.String(200))
    name = db.Column(db.String(40))
    belong = db.Column(db.String(40))

    def is_valid_password(self, in_val):
        return bcrypt.check_password_hash(self.ps, in_val)