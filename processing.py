import pandas as pd
import random
from geo import get_coordinates_google

def process_data(articles):

    data = []

    for art in articles:

        title = art.get("title", "")
        country = art.get("sourceCountry", "Unknown")
        url = art.get("url", "")

        lat, lon = get_coordinates_google(country)

        if lat is None:
            lat = random.uniform(-50, 50)
            lon = random.uniform(-100, 100)

        alert = any(word in title.lower() for word in ["explosion", "attack", "robbery", "war"])

        data.append({
            "title": title,
            "country": country,
            "url": url,
            "lat": lat,
            "lon": lon,
            "alert": alert
        })

    return pd.DataFrame(data)