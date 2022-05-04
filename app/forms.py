from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email

# FORM SECTION
class LoginForm(FlaskForm): # class inheritance --- super great now
    email = StringField('Email Address', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')