import time

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("postgresql://user:password@db:5432/mldb")

def generate_data():
    iteration = 0
    while True:
        n = 60
        # Data Drift
        drift_step = iteration * 2
        base = np.random.normal(50 + drift_step, 5, n)
        
        df = pd.DataFrame({
            "timestamp": pd.date_range(start=pd.Timestamp.now(), periods=n, freq="s"),
            "feature_1": base,
            "feature_2": base * 0.7 + np.random.normal(0, 2, n), # Korelasyonlu
            "feature_3": (
                np.clip(np.random.standard_cauchy(n), 0, 200)
                + (50 + drift_step)
            ) # Anomali kaynağı
        })
        
        # %5 NULL
        df.loc[df.sample(frac=0.05).index, "feature_3"] = np.nan
        
        df.to_sql("raw_data", engine, if_exists="append", index=False)
        iteration += 1
        time.sleep(60)


if __name__ == "__main__":
    generate_data()
