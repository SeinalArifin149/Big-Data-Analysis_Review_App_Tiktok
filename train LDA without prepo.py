import pandas as pd
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess

# 1. LOAD DATA
df = pd.read_csv('datasetnii.csv')

# --- BAGIAN YANG HILANG (PREPROCESSING) ---
# Pastikan kolom teksmu dibaca string. 
# GANTI 'isi_teks' dengan nama kolom teks di CSV-mu!
nama_kolom_teks = 'stemmed' 

# Tokenisasi sederhana (memecah kalimat jadi kata-kata)
print("Sedang memproses teks...")
data_tokens = [simple_preprocess(str(doc)) for doc in df[nama_kolom_teks]]

# Membuat Dictionary (Daftar kata unik & ID-nya)
dictionary = corpora.Dictionary(data_tokens)

# Membuat Corpus (Mengubah teks jadi format Bag-of-Words)
corpus = [dictionary.doc2bow(text) for text in data_tokens]
# ------------------------------------------

# 2. TRAIN MODEL LDA
print("Sedang melatih model LDA...")
num_topics = 4

lda_model = LdaModel(
    corpus=corpus,          # Data BoW yang sudah dibuat di atas
    id2word=dictionary,     # Dictionary yang sudah dibuat di atas
    num_topics=num_topics,
    random_state=42,
    chunksize=2000,
    passes=20,
    iterations=400,
    alpha='auto',
    eta='auto'
)

# 3. CETAK TOPIK
print("\nHasil Topik:")
for i, topic in lda_model.print_topics(num_topics=num_topics, num_words=10):
    print(f"Topik #{i+1}: {topic}")

# 4. DISTRIBUSI TOPIK PER DOKUMEN
# Kita ambil probabilitas topik dominan
topic_dist = [lda_model.get_document_topics(bow) for bow in corpus]

# Simpan ke dataframe
topic_data = []
for doc in topic_dist:
    # Buat dictionary kosong per dokumen
    doc_dict = {}
    for t, prob in doc:
        doc_dict[f"topic_{t}"] = prob
    topic_data.append(doc_dict)

topic_df = pd.DataFrame(topic_data)
topic_df = topic_df.fillna(0) # Isi 0 jika dokumen tidak mengandung topik tersebut

# 5. GABUNGKAN & SIMPAN (Perbaikan variabel f_lda -> df_lda)
df_lda = pd.concat([df, topic_df], axis=1)

# Simpan Hasil
df_lda.to_csv("hasil_lda_4_topics.csv", index=False)
lda_model.save("lda_model_4_topics.gensim")

print("\n" + "="*30)
print("✓ Model LDA selesai dilatih!")
print("✓ Distribusi topik tersimpan di variabel 'df_lda'")
print("✓ File 'hasil_lda_4_topics.csv' telah dibuat.")
print("✓ Model tersimpan: 'lda_model_4_topics.gensim'")
print("="*30)