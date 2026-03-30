from sklearn.cluster import DBSCAN

def detect_danger_zones(df):

    coords = df[["lat", "lon"]].values

    clustering = DBSCAN(eps=10, min_samples=2).fit(coords)

    df["cluster"] = clustering.labels_
    df["danger_zone"] = df["cluster"] != -1

    return df


def add_risk_score(df):

    df["risk_score"] = (
        df["alert"].astype(int) * 2 +
        df["danger_zone"].astype(int) * 3
    )

    return df