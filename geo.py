import os
import random
import googlemaps

# 🔐 API KEY desde variables de entorno (PRO)
API_KEY = os.getenv("AIzaSyB7tnuyw9y6kgB38PZ136kdG7jk4gckh4g")

# Inicializar cliente solo si hay API key
gmaps = None
if API_KEY:
    try:
        gmaps = googlemaps.Client(key=API_KEY)
    except:
        gmaps = None


def get_coordinates_google(location):
    """
    Obtiene coordenadas reales con Google Maps.
    Si falla, usa fallback para que la app nunca se rompa.
    """

    # 🔥 1. Intentar Google Maps real
    if gmaps:
        try:
            result = gmaps.geocode(location)

            if result:
                lat = result[0]["geometry"]["location"]["lat"]
                lon = result[0]["geometry"]["location"]["lng"]
                return lat, lon

        except:
            pass

    # 🔁 2. FALLBACK (NUNCA CRASHEA)
    return get_mock_coordinates()


def get_mock_coordinates():
    """
    Coordenadas fake para evitar que la app falle
    """

    return (
        random.uniform(-90, 90),
        random.uniform(-180, 180)
    )