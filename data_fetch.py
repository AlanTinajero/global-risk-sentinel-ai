import requests
import random

QUERY = """
explosion OR attack OR protest OR riot OR war OR conflict 
OR violence OR military OR crisis OR terrorism
"""

def fetch_gdelt(max_records=50):

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": QUERY,
        "mode": "ArtList",
        "maxrecords": max_records,
        "format": "json",
        "sort": "DateDesc"
    }

    try:
        r = requests.get(url, params=params, timeout=8)

        if r.status_code != 200:
            return []

        data = r.json()
        return data.get("articles", [])

    except:
        return []


def enrich_articles(raw_articles):

    articles = []

    for art in raw_articles:

        title = art.get("title", "")
        country = art.get("sourceCountry", "Unknown")
        url = art.get("url", "")

        if not url:
            url = f"https://news.google.com/search?q={title.replace(' ', '+')}"

        articles.append({
            "title": title,
            "sourceCountry": country,
            "url": url
        })

    return articles


def generate_synthetic_events():

    # 🔥 SIMULA SEÑALES (para demo PRO)
    mock = [
        ("Coordinated protest activity detected", "Germany"),
        ("Multiple explosions reported", "Brazil"),
        ("Rising conflict signals in region", "Middle East"),
    ]

    return [
        {
            "title": t,
            "sourceCountry": c,
            "url": f"https://news.google.com/search?q={t.replace(' ', '+')}"
        }
        for t, c in mock
    ]


def get_gdelt_data():

    gdelt_raw = fetch_gdelt()
    gdelt_data = enrich_articles(gdelt_raw)

    synthetic = generate_synthetic_events()

    # 🔥 combinar todo
    combined = gdelt_data + synthetic

    # evitar vacío
    if not combined:
        return generate_synthetic_events()

    return combined