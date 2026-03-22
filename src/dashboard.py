import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(layout="wide")
engine = create_engine("postgresql://user:password@db:5432/mldb")

st.title("ML Monitoring Dashboard")

placeholder = st.empty()

while True:
    try:
        df = pd.read_sql("SELECT * FROM processed_data ORDER BY timestamp DESC LIMIT 300", engine)
        
        with placeholder.container():
            # ÜST KISIM: Canlı Anomali
            st.subheader("Canlı Zaman Serisi & Anomaliler")
            fig_ts = px.scatter(df, x="timestamp", y="feature_3", color="is_anomaly",
                               color_discrete_map={0: "blue", 1: "red"},
                               title="Feature 3 (Cauchy Dağılımı ve Tespit Edilen Anomaliler)")
            st.plotly_chart(fig_ts, width="stretch")

            # ALT KISIM: Drift Takibi
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Data Drift Takibi (Feature 3 Mean)")
                fig_drift = px.line(df, x="timestamp", y="drift_score", title="Baseline'dan Sapma Miktarı")
                st.plotly_chart(fig_drift, width="stretch")
            
            with col2:
                st.metric("Güncel Drift Skoru", round(df["drift_score"].iloc[0], 2), 
                          delta=f"{round(df['drift_score'].iloc[0], 2)} unit shift")
                st.write("Not: Drift skoru arttıkça modelin yeniden eğitilmesi gerekir.")

    except:
        st.write("Veri bekleniyor...")
    
    import time
    time.sleep(5)
