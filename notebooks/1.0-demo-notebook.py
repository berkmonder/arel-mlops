import numpy as np
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


pd.options.plotting.backend = "plotly"
engine = create_engine("postgresql://user:password@localhost:5432/mldb")

df = pd.read_sql("SELECT * FROM processed_data ORDER BY timestamp LIMIT 120", engine)

df.plot(x="timestamp", y="feature_3")

(
    df
    .fillna(np.mean(df["feature_3"]))
    .plot(x="timestamp", y="feature_3")
)

np.mean(df["feature_3"]) == df["feature_3"].mean()

fig = px.parallel_coordinates(df[df["feature_3"] < 70])
fig.show()

df.corr()
