from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from . import auth_bp
from .models import User, get_user



@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = bool(request.form.get('rememberme', False))

        user = get_user(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin.index')
            return redirect(next_page)
        else:
            flash(f'Invalid email or password.', category='error')
    return render_template('auth/login.html')


@auth_bp.route("/signup/", methods=["GET", "POST"])
@login_required
def show_signup_form():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Create and save the user
        if User.objects(email=email):
            flash(f"There exists an admin with this email.", category='error')
            return render_template('auth/register.html')
        print(f'email: {email}')
        print(f'password: {password}')
        user = User(email=email)
        user.set_password(password)
        user.save()
        flash(f'New admin successfully registered.', category='info')
    return render_template("auth/register.html")


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('table.index'))