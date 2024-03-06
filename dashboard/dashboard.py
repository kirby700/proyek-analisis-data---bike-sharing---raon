import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
sns.set(style='dark')

# Fungsi untuk menghitung parameter RFM
def calculate_rfm(df):
    rfm_df = df.groupby(['season', 'weekday']).agg({
        'cnt': 'sum',  # Jumlah peminjaman sepeda
    }).reset_index()
    return rfm_df

# Fungsi untuk membuat DataFrame penjualan produk
def create_product_sales_df(df):
    product_sales_df = df.groupby('season')['cnt'].sum().reset_index()
    return product_sales_df

# Fungsi untuk membuat DataFrame demografi pelanggan
def create_customer_demographics_df(df):
    customer_demographics_df = df.groupby('weekday')['cnt'].sum().reset_index(name='count')
    return customer_demographics_df

file_path = "C:/KULIAH/SEM 6/BANGKIT 2024/LEARNING/Proyek Analisis Data/submission/dashboard/all_data.csv"

# Membaca file CSV
all_df = pd.read_csv(file_path)

# Menambahkan logo perusahaan
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

# Mengonversi kolom dteday menjadi tipe data datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Mengambil tanggal minimum dan maksimum dari kolom dteday
min_date = all_df["dteday"].min().date()
max_date = all_df["dteday"].max().date()

# Membuat widget date input untuk memilih rentang waktu
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter DataFrame berdasarkan rentang waktu yang dipilih
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                 (all_df["dteday"] <= str(end_date))]

# Membuat DataFrame penjualan produk
product_sales_df = create_product_sales_df(main_df)

# Membuat DataFrame demografi pelanggan
customer_demographics_df = create_customer_demographics_df(main_df)

# Menambahkan header pada dashboard
st.header('Bike Sharing Raon :sparkles:')

# Menampilkan informasi terkait peminjaman sepeda harian
st.subheader('Peminjaman Sepeda Harian')

# Membagi layout menjadi dua kolom
col1, col2 = st.columns(2)

# Menampilkan total peminjaman
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Peminjaman", value=total_rentals)

# Menampilkan rata-rata peminjaman
with col2:
    avg_rentals = main_df['cnt'].mean()
    st.metric("Rata-rata Peminjaman", value=avg_rentals)

# Membuat plot jumlah peminjaman harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=10)
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman')
plt.title('Jumlah Peminjaman Sepeda Harian')
plt.grid(True)

# Menampilkan plot menggunakan pyplot
st.pyplot(fig)

# Menampilkan informasi terkait performa penjualan produk terbaik dan terburuk
st.subheader("Performa Penjualan Produk")

# Plot jumlah peminjaman sepeda berdasarkan musim
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

# Produk Paling Laris
sns.barplot(x="cnt", y="season", hue="season", data=product_sales_df, palette="Blues", ax=ax[0], legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Peminjaman", fontsize=12)
ax[0].set_title("Musim dengan Peminjaman Tertinggi", fontsize=14)
ax[0].tick_params(axis='y', labelsize=10)
ax[0].tick_params(axis='x', labelsize=10)

# Demografi Pelanggan
st.subheader("Demografi Pelanggan")

# Visualisasi data demografi pelanggan
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x="weekday", y="count", hue="weekday", data=customer_demographics_df, palette="muted", legend=False)
plt.xlabel("Hari dalam Seminggu")
plt.ylabel("Jumlah Peminjaman")
plt.title("Peminjaman Berdasarkan Hari dalam Seminggu")
plt.grid(True)

st.pyplot(fig)

# Kelompokkan data berdasarkan musim dan hitung rata-rata peminjaman sepeda pada setiap musim
seasonal_rentals = main_df.groupby('season')['cnt'].mean()

# Membuat plot
plt.figure(figsize=(10, 6))
seasonal_rentals.plot(marker='o', color='b', linestyle='-')
plt.title('Tren Peminjaman Sepeda per Musim (rata-rata)')
plt.xticks(range(1, 5), ['Spring', 'Summer', 'Fall', 'Winter'])

# Menghilangkan tulisan 'season' di bawah sumbu x
plt.xlabel('')

# Menampilkan plot menggunakan st.pyplot()
st.pyplot(plt)

# Kelompokkan data berdasarkan kondisi cuaca dan hitung rata-rata jumlah pengguna sepeda pada setiap kondisi cuaca
weather_rentals = main_df.groupby('weathersit')['cnt'].mean()

# Membuat bar plot
plt.figure(figsize=(8, 5))
bars = plt.bar(weather_rentals.index, weather_rentals, color='b', alpha=0.7)

# Mengatur transparansi untuk kolom selain "Clear"
for i, bar in enumerate(bars):
    if i != 0:
        bar.set_alpha(0.3)

plt.title('Rata-rata Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
plt.xticks(weather_rentals.index, ['Clear', 'Mist', 'Light Snow', 'Heavy Rain'], rotation=45)

# Hilangkan frame dari plot
plt.box(False)

# Hilangkan tick marks dari sumbu x dan y
plt.tick_params(axis='both', which='both', bottom=False, left=False)

# Hilangkan grid lines
plt.grid(False)

# Menampilkan plot menggunakan st.pyplot()
st.pyplot(plt)

# Menghitung nilai RFM
rfm_df = calculate_rfm(main_df)

# Menampilkan informasi terkait parameter RFM
st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.cnt.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.cnt.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.cnt.mean(), "USD", locale='en_US') 
    st.metric("Average Monetary", value=avg_frequency)
 
st.caption('Copyright (c) Dicoding 2023')


# Fungsi untuk melakukan clustering
def perform_clustering(df):
    # Memilih fitur untuk clustering
    features = ['season', 'weekday', 'cnt']
    X = df[features]

    # Normalisasi data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Melakukan clustering dengan KMeans
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    return df

# Memanggil fungsi perform_clustering untuk melakukan clustering
main_df = perform_clustering(main_df)

# Menampilkan informasi terkait clustering
st.subheader("Clustering Hasil Analisis")
st.write("Hasil clustering untuk data peminjaman sepeda berdasarkan musim, hari dalam seminggu, dan jumlah peminjaman.")

# Visualisasi clustering
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_df, x='season', y='weekday', hue='cluster', palette='Set1', ax=ax)
plt.title('Clustering Peminjaman Sepeda')
plt.xlabel('Musim')
plt.ylabel('Hari dalam Seminggu')
st.pyplot(fig)
