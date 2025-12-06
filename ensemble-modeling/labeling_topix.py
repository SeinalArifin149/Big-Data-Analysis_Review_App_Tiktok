import pandas as pd
import numpy as np

# --- 1. LOAD DATA ---
# Pastikan file ini ada di folder yang sama
df = pd.read_csv('hasil_lda_4_topics.csv') 

# --- 2. DEFINISI LABEL TOPIK ---
nama_topik = {
    0: "Masalah Teknis & Bug",
    1: "Masalah Akun & Blokir",
    2: "Hiburan & Positif",
    3: "Fitur & Konten"
}

# --- 3. EKSEKUSI PELABELAN ---
# Nama kolom topik di CSV adalah 'topic_0', 'topic_1', dst.
cols = ['topic_0', 'topic_1', 'topic_2', 'topic_3'] 

# Cari nilai tertinggi (argmax) untuk tentukan ID Topik
df['topic_id'] = np.argmax(df[cols].values, axis=1)

# Ubah ID angka jadi teks Label
df['topic'] = df['topic_id'].map(nama_topik)

# --- 4. CEK HASIL (PREVIEW) ---
print("Preview 5 data teratas:")
# Saya coba tampilkan kolom teks (biasanya namanya 'content' atau 'review_text') 
# Kalau error di baris ini, hapus 'content_processed' atau sesuaikan namanya
try:
    print(df[['topic_id', 'topic']].head())
except:
    print(df[['topic_id', 'topic']].head())

# --- 5. SAVE KE CSV BARU ---
output_filename = 'hasil_lda_labeled.csv'
df.to_csv(output_filename, index=False)

print(f"\n✅ Mantap! File berhasil disimpan dengan nama: {output_filename}")