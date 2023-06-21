from collections import OrderedDict

import requests

from models import Paper, Country
from utils.country_code_map import get_country_code


def get_paper_info(doi):
    # API endpoint for CrossRef
    api_url = f'https://api.crossref.org/works/{doi}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception if the request fails
        data = response.json()

        # Extract relevant information from the response
        title = data["message"]["title"][0]
        authors = data["message"]["author"]
        year = data["message"]["created"]["date-parts"][0][0]
        venue = data["message"]["container-title"][0]

        return title, authors, year, venue
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None
    

def extract_paper_info(doi: str) -> Paper:
    paper = None
    info = get_paper_info(doi)  # Extract paper info automatically
    if info is not None:
        title, authors, year, venue = info
        id = hash(doi)
        paper = Paper(id=id)
        paper.doi = doi
        paper.title = title
        paper.year = year
        paper.venue = venue
        authors_list = [f'{a.get("given").strip()} {a.get("family").strip()}' for a in authors]
        paper.authors = list(OrderedDict.fromkeys(authors_list))
        affiliations_list = [f'{af.get("name").split(",", 1)[0].strip()}' for a in authors for af in a.get("affiliation")]
        paper.affiliations = list(OrderedDict.fromkeys(affiliations_list))
        countries_list = [f'{af.get("name").split(",")[-1].strip()}' for a in authors for af in a.get("affiliation")]
        countries_names = list(OrderedDict.fromkeys(countries_list))
        countries = []
        for country in countries_names:
            country_code = get_country_code(country)
            country_code = '--' if country_code is None else country_code.lower()
            c = Country(name=country, code=country_code)
            countries.append(c)
        paper.countries = countries
    return paper