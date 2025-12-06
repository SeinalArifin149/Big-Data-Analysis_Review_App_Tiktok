import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# ==========================================
# 1. LOAD DATA YANG SUDAH LENGKAP
# ==========================================
# Pakai file hasil merge dari langkah sebelumnya
filename = 'hasil_akhir_sentiment_per_topic.csv'

try:
    print("Sedang membaca data...")
    df = pd.read_csv(filename)
    
    # Cek apakah kolom 'at' dan 'Sentiment_NB' ada
    if 'at' not in df.columns or 'Sentiment_NB' not in df.columns:
        raise ValueError("Kolom 'at' atau 'Sentiment_NB' tidak ditemukan!")

    # ==========================================
    # 2. PREPROCESSING WAKTU
    # ==========================================
    print("Mengubah format tanggal...")
    # Ubah string tanggal jadi object datetime pandas
    # errors='coerce' akan mengubah data error jadi NaT (Not a Time) biar gak crash
    df['at'] = pd.to_datetime(df['at'], errors='coerce')
    
    # Hapus kalau ada tanggal yang gagal di-convert
    df = df.dropna(subset=['at'])
    
    # Urutkan berdasarkan waktu
    df = df.sort_values('at')

    # ==========================================
    # 3. AGGREGASI (GROUP BY WAKTU)
    # ==========================================
    # Kita set tanggal sebagai index biar bisa di-resample
    df_time = df.set_index('at')

    # Resample per BULAN ('M'). 
    # Kalau mau per Minggu ganti 'W', per Hari ganti 'D'.
    print("Menghitung tren per Bulan...")
    
    # Hitung jumlah kemunculan Positif & Negatif per bulan
    trend = df_time.groupby([pd.Grouper(freq='M'), 'Sentiment_NB']).size().unstack(fill_value=0)
    
    # (Opsional) Filter hanya Positif dan Negatif (abaikan Netral jika ada)
    cols_to_plot = ['Positif', 'Negatif']
    trend = trend[cols_to_plot]

    # Lihat data tren di terminal
    print("\n--- Data Tren Per Bulan ---")
    print(trend.head())

    # ==========================================
    # 4. VISUALISASI 1: LINE CHART (VOLUME)
    # ==========================================
    plt.figure(figsize=(14, 7))
    
    # Plotting Garis
    plt.plot(trend.index, trend['Positif'], marker='o', color='green', linewidth=2, label='Positif')
    plt.plot(trend.index, trend['Negatif'], marker='o', color='red', linewidth=2, label='Negatif')

    plt.title('Tren Sentimen Seiring Waktu (Per Bulan)', fontsize=16, fontweight='bold')
    plt.xlabel('Waktu', fontsize=12)
    plt.ylabel('Jumlah Review', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    # Format tanggal di sumbu X biar rapi
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2)) # Label muncul tiap 2 bulan
    plt.gcf().autofmt_xdate() # Miringkan tanggal biar gak tabrakan

    plt.savefig('grafik_trend_sentimen_volume.png')
    print("✓ Grafik 1 disimpan: 'grafik_trend_sentimen_volume.png'")

    # ==========================================
    # 5. VISUALISASI 2: STACKED AREA (PROPORSI)
    # ==========================================
    # Ini buat lihat persentase: Apakah negatif makin mendominasi?
    
    # Hitung persentase
    trend_pct = trend.div(trend.sum(axis=1), axis=0) * 100
    
    plt.figure(figsize=(14, 7))
    
    plt.stackplot(trend_pct.index, 
                  trend_pct['Positif'], 
                  trend_pct['Negatif'], 
                  labels=['Positif', 'Negatif'], 
                  colors=['green', 'red'], 
                  alpha=0.7)

    plt.title('Proporsi Sentimen Seiring Waktu (100% Stacked)', fontsize=16, fontweight='bold')
    plt.xlabel('Waktu', fontsize=12)
    plt.ylabel('Persentase (%)', fontsize=12)
    plt.margins(0, 0) # Hilangkan margin putih kiri kanan
    plt.legend(loc='upper left')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()

    plt.savefig('grafik_trend_sentimen_proporsi.png')
    print("✓ Grafik 2 disimpan: 'grafik_trend_sentimen_proporsi.png'")

except FileNotFoundError:
    print(f"❌ Error: File '{filename}' tidak ditemukan. Pastikan sudah menjalankan script merge sebelumnya.")
except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")