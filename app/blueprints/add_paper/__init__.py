from flask import Blueprint

# Create the blueprint instance
add_paper_bp = Blueprint('add_paper',
                          __name__,
                          template_folder='templates',
                          static_folder='static',
                          static_url_path='/static')

# Import the routes module
from . import routes