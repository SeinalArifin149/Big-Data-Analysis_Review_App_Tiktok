import pandas as pd
import os

# ==========================================
# CHECK FILES FIRST
# ==========================================
print("Files in current directory:")
for file in os.listdir('.'):
    if file.endswith('.csv'):
        print(f"  - {file}")

# ==========================================
# KONFIGURASI NAMA FILE
# ==========================================
file_hasil_analisis = 'hasil_akhir_sentiment_per_topic.csv' # File yang barisnya lebih sedikit (291k)
file_sumber_asli = 'TikTok_review_2000(1).csv'  # Added .csv extension

# Check if files exist
if not os.path.exists(file_hasil_analisis):
    print(f"❌ File tidak ditemukan: {file_hasil_analisis}")
    print("Available CSV files:")
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    for i, file in enumerate(csv_files, 1):
        print(f"  {i}. {file}")
    exit()

if not os.path.exists(file_sumber_asli):
    print(f"❌ File tidak ditemukan: {file_sumber_asli}")
    print("Available CSV files:")
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    for i, file in enumerate(csv_files, 1):
        print(f"  {i}. {file}")
    exit()

# ==========================================
# PROSES PENGGABUNGAN CERDAS (MERGE)
# ==========================================
try:
    print("Sedang membaca file...")
    # Baca file hasil analisis
    df_hasil = pd.read_csv(file_hasil_analisis)
    
    # Baca file asli
    cols_to_use = ['content', 'userName', 'score', 'at'] 
    df_sumber = pd.read_csv(file_sumber_asli, usecols=cols_to_use)

    print(f"Data Hasil Analisis : {len(df_hasil)} baris")
    print(f"Data Sumber Asli    : {len(df_sumber)} baris")  # Fixed variable name

    # --- UPDATE BARU: HAPUS MISSING VALUE (CLEANING) ---
    print("\n[Cleaning] Sedang menghapus missing value di data asli...")
    jumlah_awal = len(df_sumber)
    
    # Hapus baris jika kolom 'content' ATAU 'userName' kosong (NaN)
    df_sumber = df_sumber.dropna(subset=['content', 'userName'])
    
    jumlah_akhir = len(df_sumber)
    print(f"   - Data Awal: {jumlah_awal}")
    print(f"   - Data Bersih: {jumlah_akhir}")
    print(f"   - Dibuang: {jumlah_awal - jumlah_akhir} baris kosong.")

    # --- PENTING: Hapus Duplikat di Sumber Dulu ---
    print("\n[Cleaning] Menghapus duplikat konten di sumber...")
    df_sumber = df_sumber.drop_duplicates(subset=['content'])

    # --- JURUS MERGE (LEFT JOIN) ---
    print("\nMelakukan pencocokan data (Merge)...")
    # how='left' artinya: Pertahankan semua baris di df_hasil, 
    # lalu cari pasangannya di df_sumber. Kalau gak ketemu, biarin kosong.
    df_final = pd.merge(df_hasil, df_sumber, on='content', how='left')

    # Cek apakah ada data yang Username-nya masih kosong (artinya gak ketemu di sumber)
    jumlah_hilang = df_final['userName'].isnull().sum()
    
    if jumlah_hilang > 0:
        print(f"⚠ Info: Ada {jumlah_hilang} baris yang tidak menemukan username aslinya.")
        print("   (Kemungkinan teks berubah saat preprocessing atau ada di baris yang tadi didrop).")
    
    # Simpan
    nama_output = 'hasil_final_lengkap_dengan_user.csv'
    df_final.to_csv(nama_output, index=False)
    
    print("="*40)
    print(f"✓ SUKSES! File tersimpan sebagai: {nama_output}")
    print(f"✓ Jumlah baris akhir: {len(df_final)}")
    print("="*40)
    
    # Intip hasilnya
    print(df_final[['userName', 'score', 'Sentiment_NB', 'Label_Topik']].head())

except FileNotFoundError as e:
    print(f"\n❌ Error: File tidak ditemukan - {e}")
except KeyError as e:
    print(f"\n❌ Error: Kolom {e} tidak ditemukan. Pastikan nama kolom 'content', 'userName', dll benar.")
except Exception as e:
    print(f"\n❌ Error: {e}")