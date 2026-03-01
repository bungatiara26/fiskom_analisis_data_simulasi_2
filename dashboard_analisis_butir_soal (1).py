
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dashboard Analisis Butir Soal", layout="wide")
st.title("📊 Dashboard Analisis Deskriptif Butir Soal")

# Load data
file_path = "data_simulasi_50_siswa_20_soal.xlsx"
df = pd.read_excel(file_path)

nama_col = df.columns[0]
soal_cols = df.columns[1:]

# =====================
# Statistik Deskriptif Per Soal
# =====================
st.header("📌 Statistik Deskriptif Per Soal")

desc = pd.DataFrame({
    "Rata-rata": df[soal_cols].mean(),
    "Median": df[soal_cols].median(),
    "Std Deviasi": df[soal_cols].std(),
    "Nilai Min": df[soal_cols].min(),
    "Nilai Max": df[soal_cols].max()
})

st.dataframe(desc.round(2))

# =====================
# Distribusi Skor Jawaban
# =====================
st.header("📊 Distribusi Skor Jawaban")

soal_pilih = st.selectbox("Pilih Soal", soal_cols)

fig, ax = plt.subplots()
ax.hist(df[soal_pilih], bins=10)
ax.set_xlabel("Skor")
ax.set_ylabel("Frekuensi")
ax.set_title(f"Distribusi Skor {soal_pilih}")
st.pyplot(fig)

# =====================
# Analisis Gap Nilai
# =====================
st.header("📉 Analisis Gap Nilai")

nilai_ideal = st.slider("Tentukan Nilai Ideal", min_value=50, max_value=100, value=75)

gap = nilai_ideal - df[soal_cols].mean()

gap_df = pd.DataFrame({
    "Rata-rata": df[soal_cols].mean(),
    "Gap terhadap Nilai Ideal": gap
})

st.dataframe(gap_df.round(2))

fig2, ax2 = plt.subplots()
ax2.bar(soal_cols, gap)
ax2.axhline(0)
ax2.set_ylabel("Gap Nilai")
ax2.set_title("Gap Nilai per Soal")
ax2.tick_params(axis='x', rotation=90)
st.pyplot(fig2)

# =====================
# Kategori Tingkat Kesukaran
# =====================
st.header("📚 Kategori Tingkat Kesukaran Soal")

def kategori_kesukaran(mean):
    if mean >= 80:
        return "Mudah"
    elif mean >= 65:
        return "Sedang"
    else:
        return "Sukar"

kesukaran = df[soal_cols].mean().apply(kategori_kesukaran)

kesukaran_df = pd.DataFrame({
    "Rata-rata": df[soal_cols].mean(),
    "Kategori": kesukaran
})

st.dataframe(kesukaran_df)

# =====================
# Ringkasan Analisis
# =====================
st.header("📝 Ringkasan Otomatis")

st.write(
    "- Jumlah Siswa: **{}**\n"
    "- Jumlah Soal: **{}**\n"
    "- Soal dengan Rata-rata Tertinggi: **{}**\n"
    "- Soal dengan Rata-rata Terendah: **{}**\n"
    "- Soal Perlu Perbaikan (Gap Terbesar): **{}**"
    .format(
        len(df),
        len(soal_cols),
        desc['Rata-rata'].idxmax(),
        desc['Rata-rata'].idxmin(),
        gap.idxmax()
    )
)
