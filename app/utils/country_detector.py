# app/utils/country_detector.py

from config.country_aliases import COUNTRY_ALIASES


def detect_country(query: str) -> str:
    query = query.lower()

    for country, aliases in COUNTRY_ALIASES.items():
        for alias in aliases:
            if alias in query:
                return country

    return "europe"