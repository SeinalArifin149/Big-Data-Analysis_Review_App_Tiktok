import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
# Tambahkan library confusion_matrix
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================================
# 1. LOAD DATA & PERSIAPAN LABEL (GROUND TRUTH)
# ==========================================
# Pastikan nama filenya benar
df = pd.read_csv('hasil_lda_labeled.csv')

# Fungsi Labeling Otomatis (Lexicon)
def auto_label_sentiment(text):
    text = str(text).lower()
    # Kamus kata sederhana
    pos_words = ['bagus', 'mantap', 'keren', 'suka', 'puas', 'senang', 'membantu', 'love', 'good', 'bisa', 'lanjut', 'terbaik']
    neg_words = ['jelek', 'kecewa', 'buruk', 'gagal', 'susah', 'berat', 'lemot', 'bug', 'error', 'tolong', 'benci', 'ngelag', 'parah']
    
    score = 0
    for word in pos_words:
        if word in text: score += 1
    for word in neg_words:
        if word in text: score -= 1
        
    if score > 0: return 'Positif'
    elif score < 0: return 'Negatif'
    else: return 'Netral'

print("Sedang membuat label sentimen awal...")
df['Sentiment_Label'] = df['tokens'].apply(auto_label_sentiment)

# Filter data (Hapus Netral)
df_clean = df[df['Sentiment_Label'] != 'Netral'].copy()

# ==========================================
# 2. LATIH MODEL NAIVE BAYES
# ==========================================
print("\nSedang melatih Naive Bayes...")

X = df_clean['tokens'] 
y = df_clean['Sentiment_Label'] 

vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Training
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Prediksi Data Test
y_pred = nb_model.predict(X_test)
print(f"Akurasi Model Naive Bayes: {accuracy_score(y_test, y_pred):.2f}")

# ==========================================
# [BARU] 2.5 VISUALISASI CONFUSION MATRIX
# ==========================================
print("Sedang membuat Confusion Matrix...")

# Hitung matriks
cm = confusion_matrix(y_test, y_pred)

# Siapkan plot
plt.figure(figsize=(6, 5))

# Plot Heatmap
# fmt='d' artinya format angka bulat (integer), bukan koma
# xticklabels & yticklabels biar muncul tulisan 'Negatif' / 'Positif'
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=nb_model.classes_, 
            yticklabels=nb_model.classes_)

plt.title('Confusion Matrix (Evaluasi Model)')
plt.xlabel('Prediksi Model')
plt.ylabel('Kunci Jawaban (Aktual)')
plt.tight_layout()

# Simpan Gambar
plt.savefig('grafik_confusion_matrix.png')
print("✓ Grafik Confusion Matrix tersimpan: 'grafik_confusion_matrix.png'")


# ==========================================
# 3. PREDIKSI KE SELURUH DATASET
# ==========================================
X_all_vec = vectorizer.transform(df['tokens'].astype(str))
df['Sentiment_NB'] = nb_model.predict(X_all_vec)

df.to_csv('hasil_akhir_sentiment_per_topic.csv', index=False)

# ==========================================
# 4. VISUALISASI PER TOPIK
# ==========================================
print("Sedang membuat Grafik Per Topik...")

plt.figure(figsize=(12, 6))

ax = sns.countplot(
    data=df, 
    x='topic_id', # Changed from 'Topik_ID' to 'topic_id'
    hue='Sentiment_NB', 
    palette={'Positif': 'green', 'Negatif': 'red'},
    edgecolor='black'
)

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title('Analisis Sentimen Naive Bayes per Topik', fontsize=14, fontweight='bold')
plt.xlabel('Topik')
plt.ylabel('Jumlah Review')
plt.legend(title='Sentimen')
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig('grafik_sentimen_per_topik.png')
print("✓ Grafik Sentimen per Topik tersimpan: 'grafik_sentimen_per_topik.png'")

print("\n=== RINGKASAN DATA ===")
summary = df.groupby(['topic_id', 'Sentiment_NB']).size().unstack(fill_value=0)
print(summary)