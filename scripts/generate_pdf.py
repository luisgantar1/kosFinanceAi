"""
Skrip resmi pembuat dokumen Knowledge Base RAG:
'data/panduan_keuangan_anak_kos.pdf' (3-4 Halaman Standar ReportLab)
Teks dapat diekstrak 100% oleh PyPDFLoader / LangChain.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas untuk menambahkan header dan nomor halaman dinamis."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (halaman 2 ke atas)
        if self._pageNumber > 1:
            self.drawString(54, 750, "KosFinance AI – Panduan Manajemen Finansial & Alokasi Anggaran Anak Kos")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Dokumen Resmi Knowledge Base RAG – Maju Bareng AI (Hacktiv8 x Google.org)")
        self.drawRightString(558, 32, f"Halaman {self._pageNumber} dari {page_count}")
        self.restoreState()

def build_pdf():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "panduan_keuangan_anak_kos.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Gaya Khusus
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0F766E'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=10,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # ==================== HALAMAN 1 ====================
    story.append(Paragraph("PANDUAN MANAJEMEN FINANSIAL & ALOKASI ANGGARAN ANAK KOS", title_style))
    story.append(Paragraph("<b>Standar Tata Kelola Arus Kas, Pagu Biaya Hidup, Strategi Penghematan, dan Mitigasi Darurat Mahasiswa</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=8))

    story.append(Paragraph("BAB 1: FILOSOFI ANGGARAN & FORMULA ALOKASI MULTI-TIER", h1_style))
    story.append(Paragraph(
        "Keterbatasan uang saku dan tingginya biaya hidup mandiri sering kali memicu krisis keuangan di kalangan mahasiswa dan anak kos. "
        "Metode perencanaan keuangan konvensional seperti aturan 50/30/20 terbukti kurang efektif karena porsi biaya tempat tinggal (sewa kos) "
        "dan makan harian pada umumnya menyerap lebih dari 60% total anggaran bulanan. Oleh sebab itu, KosFinance AI menetapkan arsitektur "
        "<b>Formula 5 Pos Pengeluaran</b> yang terbagi ke dalam tiga tingkatan kapasitas anggaran (Budget Tiers).",
        body_style
    ))

    story.append(Paragraph("1.1 Definisi 5 Pos Pengeluaran Utama Anak Kos", h2_style))
    story.append(Paragraph("• <b>Pos 1 - Sewa Kos & Utilitas</b>: Beban tetap mencakup sewa kamar bulanan, iuran kebersihan, air, dan tagihan listrik token.", bullet_style))
    story.append(Paragraph("• <b>Pos 2 - Kebutuhan Pokok & Operasional Kos</b>: Kebutuhan sanitasi/mandi, detergen cuci, galon isi ulang, paket data darurat, dan transportasi bensin harian.", bullet_style))
    story.append(Paragraph("• <b>Pos 3 - Makan & Minum Harian</b>: Asupan gizi primer dengan batas pagu pengeluaran harian (daily spending limit) yang terukur.", bullet_style))
    story.append(Paragraph("• <b>Pos 4 - Hiburan, Sosial, & Senang-senang</b>: Alokasi rekreasi terjadwal, nongkrong di kedai kopi nugas, langganan musik/film patungan, dan sosialisasi.", bullet_style))
    story.append(Paragraph("• <b>Pos 5 - Investasi, Tabungan, & Dana Darurat</b>: Cadangan mitigasi risiko likuid dan pembentukan aset masa depan sedini mungkin.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("1.2 Matriks Alokasi Berdasarkan Budget Tiers", h2_style))
    
    tier_data = [
        [Paragraph("Kategori Pos", table_header), 
         Paragraph("Tier 1: Terbatas<br/>(Rp 1jt – Rp 2jt)", table_header), 
         Paragraph("Tier 2: Standar<br/>(Rp 2,1jt – Rp 3,5jt)", table_header), 
         Paragraph("Tier 3: Leluasa<br/>(Rp 3,6jt – Rp 6jt+)", table_header)],
        
        [Paragraph("<b>Sewa Kos & Utilitas</b>", table_cell), 
         Paragraph("35% (Maks Rp 700rb)", table_cell), 
         Paragraph("30% (Rp 650rb–1jt)", table_cell), 
         Paragraph("20% – 25% (Rp 1jt–1,5jt)", table_cell)],
        
        [Paragraph("<b>Kebutuhan Pokok & Ops</b>", table_cell), 
         Paragraph("10% (Rp 100rb–200rb)", table_cell), 
         Paragraph("10% (Rp 210rb–350rb)", table_cell), 
         Paragraph("6% – 8% (Rp 300rb–500rb)", table_cell)],
        
        [Paragraph("<b>Makan & Minum Harian</b>", table_cell), 
         Paragraph("30% (~Rp 15rb–20rb/hari)", table_cell), 
         Paragraph("30% (~Rp 25rb–35rb/hari)", table_cell), 
         Paragraph("35% – 38% (~Rp 50rb–75rb/hari)", table_cell)],
        
        [Paragraph("<b>Senang-senang / Gaya Hidup</b>", table_cell), 
         Paragraph("10% (~Rp 25rb–50rb/minggu)", table_cell), 
         Paragraph("15% (~Rp 80rb–130rb/minggu)", table_cell), 
         Paragraph("20% – 25% (~Rp 250rb–375rb/minggu)", table_cell)],
         
        [Paragraph("<b>Investasi & Dana Darurat</b>", table_cell), 
         Paragraph("15% (RDPU / Tabungan mini)", table_cell), 
         Paragraph("15% (Dana darurat & RDPU)", table_cell), 
         Paragraph("9% – 12% (Investasi portofolio & darurat)", table_cell)],
    ]

    tier_table = Table(tier_data, colWidths=[130, 120, 125, 129])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tier_table)

    story.append(Spacer(1, 4))
    story.append(Paragraph("1.3 Studi Kasus Simulasi Nyata (Budget Rp 5.000.000 - Rp 6.000.000)", h2_style))
    story.append(Paragraph(
        "Pada anggaran Tier 3 (seperti Rp 5.000.000 atau Rp 6.000.000) dengan preferensi khusus anak kos: "
        "Sewa kamar kos Rp 1.300.000, uang makan ditetapkan Rp 75.000/hari atau Rp 2.250.000/bulan (30 hari), "
        "maka total kedua kebutuhan dasar ini adalah Rp 3.550.000. "
        "Untuk budget Rp 5.000.000, sisa dana Rp 1.450.000 dialokasikan secara seimbang: Senang-senang Rp 750.000 (15%), "
        "Kebutuhan Pokok Operasional Rp 350.000 (7%), dan Investasi serta Dana Darurat Rp 350.000 (7%). "
        "Untuk budget Rp 6.000.000, sisa Rp 2.450.000 dapat dialokasikan: Senang-senang Rp 1.500.000 (25%), "
        "Kebutuhan Pokok Rp 400.000 (6,7%), dan Investasi/Darurat Rp 550.000 (9,1%). Struktur ini menjaga arus kas bebas defisit.",
        body_style
    ))

    # ==================== HALAMAN 2 ====================
    story.append(PageBreak())
    story.append(Paragraph("BAB 2: MANAJEMEN KONSUMSI & STRATEGI MEAL PREP HACKS", h1_style))
    story.append(Paragraph(
        "Pos pengeluaran makan dan minum merupakan komponen variabel yang paling rentan mengalami kebocoran anggaran (budget leak). "
        "Tanpa perencanaan harian yang disiplin, anak kos berisiko kehabisan dana jauh sebelum akhir bulan tiba.",
        body_style
    ))

    story.append(Paragraph("2.1 Standar Pagu Pengeluaran Makan Harian Berdasarkan Tier", h2_style))
    story.append(Paragraph("• <b>Pagu Hemat (Rp 15.000 – Rp 25.000 / hari)</b>: Mengutamakan penanak nasi (rice cooker) di kamar kos untuk menyediakan nasi putih mandiri. Pembelian berfokus pada lauk matang di warteg atau sayur matang (misal tempe orek, tahu, telur ceplok/dadar).", bullet_style))
    story.append(Paragraph("• <b>Pagu Standar (Rp 25.000 – Rp 40.000 / hari)</b>: Mengombinasikan menu kantin kampus sehat untuk makan siang dan warung makan lokal untuk makan malam.", bullet_style))
    story.append(Paragraph("• <b>Pagu Leluasa (Rp 50.000 – Rp 75.000 / hari)</b>: Memberikan fleksibilitas untuk memesan makanan melalui aplikasi pesan antar atau kafe, namun tetap dipantau dengan batas maksimum Rp 75.000 per hari.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.2 Prinsip dan Strategi Meal Prep Mandiri Anak Kos", h2_style))
    story.append(Paragraph("1. <b>Belanja Bahan Mingguan di Pasar Tradisional</b>: Pembelian bumbu dasar, telur ayam (1 kg), tempe, tahu, dan sayuran di pasar tradisional dapat memangkas pengeluaran dapur hingga 40% dibandingkan minimarket modern.", bullet_style))
    story.append(Paragraph("2. <b>Optimalisasi Multifungsi Rice Cooker</b>: Penanak nasi dapat dimanfaatkan selain menanak nasi, seperti merebus telur, mengukus sayur, hingga membuat sup sederhana tanpa kompor gas.", bullet_style))
    story.append(Paragraph("3. <b>Manajemen Logistik Air Minum</b>: Membeli galon isi ulang resmi seharga Rp 6.000 – Rp 8.000 per minggu dapat menghemat ratusan ribu rupiah dibandingkan membeli air mineral botol kemasan harian.", bullet_style))
    story.append(Paragraph("4. <b>Stok Bahan Pangan Tahan Lama</b>: Selalu sediakan telur, kornet, abon, dan mie instan (konsumsi bijak) sebagai sabuk pengaman jika dompet menipis.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.3 Manajemen Biaya Sosial dan Hiburan (Pos Senang-senang)", h2_style))
    story.append(Paragraph(
        "Kebutuhan bersosialisasi dan rekreasi merupakan bagian integral dari kehidupan mahasiswa. Namun, aturan utama pos ini adalah: "
        "<b>Pengeluaran hiburan tidak boleh mengorbankan pos kebutuhan pokok dan makan</b>. Strategi pengelolaan pos senang-senang:",
        body_style
    ))
    story.append(Paragraph("• Buat batas anggaran mingguan (weekly allowance) untuk nongkrong, bukan dihabiskan sekaligus di awal bulan.", bullet_style))
    story.append(Paragraph("• Pilih warkop atau kafe dengan fasilitas Wi-Fi cepat dan stopkontak untuk mengerjakan tugas kuliah bersama teman.", bullet_style))
    story.append(Paragraph("• Manfaatkan akun langganan musik/video secara kolektif (family plan patungan) bersama teman sekamar.", bullet_style))

    # ==================== HALAMAN 3 ====================
    story.append(PageBreak())
    story.append(Paragraph("BAB 3: PEDOMAN INVESTASI AMAN & PANTANGAN FINANSIAL (RED FLAGS)", h1_style))
    story.append(Paragraph(
        "Investasi di usia mahasiswa bertujuan utama membangun literasi finansial, kebiasaan menyisihkan uang, dan disiplin portofolio, "
        "bukan untuk mencari kekayaan instan yang spekulatif.",
        body_style
    ))

    story.append(Paragraph("3.1 Instrumen Investasi Rekomendasi untuk Mahasiswa", h2_style))
    story.append(Paragraph("• <b>Reksadana Pasar Uang (RDPU)</b>: Instrumen likuid berisiko sangat rendah yang dapat dimulai dari modal Rp 10.000 melalui aplikasi fintech terdaftar OJK. RDPU bebas biaya transaksi dan imbal hasilnya di atas bunga tabungan bank biasa.", bullet_style))
    story.append(Paragraph("• <b>Tabungan Emas Digital</b>: Alternatif lindung nilai inflasi jangka panjang yang dapat dibeli dalam nominal pecahan kecil (mulai Rp 5.000).", bullet_style))
    story.append(Paragraph("• <b>Dana Darurat Tunai Terpisah</b>: Simpanan likuid minimal Rp 300.000 – Rp 1.000.000 di rekening bank digital terpisah tanpa kartu debit, hanya boleh ditarik saat kondisi genting.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.2 Pantangan Keras & Red Flags (Batas Keamanan Finansial)", h2_style))
    story.append(Paragraph(
        "KosFinance AI secara tegas menetapkan pedoman anti-halusinasi dan proteksi pengguna terhadap jebakan finansial berisiko tinggi:",
        body_style
    ))
    story.append(Paragraph("⛔ <b>DILARANG KERAS Menggunakan Pinjol (Pinjaman Online) Ilegal maupun Legal</b> untuk menutupi gaya hidup, belanja konsumtif, atau nongkrong.", bullet_style))
    story.append(Paragraph("⛔ <b>HINDARI Fitur Paylater</b> karena suku bunga tersembunyi dan denda keterlambatan dapat menjebak anak kos dalam siklus gali lubang tutup lubang.", bullet_style))
    story.append(Paragraph("⛔ <b>TOLAK Spekulasi Kripto Koin Berisiko Tinggi dan Saham Gorengan</b> sebelum memiliki dana darurat dan pendapatan mandiri yang stabil.", bullet_style))
    story.append(Paragraph("⛔ <b>WASPADAI Skema Cepat Kaya / Robot Trading / MLM Bodong</b> yang menjanjikan keuntungan pasti harian di atas kewajaran perbankan.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("BAB 4: PROTOKOL DARURAT 'SURVIVAL AKHIR BULAN' & DISCLAIMER", h1_style))
    story.append(Paragraph("4.1 SOP Taktis Saat Sisa Uang Kurang Dari Rp 100.000", h2_style))
    story.append(Paragraph(
        "Jika kiriman uang saku berikutnya masih 3–7 hari lagi namun saldo kas tersisa kurang dari Rp 100.000, "
        "lakukan 4 langkah protokol darurat berikut secara berurutan:",
        body_style
    ))
    story.append(Paragraph("1. <b>Freeze & Audit Saldo Kas</b>: Tarik sisa uang menjadi uang tunai pecahan kecil agar visualisasi pengeluaran terpantau nyata. Hentikan seluruh transaksi non-esensial.", bullet_style))
    story.append(Paragraph("2. <b>Aktivasi Mode Dapur Kos</b>: Manfaatkan stok cadangan beras dan telur. Satu kilogram telur (~Rp 28.000 berisi 16 butir) dapat mencukupi kebutuhan protein selama 5–8 hari ke depan.", bullet_style))
    story.append(Paragraph("3. <b>Manfaatkan Fasilitas Publik Kampus</b>: Isi botol minum di dispenser kampus secara maksimal dan gunakan jaringan Wi-Fi perpustakaan untuk menghemat kuota internet pribadi.", bullet_style))
    story.append(Paragraph("4. <b>Komunikasi Transparan</b>: Jika krisis tidak terhindarkan, komunikasikan kepada keluarga lebih awal secara jujur tanpa beralih ke jeratan rentenir atau pinjol.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4.2 Batasan Sistem & Disclaimer Etika AI", h2_style))
    story.append(Paragraph(
        "Aplikasi <b>KosFinance AI</b> dirancang murni sebagai alat bantu edukasi, simulasi pengelolaan arus kas, dan perencanaan anggaran mandiri "
        "berdasarkan data yang tertera pada dokumen ini. Sistem <b>TIDAK</b> bertindak sebagai penasihat perencana keuangan berlisensi (Certified Financial Planner) "
        "dan tidak melayani rekomendasi transaksi aset berjangka atau sekuritas berisiko tinggi. Seluruh keputusan finansial akhir tetap berada pada tanggung jawab pengguna.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Berhasil Dibuat dengan ReportLab: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
