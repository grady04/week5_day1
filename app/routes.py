from flask import render_template, request
from .forms import LoginForm,PokemonForm
import requests
from app import app



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()


    if request.method == 'POST' and form.validate_on_submit():
        # all my login stuff
        email = form.email.data.lower() #form no longer comes from bootstrap
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            # login success
            return f"Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
        error_string = "incorrect email or password"
        return render_template('login.html.j2', error=error_string, form=form)

    return render_template('login.html.j2', form=form)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokename = form.pokemon.data.lower()
        # pokemon_name = request.form.get('pokemon_name') # remember property called name in bootstrap
        
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
        
        return render_template('pokemon.html.j2', pokedex_entry=pokedex_entry, form=form)

    return render_template('pokemon.html.j2', form=form)