import os
from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from . import add_paper_bp
from models import Paper, Country
from utils.extract_paper_info import extract_paper_info
from utils.country_code_map import get_country_code
from utils.recaptcha import is_human


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@add_paper_bp.route('/', methods=['GET', 'POST'])
def add_paper():
    # Global config variables for the template (to distinguished add_paper and edit_paper)
    config = {}
    config['url_for_action'] = 'add_paper.add_paper'
    config['submit_botton'] = 'Add paper'
    config['submit_action'] = 'add'
    config['pub_key'] = current_app.config['RECAPTCHA_SITE_KEY']

    if request.method == 'POST':
        if not current_user.is_authenticated:
            captcha_response = request.form['g-recaptcha-response']
            if not is_human(captcha_response):
                flash(f'Invalid captcha.', category='error')
                return redirect(request.referrer)
        paper = extract_paper_from_request(request)
        # Paper is None because the certificate file exceedes the size limit.
        if paper is None:
            return redirect(request.referrer)
        
        # Check if the paper already exists
        if Paper.objects(doi=paper.doi):
            flash(f"There exists a best paper award assigned to this DOI/URL.", category='error')
            return render_template('add_paper/index.html', data=paper, config=config)

        # Extract paper action
        if 'extract' in request.form:
            print(f'extracint info...............................')
            paper_info = extract_paper_info(paper.doi)
            if paper_info is None:
                print(f'extracint info fail...............................')
                flash(f"Information couldn't retrieved automatically. Please, fill it out.", category='warning')
            else:
                if paper_info.title: paper.title = paper_info.title
                if paper_info.venue: paper.venue = paper_info.venue
                if paper_info.year: paper.year = paper_info.year
                if paper_info.authors: paper.authors = paper_info.authors
                if paper_info.affiliations: paper.affiliations = paper_info.affiliations
                if paper_info.countries: paper.countries = paper_info.countries
            return render_template('add_paper/index.html', data=paper, config=config)
        
        # Add paper action
        elif 'add' in request.form:
            certificate_file = request.files['certificate']
            filename = None
            if certificate_file:
                if allowed_file(certificate_file.filename):
                    filename = secure_filename(certificate_file.filename)
                    certificate_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash(f'Invalid file extension for certificate. Please, use one of these: {", ".join(ALLOWED_EXTENSIONS)}', category='error')
                    return render_template('add_paper/index.html', data=paper, config=config)
            paper.certificate = filename
            for c in paper.countries:
                c.save()
            paper.save()
            if current_user.is_authenticated:
                return redirect(url_for('admin.index'))    
            else:
                return redirect(url_for('table.index'))
    return render_template('add_paper/index.html', config=config) 


def extract_paper_from_request(request) -> Paper:
    try:
        doi = request.form['doi']
    except RequestEntityTooLarge:
        flash(f'Certificate file exceded the size limit ({int(current_app.config["MAX_CONTENT_LENGTH"])/1e6} MB).', category='error')
        return None
    id = hash(doi)
    title = request.form['title']
    year = request.form['year']
    venue = request.form['venue']
    award = request.form['award']
    extended_doi = request.form['extended_doi']
    verified = True if request.form.get('verified', False) == 'on' else False
    # Process authors
    authors = request.form['authors']
    authors = [a.strip() for a in authors.split(',')] if authors else []
    # Process affiliations
    affiliations = request.form['affiliations']
    affiliations = [a.strip() for a in affiliations.split(',')] if affiliations else []
    # Process countries
    countries = request.form['countries']
    countries_names = [c.strip() for c in countries.split(',')] if countries else []
    countries = []
    for country in countries_names:
        country_code = get_country_code(country)
        country_code = None if country_code is None else country_code.lower()
        c = Country(name=country, code=country_code)
        countries.append(c)
    # Create paper
    paper = Paper(id=id)
    paper.doi = doi
    paper.title = title if title else None
    paper.year = year if year else None
    paper.venue = venue if venue else None
    paper.award = award if award else None
    paper.extended_doi = extended_doi if extended_doi else None
    paper.verified = verified
    paper.authors = authors
    paper.affiliations = affiliations
    paper.countries = countries
    return paper
