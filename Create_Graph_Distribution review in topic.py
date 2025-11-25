import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =======================================
#     Print Distribution Topic
# =======================================

df = pd.read_csv('hasil_lda_sudah_labeling.csv')
print("Total Data:", len(df))

# 1. Tampilkan Jumlah Angka di Terminal (Buat cross-check)
print("\n=== Rincian Jumlah Review per Topik ===")
print(df['Topik_ID'].value_counts())
print("=======================================\n")

plt.figure(figsize=(10, 6))

# 2. Simpan plot ke variabel 'ax' (PENTING!)
ax = sns.countplot(
    data=df, 
    x='Topik_ID', 
    hue='Topik_ID', 
    legend=False, 
    palette='viridis'
)

# 3. FITUR BARU: Menambahkan Angka di Atas Batang
# Kita loop setiap 'container' (batang) dan kasih label
for container in ax.containers:
    ax.bar_label(container, padding=3) # padding=3 biar angkanya gak nempel banget sama batang

plt.title('Jumlah Ulasan per Topik')
plt.xlabel('Topik')
plt.ylabel('Jumlah')
plt.xticks(rotation=15)
plt.tight_layout()

# Simpan
plt.savefig('grafik_distribusi_topik_angka.png') 

print("\n✓ Sukses! Grafik dengan angka telah disimpan: 'grafik_distribusi_topik_angka.png'")
