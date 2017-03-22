from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, required, Length, EqualTo

class SignInForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password_check = PasswordField('password_check', validators=[DataRequired()])

    name = StringField('name', validators=[DataRequired()])
    belong = StringField('belong', validators=[DataRequired()])