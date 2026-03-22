import argparse
import time
from dataclasses import dataclass, asdict

import pandas as pd
from prefect import task, flow
from sklearn.ensemble import IsolationForest
from sklearn.mixture import GaussianMixture
from sqlalchemy import create_engine


engine = create_engine("postgresql://user:password@db:5432/mldb")

@dataclass
class Params:
    n_components: int
    contamination: float

@task
def process_data() -> pd.DataFrame:
    # Son 2 dakikayı çek
    df = pd.read_sql("SELECT * FROM raw_data ORDER BY timestamp DESC LIMIT 120", engine)
    print(f"Okunan veri boyutu: {df.size}")
    if len(df) < 120:
        return pd.DataFrame()
    return df


@task
def train_data(df: pd.DataFrame, n_components: int, contamination: float) -> tuple:
    train_df = df.iloc[60:].fillna(df.mean())
    inf_df = df.iloc[:60].copy()
    
    # GMM ile Outlier Temizliği (Sadece Train seti için)
    gmm = GaussianMixture(n_components=n_components)
    gmm.fit(train_df[["feature_3"]])
    scores = gmm.score_samples(train_df[["feature_3"]])
    clean_train = train_df[scores > pd.Series(scores).quantile(0.05)]
    print(f"Temizlenen aykırı veri sayısı: {clean_train.shape[0]}")

    # Isolation Forest Eğitimi
    model = IsolationForest(contamination=contamination)
    model.fit(clean_train[["feature_3"]])
    print("Isolation Forest modeli eğitildi.")

    return model, train_df, inf_df


@task
def inference_data(model: IsolationForest, train_df: pd.DataFrame, inf_df: pd.DataFrame) -> pd.DataFrame:
    # Inference
    inf_df["is_anomaly"] = model.predict(inf_df[["feature_3"]])
    inf_df["is_anomaly"] = inf_df["is_anomaly"].map({1: 0, -1: 1}) # 1=Anomali
    print(f"Yakalanan anomali sayısı: {inf_df['is_anomaly'].sum()}")

    # Basit Data Drift Hesabı
    ref_mean = 50.0 # Başlangıç referans değeri
    current_mean = inf_df["feature_3"].mean()
    drift_score = abs(current_mean - ref_mean)

    inf_df["drift_score"] = drift_score
    return inf_df


@task
def save_to_db(inf_df: pd.DataFrame) -> None:
    inf_df.to_sql("processed_data", engine, if_exists="append", index=False)


@flow(log_prints=True)
def ml_workflow(params):
    df = process_data()
    model, train_df, inf_df = train_data(df=df, **asdict(params))
    inf_df = inference_data(model, train_df, inf_df)
    save_to_db(inf_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basit prod pipeline demosu.")

    parser.add_argument("--n_components", "-n", type=int, default=1)
    parser.add_argument("--contamination", "-c", type=float, default=0.05)

    args = parser.parse_args()

    while True:
        params = Params(**vars(args))
        ml_workflow(params)
        time.sleep(60)
