from flask import render_template, send_from_directory, current_app
from . import table_bp
from models import Paper


# Define routes and views
@table_bp.route('/')
def index():
    papers = Paper.objects().order_by('-year')
    return render_template('table/index.html', data=papers)


@table_bp.route('/certificate/<path:certificate>/', methods=['GET'])
def download_certificate(certificate):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], certificate, as_attachment=True)
