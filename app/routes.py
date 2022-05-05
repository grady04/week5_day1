from flask import render_template, request, flash, redirect, url_for
from .forms import LoginForm,PokemonForm,RegisterForm
import requests
from app import app
from .models import User
from flask_login import current_user,logout_user,login_user,login_required



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        # all my login stuff
        email = form.email.data.lower()
        password = form.password.data

        # look up user by email address
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash("Login Success! Get ready to battle!", 'success')
            return redirect(url_for('index'))
        flash('Incorrect email, password combo', 'danger')
        return render_template('login.html.j2', form=form)

    return render_template('login.html.j2', form=form)


@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # all the registration stuff
        # used try because that's what Kevin did
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }

            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        
        except:
            flash("Error creating account, please try again later", "danger")
            return render_template("register.html.j2", form=form)
        return redirect(url_for("login"))
    return render_template("register.html.j2", form=form)




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