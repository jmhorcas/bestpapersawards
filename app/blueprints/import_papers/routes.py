import io
import csv
import requests
import logging
from flask import render_template, request, flash
from flask_login import login_required
from . import import_bp
from models import Paper, Country
from bs4 import BeautifulSoup

from utils.extract_paper_info import extract_paper_info
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

    # Connect to the ACM Bets Paper Award page
    ACM_URL_BEST_PAPERS = "https://www.acm.org/conferences/best-paper-awards"
    r = requests.get(ACM_URL_BEST_PAPERS)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find_all('p')
    n_paper_imported = 0
    n_paper_duplicated = 0
    n_paper_errors = 0
    for row in table[33:]:  # 33 is the first <p> of a best paper (TODO: improve this)
        """
        Extract data directly from ACM Best Paper Award page
        Example of entry for a best paper:
        <p><a href="http://dl.acm.org/citation.cfm?id=3590978" target="_blank">The World is Too Big to Download: 3D Model Retrieval for World-Scale Augmented Reality</a><br/>
        By Yi-Zhen Tsai, James Luo, Yunshu Wang, Jiasi Chen<br/>
        Best Paper Award at MMSys '23: ACM Multimedia Systems Conference 2023</p>
        """
        try:
            url = row.a['href']
            text = row.getText().split('\n')
            title = text[0]
            authors = text[1][3:]
            award = text[2][0:text[2].find(' at ')]
            venue = text[2][text[2].find(':')+2:]

            # Try to get the DOI and verification of best paper using the URL
            doi_content = requests.get(url)
            doi_soup = BeautifulSoup(doi_content.content, 'html5lib')
            doi_html = doi_soup.find('a', attrs={'class': 'issue-item__doi'})
            doi = doi_html.getText()
            print('------')
            print(f'URL: {url}')
            print(f'title: {title}')
            print(f'authors: {authors}')
            print(f'award: {award}')
            print(f'venue: {venue}')
            print(f'DOI: {doi}')
            
            if Paper.objects(doi=doi):
                n_paper_duplicated += 1
            else:
                paper = extract_paper_info(doi)
                if paper is None:  # Extract the information from the web (previous values obtained)
                    id = hash(doi)
                    paper = Paper(id=id)
                    paper.doi = doi
                    paper.title = title
                    paper.authors = [a.strip() for a in authors.split(',')]
                else:
                    # Double check title for ACM errors
                    doi_title_html = doi_soup.find('h1', attrs={'class': 'citation__title'})
                    doi_title = doi_title_html.getText() if doi_title_html else ''
                    if title.lower() != doi_title.lower():
                        n_paper_errors += 1
                        logging(f'Paper (title) with error: {title}')
                        continue
                    # Verify the best paper
                    best_paper_verified_html = doi_soup.find('a', attrs={'data-title': 'Best Paper'})
                    paper.verified = True if best_paper_verified_html else False
                paper.award = award
                for c in paper.countries:
                    c.save()
                paper.save()
                n_paper_imported += 1
        except:
            n_paper_errors += 1
    flash(f'{n_paper_imported} papers were correctly imported. {n_paper_duplicated + n_paper_errors} papers not imported ({n_paper_duplicated} duplicated, {n_paper_errors} errors).', category='info')
    return render_template('import_papers/import_data.html', config=config)