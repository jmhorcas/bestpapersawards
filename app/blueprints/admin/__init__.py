from flask import Blueprint

# Create the blueprint instance
admin_bp = Blueprint('admin',
                     __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/table/static')

# Import the routes module
from . import routes