import requests


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