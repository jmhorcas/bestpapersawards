import os
from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from . import auth_bp
from .models import User, get_user
from utils.recaptcha import is_human


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    config = {}
    config['pub_key'] = current_app.config['RECAPTCHA_SITE_KEY']

    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        captcha_response = request.form['g-recaptcha-response']
        if not is_human(captcha_response):
            flash(f'Invalid captcha.', category='error')
            return redirect(request.referrer)
        else:
            email = request.form['email']
            password = request.form['password']
            remember_me = True if request.form.get('rememberme', False) == 'on' else False

            user = get_user(email)
            if user is not None and user.check_password(password):
                login_user(user, remember=remember_me)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('admin.index')
                return redirect(next_page)
            else:
                flash(f'Invalid email or password.', category='error')
    # Create default admin
    ENVIRONMENT_ADMIN_USER_EMAIL = os.environ.get("ADMIN_USER_EMAIL")
    ENVIRONMENT_ADMIN_PASS = os.environ.get("ADMIN_PASS")
    # Launch the app
    if not User.objects(email=ENVIRONMENT_ADMIN_USER_EMAIL):
        id = hash(ENVIRONMENT_ADMIN_USER_EMAIL)
        user = User(id=id)
        user.email = ENVIRONMENT_ADMIN_USER_EMAIL
        user.set_password(ENVIRONMENT_ADMIN_PASS)
        user.save()
    return render_template('auth/login.html', config=config)


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
        id = hash(email)
        user = User(id=id)
        user.email = email
        user.set_password(password)
        user.save()
        flash(f'New admin successfully registered.', category='info')
    return render_template("auth/register.html")


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('table.index'))