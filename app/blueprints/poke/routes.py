from flask import render_template, request, g
from .forms import PokemonForm
import requests
from .import bp as poke
from ...models import User, Pokemon
from app.blueprints.auth.auth import token_auth
from flask_login import current_user,login_required


@poke.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokename = form.pokemon.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokename}'
        response = requests.get(url)
        if not response.ok:
            return "We're Blasting off again!"
        data = response.json()
        pokedex_entry = {
            "name": data['name'],
            "base_exp" : data['base_experience'],
            "sprites": data['sprites']['front_shiny'],
            "ability": data['abilities'][0]['ability']['name'],
            "hp": data['stats'][0]['base_stat'],
            "attack": data['stats'][1]['base_stat'],
            "defense": data['stats'][2]['base_stat'],
        }
        wild = Pokemon()
        wild.from_dict(pokedex_entry)
        wild.save()
        
        return render_template('pokemon.html.j2', pokedex_entry=pokedex_entry, form=form)

    return render_template('pokemon.html.j2', form=form)