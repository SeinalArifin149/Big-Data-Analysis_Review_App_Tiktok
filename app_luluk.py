import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===============================
# Konfigurasi Halaman
# ===============================
st.set_page_config(
    page_title="TikTok Aspect-Based Sentiment Analysis",
    page_icon="📊",
    layout="wide"
)

# ===============================
# Dictionary Aspek (Global)
# ===============================
ASPEK_DICT = {
    "UI/UX": [
        "tampilan", "antarmuka", "desain", "tema", "warna", "tata", "letak",
        "navigasi", "ikon", "huruf", "gelap", "mudah", "transisi",
        "animasi", "responsif", "sederhana", "praktis", "scroll",
        "gerakan", "malam", "ikonografi", "struktur", "interaktif",
        "dasbor", "menu", "submenu", "tipografi", "keterbacaan",
        "akses", "pintasan", "seret", "cubitan", "perbesar",
        "sentuhan", "geser", "hambatan", "grid", "petunjuk",
        "widget", "slider", "tab", "panel", "breadcrumb",
        "tooltip", "popup", "tablet", "ponsel", "alur",
        "microinteraksi", "jelas", "kontras", "intuitif",
        "fokus", "efek", "keseragaman", "terang", "gelap",
        "aksesibilitas", "bersih", "simbol", "mudah dipahami",
        "fluid", "responsif", "tata letak", "geser seret", "sapuan",
        "sentuh", "pintasan", "layar penuh", "minimalis", "transparan",
        "sorot", "kontras", "padding", "margin", "ramah pengguna",
        "gesture sentuh", "drag & drop"
    ],
    "Fitur": [
        "fitur", "fungsi", "pembaruan", "filter", "efek", "stiker",
        "emoji", "duet", "gabung", "siaran", "unduh", "unggah",
        "edit", "rekam", "musik", "suara", "daftar putar", "komen",
        "obrolan", "cerita", "sorotan", "templat", "tanda", "pin",
        "penanda", "multiakun", "sinkronisasi", "simpan", "otomatis",
        "rekomendasi", "draft", "pemberitahuan", "ulang", "bagikan",
        "cadangan", "pulihkan", "impor", "ekspor", "perpustakaan",
        "konten", "penyesuaian", "potong", "privat", "publik",
        "caption", "lokasi", "rekaman", "langsung", "transisi",
        "kecepatan", "kolaborasi", "animasi", "watermark",
        "mode gelap", "pintasan", "loop", "pin video", "favorit",
        "sorot", "simpan otomatis", "duet teman", "kolaborasi",
        "reaksi cerita", "musik cerita", "tag", "mention", "polling",
        "stiker cerita", "jadwal posting"
    ],
    "Performa": [
        "cepat", "lambat", "lemot", "macet", "kesalahan", "memuat",
        "tutup", "terhenti", "bug", "beku", "tertunda", "fps",
        "optimal", "stabil", "respon", "memori", "prosesor", "grafik",
        "restart", "buffering", "panas", "waktu", "buruk", "ram",
        "baterai", "segarkan", "timeout", "drop", "perlambatan",
        "freeze", "lag", "loading", "macet klik", "panas berlebih",
        "cpu", "gpu", "refresh", "input", "server", "antarmuka",
        "pembaruan", "reaksi", "konten", "kecepatan", "lancar",
        "jitter", "lambat", "tunda", "crash", "hang", "restart aplikasi",
        "lag", "stutter", "startup", "shutdown", "boot", "fps drop",
        "gerakan lambat", "glitch"
    ],
    "Keamanan": [
        "privasi", "izin", "keamanan", "data", "akun", "blokir",
        "tangguh", "peretas", "penipuan", "kata sandi", "enkripsi",
        "otp", "phishing", "ilegal", "verifikasi", "pelacakan",
        "bocor", "login", "perlindungan", "autentikasi", "pemulihan",
        "captcha", "virus", "spam", "tautan", "pemantauan",
        "identitas", "sadap", "transaksi", "logout", "pengaturan",
        "sidik jari", "wajah", "lokasi", "sensitif", "aman",
        "pihak ketiga", "notifikasi", "peringatan",
        "firewall", "antivirus", "cadangan", "keamanan data", "token",
        "hash", "verifikasi otp", "aman", "enkripsi AES", "TLS",
        "multi-faktor", "authenticator", "perlindungan data",
        "intrusi", "malware", "perekam tombol", "kebocoran privasi", "peringatan keamanan"
    ],
    "Layanan": [
        "layanan", "dukungan", "respon", "admin", "cs", "bantuan",
        "komplain", "laporan", "masukan", "obrolan", "tiket", "solusi",
        "panduan", "manual", "email", "tindak lanjut", "tutorial",
        "qa", "call center", "video", "teknis", "pengguna", "jawaban",
        "sopan", "lambat", "keluhan", "komunitas", "panduan lengkap",
        "dukungan", "helpdesk", "responsif", "sistem tiket", "umpan balik",
        "pemecahan masalah", "pelanggan", "servis desk", "obrolan langsung",
        "respon", "sla", "bantuan", "penyelesaian masalah", "panduan"
    ],
    "Konten": [
        "konten", "video", "vidio", "viral", "tren", "tantangan", "negatif",
        "dewasa", "edukasi", "musik", "rekomendasi", "humor", "informasi",
        "berita", "mode", "kecantikan", "permainan", "kuliner", "tutorial",
        "ulasan", "unboxing", "cerita", "blog", "artikel", "headline",
        "infografis", "siaran", "reaksi", "parodi", "kolaborasi",
        "menarik", "baru", "pendek", "panjang", "lucu", "instruktif",
        "hiburan", "review", "pendidikan", "dokumenter", "podcast",
        "siaran langsung", "shorts", "sorotan", "sinematik", "klip viral"
    ],
    "Iklan": [
        "iklan", "berbayar", "koin", "hadiah", "dana", "penghasilan",
        "monetisasi", "sponsor", "promo", "langganan", "konten",
        "voucher", "bonus", "isi ulang", "donasi", "pelanggan", "premium",
        "pendapatan", "reward", "pembelian", "virtual", "penempatan",
        "mingguan", "bulanan", "kreator", "tambahan", "penonton",
        "iklan", "kampanye", "berbayar", "bersponsor", "pop-up", "spanduk"
    ],
    "Algoritma": [
        "rekomendasi", "algoritma", "tidak", "naik", "penonton",
        "suka", "pengikut", "interaksi", "jangkauan", "tayangan",
        "personal", "kurasi", "peringkat", "umpan", "jelajahi",
        "saran", "tren", "bayangan", "analisis", "wawasan",
        "pertumbuhan", "statistik", "visibilitas", "relevan",
        "serupa", "populer", "trending", "disesuaikan", "prioritas",
        "umpan", "rekomendasi pribadi", "pembelajaran mesin", "AI", "peringkat",
        "personalisasi", "gelembung filter", "bias"
    ],
    "Konektivitas": [
        "internet", "jaringan", "wifi", "sinyal", "putus", "offline",
        "koneksi", "seluler", "latensi", "kecepatan", "stabilitas",
        "ping", "hotspot", "bandwidth", "gangguan", "hilang",
        "lambat", "sambungan", "tidak stabil", "terputus", "mode offline",
        "online", "drop sinyal", "jaringan", "cakupan", "data", "konektivitas"
    ],
    "Audio": [
        "suara", "audio", "musik", "volume", "lirik", "lagu",
        "rekaman", "mikrofon", "gangguan", "penyeimbang", "headphone",
        "speaker", "bas", "treble", "loop", "hening", "jelas",
        "sinkronisasi", "efek", "karaoke", "pecah", "hilang", "lambat",
        "mic", "suara", "derau", "musik latar", "suara", "earphone",
        "distorsi", "umpan balik", "putar ulang", "equalizer", "level audio"
    ],
    "Notifikasi": [
        "notifikasi", "pemberitahuan", "tidak", "peringatan", "pengingat",
        "popup", "pembaruan", "lencana", "suara", "getar", "pesan",
        "pengaturan", "senyap", "tertunda", "kesalahan", "frekuensi",
        "pengingat", "peringatan", "push", "lencana", "informasi",
        "peringatan", "jadwal", "nada dering", "getar", "notifikasi"
    ],
    "Akses": [
        "masuk", "daftar", "verifikasi", "kata", "sandi", "nomor",
        "otp", "registrasi", "akun", "sosial", "lupa", "atur",
        "ulang", "autentikasi", "sidik jari", "wajah", "cepat", "sekali",
        "pulihkan", "mudah", "login", "masuk", "daftar", "atur ulang kata sandi",
        "kredensial", "token", "buka kunci", "login cepat"
    ],
    "Komunitas": [
        "komen", "balas", "ikuti", "bagikan", "lapor", "grup",
        "teman", "lingkaran", "tanda", "reaksi", "sebut", "diskusi",
        "forum", "obrolan", "kolaborasi", "interaksi", "posting",
        "permintaan", "interaksi", "aturan", "komunitas", "suka",
        "bagikan", "mention", "ikuti", "balas", "thread", "sosial",
        "diskusi", "umpan balik", "interaksi", "moderasi"
    ],
    "Penyimpanan": [
        "memori", "penyimpanan", "file", "boros", "cache", "unduh",
        "pembaruan", "optimalisasi", "kompresi", "cadangan", "sinkronisasi",
        "sementara", "pembersihan", "ruang", "aplikasi", "terbatas", "efisien",
        "penyimpanan", "disk", "kapasitas", "awan", "simpan", "cadangan",
        "arsip", "bebaskan", "optimalkan", "manajemen data"
    ],
    "TiktokShop": [
        "belanja", "checkout", "keranjang", "produk", "diskon", "promo",
        "voucher", "kupon", "cashback", "harga", "ongkir", "pengiriman",
        "resi", "pelacakan", "kurir", "paket", "retur", "refund",
        "penukaran", "bayar", "pembayaran", "transfer", "saldo",
        "dompet", "invoice", "tagihan", "garansi", "status", "preorder",
        "cod", "kartu", "debit", "ewallet", "flash", "wishlist",
        "pengiriman", "pelacakan", "pengiriman paket", "pesanan", "penjual",
        "toko", "keranjang belanja", "proses checkout", "promosi"
    ]
}

# ===============================
# Fungsi Helper
# ===============================
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
def process_data(df):
    """
    Fungsi utama untuk memproses dataframe:
    1. Konversi Tanggal
    2. Deteksi Aspek
    3. Explode data untuk analisis
    """
    # 1. Pastikan kolom datetime
    if 'at' in df.columns:
        df['at'] = pd.to_datetime(df['at'], errors='coerce')
    else:
        st.error("Kolom 'at' (tanggal) tidak ditemukan dalam CSV.")
        return None, None

    # 2. Deteksi Aspek
    if 'content_clean' not in df.columns or 'sentiment' not in df.columns:
         st.error("Kolom 'content_clean' atau 'sentiment' tidak ditemukan.")
         return None, None
         
    df["aspek_sentimen"] = df.apply(
        lambda row: detect_aspect_sentiment(row["content_clean"], row["sentiment"]),
        axis=1
    )

    # Buat string untuk di-download nanti
    df["aspek_sentimen_str"] = df["aspek_sentimen"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else ""
    )
    
    # 3. Buat DataFrame 'Exploded' untuk visualisasi (Satu baris per aspek)
    df_exploded = df.explode('aspek_sentimen')
    df_exploded = df_exploded.dropna(subset=['aspek_sentimen'])
    
    # Ekstrak Nama Aspek dan Nilai Sentimen
    df_exploded[['Aspek', 'Sentimen_Raw']] = (
        df_exploded['aspek_sentimen'].str.extract(r'(.*) \((.*)\)')
    )
    
    # Mapping Label Sentimen
    df_exploded['Sentimen_Label'] = df_exploded['Sentimen_Raw'].astype(float).map({
        0.0: 'Negative',
        1.0: 'Positive'
    })
    
    return df, df_exploded

# ===============================
# Main Interface
# ===============================
st.title("📱 Analisis Sentimen Berbasis Aspek (TikTok)")
st.markdown("Aplikasi ini otomatis membaca data, menganalisis aspek, dan menampilkan visualisasi.")

# --- Bagian Loading File Otomatis ---
FILE_PATH = "tiktok_sentiment_analysis_results.csv"

# Cek apakah file ada
if os.path.exists(FILE_PATH):
    # Load Data
    try:
        # Baca langsung file dari path
        df_raw = pd.read_csv(FILE_PATH)
        
        # Proses Data
        with st.spinner('Sedang memproses aspek dan sentimen...'):
            df_processed, df_exploded = process_data(df_raw)
            
        if df_processed is not None and df_exploded is not None:
            
            # --- SELEKSI BULAN (MULTI-SELECT) ---
            # Buat kolom Bulan String (YYYY-MM) untuk filter
            df_exploded['Bulan_Str'] = df_exploded['at'].dt.to_period('M').astype(str)
            list_bulan = sorted(df_exploded['Bulan_Str'].unique())
            
            # Filter diletakkan di atas tab
            st.header("⚙️ Filter Data")
            col_filter, col_info = st.columns([1, 3])
            
            with col_filter:
                # Menggunakan multiselect agar bisa pilih lebih dari satu
                selected_months = st.multiselect(
                    "Pilih Bulan (Bisa lebih dari satu):", 
                    options=list_bulan, 
                    default=[list_bulan[-1]], # Default pilih bulan terakhir
                    key="month_selector"
                )
            
            with col_info:
                st.info(f"Total data ulasan tersedia dari **{list_bulan[0]}** hingga **{list_bulan[-1]}**.")
            
            st.markdown("---")
            
            # 2. Tabs untuk Navigasi
            tab1, tab2, tab3 = st.tabs(["📊 Analisis Keseluruhan", "📈 Analisis Filter Bulan", "📥 Data Hasil"])
            
            # --- TAB 1: Analisis Keseluruhan (TETAP SEMUA DATA) ---
            with tab1:
                st.subheader("Distribusi Sentimen per Aspek (Total Semua Data)")
                
                total_counts = df_exploded.groupby(['Aspek', 'Sentimen_Label']).size().reset_index(name='Jumlah')
                
                fig, ax = plt.subplots(figsize=(14, 7))
                sns.barplot(data=total_counts, x="Aspek", y="Jumlah", hue="Sentimen_Label", 
                            palette={'Negative': '#ff6b6b', 'Positive': '#51cf66'}, ax=ax)
                ax.set_title("Total Ulasan per Aspek dan Sentimen")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
                ax.grid(axis='y', linestyle='--', alpha=0.5)
                st.pyplot(fig)

            # --- TAB 2: Analisis Filter Bulan (Mengikuti Input Multiselect) ---
            with tab2:
                if selected_months:
                    st.subheader(f"Analisis Aspek untuk Bulan: {', '.join(selected_months)}")
                    
                    # Filter data berdasarkan list bulan yang dipilih
                    monthly_data = df_exploded[df_exploded['Bulan_Str'].isin(selected_months)]
                    monthly_counts = monthly_data.groupby(['Aspek', 'Sentimen_Label']).size().reset_index(name='Jumlah')
                    
                    if not monthly_counts.empty:
                        fig_m, ax_m = plt.subplots(figsize=(14, 7))
                        sns.barplot(data=monthly_counts, x="Aspek", y="Jumlah", hue="Sentimen_Label", 
                                    palette={'Negative': '#ff6b6b', 'Positive': '#51cf66'}, ax=ax_m)
                        ax_m.set_title(f"Distribusi Sentimen Gabungan ({', '.join(selected_months)})")
                        ax_m.set_xticklabels(ax_m.get_xticklabels(), rotation=45, ha="right")
                        ax_m.grid(axis='y', linestyle='--', alpha=0.5)
                        st.pyplot(fig_m)
                    else:
                        st.warning(f"Tidak ada data aspek yang ditemukan pada bulan yang dipilih.")
                else:
                    st.warning("⚠️ Silakan pilih setidaknya satu bulan pada filter di atas.")

            # --- TAB 3: Data & Download ---
            with tab3:
                st.subheader("Data Hasil Analisis")
                st.dataframe(df_processed[['content_clean', 'sentiment', 'aspek_sentimen_str']].head(100))
                
                csv_buffer = df_processed.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV Lengkap",
                    data=csv_buffer,
                    file_name="tiktok_sentiment_with_aspects.csv",
                    mime="text/csv"
                )
                
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    # Pesan Error jika file tidak ditemukan
    st.error(f"❌ File '{FILE_PATH}' tidak ditemukan!")
    st.info(f"Pastikan file CSV bernama '{FILE_PATH}' berada di folder yang sama dengan skrip ini.")