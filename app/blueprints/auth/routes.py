from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from . import auth_bp
from .forms import LoginForm, SignupForm
from .models import User, get_user



@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('table.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('table.index')
            return redirect(next_page)
    return render_template('auth/login.html', form=form)


@auth_bp.route("/signup/", methods=["GET", "POST"])
@login_required
def show_signup_form():
    #if current_user.is_authenticated:
    #    return redirect(url_for('table.index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Create and save the user
        user_id = len(User.objects) + 1
        user = User(id=user_id, username=name, email=email)
        user.set_password(password)
        user.save()
        flash(f'New admin successfully registered.')
        # Maintain the user logged
        #login_user(user, remember=True)
        #next_page = request.args.get('next', None)
        #if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('table.index')
        #return redirect(next_page)
    return render_template("auth/register.html", form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('table.index'))