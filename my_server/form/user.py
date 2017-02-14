from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, required, Length, EqualTo

# Todo Form have to change FlaskForm
class SignInForm(Form):
    username = StringField('username', validators=[DataRequired])
    password = PasswordField('password', validators=[DataRequired])