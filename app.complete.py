import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns # Tambahan library untuk chart aspek
import os

# ==========================================
# 1. KONFIGURASI HALAMAN & GLOBAL VARIABEL
# ==========================================
st.set_page_config(
    page_title="Aplikasi Analisis Sentimen TikTok",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path file CSV
# Pastikan kedua file ini ada di folder yang sama!
CSV_TOPIK_PATH = 'hasil_akhir_sentiment_per_topic.csv'
CSV_ASPEK_PATH = 'tiktok_sentiment_analysis_results.csv'

# ==========================================
# 2. DICTIONARY ASPEK (Global)
# ==========================================
ASPEK_DICT = {
    "UI/UX": ["tampilan", "antarmuka", "desain", "tema", "warna", "navigasi", "ikon", "huruf", "gelap", "mudah", "transisi", "animasi", "responsif", "sederhana", "praktis", "scroll", "gerakan", "malam", "ikonografi", "struktur", "interaktif", "dasbor", "menu", "submenu", "tipografi", "keterbacaan", "akses", "pintasan", "seret", "cubitan", "perbesar", "sentuhan", "geser", "hambatan", "grid", "petunjuk", "widget", "slider", "tab", "panel", "breadcrumb", "tooltip", "popup", "tablet", "ponsel", "alur", "microinteraksi", "jelas", "kontras", "intuitif", "fokus", "efek", "keseragaman", "terang", "gelap", "aksesibilitas", "bersih", "simbol", "mudah dipahami", "fluid", "responsif", "tata letak", "geser seret", "sapuan", "sentuh", "pintasan", "layar penuh", "minimalis", "transparan", "sorot", "kontras", "padding", "margin", "ramah pengguna", "gesture sentuh", "drag & drop"],
    "Fitur": ["fitur", "fungsi", "pembaruan", "filter", "efek", "stiker", "emoji", "duet", "gabung", "siaran", "unduh", "unggah", "edit", "rekam", "musik", "suara", "daftar putar", "komen", "obrolan", "cerita", "sorotan", "templat", "tanda", "pin", "penanda", "multiakun", "sinkronisasi", "simpan", "otomatis", "rekomendasi", "draft", "pemberitahuan", "ulang", "bagikan", "cadangan", "pulihkan", "impor", "ekspor", "perpustakaan", "konten", "penyesuaian", "potong", "privat", "publik", "caption", "lokasi", "rekaman", "langsung", "transisi", "kecepatan", "kolaborasi", "animasi", "watermark", "mode gelap", "pintasan", "loop", "pin video", "favorit", "sorot", "simpan otomatis", "duet teman", "kolaborasi", "reaksi cerita", "musik cerita", "tag", "mention", "polling", "stiker cerita", "jadwal posting"],
    "Performa": ["cepat", "lambat", "lemot", "macet", "kesalahan", "memuat", "tutup", "terhenti", "bug", "beku", "tertunda", "fps", "optimal", "stabil", "respon", "memori", "prosesor", "grafik", "restart", "buffering", "panas", "waktu", "buruk", "ram", "baterai", "segarkan", "timeout", "drop", "perlambatan", "freeze", "lag", "loading", "macet klik", "panas berlebih", "cpu", "gpu", "refresh", "input", "server", "antarmuka", "pembaruan", "reaksi", "konten", "kecepatan", "lancar", "jitter", "lambat", "tunda", "crash", "hang", "restart aplikasi", "lag", "stutter", "startup", "shutdown", "boot", "fps drop", "gerakan lambat", "glitch"],
    "Keamanan": ["privasi", "izin", "keamanan", "data", "akun", "blokir", "tangguh", "peretas", "penipuan", "kata sandi", "enkripsi", "otp", "phishing", "ilegal", "verifikasi", "pelacakan", "bocor", "login", "perlindungan", "autentikasi", "pemulihan", "captcha", "virus", "spam", "tautan", "pemantauan", "identitas", "sadap", "transaksi", "logout", "pengaturan", "sidik jari", "wajah", "lokasi", "sensitif", "aman", "pihak ketiga", "notifikasi", "peringatan", "firewall", "antivirus", "cadangan", "keamanan data", "token", "hash", "verifikasi otp", "aman", "enkripsi AES", "TLS", "multi-faktor", "authenticator", "perlindungan data", "intrusi", "malware", "perekam tombol", "kebocoran privasi", "peringatan keamanan"],
    "Layanan": ["layanan", "dukungan", "respon", "admin", "cs", "bantuan", "komplain", "laporan", "masukan", "obrolan", "tiket", "solusi", "panduan", "manual", "email", "tindak lanjut", "tutorial", "qa", "call center", "video", "teknis", "pengguna", "jawaban", "sopan", "lambat", "keluhan", "komunitas", "panduan lengkap", "dukungan", "helpdesk", "responsif", "sistem tiket", "umpan balik", "pemecahan masalah", "pelanggan", "servis desk", "obrolan langsung", "respon", "sla", "bantuan", "penyelesaian masalah", "panduan"],
    "Konten": ["konten", "video", "vidio", "viral", "tren", "tantangan", "negatif", "dewasa", "edukasi", "musik", "rekomendasi", "humor", "informasi", "berita", "mode", "kecantikan", "permainan", "kuliner", "tutorial", "ulasan", "unboxing", "cerita", "blog", "artikel", "headline", "infografis", "siaran", "reaksi", "parodi", "kolaborasi", "menarik", "baru", "pendek", "panjang", "lucu", "instruktif", "hiburan", "review", "pendidikan", "dokumenter", "podcast", "siaran langsung", "shorts", "sorotan", "sinematik", "klip viral"],
    "Iklan": ["iklan", "berbayar", "koin", "hadiah", "dana", "penghasilan", "monetisasi", "sponsor", "promo", "langganan", "konten", "voucher", "kupon", "cashback", "harga", "ongkir", "pengiriman", "resi", "pelacakan", "kurir", "paket", "retur", "refund", "penukaran", "bayar", "pembayaran", "transfer", "saldo", "dompet", "invoice", "tagihan", "garansi", "status", "preorder", "cod", "kartu", "debit", "ewallet", "flash", "wishlist", "pengiriman", "pelacakan", "pengiriman paket", "pesanan", "penjual", "toko", "keranjang belanja", "proses checkout", "promosi"],
    "Algoritma": ["rekomendasi", "algoritma", "tidak", "naik", "penonton", "suka", "pengikut", "interaksi", "jangkauan", "tayangan", "personal", "kurasi", "peringkat", "umpan", "jelajahi", "saran", "tren", "bayangan", "analisis", "wawasan", "pertumbuhan", "statistik", "visibilitas", "relevan", "serupa", "populer", "trending", "disesuaikan", "prioritas", "umpan", "rekomendasi pribadi", "pembelajaran mesin", "AI", "peringkat", "personalisasi", "gelembung filter", "bias"],
    "Konektivitas": ["internet", "jaringan", "wifi", "sinyal", "putus", "offline", "koneksi", "seluler", "latensi", "kecepatan", "stabilitas", "ping", "hotspot", "bandwidth", "gangguan", "hilang", "lambat", "sambungan", "tidak stabil", "terputus", "mode offline", "online", "drop sinyal", "jaringan", "cakupan", "data", "konektivitas"],
    "Audio": ["suara", "audio", "musik", "volume", "lirik", "lagu", "rekaman", "mikrofon", "gangguan", "penyeimbang", "headphone", "speaker", "bas", "treble", "loop", "hening", "jelas", "sinkronisasi", "efek", "karaoke", "pecah", "hilang", "lambat", "mic", "suara", "derau", "musik latar", "suara", "earphone", "distorsi", "umpan balik", "putar ulang", "equalizer", "level audio"],
    "Notifikasi": ["notifikasi", "pemberitahuan", "tidak", "peringatan", "pengingat", "popup", "pembaruan", "lencana", "suara", "getar", "pesan", "pengaturan", "senyap", "tertunda", "kesalahan", "frekuensi", "pengingat", "peringatan", "push", "lencana", "informasi", "peringatan", "jadwal", "nada dering", "getar", "notifikasi"],
    "Akses": ["masuk", "daftar", "verifikasi", "kata", "sandi", "nomor", "otp", "registrasi", "akun", "sosial", "lupa", "atur", "ulang", "autentikasi", "sidik jari", "wajah", "cepat", "sekali", "pulihkan", "mudah", "login", "masuk", "daftar", "atur ulang kata sandi", "kredensial", "token", "buka kunci", "login cepat"],
    "Komunitas": ["komen", "balas", "ikuti", "bagikan", "lapor", "grup", "teman", "lingkaran", "tanda", "reaksi", "sebut", "diskusi", "forum", "obrolan", "kolaborasi", "interaksi", "posting", "permintaan", "interaksi", "aturan", "komunitas", "suka", "bagikan", "mention", "ikuti", "balas", "thread", "sosial", "diskusi", "umpan balik", "interaksi", "moderasi"],
    "Penyimpanan": ["memori", "penyimpanan", "file", "boros", "cache", "unduh", "pembaruan", "optimalisasi", "kompresi", "cadangan", "sinkronisasi", "sementara", "pembersihan", "ruang", "aplikasi", "terbatas", "efisien", "penyimpanan", "disk", "kapasitas", "awan", "simpan", "cadangan", "arsip", "bebaskan", "optimalkan", "manajemen data"],
    "TiktokShop": ["belanja", "checkout", "keranjang", "produk", "diskon", "promo", "voucher", "kupon", "cashback", "harga", "ongkir", "pengiriman", "resi", "pelacakan", "kurir", "paket", "retur", "refund", "penukaran", "bayar", "pembayaran", "transfer", "saldo", "dompet", "invoice", "tagihan", "garansi", "status", "preorder", "cod", "kartu", "debit", "ewallet", "flash", "wishlist", "pengiriman", "pelacakan", "pengiriman paket", "pesanan", "penjual", "toko", "keranjang belanja", "proses checkout", "promosi"]
}

# ==========================================
# 3. FUNGSI PEMUATAN DATA (UMUM & ASPEK)
# ==========================================

# --- A. Loader untuk Analisis Topik (CSV Pertama) ---
@st.cache_data
def load_and_preprocess_data(filepath):
    try:
        df = pd.read_csv(filepath)
        if 'at' not in df.columns:
            st.error(f"Kolom 'at' tidak ditemukan di {filepath}!")
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
        # Jangan error keras jika file belum ada (agar halaman lain tetap jalan)
        return pd.DataFrame()

# --- B. Loader & Processing untuk Analisis Aspek (CSV Kedua) ---
def detect_aspect_sentiment(text, sentiment):
    """Mendeteksi aspek dalam teks dan memasangkan dengan sentimen."""
    results = []
    if isinstance(text, str):
        text_lower = text.lower()
        for aspect, keywords in ASPEK_DICT.items():
            if any(word in text_lower for word in keywords):
                results.append(f"{aspect} ({sentiment})")
    return list(set(results))

@st.cache_data
def process_aspect_data(filepath):
    """Memproses data khusus untuk analisis aspek."""
    if not os.path.exists(filepath):
        return None, None
        
    try:
        df = pd.read_csv(filepath)
        
        # 1. Cek Kolom Wajib
        if 'at' not in df.columns: return None, None
        if 'content_clean' not in df.columns or 'sentiment' not in df.columns: return None, None
        
        # 2. Preprocess Tanggal
        df['at'] = pd.to_datetime(df['at'], errors='coerce')
        
        # 3. Deteksi Aspek (Ini bagian berat, makanya di-cache)
        df["aspek_sentimen"] = df.apply(
            lambda row: detect_aspect_sentiment(row["content_clean"], row["sentiment"]),
            axis=1
        )
        
        # String untuk display/download
        df["aspek_sentimen_str"] = df["aspek_sentimen"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else ""
        )
        
        # 4. Explode Data (1 baris per aspek yang ditemukan)
        df_exploded = df.explode('aspek_sentimen')
        df_exploded = df_exploded.dropna(subset=['aspek_sentimen'])
        
        # Ekstrak Nama Aspek dan Nilai Sentimen
        df_exploded[['Aspek', 'Sentimen_Raw']] = (
            df_exploded['aspek_sentimen'].str.extract(r'(.*) \((.*)\)')
        )
        
        # Mapping Label Sentimen (0.0 -> Negatif, 1.0 -> Positif)
        df_exploded['Sentimen_Label'] = df_exploded['Sentimen_Raw'].astype(float).map({
            0.0: 'Negative',
            1.0: 'Positive'
        })
        
        # Kolom Bulan untuk Filter
        df_exploded['Bulan_Str'] = df_exploded['at'].dt.to_period('M').astype(str)
        
        return df, df_exploded
        
    except Exception as e:
        st.error(f"Error processing aspect data: {e}")
        return None, None

# ==========================================
# 4. HALAMAN - HALAMAN FITUR
# ==========================================

def data_page(df):
    """Halaman Utama: Distribusi Sentimen Global."""
    st.header("📈 Distribusi Sentimen Global")
    st.markdown("Ringkasan statistik sentimen dari seluruh data.")
    
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
    
    total = len(df_filtered)
    counts = df_filtered['Sentiment'].value_counts()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Ulasan", f"{total:,}")
    if 'Positif' in counts:
        c2.metric("Positif", f"{counts['Positif']:,}", f"{(counts['Positif']/total)*100:.1f}%")
    if 'Negatif' in counts:
        c3.metric("Negatif", f"{counts['Negatif']:,}", f"{(counts['Negatif']/total)*100:.1f}%")

    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        st.subheader("Proporsi Sentimen")
        fig = px.pie(names=counts.index, values=counts.values, color_discrete_map={'Positif':'green', 'Negatif':'red'})
        st.plotly_chart(fig, use_container_width=True)
        
    with c_chart2:
        st.subheader("Sentimen per Topik")
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

    fig = px.bar(df_f.groupby(['topic', 'Sentiment']).size().reset_index(name='Jml'), 
                 x='Sentiment', y='Jml', color='Sentiment', facet_col='topic',
                 color_discrete_map={'Positif':'green', 'Negatif':'red'})
    st.plotly_chart(fig, use_container_width=True)

def about_page(df):
    """Halaman Tren Waktu."""
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
        else:
            st.warning("Data tidak ditemukan untuk kombinasi ini.")

def wordcloud_page(df):
    """Halaman Visualisasi Word Cloud."""
    st.header("☁️ Word Cloud Analysis")
    
    st.sidebar.divider()
    st.sidebar.subheader("Filter Word Cloud")
    months = sorted(df['month_name'].unique().tolist())
    sel_month = st.sidebar.multiselect("Pilih Bulan:", options=months, default=months, key="wc_month")
    sentiment_opt = st.sidebar.radio("Pilih Sentimen:", ["Positif", "Negatif", "Gabungan (Semua)"], key="wc_sentiment")
    
    if not sel_month:
        st.warning("Silakan pilih setidaknya satu bulan di sidebar.")
        return

    df_wc = df[df['month_name'].isin(sel_month)]
    
    if sentiment_opt == "Positif":
        df_wc = df_wc[df_wc['Sentiment'] == 'Positif']
        colormap_style = "Greens"
    elif sentiment_opt == "Negatif":
        df_wc = df_wc[df_wc['Sentiment'] == 'Negatif']
        colormap_style = "Reds"
    else:
        colormap_style = "viridis"

    if df_wc.empty:
        st.info(f"Tidak ada data ulasan {sentiment_opt} pada bulan yang dipilih.")
        return

    text_col = 'final_text' if 'final_text' in df.columns else 'content'
    all_text = " ".join(df_wc[text_col].astype(str).tolist())
    
    if not all_text.strip():
        st.warning("Data teks kosong, tidak bisa membuat Word Cloud.")
        return

    wc = WordCloud(width=800, height=400, background_color='white', colormap=colormap_style, min_font_size=10).generate(all_text)

    st.subheader(f"Word Cloud: {sentiment_opt}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    
    with st.expander(f"Lihat Sampel Ulasan ({sentiment_opt})"):
        st.dataframe(df_wc[[text_col, 'Sentiment']].head(10), use_container_width=True)

# --- HALAMAN BARU: ANALISIS ASPEK (TIKTOK) ---
def aspect_analysis_page():
    """Halaman Analisis Aspek (Fitur baru yang diminta)."""
    st.header("📱 Analisis Sentimen Berbasis Aspek (TikTok)")
    st.markdown("Analisis UI/UX, Fitur, Performa, dll berdasarkan data aspek.")

    # Cek apakah file aspek ada
    if not os.path.exists(CSV_ASPEK_PATH):
        st.error(f"File '{CSV_ASPEK_PATH}' tidak ditemukan di folder!")
        st.info("Pastikan file hasil analisis aspek sudah diupload ke folder yang sama dengan app.py")
        return

    # Load data aspek
    with st.spinner('Sedang memproses aspek dan sentimen...'):
        df_proc, df_exp = process_aspect_data(CSV_ASPEK_PATH)
    
    if df_proc is None or df_exp is None:
        st.error("Gagal memproses data aspek.")
        return

    # --- SIDEBAR FILTER KHUSUS HALAMAN INI ---
    st.sidebar.divider()
    st.sidebar.subheader("Filter Aspek")
    
    list_bulan = sorted(df_exp['Bulan_Str'].unique())
    selected_months = st.sidebar.multiselect(
        "Pilih Bulan Aspek:", 
        options=list_bulan, 
        default=[list_bulan[-1]] if list_bulan else [], 
        key="aspect_month_selector"
    )
    
    st.sidebar.info(f"Total data: {len(df_proc)} ulasan.")

    # --- TABS VISUALISASI ---
    tab1, tab2, tab3 = st.tabs(["📊 Analisis Keseluruhan", "📈 Analisis Filter Bulan", "📥 Data Hasil"])
    
    # Tab 1: Total
    with tab1:
        st.subheader("Distribusi Sentimen per Aspek (Total Semua Data)")
        total_counts = df_exp.groupby(['Aspek', 'Sentimen_Label']).size().reset_index(name='Jumlah')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=total_counts, x="Aspek", y="Jumlah", hue="Sentimen_Label", 
                    palette={'Negative': '#ff6b6b', 'Positive': '#51cf66'}, ax=ax)
        ax.set_title("Total Ulasan per Aspek dan Sentimen")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig)

    # Tab 2: Filter Bulan
    with tab2:
        if selected_months:
            st.subheader(f"Analisis Aspek untuk Bulan: {', '.join(selected_months)}")
            
            monthly_data = df_exp[df_exp['Bulan_Str'].isin(selected_months)]
            monthly_counts = monthly_data.groupby(['Aspek', 'Sentimen_Label']).size().reset_index(name='Jumlah')
            
            if not monthly_counts.empty:
                fig_m, ax_m = plt.subplots(figsize=(12, 6))
                sns.barplot(data=monthly_counts, x="Aspek", y="Jumlah", hue="Sentimen_Label", 
                            palette={'Negative': '#ff6b6b', 'Positive': '#51cf66'}, ax=ax_m)
                ax_m.set_title(f"Distribusi Sentimen Gabungan ({', '.join(selected_months)})")
                ax_m.set_xticklabels(ax_m.get_xticklabels(), rotation=45, ha="right")
                ax_m.grid(axis='y', linestyle='--', alpha=0.5)
                st.pyplot(fig_m)
            else:
                st.warning("Tidak ada data aspek ditemukan pada bulan yang dipilih.")
        else:
            st.warning("Silakan pilih bulan di sidebar.")

    # Tab 3: Data
    with tab3:
        st.subheader("Data Hasil Analisis")
        st.dataframe(df_proc[['content_clean', 'sentiment', 'aspek_sentimen_str']].head(100))
        
        csv_buffer = df_proc.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV Lengkap",
            data=csv_buffer,
            file_name="tiktok_sentiment_with_aspects.csv",
            mime="text/csv"
        )

def welcome_page():
    st.title("Tentang Aplikasi")
    st.info("Aplikasi Dashboard Analisis Sentimen TikTok (Topik, Tren, dan Aspek UI/UX).")

# ==========================================
# 5. MAIN LOGIC (NAVIGASI)
# ==========================================

# Load Data Topik (Untuk fitur-fitur lama)
df_topic = load_and_preprocess_data(CSV_TOPIK_PATH)

# Definisi Menu (Tambah menu "Analisis Aspek")
MENU_OPTIONS = {
    "📈 Distribusi Sentimen": "data",
    "🏡 Analisis Topik": "home",
    "⏰ Tren Waktu": "about",
    "☁️ Word Cloud": "wordcloud",
    "📱 Analisis Aspek (UI/UX)": "aspect", # <--- Menu Baru Ditambahkan Disini
    "ℹ️ Info Aplikasi": "welcome"
}

st.sidebar.title("Navigasi")
selection = st.sidebar.radio("Pilih Halaman:", list(MENU_OPTIONS.keys()))
page = MENU_OPTIONS[selection]

# Routing Halaman
if page == "aspect":
    # Halaman Aspek punya data loader sendiri, jadi langsung panggil
    aspect_analysis_page()

elif page == "welcome":
    welcome_page()

else:
    # Halaman lain butuh data topik, cek dulu datanya ada atau tidak
    if not df_topic.empty:
        if page == "data":
            data_page(df_topic)
        elif page == "home":
            home_page(df_topic)
        elif page == "about":
            about_page(df_topic)
        elif page == "wordcloud":
            wordcloud_page(df_topic)
    else:
        st.warning(f"Menunggu data topik ('{CSV_TOPIK_PATH}')... atau file tidak ditemukan.")