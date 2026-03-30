import googlemaps

API_KEY = "AIzaSyB7tnuyw9y6kgB38PZ136kdG7jk4gckh4g"

gmaps = googlemaps.Client(key=API_KEY)

def get_coordinates_google(location):

    try:
        result = gmaps.geocode(location)

        if result:
            lat = result[0]["geometry"]["location"]["lat"]
            lon = result[0]["geometry"]["location"]["lng"]
            return lat, lon

    except:
        return None, None

    return None, None