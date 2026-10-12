"""
Modul RAG Pipeline untuk KosFinance AI.
Mengintegrasikan PyPDFLoader, RecursiveCharacterTextSplitter, FAISS,
GoogleGenerativeAIEmbeddings, dan ChatGoogleGenerativeAI via LangChain LCEL.
"""

import os
from typing import List, Tuple
from langchain_community.document_loaders import PyPDFLoader
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.prompt_templates import get_rag_prompt

def load_and_split_pdf(pdf_path: str):
    """Membaca file PDF panduan dan memecahnya menjadi potongan chunk ber-overlap."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Dokumen PDF tidak ditemukan di: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n\n", "\n", "•", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    return chunks

import re
from langchain_core.runnables import RunnableLambda

def build_vector_store(chunks, api_key: str):
    """
    Membangun sistem temu balik (retrieval) dokumen dari teks chunk.
    1. Mencoba GoogleGenerativeAIEmbeddings resmi.
    2. Jika API embedding Google mengalami penolakan/404/quota, otomatis
       beralih ke Local Semantic/Keyword Retriever berkecepatan tinggi agar
       sistem RAG tetap berfungsi 100% tanpa pernah crash.
    """
    candidate_models = [
        "gemini-embedding-001",
        "text-embedding-004",
        "gemini-embedding-2-preview"
    ]
    for m in candidate_models:
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model=m,
                google_api_key=api_key
            )
            # Tes koneksi embedding 1 kata
            embeddings.embed_query("tes")
            vectorstore = FAISS.from_documents(chunks, embeddings)
            return vectorstore
        except Exception:
            continue

    # Fallback Cerdas Mandiri (Zero-Dependency Local Retriever)
    def local_search(query: str):
        words = [w.lower() for w in re.findall(r'\w+', query) if len(w) > 2]
        scored = []
        for doc in chunks:
            text_lower = doc.page_content.lower()
            # Hitung frekuensi kemunculan kata kunci
            score = sum(text_lower.count(w) for w in words)
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:3]]

    return RunnableLambda(local_search)

def format_docs(docs) -> str:
    """Menggabungkan teks dari potongan dokumen menjadi satu string konteks terpadu."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

def get_chat_model(api_key: str):
    """
    Mengembalikan model chat Gemini dengan auto-fallback cerdas
    ke model-model aktif yang tersedia di Google API.
    """
    candidate_models = [
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]
    primary = ChatGoogleGenerativeAI(
        model=candidate_models[0],
        temperature=0.1,
        google_api_key=api_key
    )
    fallbacks = [
        ChatGoogleGenerativeAI(
            model=m,
            temperature=0.1,
            google_api_key=api_key
        )
        for m in candidate_models[1:]
    ]
    return primary.with_fallbacks(fallbacks)

def create_rag_chain(vector_or_retriever, api_key: str):
    """
    Membuat rantai operasi RAG berbasis LangChain Expression Language (LCEL).
    Mendukung input Vector Store FAISS maupun BM25 Retriever.
    """
    if hasattr(vector_or_retriever, "as_retriever"):
        retriever = vector_or_retriever.as_retriever(search_kwargs={"k": 3})
    else:
        retriever = vector_or_retriever
    
    llm = get_chat_model(api_key)
    
    prompt = get_rag_prompt()
    
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain, retriever, llm

def extract_budget_data_from_query(query: str, llm) -> dict:
    """
    Menggunakan Gemini LLM untuk mengekstrak atau menghitung parameter pos anggaran
    ke dalam bentuk JSON terstruktur untuk pembuatan file Excel.
    """
    prompt_extract = f"""
    Pengguna memberikan informasi/pertanyaan berikut terkait anggaran anak kos:
    "{query}"

    Tugas Anda: Ekstrak atau hitung nominal anggaran ke dalam 5 pos keuangan anak kos (harus angka float/integer tanpa simbol Rp).
    Jika pengguna hanya menyebutkan total uang saku (misal 2.000.000 atau 6.000.000), hitung pembagian idealnya.
    Jika ada preferensi khusus (seperti kos 1.300.000, makan 75.000/hari -> makan = 2.250.000, senang-senang 1.500.000), sesuaikan sisanya ke kebutuhan pokok dan investasi agar TOTAL PAS sama dengan uang saku.

    Keluarkan HANYA format JSON valid tanpa teks pengantar atau markdown lainnya:
    {{
        "total_allowance": 6000000,
        "kos_amount": 1300000,
        "kebutuhan_amount": 400000,
        "makan_amount": 2250000,
        "hiburan_amount": 1500000,
        "investasi_amount": 550000,
        "notes": "Anggaran Tier 3 Leluasa disesuaikan dengan preferensi pengguna"
    }}
    """
    try:
        response = llm.invoke(prompt_extract)
        content = response.content.strip()
        # Bersihkan format markdown jika model menambahkan ```json
        if "```json" in content:
            parts = content.split("```json")
            if len(parts) > 1:
                content = parts[1].split("```")[0].strip()
        elif "```" in content:
            parts = content.split("```")
            if len(parts) > 1:
                content = parts[1].split("```")[0].strip()
        
        import json
        data = json.loads(content)
        return data
    except Exception as e:
        return None
