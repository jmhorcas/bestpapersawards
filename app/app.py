from flask import Flask, render_template
from flask_login import LoginManager
import mongoengine
import secrets

from blueprints.table import table_bp
from blueprints.add_paper import add_paper_bp
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp

from blueprints.auth.models import User


UPLOAD_FOLDER = 'uploads/certificates'


# Create the App
app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secrets.token_urlsafe(16)


# Connect to the database
mongoengine.connect('bpa_db', host='127.0.0.1', port=27017)


# Configure login
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


# Register blueprints
#app.register_blueprint(repository_bp, url_prefix='/repo')
app.register_blueprint(table_bp, url_prefix='/')
app.register_blueprint(add_paper_bp, url_prefix='/add')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')


# Error pages
def page_not_found(e):
  return render_template('404.html'), 404
app.register_error_handler(404, page_not_found)


# Login
@login_manager.user_loader
def load_user(user_email):
    return User.objects(email=user_email).first()


if __name__ == "__main__":
    # Launch the app
    if not User.objects(email='horcas@uma.es'):
      user = User(email='horcas@uma.es')
      user.set_password('basket')
      user.save()
    app.run(debug=True)