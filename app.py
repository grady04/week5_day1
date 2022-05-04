from flask import Flask, render_template, request
import requests



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name') # remember property called name in bootstrap
        
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
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
        
        return render_template('pokemon.html.j2', pokedex_entry=pokedex_entry)

    return render_template('pokemon.html.j2')