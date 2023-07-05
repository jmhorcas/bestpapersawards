import os
from flask import render_template, current_app, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from . import admin_bp
from blueprints.add_paper.routes import ALLOWED_EXTENSIONS, allowed_file, extract_paper_from_request
from models import Paper, Country

from utils.extract_paper_info import extract_paper_info


# Define routes and views
@admin_bp.route('/')
@login_required
def index():
    papers = Paper.objects().order_by('-year')
    return render_template('admin/index.html', data=papers)


@admin_bp.route('/edit/<path:id>/', methods=['GET'])
@login_required
def edit_paper(id):
    # Global config variables for the template (to distinguished add_paper and edit_paper)
    config = {}
    config['url_for_action'] = 'admin.update_paper'
    config['submit_botton'] = 'Update paper'
    config['submit_action'] = 'update'
    config['readonly_doi'] = True
    config['download_certificate'] = True

    paper = Paper.objects(id=id).first()
    return render_template('admin/edit_paper.html', data=paper, config=config)
    

@admin_bp.route('/update/', methods=['POST'])
@login_required
def update_paper():
    # Global config variables for the template (to distinguished add_paper and edit_paper)
    config = {}
    config['url_for_action'] = 'admin.update_paper'
    config['submit_botton'] = 'Update paper'
    config['submit_action'] = 'update'
    config['readonly_doi'] = True
    config['download_certificate'] = True

    if request.method == 'POST':
        paper = extract_paper_from_request(request)
        # Paper is None because the certificate file exceedes the size limit.
        if paper is None:
            return redirect(request.referrer)
        
        original_paper = Paper.objects(doi=paper.doi).first()
        paper.certificate = original_paper.certificate

        # Extract paper action
        if 'extract' in request.form:
            paper_info = extract_paper_info(paper.doi)
            if paper_info is None:
                flash(f"Information couldn't retrieved automatically. Please, fill it out.", category='info')
            else:
                if paper_info.title: paper.title = paper_info.title
                if paper_info.venue: paper.venue = paper_info.venue
                if paper_info.year: paper.year = paper_info.year
                if paper_info.authors: paper.authors = paper_info.authors
                if paper_info.affiliations: paper.affiliations = paper_info.affiliations
                if paper_info.countries: paper.countries = paper_info.countries
            return render_template('admin/edit_paper.html', data=paper, config=config)
        
        # Add paper action
        elif 'update' in request.form:
            certificate_file = request.files['certificate']
            filename = None
            if certificate_file:
                if allowed_file(certificate_file.filename):
                    filename = secure_filename(certificate_file.filename)
                    certificate_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    paper.certificate = filename
                else:
                    flash(f'Invalid file extension for certificate. Please, use one of these: {", ".join(ALLOWED_EXTENSIONS)}', category='error')
                    return render_template('admin/edit_paper.html', data=paper, config=config)
            for c in paper.countries:
                if not Country.objects(name=c.name):
                    c.save()
            original_paper.title = paper.title
            original_paper.extended_doi = paper.extended_doi
            original_paper.venue = paper.venue
            original_paper.year = paper.year
            original_paper.authors = paper.authors
            original_paper.affiliations = paper.affiliations
            original_paper.countries = paper.countries
            original_paper.award = paper.award
            original_paper.certificate = paper.certificate
            original_paper.verified = paper.verified
            original_paper.save()
            return redirect(url_for('admin.index'))
   

@admin_bp.route('/delete/<path:id>/', methods=['GET'])
@login_required
def delete_paper(id):
    paper = Paper.objects(id=id).first()
    if paper.certificate:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], paper.certificate))
    paper.delete()
    return redirect(url_for('admin.index'))
