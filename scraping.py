from google_play_scraper import app, reviews, Sort
import pandas as pd
from google.colab import files

# Ambil metadata aplikasi
result = app(
    'com.ss.android.ugc.trill',   # Tiktok
    lang='id',          # bahasa Indonesia
    country='id'        # region Indonesia
)

# Ambil review aplikasi (20 terbaru)
app_reviews, _ = reviews(
    'com.ss.android.ugc.trill',
    lang='id',
    country='id',
    sort=Sort.NEWEST,
    count=400000
)

# Simpan review ke DataFrame
df = pd.DataFrame(app_reviews)[['userName','score','at','content']]

# Bikin nama file dari judul app
filename = f"{result['title']}_review_2000.csv".replace(" ", "_")

# Simpan ke CSV
df.to_csv(filename, index=False, encoding='utf-8-sig')

# Download file CSV ke lokal
files.download(filename)

# Cetak informasi aplikasi
print("Data berhasil disimpan ke:", filename)
print("Nama Aplikasi:", result['title'])
print("Rating:", result['score'])
print("Jumlah Review yang diambil:", len(df))
