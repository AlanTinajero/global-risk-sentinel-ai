import pandas as pd
import os

DB_FILE = "events_db.csv"

def save_events(df):

    if df.empty:
        return

    if os.path.exists(DB_FILE):

        try:
            old = pd.read_csv(DB_FILE)

            # combinar y evitar duplicados
            df = pd.concat([old, df]).drop_duplicates(subset=["title"])

        except Exception:
            # 🔥 si el archivo está corrupto, lo reinicia
            df = df

    df.to_csv(DB_FILE, index=False)


def load_events():

    if os.path.exists(DB_FILE):

        try:
            return pd.read_csv(DB_FILE)
        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()