# DOKUMEN PERENCANAAN STRATEGIS: FINAL PROJECT LLM & RAG
**Program**: Maju Bareng AI – LLM-Based Tools & Gemini API Integration for Data Scientists  
**Penyelenggara**: Hacktiv8 x Google.org x Asian Development Bank (ADB)  
**Tujuan Dokumen**: Master Plan & Context Document untuk diskusi perancangan proyek sebelum tahap implementasi kode.

---

## 1. SINTESIS MATERI PEMBELAJARAN (SESI 1 - SESI 3)

Dokumen ini mengintegrasikan seluruh konsep teoritis dan praktis yang telah dipelajari sebagai acuan standar rekayasa sistem yang akan dibangun.

### 1.1 Sesi 1: Generative AI, Etika, Rekayasa Prompt, dan Gemini API
* **Evolusi Model Bahasa**:
  - Transformasi kecerdasan buatan dari sistem berbasis aturan (*rule-based*) menuju *Machine Learning*, *Deep Learning*, hingga *Generative AI* berbasis arsitektur *Transformer* (*Self-Attention Mechanism* dan lapisan *Encoder-Decoder*).
  - LLM bekerja dengan memprediksi token berikutnya berdasarkan probabilitas statistik dari data pelatihan skala masif.
* **Etika AI (Standar UNESCO 2021)**:
  - **4 Nilai Inti**: Hak Asasi & Martabat Manusia, Masyarakat Damai & Berkeadilan, Keanekaragaman & Inklusivitas, serta Keberlanjutan Lingkungan.
  - **Prinsip Operasional**: Transparansi (alur inferensi jelas), Keadilan (bebas bias data), Akuntabilitas (tanggung jawab berada pada perancang manusia), Privasi (perlindungan data rahasia), dan Keamanan (tahan terhadap eksploitasi prompt).
* **Fenomena Halusinasi & Mitigasi Prompting**:
  - *Penyebab Halusinasi*: Ketiadaan akses data dunia nyata terverifikasi, ketergantungan pola token, ketiadaan mekanisme fact-checking bawaan, dan instruksi prompt yang ambigu.
  - *Spektrum Rekayasa Prompt*:
    - Dasar: *Zero-Shot*, *One-Shot*, *Few-Shot*, *Instructional*, *Role-Based*, dan *Comparative Prompting*.
    - Lanjutan: *Chain-of-Thought* (CoT) untuk penalaran bertahap, *Tree of Thoughts* (ToT) untuk penelusuran pohon keputusan multi-skenario, dan *ReAct* (*Reasoning + Acting*) untuk siklus berpikir dan pemanggilan tindakan.
* **Konfigurasi Parameter Inferensi**:
  - `temperature` (0.0 – 2.0): Mengontrol tingkat keacakan. Untuk jawaban faktual berbasis data dokumen acuan, nilai wajib disetel rendah (0.0 – 0.2) agar deterministik.
  - `max_output_tokens`: Membatasi panjang respons agar tidak terpotong atau boros komputasi.
  - `top_k` dan `top_p`: Ambang batas pemilihan kumpulan probabilitas token kandidat (*nucleus sampling*).
* **Function Calling**:
  - Kemampuan LLM menghasilkan output terstruktur (seperti format JSON) untuk memicu pemanggilan sistem eksternal, database, atau API pihak ketiga.

---

### 1.2 Sesi 2: Arsitektur RAG, Vector Database, dan Orkestrasi LangChain
* **Paradigma RAG (Retrieval-Augmented Generation)**:
  - Solusi utama dalam mencegah halusinasi dan mengatasi batasan batas waktu pengetahuan model (*knowledge cutoff*) tanpa perlu melatih ulang (*re-training*) atau *fine-tuning* model fondasi.
  - Terdiri dari dua komponen utama:
    1. *Retrieval Component*: Mengambil potongan dokumen yang relevan dari pangkalan data eksternal.
    2. *Augmented-Generation Component*: LLM menyintesis jawaban akhir dengan hanya merujuk pada potongan konteks yang berhasil ditemukan.
* **Alur Pemrosesan Data Dokumen (RAG Pipeline)**:
  1. *Loading*: Membaca korpus dokumen acuan (file PDF 2–5 halaman).
  2. *Chunking*: Memecah dokumen menjadi potongan-potongan teks kecil menggunakan `RecursiveCharacterTextSplitter` dengan parameter ukuran potongan (*chunk size*) dan irisan penghubung (*chunk overlap*) agar konteks makna tidak terputus.
  3. *Embedding*: Mengubah teks setiap potongan menjadi representasi vektor numerik (*dense vector*) berdimensi tinggi.
  4. *Vector Storage & Indexing*: Menyimpan vektor ke dalam pangkalan data vektor lokal (*Chroma* atau *FAISS*) menggunakan algoritma pencarian kemiripan terindeks (seperti HNSW atau IVF-PQ).
  5. *Similarity Retrieval*: Mengubah kueri pengguna menjadi vektor, kemudian mencari potongan dokumen terdekat menggunakan metrik kedekatan matematis (seperti *Cosine Similarity*).
* **Framework Orkestrasi (LangChain)**:
  - Menyediakan komponen modular: model wrapper, template prompt (`ChatPromptTemplate`), dan rantai operasi (`Chains`) yang menggabungkan proses temu balik data dan inferensi model secara otomatis.
* **Alternatif Model Sumber Terbuka (Llama via Groq)**:
  - Penggunaan Groq Cloud LPU untuk inferensi Llama 3 berlatensi ultra-rendah dengan pengaturan parameter tambahan seperti `frequency_penalty` dan `presence_penalty`.

---

### 1.3 Sesi 3: Antarmuka Interaktif Streamlit, AI Agents, dan Deployment Cloud
* **Antarmuka Pengguna (Streamlit Framework)**:
  - Pustaka Python *low-code* untuk membangun antarmuka web interaktif tanpa memerlukan penguasaan CSS atau JavaScript.
  - Komponen krusial:
    - `st.chat_input`: Form input chat dinamis.
    - `st.chat_message`: Kontainer percakapan untuk peran pengguna (*user*) dan asisten (*assistant*).
    - `st.session_state`: Mekanisme penyimpanan memori lokal di browser agar riwayat pesan tidak hilang saat aplikasi melakukan eksekusi ulang (*rerun*).
    - `st.cache_resource`: Mekanisme *caching* agar proses berat (pembacaan PDF, pembuatan vektor, dan inisialisasi chain) hanya dieksekusi satu kali di awal sesi.
    - `st.sidebar`: Panel samping untuk konfigurasi sistem, parameter model, dan informasi panduan.
* **Diferensiasi Konsep AI Assistant vs AI Agent**:
  - *AI Assistant*: Bersifat pasif-reaktif, bertugas menjawab pertanyaan atau memberikan saran berdasarkan masukan pengguna.
  - *AI Agent*: Bersifat proaktif dan berorientasi tujuan (*goal-oriented*), memecah tugas kompleks menjadi sub-tugas, serta mengeksekusi alat bantu (*tools*) secara mandiri.
* **Mekanisme Deployment Produksi (Streamlit Community Cloud)**:
  - Kode program dan file pendukung dikelola dalam repositori GitHub publik.
  - Aplikasi dideploy langsung melalui dasbor `share.streamlit.io`.
  - Kredensial rahasia (API Key) diisolasi melalui panel *Streamlit Secrets* (`st.secrets`) untuk mencegah kebocoran data sensitif ke publik.

---

## 2. KETENTUAN DAN SPESIFIKASI FINAL PROJECT

| Parameter | Ketentuan Resmi | Catatan Teknis / Rekomendasi |
| :--- | :--- | :--- |
| **Bentuk Proyek** | Aplikasi Chatbot AI Interaktif (Bukan riset/paper) | Harus berbasis produk fungsional dengan antarmuka web langsung pakai |
| **Metode LLM** | RAG (Retrieval-Augmented Generation) | Tanpa training; menggunakan embedding & vector retriever |
| **Dokumen Acuan** | 1 Dokumen PDF | Panjang berkisar **2 sampai 5 halaman**, fokus pada topik terstruktur |
| **Parameter Kreatif** | Persona, gaya bahasa, batasan domain | *Temperature* disetel 0.0 – 0.2; prompt memiliki batas anti-halusinasi ketat |
| **Platform Deployment**| Streamlit Community Cloud | Terhubung otomatis ke repositori GitHub publik |
| **Keamanan Kunci API**| Tidak boleh di-*hardcode* di dalam script | Menggunakan `.env` untuk lokal dan `st.secrets` untuk Cloud |
| **Deliverables Wajib** | 1. URL Repositori GitHub Publik<br>2. Tangkapan Layar (Screenshot) UI | Dikirimkan ke form resmi: `https://bit.ly/finalproject-data` |

---

## 3. ARSITEKTUR DAN ALUR KERJA SISTEM (CONCEPTUAL BLUEPRINT)

Sistem akan dirancang dengan alur kerja sekuensial berikut:

1. **Tahap Inisialisasi Data (One-Time Execution via Cache)**:
   - Dokumen PDF acuan dibaca oleh sistem.
   - Dokumen dipartisi menjadi segmen-segmen teks kecil (*chunks*) dengan ukuran terukur dan irisan overlap.
   - Setiap segmen diubah menjadi representasi vektor menggunakan model embedding.
   - Vektor diindeks dan disimpan ke dalam vector store lokal (*Chroma* / *FAISS*).

2. **Tahap Interaksi Pengguna (Runtime Loop)**:
   - Pengguna memasukkan pertanyaan melalui form antarmuka chat Streamlit.
   - Input disimpan ke dalam `session_state` dan langsung dirender di layar.
   - Pertanyaan dikonversi menjadi vektor kueri untuk melakukan penelusuran dokumen terdekat (*Cosine Similarity Search*).
   - $K$ potongan teks paling relevan (misal $K=3$) diekstrak sebagai konteks acuan.

3. **Tahap Sintesis Jawaban (Grounded Inference)**:
   - Konteks dokumen yang lolos saring digabungkan bersama pertanyaan pengguna ke dalam *System Prompt Template*.
   - Prompt menginstruksikan LLM:
     * Menjawab secara runut sesuai persona yang ditentukan.
     * Menggunakan data faktual dari konteks dokumen saja.
     * **Aturan Khusus**: Jika jawaban tidak ada pada teks konteks, model diwajibkan menolak dengan sopan tanpa mengarang bebas.
   - Jawaban model ditampilkan ke layar dan dicatat ke dalam riwayat obrolan `session_state`.

---

## 4. EKSPLORASI OPSI PROYEK (BRAINSTORMING CANDIDATES)

Berikut adalah 4 kandidat use case yang dirancang sesuai batasan teknis (dokumen PDF 2–5 halaman):

### Opsi A: E-Commerce Customer Service & Return Policy Bot (Rekomendasi Utama)
* **Karakteristik Dokumen**: Dokumen PDF 3–4 halaman berisi Kebijakan Pengembalian Dana (*Refund*), Syarat Klaim Garansi Produk, Estimasi Waktu Ekspedisi, dan FAQ Kendala Barang Rusak.
* **Persona Bot**: Representatif *Customer Service* resmi yang ramah, solutif, empatik, namun taat pada klausul pasal garansi.
* **Keunggulan**: Mudah diuji validitas faktualnya, relevan dengan dunia industri nyata, serta mudah menetapkan batas anti-halusinasi saat pengguna menanyakan kasus di luar aturan retur.

### Opsi B: Outdoor & Travel Safety Guide Assistant (Skenario Konservasi Alam)
* **Karakteristik Dokumen**: Dokumen PDF 3–4 halaman berisi Standar Operasional Prosedur (SOP) Pendakian Taman Nasional, daftar perlengkapan wajib, etika konservasi, aturan kuota simaksi, dan protokol darurat penanganan hipotermia.
* **Persona Bot**: Pemandu alam (*Ranger*) yang komunikatif, informatif, dan sangat mengutamakan keselamatan pendaki.
* **Keunggulan**: Konsep menarik dan edukatif, selaras dengan contoh proyek batch sebelumnya (*Puncak Nusantara*).

### Opsi C: Academic Course & Certification Syllabus Assistant (Education Bot)
* **Karakteristik Dokumen**: Dokumen PDF 3–4 halaman berisi silabus lengkap sebuah program pelatihan/bootcamp (tujuan pembelajaran, modul mingguan, kriteria kelulusan, dan jadwal tugas akhir).
* **Persona Bot**: Asisten akademik virtual yang suportif, terstruktur, dan siap memandu peserta belajar secara jelas.
* **Keunggulan**: Selaras langsung dengan lingkungan pembelajaran Hacktiv8 dan mudah dibuatkan dokumen rujukannya.

### Opsi D: Klinik / Fasilitas Layanan Medis FAQ Bot (Layanan Publik)
* **Karakteristik Dokumen**: Dokumen PDF 2–3 halaman berisi SOP Pendaftaran Pasien, jadwal poliklinik spesialis, alur rujukan BPJS/asuransi, dan tata tertib jam besuk pasien.
* **Persona Bot**: Resepsionis medis yang tenang, formal, jelas, dan selalu menyertakan disclaimer bahwa bot tidak memberikan diagnosis klinis.
* **Keunggulan**: Menunjukkan kepatuhan etika AI yang sangat ketat dalam membatasi batas kompetensi sistem.

---

## 5. RENCANA KERJA TAHAP IMPLEMENTASI (ROADMAP)

1. **Fase 1: Penentuan Topik & Persona (Diskusi Awal)**
   - Memilih 1 use case dari opsi di atas (atau ide alternatif yang disepakati).
   - Menetapkan nama asisten, persona gaya bahasa, dan parameter kreatif.

2. **Fase 2: Kurasi Dokumen Pengetahuan**
   - Menyiapkan dokumen PDF acuan (panjang tepat 2–5 halaman, teks bersih tanpa format rumit/tabel rusak).
   - Menempatkan dokumen di folder proyek dengan penamaan terstandar (`knowledge_base.pdf`).

3. **Fase 3: Perumusan Grounding & Prompt Guardrails**
   - Merancang teks *system prompt* untuk memastikan jawaban faktual dan mengunci model agar tidak berhalusinasi.

4. **Fase 4: Rekayasa Kode Program di Antigravity IDE**
   - Pembuatan file dependensi (`requirements.txt`).
   - Pembuatan skrip aplikasi terpadu (`app.py`) mencakup caching pipeline RAG dan UI chat Streamlit.
   - Pengujian fungsional secara lokal (`streamlit run app.py`).

5. **Fase 5: Git Versioning & Cloud Deployment**
   - Pembuatan repositori publik di GitHub.
   - Hubungkan ke Streamlit Community Cloud dan atur *Secrets Management*.
   - Dokumentasi tangkapan layar antarmuka untuk kebutuhan pengumpulan formulir tugas akhir.