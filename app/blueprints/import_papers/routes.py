import io
import csv
import requests
from flask import render_template, request, flash
from flask_login import login_required
from . import import_bp
from models import Paper, Country
from bs4 import BeautifulSoup

from utils.country_code_map import get_country_code


@import_bp.route('/', methods=['GET'])
@login_required
def import_data():
    return render_template('import_papers/import_data.html')


@import_bp.route('/from_csv/', methods=['GET', 'POST'])
@login_required
def import_from_csv():
    config = {}
    config['action'] = 'csv'

    if request.method == 'POST':
        csv_file = request.files['data_file']
        filename = csv_file.filename
        if '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv':
            # data = csv_file.read()
            stream = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
            content_data = csv.DictReader(stream)
            # next(content_data, None)  # skip the headers
            n_paper_imported = 0
            n_paper_duplicated = 0
            n_paper_errors = 0
            for row in content_data:
                doi = doi=row['DOI']
                id = hash(doi)
                paper = Paper(id=id)
                if Paper.objects(doi=doi):
                    n_paper_duplicated += 1
                else:
                    try:
                        paper.doi = doi
                        paper.title = row.get('Title', None)
                        paper.year = row.get('Year', None)
                        paper.venue = row.get('Venue', None)
                        paper.award = row.get('Award', None)
                        paper.extended_doi = row.get('Ext.', None)
                        paper.verified = True if row.get('Verified', False) == 'True' else False
                        authors = row.get('Authors', [])
                        authors = [a.strip() for a in authors.split(',')] if authors else []
                        paper.authors = authors
                        affiliations = row.get('Affiliations', [])
                        affiliations = [a.strip() for a in affiliations.split(',')] if affiliations else []
                        paper.affiliations = affiliations
                        countries_names = row.get('Countries', [])
                        countries_names = [c.strip() for c in countries_names.split(',')] if countries_names else []
                        countries = []
                        for country in countries_names:
                            country_code = get_country_code(country)
                            country_code = None if country_code is None else country_code.lower()
                            c = Country(name=country, code=country_code)
                            countries.append(c)
                            if not Country.objects(name=c.name):
                                c.save()
                        paper.countries = countries
                        paper.save()
                    except:
                        n_paper_errors += 1
                    n_paper_imported += 1
            flash(f'{n_paper_imported} papers were correctly imported. {n_paper_duplicated + n_paper_errors} papers not imported ({n_paper_duplicated} duplicated, {n_paper_errors} errors).', category='info')
        else:
            flash(f'Invalid file. It must be a .csv file.', category='error')
            return render_template('import_papers/import_data.html', config=config)
    return render_template('import_papers/import_data.html', config=config)


@import_bp.route('/from_acm/', methods=['GET', 'POST'])
@login_required
def import_from_acm():
    config = {}
    config['action'] = 'acm'

    ACM_URL_BEST_PAPERS = "https://www.acm.org/conferences/best-paper-awards"
    r = requests.get(ACM_URL_BEST_PAPERS)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find_all('p')
    for row in table[33:34]:  # 33 is the first <p> of a best paper (TODO: improve this)
        print(row)
        doi = row.a['href']
        title = row.a
        print(f'DOI: {doi}')
        print(f'title: {title}')
    #print(r.content)
    flash(f'This functionality is experimental.', category='warning')
    return render_template('import_papers/import_data.html', config=config)