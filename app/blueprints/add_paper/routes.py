import os
from flask import render_template, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from . import add_paper_bp
from models import Paper, Country

from utils.extract_paper_info import get_paper_info
from utils.country_code_map import get_country_code


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@add_paper_bp.route('/add', methods=['GET', 'POST'])
def add_paper():
    if request.method == 'POST':
        if 'extract' in request.form:
            doi = request.form['doi']
            paper_info = extract_paper_info(doi)
            if paper_info is None:
                flash(f"Information couldn't retrieved automatically. Please, fill it out.", category='info')
                paper_info = {}
            paper_info['doi'] = doi
            return render_template('add_paper/index.html', data=paper_info)
        elif 'add' in request.form:
            doi = request.form['doi']
            title = request.form['title']
            year = request.form['year']
            venue = request.form['venue']
            authors = request.form['authors']
            affiliations = request.form['affiliations']
            countries = request.form['countries']
            award = request.form['award']
            certificate_file = request.files['certificate']

            authors = authors.split(',') if authors else []
            affiliations = affiliations.split(',') if affiliations else []
            countries_names = countries.split(',') if countries else []
            countries = []
            for country in countries_names:
                country_code = get_country_code(country).lower()
                c = Country(name=country, code=country_code).save()
                countries.append(c)

            filename = None
            if certificate_file:
                if allowed_file(certificate_file.filename):
                    filename = secure_filename(certificate_file.filename)
                    certificate_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash(f'Invalid file extension for certificate. Please, use one of these: {", ".join(ALLOWED_EXTENSIONS)}', category='error')
                    paper_info = {}
                    paper_info['doi'] = request.form['doi']
                    paper_info['title'] = request.form['title']
                    paper_info['year'] = request.form['year']
                    paper_info['venue'] = request.form['venue']
                    paper_info['authors'] = request.form['authors']
                    paper_info['affiliations'] = request.form['affiliations']
                    paper_info['countries'] = request.form['countries']
                    paper_info['award'] = request.form['award']
                    return render_template('add_paper/index.html', data=paper_info)
            
            print(f'Filename: {filename}')
            paper = Paper(doi=doi,
                          title=title,
                          year=year,
                          venue=venue,
                          authors=authors,
                          affiliations=affiliations,
                          countries=countries,
                          award=award,
                          certificate=filename).save()
            # with open(certificate, 'rb') as fd:
            #     paper.certificate.put(fd)
            # paper.save()
            
            return redirect(url_for('table.index'))
    return render_template('add_paper/index.html') 


def extract_paper_info(doi: str) -> dict[str, str]:
    paper_info = None
    info = get_paper_info(doi)  # Extract paper info automatically
    if info is not None:
        title, authors, year, venue = info
        paper_info = {}
        paper_info['title'] = title
        paper_info['year'] = year
        paper_info['venue'] = venue
        paper_info['authors'] = ', '.join([f'{a.get("given")} {a.get("family")}' for a in authors])
        paper_info['affiliations'] = ', '.join({f'{af.get("name").split(",", 1)[0]}' for a in authors for af in a.get("affiliation")})
        paper_info['countries'] = ', '.join({f'{af.get("name").split(",")[-1].strip()}' for a in authors for af in a.get("affiliation")})
    return paper_info