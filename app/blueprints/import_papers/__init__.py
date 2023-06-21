from flask import Blueprint

# Create the blueprint instance
import_bp = Blueprint('import_papers',
                     __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/import_papers/static')

# Import the routes module
from . import routes