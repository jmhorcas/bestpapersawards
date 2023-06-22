import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
import mongoengine

from dotenv import load_dotenv
load_dotenv('.env')

from blueprints.table import table_bp
from blueprints.add_paper import add_paper_bp
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.import_papers import import_bp

from blueprints.auth.models import User


# Create the App
app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_FILE_SIZE_MB')) * 1000 * 1000
app.secret_key = os.environ.get('SECRET_KEY')


# Connect to the database
user_db = os.environ.get('USER_DB')
pass_db = os.environ.get('PASS_DB')
mongoengine.connect('bpa_db', host='localhost', port=27017, username=user_db, password=pass_db, authentication_source='bpa_db')
#mongoengine.connect('bpa_db', host='127.0.0.1', port=27017)


# Configure login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


# Configura re-captcha
app.config['RECAPTCHA_SITE_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')


# Register blueprints
#app.register_blueprint(repository_bp, url_prefix='/repo')
app.register_blueprint(table_bp, url_prefix='/')
app.register_blueprint(add_paper_bp, url_prefix='/add')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(import_bp, url_prefix='/import')


# Error pages
def page_not_found(e):
    return render_template('404.html'), 404
app.register_error_handler(404, page_not_found)


# About page
@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(413)
def request_entity_too_large(error):
    doi = request.form['doi']
    flash("File too big.", category='error')
    return redirect(url_for('admin.edit_paper'), doi=doi)


# Help page
@app.route('/help')
def help():
    return render_template('help.html')


# Login
@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
