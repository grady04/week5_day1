from flask import render_template, request, flash, redirect, url_for
from .forms import LoginForm,RegisterForm,EditProfileForm
import requests
from .import bp as auth
from ...models import User
from flask_login import current_user,logout_user,login_user,login_required


@auth.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('poke.search_pokemon'))
        flash('Incorrect email, password combo', 'danger')
        return render_template('login.html.j2', form=form)

    return render_template('login.html.j2', form=form)


@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for("auth.login"))
    return render_template("register.html.j2", form=form)

@auth.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method=='POST' and form.validate_on_submit():
        new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
            }
        user = User.query.filter_by(email=new_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash('Email is already in use', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated','success')
        except:
            flash('Ther was an unexpected. Please Try again', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html.j2', form=form)