from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from ...models import User

# need to make a class for pokemon form
class PokemonForm(FlaskForm):
    pokemon = StringField('Pokemon Name', validators = [DataRequired()])
    find = SubmitField("Gotta Catch 'em all!")