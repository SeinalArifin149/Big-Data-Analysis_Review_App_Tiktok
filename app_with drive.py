# import streamlit as st
# # import gdown
# import pandas as pd
# import pandas as pd
# import plotly.express as px
# import numpy as np

# # --- Konfigurasi Awal dan Data ---

# # GDRIVE_URL = "https://drive.google.com/file/d/1vpLw46rVIJo9kdagyVNS0Z--8P94xKWd/view?usp=drive_link"
# # LOCAL_CSV_NAME = 'Dataset_Review-Tiktok.csv'
# # SENTIMENT_COLS = ['Sentiment_NB Negatif', 'Sentiment_NB Positif']

# st.set_page_config(
#     page_title="Aplikasi Analisis Sentimen TikTok",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- 1. Fungsi Pemuatan Data dan Cache ---

# @st.cache_data
# def download_data(url, output_name):
#     """Mengunduh file dari Google Drive menggunakan gdown."""
#     try:
#         # Mengambil ID file dari URL
#         file_id = url.split('/')[-2]
#         st.info(f"Mengunduh data dari Google Drive (ID: {file_id}). Ini mungkin membutuhkan waktu sebentar.")
        
#         # URL untuk gdown
#         # download_url = f'https://drive.google.com/uc?id={file_id}'
#         gdown.download(download_url, output_name, quiet=False)
#         return True
#     except Exception as e:
#         st.error(f"Gagal mengunduh file: {e}")
#         return False

# @st.cache_data
# def load_and_preprocess_data(filename):
#     """Memuat data, membersihkan, dan melakukan pre-processing."""
#     try:
#         # Memuat data
#         df = pd.read_csv(filename)
        
#         # Mengubah kolom 'at' (tanggal) ke tipe datetime
#         df['at'] = pd.to_datetime(df['at'])
        
#         # Menambahkan kolom Sentimen Tunggal (untuk memudahkan)
#         # Asumsi: Jika Positif > Negatif -> Positif, sebaliknya Negatif, atau bisa dibuat 'Netral'
#         df['Sentiment'] = np.where(
#             df['Sentiment_NB Positif'] > df['Sentiment_NB Negatif'],
#             'Positif',
#             'Negatif'
#         )
        
#         st.success("Data berhasil dimuat dan diproses!")
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat atau memproses data: {e}")
#         return pd.DataFrame()


# # --- 2. Implementasi Halaman ---

# def home_page(df):
#     """Menampilkan analisis per Topik."""
#     st.title("🏡 Analisis Sentimen Berdasarkan Topik")
#     st.markdown("Pilih satu atau lebih topik untuk melihat distribusi sentimen dan trennya.")
    
#     # Sidebar Filter Topik
#     unique_topics = df['Label_Topik'].unique().tolist()
#     selected_topics = st.sidebar.multiselect(
#         "Pilih Topik untuk Analisis:",
#         options=unique_topics,
#         default=unique_topics[0] if unique_topics else []
#     )
    
#     if not selected_topics:
#         st.warning("Silakan pilih setidaknya satu Topik dari sidebar.")
#         return

#     df_filtered = df[df['Label_Topik'].isin(selected_topics)]
    
#     if df_filtered.empty:
#         st.info("Tidak ada data untuk topik yang dipilih.")
#         return

#     st.header(f"Ringkasan untuk Topik: {', '.join(selected_topics)}")
    
#     # 1. Bar Chart Sentimen per Topik
#     topic_sentiment_count = df_filtered.groupby(['Label_Topik', 'Sentiment']).size().reset_index(name='Jumlah')
    
#     fig1 = px.bar(
#         topic_sentiment_count,
#         x='Sentiment',
#         y='Jumlah',
#         color='Sentiment',
#         facet_col='Label_Topik',
#         title='Distribusi Sentimen (Positif vs Negatif) per Topik',
#         color_discrete_map={'Positif': 'green', 'Negatif': 'red'}
#     )
#     st.plotly_chart(fig1, use_container_width=True)
    
#     # 2. Distribusi Ulasan dari Waktu ke Waktu untuk Topik ini
#     df_filtered_daily = df_filtered.set_index('at').resample('D').size().reset_index(name='Jumlah Ulasan')
#     fig2 = px.line(
#         df_filtered_daily,
#         x='at',
#         y='Jumlah Ulasan',
#         title=f'Volume Ulasan dari Waktu ke Waktu (Topik: {", ".join(selected_topics)})'
#     )
#     st.plotly_chart(fig2, use_container_width=True)


# def data_page(df):
#     """Menampilkan distribusi Sentimen Global."""
#     st.title("📈 Distribusi Sentimen Global")
#     st.markdown("Analisis keseluruhan sentimen di seluruh dataset, dipecah berdasarkan topik.")
    
#     total_reviews = len(df)
#     sentiment_counts = df['Sentiment'].value_counts()
    
#     # Metrik Global
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Ulasan", f"{total_reviews:,}")
    
#     if 'Positif' in sentiment_counts:
#         pos_count = sentiment_counts.get('Positif', 0)
#         pos_percentage = (pos_count / total_reviews) * 100
#         col2.metric("Total Positif", f"{pos_count:,}", f"{pos_percentage:.1f}%")
        
#     if 'Negatif' in sentiment_counts:
#         neg_count = sentiment_counts.get('Negatif', 0)
#         neg_percentage = (neg_count / total_reviews) * 100
#         col3.metric("Total Negatif", f"{neg_count:,}", f"{neg_percentage:.1f}%")

#     st.subheader("Proporsi Sentimen Keseluruhan")
#     fig3 = px.pie(
#         names=sentiment_counts.index,
#         values=sentiment_counts.values,
#         title='Proporsi Sentimen Positif vs Negatif',
#         color_discrete_map={'Positif': 'green', 'Negatif': 'red'}
#     )
#     st.plotly_chart(fig3, use_container_width=True)
    
#     st.subheader("Perbandingan Sentimen Lintas Topik")
#     # Bar Chart Agregat Sentimen per Topik
#     df_topic_summary = df.groupby('Label_Topik')['Sentiment'].value_counts().unstack(fill_value=0)
#     df_topic_summary['Total'] = df_topic_summary.sum(axis=1)
#     df_topic_summary = df_topic_summary.sort_values(by='Total', ascending=False).reset_index()
    
#     fig4 = px.bar(
#         df_topic_summary.melt(id_vars=['Label_Topik'], value_vars=['Positif', 'Negatif'], var_name='Sentiment', value_name='Jumlah'),
#         x='Label_Topik',
#         y='Jumlah',
#         color='Sentiment',
#         title='Jumlah Ulasan Positif dan Negatif per Label Topik',
#         color_discrete_map={'Positif': 'green', 'Negatif': 'red'}
#     )
#     st.plotly_chart(fig4, use_container_width=True)


# def about_page(df):
#     """Menampilkan Analisis Sentimen Temporal."""
#     st.title("⏰ Analisis Sentimen Temporal (Waktu ke Waktu)")
#     st.markdown("Lihat bagaimana sentimen ulasan berubah seiring berjalannya waktu.")

#     # Sidebar Filter Tanggal
#     min_date = df['at'].min().date()
#     max_date = df['at'].max().date()
    
#     date_range = st.sidebar.date_input(
#         "Pilih Rentang Tanggal:",
#         value=(min_date, max_date),
#         min_value=min_date,
#         max_value=max_date
#     )
    
#     # Pastikan rentang tanggal dipilih dengan benar
#     if len(date_range) == 2:
#         start_date, end_date = date_range
#         df_time_filtered = df[(df['at'].dt.date >= start_date) & (df['at'].dt.date <= end_date)]
#     else:
#         st.warning("Pilih rentang tanggal yang valid.")
#         return

#     if df_time_filtered.empty:
#         st.info("Tidak ada data dalam rentang tanggal yang dipilih.")
#         return

#     # Hitung tren sentimen harian
#     df_daily_sentiment = df_time_filtered.groupby([df_time_filtered['at'].dt.date, 'Sentiment']).size().unstack(fill_value=0).reset_index()
#     df_daily_sentiment.columns = ['Date', 'Negatif', 'Positif']
#     df_daily_sentiment['Date'] = pd.to_datetime(df_daily_sentiment['Date'])
    
#     # Plot Tren Sentimen
#     df_plot = df_daily_sentiment.melt('Date', var_name='Sentiment', value_name='Count')

#     fig5 = px.line(
#         df_plot,
#         x='Date',
#         y='Count',
#         color='Sentiment',
#         title=f'Tren Jumlah Ulasan Positif dan Negatif ({start_date} hingga {end_date})',
#         color_discrete_map={'Positif': 'green', 'Negatif': 'red'}
#     )
#     fig5.update_xaxes(title_text="Tanggal")
#     fig5.update_yaxes(title_text="Jumlah Ulasan")
#     st.plotly_chart(fig5, use_container_width=True)


# def welcome_page():
#     """Halaman Selamat Datang."""
#     st.title("👋 Selamat Datang di Aplikasi Analisis Sentimen TikTok")
#     st.header("Analisis Data Ulasan TikTok")
#     st.info("Gunakan navigasi di atas untuk menjelajahi wawasan sentimen berdasarkan **Topik**, **Distribusi Sentimen Global**, dan **Tren Temporal**.")
#     st.image("https://images.unsplash.com/photo-1629731637777-62f91361c4f1?fit=crop&w=1200&h=600", caption="Ilustrasi Analisis Data")


# # --- 3. Main Aplikasi ---

# # State Management (Menggunakan query params untuk menjaga state antar tombol)
# query_params = st.query_params

# # Inisialisasi state halaman
# if "page" not in query_params:
#     st.query_params["page"] = "welcome"

# # Header dan Navigasi
# st.sidebar.title("Kontrol Data")
# st.title("Dashboard Analisis Sentimen")

# # --- Tombol Navigasi ---
# col1, col2, col3 = st.columns(3)

# if col1.button("🏡 Topik"):
#     st.query_params["page"] = "home"
# if col2.button("📈 Sentiment"):
#     st.query_params["page"] = "data"
# if col3.button("⏰ Temporal Sentiment"):
#     st.query_params["page"] = "about"

# # --- 4. Proses Loading Data ---
# if download_data(GDRIVE_URL, LOCAL_CSV_NAME):
#     df = load_and_preprocess_data(LOCAL_CSV_NAME)
# else:
#     # Tampilkan halaman selamat datang atau pesan error jika gagal memuat
#     df = pd.DataFrame()
#     if st.query_params["page"] != "welcome":
#         st.error("Tidak dapat memuat data. Silakan cek koneksi atau URL Google Drive.")
#         st.query_params["page"] = "welcome"


# # --- 5. Routing Halaman ---
# if not df.empty:
#     page = st.query_params["page"]
    
#     st.divider() # Pemisah visual
    
#     if page == "home":
#         home_page(df)
#     elif page == "data":
#         data_page(df)
#     elif page == "about":
#         about_page(df)
#     elif page == "welcome":
#         welcome_page()
# else:
#     # Tampilkan selamat datang hanya jika belum ada data dan belum ada error
#     if st.query_params["page"] == "welcome":
#         welcome_page()

# st.sidebar.divider()
# st.sidebar.caption("Dibuat dengan Streamlit & Plotly")