import pandas as pd
import random
from geo import get_coordinates_google

RISK_KEYWORDS = [
    "explosion", "attack", "war", "conflict",
    "riot", "protest", "violence", "terror"
]

def process_data(articles):

    data = []

    for art in articles:

        title = art.get("title", "").lower()
        country = art.get("sourceCountry", "Unknown")
        url = art.get("url", "")

        lat, lon = get_coordinates_google(country)

        if lat is None or lon is None:
            lat = random.uniform(-50, 50)
            lon = random.uniform(-100, 100)

        keyword_count = sum(1 for w in RISK_KEYWORDS if w in title)

        data.append({
            "title": title,
            "country": country,
            "url": url,
            "lat": lat,
            "lon": lon,
            "keyword_count": keyword_count,
            "alert": keyword_count > 0
        })

    df = pd.DataFrame(data)

    # 🔥 LIMPIEZA CLAVE
    df = df.dropna(subset=["lat", "lon"])

    return df