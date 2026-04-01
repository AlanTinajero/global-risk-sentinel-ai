import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

from data_fetch import get_gdelt_data
from processing import process_data
from ml_model import run_full_analysis
from alerts import send_unique_alert
from storage import save_events, load_events

st.set_page_config(layout="wide")

st.title("🌍 Global Risk Sentinel")

# DATA
articles = get_gdelt_data()
df = process_data(articles)
df = run_full_analysis(df)

# 🔥 LIMPIEZA (CLAVE)
df = df.dropna(subset=["lat", "lon"])

# SAVE
save_events(df)
history = load_events()

# DASHBOARD
st.subheader("📊 Intelligence Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Events", len(df))
col2.metric("High Risk", len(df[df["risk_score"] >= 4]))
col3.metric("Stored", len(history))

# FILTER
min_risk = st.sidebar.slider("Minimum Risk", 0, 5, 2)
df = df[df["risk_score"] >= min_risk]

# MAP
def generate_map(df):

    if df.empty:
        return folium.Map(location=[0, 0], zoom_start=2)

    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=3,
        tiles="cartodb dark_matter"
    )

    cluster = MarkerCluster().add_to(m)

    for _, r in df.iterrows():

        if r["risk_score"] >= 4:
            color = "red"
        elif r["risk_score"] >= 2:
            color = "orange"
        else:
            color = "blue"

        if r.get("coordination_flag"):
            color = "purple"

        folium.CircleMarker(
            location=[r["lat"], r["lon"]],
            radius=6 + r["risk_score"],
            color=color,
            fill=True,
            fill_opacity=0.9,
            popup=r["title"]
        ).add_to(cluster)

    return m

st.subheader("🌍 Global Intelligence Map")
st_folium(generate_map(df), height=500)

# ALERTS
for _, r in df[df["risk_score"] >= 4].iterrows():
    send_unique_alert(r["title"])

# FEED
st.subheader("📰 Intelligence Feed")

for _, r in df.iterrows():

    st.markdown(f"### {r['title']}")
    st.caption(r["country"])

    if r["risk_score"] >= 4:
        st.error("🔥 HIGH RISK")
    elif r["risk_score"] >= 2:
        st.warning("⚠️ MEDIUM RISK")
    else:
        st.info("🟢 LOW RISK")

    st.markdown(r["url"])
    st.markdown("---")