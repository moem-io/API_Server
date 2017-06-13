from my_server.app import db, app
from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text

class AppModel(db.Model):
    __bind_key__ = app.config.get('API_APP_DB')

    __tablename__ = 'app_model'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, nullable=False)
    app_name = db.Column(db.String(100), nullable=False )
    app_detail = db.Column(db.String(100), nullable=False )
    app_switch = db.Column(db.Boolean, default=True)
    app_input = db.Column(db.String(100), nullable=False )
    app_input_detail = db.Column(db.String(100), nullable=False )
    app_output = db.Column(db.String(100), nullable=False )
    app_output_detail = db.Column(db.String(100), nullable=False)

    created_date = db.Column(
        db.String(100),
        default=str(datetime.datetime.utcnow()).split('.')[0],
    )

    def __init__(self, app_id, app_name, app_detail, app_switch, app_input, app_input_detail, app_output, app_output_detail, created_date):
        self.app_id = app_id
        self.app_name = app_name
        self.app_detail = app_detail
        self.app_switch = app_switch
        self.app_input = app_input
        self.app_input_detail = app_input_detail
        self.app_output = app_output
        self.app_output_detail = app_output_detail
        self.created_date = created_date

    def __repr__(self):
        return "<Nodes('%s', '%s', '%s')>" % (self.id, self.app_name, self.app_detail)