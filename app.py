"""
KosFinance AI – Aplikasi Chatbot Interaktif RAG & Perencana Keuangan Anak Kos
Program: Maju Bareng AI (Hacktiv8 x Google.org x ADB)
Framework: Streamlit & LangChain (Gemini API)
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Import modul internal
from src.rag_pipeline import (
    load_and_split_pdf,
    build_vector_store,
    create_rag_chain,
    extract_budget_data_from_query
)
from src.excel_generator import generate_budget_excel

# Load environment variables lokal
load_dotenv()

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="KosFinance AI – Asisten Keuangan Anak Kos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS untuk tampilan UI yang lebih modern dan rapi
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .badge-rag {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #BFDBFE;
    }
    .excel-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Lokasi file PDF Knowledge Base
PDF_PATH = os.path.join(os.path.dirname(__file__), "data", "panduan_keuangan_anak_kos.pdf")

# Sidebar: Pengaturan & Konfigurasi
with st.sidebar:
    st.title("🎓 KosFinance AI")
    st.caption("Asisten Cerdas & Mentor Anggaran Anak Kos")
    st.markdown('<span class="badge-rag">RAG Architecture + Gemini API</span>', unsafe_allow_html=True)
    st.markdown("---")

    # Manajemen API Key (Prioritas: st.secrets -> .env -> Manual input)
    api_key_from_env = os.getenv("GEMINI_API_KEY")
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key_from_env = st.secrets["GEMINI_API_KEY"]
    except Exception:
        # st.secrets tidak ada di lokal (menggunakan .env)
        pass

    if api_key_from_env and api_key_from_env != "your_gemini_api_key_here":
        api_key = api_key_from_env
        st.success("✅ Gemini API Key terdeteksi aktif")
    else:
        api_key = st.text_input(
            "Masukkan Gemini API Key:",
            type="password",
            placeholder="AIzaSy...",
            help="Dapatkan gratis di https://aistudio.google.com/app/apikey"
        )
        if not api_key:
            st.warning("⚠️ Masukkan API Key untuk mengaktifkan model.")

    st.markdown("---")
    st.subheader("📚 Status Knowledge Base")
    if os.path.exists(PDF_PATH):
        st.success("📄 Dokumen PDF: Siap & Terindeks")
        with open(PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Unduh PDF Panduan Resmi",
            data=pdf_bytes,
            file_name="panduan_keuangan_anak_kos.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.error("❌ File PDF belum ditemukan di folder data/.")

    st.markdown("---")
    st.subheader("💡 Pertanyaan Cepat (Inspirasi)")
    quick_prompts = [
        "Berapa alokasi uang saku Rp 1.500.000 menurut panduan?",
        "Uang saku sisa Rp 80.000 padahal kiriman masih 4 hari lagi. Apa yang harus saya lakukan?",
        "Bolehkah saya pakai Paylater buat beli sepatu diskon?"
    ]
    for q in quick_prompts:
        if st.button(q, key=f"quick_{q[:15]}", use_container_width=True):
            st.session_state["user_quick_input"] = q

    st.markdown("---")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        if st.button("🗑️ Hapus Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_sb2:
        if st.button("🔄 Reset Cache", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()

# Inisialisasi Cache Resource untuk RAG Pipeline
@st.cache_resource(show_spinner="Menyiapkan Vector Store & Dokumen Panduan...")
def initialize_rag_system(pdf_path: str, key: str):
    """Memuat PDF, memecah chunks, dan mengindeks ke FAISS (hanya sekali dieksekusi)."""
    chunks = load_and_split_pdf(pdf_path)
    vectorstore = build_vector_store(chunks, key)
    return vectorstore

# Inisialisasi State Percakapan
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Halo! Saya **KosFinance AI**, asisten dan mentor keuangan personalmu. 🎓\n\n"
                "Saya siap membantumu mengelola uang saku bulanan, membagi pos anggaran, "
                "merencanakan pagu makan hemat, hingga membuatkan template file Excel rencana keuangan.\n\n"
                "Ada yang bisa saya bantu hari ini? Kamu bisa mulai dengan menyebutkan nominal uang saku bulananmu!"
            ),
            "excel_data": None
        }
    ]

# Tampilan Header Utama
st.markdown('<div class="main-header">💰 KosFinance AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    'Asisten Cerdas & Mentor Pengelolaan Arus Kas Mahasiswa berbasis RAG (Retrieval-Augmented Generation) & Gemini API.'
    '</div>', 
    unsafe_allow_html=True
)

# Render Riwayat Pesan
for msg_idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Jika pesan memiliki data Excel yang di-generate
        if msg.get("excel_data"):
            st.markdown("---")
            st.markdown("📊 **Template Perencanaan Anggaran Tersedia:**")
            st.download_button(
                label="📥 Unduh File Perencanaan (.xlsx)",
                data=msg["excel_data"],
                file_name="Rencana_Keuangan_Kos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"dl_btn_{msg_idx}"
            )

# Input Chat Pengguna
user_input = st.chat_input("Ketik pertanyaan atau nominal uang sakumu di sini...")

# Handle trigger dari tombol Quick Question di sidebar
if "user_quick_input" in st.session_state:
    user_input = st.session_state.pop("user_quick_input")

if user_input:
    if not api_key or api_key == "your_gemini_api_key_here":
        st.error("Silakan masukkan Gemini API Key yang valid pada panel sidebar terlebih dahulu.")
        st.stop()

    if not os.path.exists(PDF_PATH):
        st.error("File basis data PDF belum ada. Silakan generate file PDF terlebih dahulu.")
        st.stop()

    # Tampilkan pesan pengguna di antarmuka
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Proses Jawaban Assistant
    with st.chat_message("assistant"):
        with st.spinner("Mencari referensi panduan & merumuskan rekomendasi..."):
            try:
                # 1. Inisialisasi Vector Store & Chain
                vectorstore = initialize_rag_system(PDF_PATH, api_key)
                chain, retriever, llm = create_rag_chain(vectorstore, api_key)

                # 2. Ambil dokumen relevan & generate respons RAG
                retrieved_docs = retriever.invoke(user_input)
                bot_response = chain.invoke(user_input)
                st.markdown(bot_response)

                # 3. Fitur Agen Cerdas: Deteksi apakah pengguna meminta pembagian anggaran / Excel
                excel_bytes = None
                budget_data = extract_budget_data_from_query(user_input, llm)
                
                # Cek apakah query relevan dengan anggaran nominal
                keywords = ["excel", "bagi", "alokasi", "anggaran", "budget", "uang saku", "kos", "juta", "ribu"]
                is_budget_request = any(k in user_input.lower() for k in keywords)

                if budget_data and is_budget_request and budget_data.get("total_allowance", 0) > 0:
                    try:
                        excel_stream = generate_budget_excel(
                            total_allowance=float(budget_data.get("total_allowance", 0)),
                            kos_amount=float(budget_data.get("kos_amount", 0)),
                            kebutuhan_amount=float(budget_data.get("kebutuhan_amount", 0)),
                            makan_amount=float(budget_data.get("makan_amount", 0)),
                            hiburan_amount=float(budget_data.get("hiburan_amount", 0)),
                            investasi_amount=float(budget_data.get("investasi_amount", 0)),
                            notes=budget_data.get("notes", "Disusun otomatis oleh KosFinance AI")
                        )
                        excel_bytes = excel_stream.getvalue()

                        st.markdown("---")
                        st.markdown("📊 **File Excel Perencanaan Anggaran Telah Dibuat:**")
                        st.download_button(
                            label="📥 Unduh Rencana Keuangan (.xlsx)",
                            data=excel_bytes,
                            file_name="Rencana_Keuangan_Kos.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_btn_live_{len(st.session_state.messages)}"
                        )
                    except Exception as exc:
                        st.warning(f"Gagal memproses file Excel: {exc}")

                # 4. Transparansi Etika AI (Menampilkan rujukan potongan dokumen yang diambil)
                with st.expander("🔍 Lihat Potongan Dokumen Rujukan RAG (Transparansi Sistem)"):
                    for i, doc in enumerate(retrieved_docs, start=1):
                        st.markdown(f"**Kutipan {i} (Halaman {doc.metadata.get('page', 0) + 1}):**")
                        st.caption(doc.page_content)

                # Simpan ke memori percakapan
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response,
                    "excel_data": excel_bytes
                })

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses jawaban: {str(e)}")
