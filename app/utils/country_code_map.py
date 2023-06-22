import pycountry


def get_country_code(country_name: str) -> str:
    """Given a name of a country, returns its two-letter code (ISO 3166-1 alpha-2).

    Example usage:
    country_name = "United States"
    country_code = get_country_code(country_name)
    print(country_code)  # Output: US
    """
    try:
        country = pycountry.countries.get(name=country_name)
        if country is not None:
            return country.alpha_2
        else:
            country = pycountry.countries.lookup(country_name)
            if country is not None:
                return country.alpha_2
    except (KeyError, LookupError):
        return None
    return None
