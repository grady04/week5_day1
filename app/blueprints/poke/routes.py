from flask import render_template, request, flash, redirect, url_for
from .forms import PokemonForm
import requests
from .import bp as poke
from ...models import User, Pokemon
from app.blueprints.auth.auth import token_auth
from flask_login import current_user,login_required

# replace render_template

@poke.route('/pokemon', methods=['GET', 'POST'])
@login_required
def search_pokemon():
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

# have to edit redirects

@poke.route("/catch/<string:name>")
@login_required
def catch_em(name):
    pokemon = Pokemon().query.filter_by(name=name).first()
    if current_user.if_caught(pokemon):
        flash(f"{pokemon.name.title()} is already in your team!","warning")
        return redirect(url_for("poke.search_pokemon"))
    elif not current_user.if_caught(pokemon) and current_user.pokemon.count() < 5:
        current_user.catch_em(pokemon)
        flash(f"{pokemon.name.title()} has been caught!","success")
        return redirect(url_for("poke.search_pokemon"))
    elif current_user.pokemon.count() == 5:
        flash("You have a full team of Pokemon! Let's battle!", "success")
        return redirect(url_for("poke.search_pokemon"))
    flash("There was an unexpected error.")
    return redirect(url_for("poke.search_pokemon"))

@poke.route("/pokemonteam")
@login_required
def pokemon_team():
    if current_user.pokemon.count() > 0:
        return render_template('pokemonteam.html.j2')
    else:
        flash("Go find some pokemon!")
        return redirect(url_for("poke.search_pokemon"))