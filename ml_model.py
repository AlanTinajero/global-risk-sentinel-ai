from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

RISK_KEYWORDS = [
    "attack", "explosion", "riot", "war",
    "conflict", "violence", "terror"
]

def detect_geo_clusters(df):
    coords = df[["lat", "lon"]].values
    clustering = DBSCAN(eps=1.5, min_samples=3).fit(coords)
    df["geo_cluster"] = clustering.labels_
    df["danger_zone"] = df["geo_cluster"] != -1
    return df

def detect_text_similarity(df):
    vec = TfidfVectorizer(stop_words="english")
    tfidf = vec.fit_transform(df["title"])
    sim = cosine_similarity(tfidf)
    df["text_similarity"] = sim.mean(axis=1)
    return df

def detect_keywords(df):
    df["keyword_risk"] = df["keyword_count"]
    return df

def detect_coordination(df):
    counts = df["title"].value_counts()
    df["coordination_flag"] = df["title"].map(counts) > 2
    return df

def add_risk_score(df):
    df["risk_score"] = (
        df["danger_zone"].astype(int) * 2 +
        df["keyword_risk"] +
        df["text_similarity"] * 2 +
        df["coordination_flag"].astype(int) * 2 +
        np.random.randint(1, 3, size=len(df))
    )
    df["risk_score"] = df["risk_score"].clip(0, 5)
    return df

def run_full_analysis(df):
    df = detect_geo_clusters(df)
    df = detect_text_similarity(df)
    df = detect_keywords(df)
    df = detect_coordination(df)
    df = add_risk_score(df)
    return df