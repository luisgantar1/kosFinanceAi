# 💰 KosFinance AI: Asisten & Perencana Keuangan Cerdas Anak Kos

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain%20LCEL-green.svg)](https://python.langchain.com)
[![Google Gemini API](https://img.shields.io/badge/Model-Gemini%201.5%20Flash-orange.svg)](https://aistudio.google.com)

**KosFinance AI** adalah aplikasi chatbot interaktif berbasis **Retrieval-Augmented Generation (RAG)** dan **AI Agent Action** yang dirancang untuk mendampingi mahasiswa dan anak kos dalam mengelola arus kas bulanan secara disiplin, realistis, dan bebas dari jeratan finansial berisiko tinggi.

Proyek ini disusun sebagai pemenuhan **Final Project** pada program **Maju Bareng AI: LLM-Based Tools & Gemini API Integration for Data Scientists** (Hacktiv8 x Google.org x Asian Development Bank).

---

## 📌 Fitur Utama

1. **RAG Grounded Intelligence**:
   - Menjawab pertanyaan keuangan berdasarkan **Dokumen Acuan Resmi (PDF 3 Halaman)**: *"Panduan Manajemen Finansial & Alokasi Anggaran Anak Kos"*.
   - Parameter suhu rendah (`temperature: 0.1`) dengan batasan ketat anti-halusinasi (menolak menjawab di luar konteks korpus).
2. **Formula Anggaran Multi-Tier**:
   - Menganalisis kapasitas finansial ke dalam 3 tingkatan (*Tier 1: Terbatas, Tier 2: Standar, Tier 3: Leluasa*).
   - Menghitung porsi realistis untuk **5 Pos Pengeluaran**: Sewa Kos, Kebutuhan Pokok/Operasional, Makan Harian, Senang-senang/Gaya Hidup, serta Investasi & Dana Darurat.
3. **Actionable AI Agent (Excel Generator)**:
   - Menghasilkan file spreadsheet interaktif (`.xlsx`) siap pakai langsung dari antarmuka chat.
   - Dilengkapi 2 sheet: *Rencana Anggaran Bulanan* (dengan formula otomatis) dan *Log Pelacak Pengeluaran Harian*.
4. **Kepatuhan Etika AI (UNESCO 2021)**:
   - **Transparansi**: Dilengkapi drawer interaktif yang menampilkan kutipan rujukan dokumen asli untuk setiap jawaban.
   - **Keamanan Finansial**: Memiliki guardrail tegas menolak Pinjol, Paylater konsumtif, dan instrumen spekulasi berisiko tinggi.
   - **Disclaimer**: Memiliki batasan etis bahwa sistem bukan penasihat keuangan berlisensi.

---

## 🏗️ Arsitektur Sistem

```text
                                [ User Query ]
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   Streamlit Web Interface │
                        └─────────────┬─────────────┘
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│       Pipeline RAG (LCEL)     │               │    Agent Action (Tools)       │
├───────────────────────────────┤               ├───────────────────────────────┤
│ 1. PDF Loader (3 Halaman)     │               │ 1. JSON Parameter Extractor   │
│ 2. Text Splitter (Overlap)    │               │ 2. OpenPyXL Workbook Engine   │
│ 3. Gemini Embedding           │               │ 3. In-Memory .xlsx Generation │
│ 4. FAISS Vector Store         │               └───────────────┬───────────────┘
│ 5. Similarity Retrieval (K=3) │                               │
│ 6. Grounded Gemini Inference  │                               │
└───────────────┬───────────────┘                               │
                │                                               │
                └───────────────────────┬───────────────────────┘
                                        │
                                        ▼
                     [ Jawaban Terstruktur + Download Excel ]
```

---

## 📁 Struktur Repositori

```text
LLM/
│
├── .env                                # Konfigurasi API Key lokal (diabaikan git)
├── .env.example                        # Contoh template environment variable
├── .gitignore                          # Filter file rahasia, venv, dan cache
├── requirements.txt                    # Daftar library python
├── README.md                           # Dokumentasi lengkap proyek
├── app.py                              # Entrypoint aplikasi web Streamlit
├── perencanaan_final_project_rag.md    # Dokumen perencanaan awal
│
├── data/
│   └── panduan_keuangan_anak_kos.pdf   # Dokumen acuan Knowledge Base RAG
│
├── src/
│   ├── __init__.py
│   ├── rag_pipeline.py                 # Orkestrasi LangChain, FAISS, & Gemini
│   ├── excel_generator.py              # Generator spreadsheet (.xlsx) openpyxl
│   └── prompt_templates.py             # System prompt persona & guardrail anti-halusinasi
│
└── scripts/
    └── generate_pdf.py                 # Skrip penyusun PDF resmi via ReportLab
```

---

## 🚀 Panduan Instalasi & Menjalankan Lokal

### 1. Prasyarat Sistem
- Python versi 3.10 atau yang lebih baru.
- Koneksi internet untuk mengakses Gemini API.

### 2. Kloning Repositori & Buat Virtual Environment
Buka terminal (Command Prompt / PowerShell / Bash) di direktori proyek:

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment:
# Di Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Di Windows (CMD):
.\venv\Scripts\activate.bat
# Di Linux/MacOS:
source venv/bin/activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key
Salin file `.env.example` menjadi `.env`, lalu masukkan Gemini API Key Anda:
```bash
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxx
```
*(Dapatkan kunci gratis melalui [Google AI Studio](https://aistudio.google.com/app/apikey))*

### 5. Generate Dokumen PDF Knowledge Base
Pastikan file PDF acuan dibuat terlebih dahulu:
```bash
python scripts/generate_pdf.py
```

### 6. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser pada alamat `http://localhost:8501`.

---

## 🌐 Panduan Deployment ke Streamlit Community Cloud

1. Unggah seluruh proyek ke repositori **GitHub Publik**.
2. Masuk ke [share.streamlit.io](https://share.streamlit.io) menggunakan akun GitHub Anda.
3. Klik **"New app"**, lalu pilih repositori proyek ini.
4. Tentukan *Main file path*: `app.py`.
5. Buka menu **Advanced settings** -> **Secrets**, lalu tambahkan konfigurasi API key:
   ```toml
   GEMINI_API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxxxxxxx"
   ```
6. Klik **"Deploy!"**. Aplikasi Anda sekarang dapat diakses secara publik di seluruh dunia!

---

## ⚖️ Etika & Lisensi
Proyek ini mematuhi standar UNESCO Recommendation on the Ethics of Artificial Intelligence (2021) dengan mengedepankan transparansi rujukan (*citation/grounding*), akuntabilitas pengembang, dan perlindungan privasi pengguna.
