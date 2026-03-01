
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Dashboard Kepuasan Interaktif", layout="wide")

st.title("📊 Dashboard Kepuasan Interaktif Modern")
st.markdown("Dashboard ini menampilkan analisis deskriptif dan segmentasi secara visual & interaktif")

# ==========================
# Upload Data
# ==========================
file = st.file_uploader("Upload Data Excel", type=["xlsx"])

if file is not None:

    df = pd.read_excel(file)
    indikator = df.iloc[:, 1:6].apply(pd.to_numeric, errors="coerce")

    st.sidebar.header("Filter Data")

    indikator_pilih = st.sidebar.multiselect(
        "Pilih Indikator",
        indikator.columns.tolist(),
        default=indikator.columns.tolist()
    )

    data_filtered = indikator[indikator_pilih]

    # ==========================
    # Statistik Deskriptif
    # ==========================
    st.subheader("1️⃣ Statistik Deskriptif")

    deskripsi = data_filtered.describe().T
    st.dataframe(deskripsi)

    # ==========================
    # Grafik Rata-rata
    # ==========================
    st.subheader("2️⃣ Grafik Rata-rata Indikator")

    mean_values = data_filtered.mean().reset_index()
    mean_values.columns = ["Indikator", "Rata-rata"]

    fig_bar = px.bar(mean_values, x="Indikator", y="Rata-rata",
                     text="Rata-rata",
                     title="Rata-rata Penilaian per Indikator")
    fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================
    # Distribusi Nilai
    # ==========================
    st.subheader("3️⃣ Distribusi Nilai")

    indikator_hist = st.selectbox("Pilih indikator untuk distribusi",
                                   data_filtered.columns)

    fig_hist = px.histogram(data_filtered, x=indikator_hist,
                            nbins=5,
                            title=f"Distribusi Nilai {indikator_hist}")
    st.plotly_chart(fig_hist, use_container_width=True)

    # ==========================
    # Clustering Visual
    # ==========================
    st.subheader("4️⃣ Segmentasi Responden (Clustering)")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data_filtered.fillna(data_filtered.mean()))

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster = kmeans.fit_predict(X_scaled)

    df_cluster = data_filtered.copy()
    df_cluster["Cluster"] = cluster

    st.write("Jumlah Responden per Cluster")
    st.dataframe(df_cluster["Cluster"].value_counts())

    fig_cluster = px.scatter_matrix(
        df_cluster,
        dimensions=data_filtered.columns,
        color="Cluster",
        title="Visualisasi Cluster Responden"
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    st.success("Dashboard Interaktif Selesai 🚀")

else:
    st.warning("Silakan upload file Excel terlebih dahulu.")
