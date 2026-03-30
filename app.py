import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from data_fetch import get_gdelt_data
from processing import process_data
from ml_model import detect_danger_zones, add_risk_score
from alerts import send_alert

try:
    import folium
except:
    import subprocess
    subprocess.check_call(["pip", "install", "folium"])
    import folium

st.set_page_config(layout="wide")

# 🎨 FIX PANTALLA BLANCA + ESTILO
st.markdown("""
<style>
iframe { pointer-events: auto !important; }
.stApp { background-color: #0e1117; color: white; }
</style>
""", unsafe_allow_html=True)

# 🌐 IDIOMA
language = st.sidebar.selectbox("🌐 Language", ["English", "Español"])

# 🧠 TEXTOS
if language == "English":
    title = "🌍 Global Risk Sentinel"
    alert_text = "⚠️ Active Risk"
    danger_text = "🔥 Danger Zone"
    btn_text = "Send Alert"
    source_text = "View Source"
else:
    title = "🌍 Global Risk Sentinel"
    alert_text = "⚠️ Riesgo Activo"
    danger_text = "🔥 Zona Peligrosa"
    btn_text = "Enviar Alerta"
    source_text = "Ver Fuente"

st.title(title)

# 🔄 REFRESH
if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.session_state.clear()

# 📡 DATA
articles = get_gdelt_data()
df = process_data(articles)

if df.empty:
    st.warning("No data available")
    st.stop()

# 🧠 IA
df = detect_danger_zones(df)
df = add_risk_score(df)

# 🔥 TICKER (NOTICIAS EN VIVO)
st.markdown("### 🚨 Live Global Alerts")

ticker_text = "  |  ".join(df["title"].tolist())

st.markdown(f"""
<marquee behavior="scroll" direction="left" scrollamount="6">
{ticker_text}
</marquee>
""", unsafe_allow_html=True)

# 🌍 MAPA (ESTABLE)
@st.cache_data
def generate_map(df):

    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=3)

    heat_data = []

    for _, row in df.iterrows():

        intensity = 3 if row["alert"] else 1
        heat_data.append([row["lat"], row["lon"], intensity])

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=10 if row["alert"] else 6,
            color="red" if row["alert"] else "blue",
            fill=True,
            fill_opacity=0.8,
            popup=f"{row['title']}"
        ).add_to(m)

    HeatMap(heat_data).add_to(m)

    return m


# 🛑 EVITA PARPADEO
if "map" not in st.session_state:
    st.session_state["map"] = generate_map(df)

st.subheader("🌍 Global Heatmap")
st_folium(st.session_state["map"], height=500)

# 📰 FEED
st.subheader("📰 Live Feed")

for i, row in df.iterrows():

    with st.container():

        st.markdown(f"### {row['title']}")
        st.caption(f"📍 {row['country']}")

        if row["danger_zone"]:
            st.error(danger_text)
        elif row["alert"]:
            st.warning(alert_text)

        # 📊 RIESGO
        st.progress(min(row["risk_score"] / 5, 1.0))

        # 🔗 LINKS
        st.markdown(f"[🌐 {source_text}]({row['url']})")
        st.markdown(f"[📍 Open in Maps](https://www.google.com/maps?q={row['lat']},{row['lon']})")

        # 🚨 ALERTA
        if st.button(f"{btn_text} {i}"):
            send_alert(f"🚨 {row['title']} - {row['country']}")
            st.success("Alert sent")

        st.markdown("---")