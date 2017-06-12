from my_server.app import db, app
from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text

class AppSetting(db.Model):
    __bind_key__ = app.config.get('DB_NAME')

    __tablename__ = 'app_setting'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, nullable=False )
    in_node = db.Column(db.Integer, nullable=False )
    in_sensor = db.Column(db.Integer, nullable=False )
    out_node = db.Column(db.Integer, nullable=False )
    out_sensor = db.Column(db.Integer, nullable=False )

    created_date = db.Column(
        db.String(100),
        default=datetime.datetime.utcnow,
    )

    def __init__(self, app_id, in_node, in_sensor, out_node, out_sensor):
        self.app_id = app_id
        self.in_node = in_node
        self.in_sensor = in_sensor
        self.out_node = out_node
        self.out_sensor = out_sensor

    def __repr__(self):
        return "<app_setting('%s', '%s', '%s')>" % (self.id, self.app_id, self.in_node)