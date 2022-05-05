from flask_wtf import FlaskForm
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError
from .models import User

# FORM SECTION
class LoginForm(FlaskForm): # class inheritance --- super great now
    email = StringField('Email Address', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

# need to make a class for pokemon form
class PokemonForm(FlaskForm): # again class inheritance, keep an eye on it
    pokemon = StringField('Pokemon Name', validators = [DataRequired()])
    find = SubmitField("Gotta Catch 'em all!")

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Password', validators = [DataRequired(), EqualTo('password', message= 'passwords must match')])
    submit = SubmitField('Register')

    # need to be sure the email isn't already used
    # must be named this way for a custom validator: validate_fieldname
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
                # SELECT * FROM User WHERE email = ???
                # filter_by will always return list unless you use first
        if same_email_user:
            raise ValidationError("email already in use")