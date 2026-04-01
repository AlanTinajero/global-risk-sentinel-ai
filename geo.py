import random

# 🌍 Coordenadas simples por país (OSINT style)
COUNTRY_COORDS = {
    "Mexico": (23.6345, -102.5528),
    "USA": (37.0902, -95.7129),
    "France": (46.6034, 1.8883),
    "Germany": (51.1657, 10.4515),
    "Japan": (36.2048, 138.2529),
    "Brazil": (-14.2350, -51.9253),
    "Ukraine": (48.3794, 31.1656)
}

def get_coordinates_google(country):

    if country in COUNTRY_COORDS:
        return COUNTRY_COORDS[country]

    # fallback random (para no romper app)
    return (
        random.uniform(-50, 50),
        random.uniform(-100, 100)
    )