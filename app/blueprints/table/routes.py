from flask import render_template, send_from_directory, current_app
from . import table_bp
from models import Paper


# Define routes and views
@table_bp.route('/')
def index():
    config = {}
    config['table_id'] = 'bpa_table'

    papers = Paper.objects().order_by('-year')
    return render_template('table/index.html', data=papers, config=config)


@table_bp.route('/certificate/<path:doi>', methods=['GET'])
def download_certificate(doi):
    paper = Paper.objects(doi=doi).first()
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], paper.certificate, as_attachment=True)
