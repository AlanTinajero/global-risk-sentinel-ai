import requests

def get_gdelt_data():

    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"

        params = {
            "query": "explosion OR protest OR robbery OR attack OR earthquake",
            "mode": "ArtList",
            "maxrecords": 10,
            "format": "json"
        }

        r = requests.get(url, params=params, timeout=5)

        if r.status_code != 200:
            return get_mock()

        data = r.json()

        if "articles" not in data:
            return get_mock()

        articles = []

        for art in data["articles"]:

            title = art.get("title", "")
            country = art.get("sourceCountry", "Unknown")

            url = art.get("url")

            if not url:
                url = f"https://news.google.com/search?q={title.replace(' ', '+')}"

            articles.append({
                "title": title,
                "sourceCountry": country,
                "url": url
            })

        return articles

    except:
        return get_mock()


def get_mock():
    return [
        {"title": "Explosion in Mexico City", "sourceCountry": "Mexico", "url": "https://news.google.com/search?q=explosion+mexico"},
        {"title": "Robbery in New York", "sourceCountry": "USA", "url": "https://news.google.com/search?q=robbery+new+york"},
        {"title": "Earthquake in Japan", "sourceCountry": "Japan", "url": "https://news.google.com/search?q=earthquake+japan"},
    ]