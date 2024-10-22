import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

@st.cache
def load_data():
    data_dir = 'PRSA_Data_20130301-20170228/'
    files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]
    dataframes = []
    for file in files:
        df = pd.read_csv(os.path.join(data_dir, file))
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.replace('NA', np.nan, inplace=True)
    numeric_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    combined_df[numeric_columns] = combined_df[numeric_columns].apply(pd.to_numeric)
    combined_df.dropna(subset=['year', 'month', 'day', 'hour'] + numeric_columns, inplace=True)
    combined_df['date'] = pd.to_datetime(combined_df[['year', 'month', 'day', 'hour']])
    return combined_df

df = load_data()

st.title('Analisis Data Kualitas Udara')

st.subheader('Data Kualitas Udara')
st.write(df.head())

st.sidebar.header('Filter Data')
selected_year = st.sidebar.selectbox('Pilih Tahun', df['year'].unique())
selected_months = st.sidebar.multiselect('Pilih Bulan', df['month'].unique(), default=df['month'].unique())

filtered_df = df[(df['year'] == selected_year) & (df['month'].isin(selected_months))]

st.subheader(f'Data Kualitas Udara untuk Tahun {selected_year} dan Bulan {selected_months}')
st.write(filtered_df)

st.subheader('Tren Kualitas Udara (PM2.5)')
filtered_df['month_year'] = filtered_df['date'].dt.to_period('M')
monthly_avg_pm25 = filtered_df.groupby('month_year')['PM2.5'].mean()

plt.figure(figsize=(12, 6))
monthly_avg_pm25.plot(kind='line')
plt.title('Rata-rata PM2.5 per Bulan')
plt.xlabel('Bulan')
plt.ylabel('PM2.5')
st.pyplot(plt)

st.subheader('Korelasi antara Kondisi Cuaca dan PM2.5')
correlation_matrix = filtered_df[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Korelasi antara Variabel Cuaca dan PM2.5')
st.pyplot(plt)
