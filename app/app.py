from flask import Flask
import mongoengine

from blueprints.table import table_bp
from blueprints.add_paper import add_paper_bp



UPLOAD_FOLDER = 'uploads/certificates'


# Create the App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Connect to the database
mongoengine.connect('bpa_db', host='127.0.0.1', port=27017)

# Register blueprints
#app.register_blueprint(repository_bp, url_prefix='/repo')
app.register_blueprint(table_bp, url_prefix='/')
app.register_blueprint(add_paper_bp, url_prefix='/')


if __name__ == "__main__":
    #models.Model(name='Pizzas', year=2017, paper_reference='https://doi.org/10.1016/j.jss.2022.111551').save()
    #models.Model(name='WeaFQAs', year=2018, paper_reference='https://doi.org/10.1016/j.jss.2022.111551').save()
    #au = models.Author(orcid='0000-0002-7771-0575', first_name='Jose-Miguel', last_name='Horcas').save()
    #print(au)
    # Launch the app
    app.run(debug=True)