import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- Konfigurasi Awal ---
LOCAL_CSV_PATH = 'hasil_akhir_sentiment_per_topic.csv'

st.set_page_config(
    page_title="Aplikasi Analisis Sentimen TikTok",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. Fungsi Pemuatan Data ---
@st.cache_data
def load_and_preprocess_data(filepath):
    try:
        df = pd.read_csv(filepath)
        if 'at' not in df.columns:
            st.error("Kolom 'at' tidak ditemukan!")
            return pd.DataFrame()
        df['at'] = pd.to_datetime(df['at'], errors='coerce')
        df = df.dropna(subset=['at'])
        if df.empty: return pd.DataFrame()
        
        df['year_month'] = df['at'].dt.to_period('M')
        df['month_name'] = df['at'].dt.strftime('%B %Y')
        
        if 'Sentiment_NB' in df.columns:
            df['Sentiment'] = df['Sentiment_NB']
        else:
            st.error("Kolom 'Sentiment_NB' tidak ada!")
            return pd.DataFrame()
            
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# --- 2. Halaman-Halaman ---

def data_page(df):
    """Halaman Utama: Distribusi Sentimen Global."""
    st.header("📈 Distribusi Sentimen Global")
    st.markdown("Ringkasan statistik sentimen dari seluruh data.")
    
    # Sidebar Filter
    st.sidebar.divider()
    st.sidebar.subheader("Filter Data")
    unique_months = sorted(df['month_name'].unique().tolist())
    selected_months = st.sidebar.multiselect(
        "Pilih Bulan:", options=unique_months, default=unique_months, key="data_filter"
    )
    
    if not selected_months:
        st.warning("Pilih bulan di sidebar.")
        return
        
    df_filtered = df[df['month_name'].isin(selected_months)]
    
    # Metrik
    total = len(df_filtered)
    counts = df_filtered['Sentiment'].value_counts()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Ulasan", f"{total:,}")
    if 'Positif' in counts:
        c2.metric("Positif", f"{counts['Positif']:,}", f"{(counts['Positif']/total)*100:.1f}%")
    if 'Negatif' in counts:
        c3.metric("Negatif", f"{counts['Negatif']:,}", f"{(counts['Negatif']/total)*100:.1f}%")

    # Chart Pie & Bar
    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        st.subheader("Proporsi Sentimen")
        fig = px.pie(names=counts.index, values=counts.values, color_discrete_map={'Positif':'green', 'Negatif':'red'})
        st.plotly_chart(fig, use_container_width=True)
        
    with c_chart2:
        st.subheader("Sentimen per Topik")
        # Logika perbaikan bug melt
        df_top = df_filtered.groupby('topic')['Sentiment'].value_counts().unstack(fill_value=0).reset_index()
        cols_available = [c for c in ['Positif', 'Negatif'] if c in df_top.columns]
        df_top['Total'] = df_top[cols_available].sum(axis=1)
        df_top = df_top.sort_values('Total', ascending=False)
        
        df_melted = df_top.melt(id_vars='topic', value_vars=cols_available, var_name='Sentiment', value_name='Jml')
        
        fig2 = px.bar(df_melted, x='topic', y='Jml', color='Sentiment', 
                      color_discrete_map={'Positif':'green', 'Negatif':'red'})
        st.plotly_chart(fig2, use_container_width=True)

def home_page(df):
    """Halaman Detail per Topik."""
    st.header("🏡 Analisis Detail per Topik")
    
    st.sidebar.divider()
    st.sidebar.subheader("Filter Topik")
    topics = df['topic'].unique().tolist()
    sel_topic = st.sidebar.multiselect("Pilih Topik:", options=topics, default=[topics[0]] if topics else [])
    
    months = sorted(df['month_name'].unique().tolist())
    sel_month = st.sidebar.multiselect("Pilih Bulan:", options=months, default=months, key="topic_filter_month")
    
    if not sel_topic or not sel_month:
        st.warning("Pilih topik dan bulan.")
        return

    df_f = df[(df['topic'].isin(sel_topic)) & (df['month_name'].isin(sel_month))]
    
    if df_f.empty: st.info("Data kosong."); return

    # Chart
    fig = px.bar(df_f.groupby(['topic', 'Sentiment']).size().reset_index(name='Jml'), 
                 x='Sentiment', y='Jml', color='Sentiment', facet_col='topic',
                 color_discrete_map={'Positif':'green', 'Negatif':'red'})
    st.plotly_chart(fig, use_container_width=True)

def about_page(df):
    """Halaman Tren Waktu dengan 3 Tab."""
    st.header("⏰ Analisis Tren Waktu")
    
    st.sidebar.divider()
    st.sidebar.subheader("Filter Waktu Global")
    months = sorted(df['month_name'].unique().tolist())
    sel_month = st.sidebar.multiselect("Pilih Bulan:", options=months, default=months, key="time_filter")
    
    if not sel_month: st.warning("Silakan pilih bulan."); return
    
    df_f = df[df['month_name'].isin(sel_month)]
    
    tab1, tab2, tab3 = st.tabs(["📊 Tren Sentimen Global", "🔥 Tren Popularitas Topik", "🎯 Tren Spesifik per Topik"])

    with tab1:
        st.subheader("Pergerakan Sentimen Harian")
        daily = df_f.groupby([df_f['at'].dt.date, 'Sentiment']).size().reset_index(name='Jml')
        fig1 = px.line(daily, x='at', y='Jml', color='Sentiment', 
                      color_discrete_map={'Positif':'green', 'Negatif':'red'}, markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("Pergerakan Popularitas Topik")
        daily_topic = df_f.groupby([df_f['at'].dt.date, 'topic']).size().reset_index(name='Jml')
        fig2 = px.line(daily_topic, x='at', y='Jml', color='topic', markers=True)
        fig2.update_layout(hovermode="x unified")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Analisis Mendalam: Topik & Sentimen Spesifik")
        c1, c2 = st.columns(2)
        topic_opt = sorted(df_f['topic'].unique())
        choosen_topic = c1.selectbox("Pilih Topik:", topic_opt)
        choosen_sentiment = c2.radio("Pilih Sentimen:", ["Positif", "Negatif"], horizontal=True)
        
        df_detail = df_f[(df_f['topic'] == choosen_topic) & (df_f['Sentiment'] == choosen_sentiment)]
        
        if not df_detail.empty:
            daily_detail = df_detail.groupby(df_detail['at'].dt.date).size().reset_index(name='Jml')
            color_map = 'green' if choosen_sentiment == 'Positif' else 'red'
            fig3 = px.line(daily_detail, x='at', y='Jml', markers=True)
            fig3.update_traces(line_color=color_map)
            st.plotly_chart(fig3, use_container_width=True)
            with st.expander("Lihat Data Mentah"):
                # Cek kolom teks yang tersedia
                text_col = 'final_text' if 'final_text' in df.columns else 'content'
                cols_show = ['at', 'userName', text_col, 'Sentiment'] if 'userName' in df.columns else ['at', text_col, 'Sentiment']
                st.dataframe(df_detail[cols_show].sort_values('at', ascending=False), use_container_width=True)
        else:
            st.warning("Data tidak ditemukan untuk kombinasi ini.")

# --- HALAMAN BARU: WORD CLOUD ---
def wordcloud_page(df):
    """Halaman Visualisasi Word Cloud."""
    st.header("☁️ Word Cloud Analysis")
    st.markdown("Visualisasi kata-kata yang paling sering muncul berdasarkan sentimen.")
    
    # 1. Filter Sidebar Khusus Wordcloud
    st.sidebar.divider()
    st.sidebar.subheader("Filter Word Cloud")
    
    # Filter Bulan
    months = sorted(df['month_name'].unique().tolist())
    sel_month = st.sidebar.multiselect("Pilih Bulan:", options=months, default=months, key="wc_month")
    
    # Filter Sentimen
    sentiment_opt = st.sidebar.radio("Pilih Sentimen:", ["Positif", "Negatif", "Gabungan (Semua)"], key="wc_sentiment")
    
    if not sel_month:
        st.warning("Silakan pilih setidaknya satu bulan di sidebar.")
        return

    # 2. Filtering Data
    df_wc = df[df['month_name'].isin(sel_month)]
    
    if sentiment_opt == "Positif":
        df_wc = df_wc[df_wc['Sentiment'] == 'Positif']
        colormap_style = "Greens" # Nuansa Hijau
    elif sentiment_opt == "Negatif":
        df_wc = df_wc[df_wc['Sentiment'] == 'Negatif']
        colormap_style = "Reds"   # Nuansa Merah
    else:
        colormap_style = "viridis" # Warna-warni

    if df_wc.empty:
        st.info(f"Tidak ada data ulasan {sentiment_opt} pada bulan yang dipilih.")
        return

    # 3. Ambil Teks
    # Cek kolom mana yang berisi teks bersih (final_text atau content)
    text_col = 'final_text' if 'final_text' in df.columns else 'content'
    
    # Gabungkan semua teks menjadi satu string panjang
    all_text = " ".join(df_wc[text_col].astype(str).tolist())
    
    if not all_text.strip():
        st.warning("Data teks kosong, tidak bisa membuat Word Cloud.")
        return

    # 4. Generate Word Cloud
    # Anda bisa menambahkan parameter stopwords=set(['kata', 'sambung']) jika ingin menghapus kata umum
    wc = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap=colormap_style,
        min_font_size=10
    ).generate(all_text)

    # 5. Tampilkan Plot
    st.subheader(f"Word Cloud: {sentiment_opt}")
    st.caption(f"Berdasarkan {len(df_wc)} ulasan pada periode: {', '.join(sel_month)}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    
    # Tampilkan sampel ulasan
    with st.expander(f"Lihat Sampel Ulasan ({sentiment_opt})"):
        st.dataframe(df_wc[[text_col, 'Sentiment']].head(10), use_container_width=True)


def welcome_page():
    st.title("Tentang Aplikasi")
    st.info("Aplikasi Dashboard Analisis Sentimen TikTok.")

# --- 3. Main Logic (Navigasi) ---
df = load_and_preprocess_data(LOCAL_CSV_PATH)

# Definisi Menu
MENU_OPTIONS = {
    "📈 Distribusi Sentimen": "data",
    "🏡 Analisis Topik": "home",
    "⏰ Tren Waktu": "about",
    "☁️ Word Cloud": "wordcloud", # <--- Menu Baru
    "ℹ️ Info Aplikasi": "welcome"
}

st.sidebar.title("Navigasi")
selection = st.sidebar.radio("Pilih Halaman:", list(MENU_OPTIONS.keys()))
page = MENU_OPTIONS[selection]

if not df.empty:
    if page == "data":
        data_page(df)
    elif page == "home":
        home_page(df)
    elif page == "about":
        about_page(df)
    elif page == "wordcloud":
        wordcloud_page(df) # <--- Panggil fungsi baru
    elif page == "welcome":
        welcome_page()
else:
    st.warning("Menunggu data...")