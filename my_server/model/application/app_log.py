from my_server.app import db, app
from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text

class AppLog(db.Model):
    __bind_key__ = app.config.get('DB_NAME')

    __tablename__ = 'app_log'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = db.Column(db.Integer, primary_key=True)
    log_content = db.Column(db.String(100), nullable=False)
    app_id = db.Column(db.Integer, nullable=False)
    node = db.Column(db.String(100), nullable=False)
    sensor = db.Column(db.String(100), nullable=False)

    created_date = db.Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        server_default=text('CURRENT_TIMESTAMP')
    )

    def __init__(self, log_content, app_id, node, sensor, created_date):
        self.log_content = log_content
        self.app_id = app_id
        self.node = node
        self.sensor = sensor
        self.created_date = created_date

    def __repr__(self):
        return "<AppLog('%s', '%s')>" % (self.id, self.log_content)