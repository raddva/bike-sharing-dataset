import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

st.title('Analisis Bike Sharing Dataset')

# Load dataset
main_data = pd.read_csv("dashboard/main_data.csv")
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

# Map deskripsi
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_mapping = {
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Light Rain',
    4: 'Heavy Rain/Snow'
}
weekday_mapping = {
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
    4: 'Thursday', 5: 'Friday', 6: 'Saturday'
}

# Add label
main_data['season_label'] = main_data['season'].map(season_mapping)
main_data['weather_label'] = main_data['weathersit'].map(weather_mapping)
main_data['weekday_label'] = main_data['weekday'].map(weekday_mapping)
main_data['month'] = main_data['dteday'].dt.month
main_data['year'] = main_data['dteday'].dt.year

# Sidebar
st.sidebar.header("Filter")

# Filter
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=main_data['season_label'].unique(),
    default=main_data['season_label'].unique()
)

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=main_data['weather_label'].unique(),
    default=main_data['weather_label'].unique()
)

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(main_data['dteday'].min(), main_data['dteday'].max()),
    min_value=main_data['dteday'].min(),
    max_value=main_data['dteday'].max()
)

hour_range = st.sidebar.slider(
    "Pilih Rentang Waktu/Jam",
    min_value=int(main_data['hr'].min()),
    max_value=int(main_data['hr'].max()),
    value=(int(main_data['hr'].min()), int(main_data['hr'].max()))
)

temperature_range = st.sidebar.slider(
    "Pilih Rentang Temperatur (°C)",
    min_value=float(main_data['temp'].min()),
    max_value=float(main_data['temp'].max()),
    value=(float(main_data['temp'].min()), float(main_data['temp'].max()))
)

# Cek filter rentang
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date_range
    end_date = None

if end_date:
    filtered_data = main_data[
        (main_data['season_label'].isin(selected_season)) &
        (main_data['weather_label'].isin(selected_weather)) &
        (main_data['dteday'].between(pd.Timestamp(start_date), pd.Timestamp(end_date))) &
        (main_data['hr'].between(hour_range[0], hour_range[1])) &
        (main_data['temp'].between(temperature_range[0], temperature_range[1]))
    ]
else:
    filtered_data = main_data

# Visualisasi Diagram
st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='season_label', ax=ax,  palette='viridis',  hue='season_label', dodge=False)
ax.set_title("Distribusi Penyewaan Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("Penyewaan Berdasarkan Hari")
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='weekday_label', ax=ax, palette='coolwarm', hue='weekday_label', dodge=False, order=[
    'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
])
ax.set_title("Distribusi Penyewaan Berdasarkan Hari")
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("Penyewaan Berdasarkan Jam")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='hr', y='cnt', hue='season_label', ax=ax)
ax.set_title("Tren Penyewaan Berdasarkan Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Data yang telah di filter
st.write("Data", filtered_data)

st.caption('© Nadya, 2024')