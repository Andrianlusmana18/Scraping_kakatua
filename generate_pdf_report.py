#!/usr/bin/env python3
"""
Script Generator PDF Laporan Resmi UTS Automation Systems
Universitas Pelita Bangsa - Teknik Informatika
Menghasilkan dokumentasi/laporan_uts.pdf sesuai standar format akademis.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def build_pdf(filename="dokumentasi/laporan_uts.pdf"):
    Path("dokumentasi").mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        textColor=colors.HexColor('#0F2C59')
    )

    subtitle_style = ParagraphStyle(
        'CoverSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#333333')
    )

    univ_style = ParagraphStyle(
        'CoverUniv',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#1E3E62')
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F2C59'),
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3E62'),
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=4, # Justify
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1A1A1A'),
        backColor=colors.HexColor('#F4F6F8'),
        borderPadding=6,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # HALAMAN COVER / JUDUL
    # =========================================================================
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("UNIVERSITAS PELITA BANGSA", univ_style))
    story.append(Paragraph("FAKULTAS TEKNIK - PROGRAM STUDI TEKNIK INFORMATIKA", ParagraphStyle('SubUniv', parent=univ_style, fontSize=11, fontName='Helvetica')))
    story.append(Paragraph("Jl. Inspeksi Kalimalang Tegal Danas, Cikarang Pusat - Kab. Bekasi", ParagraphStyle('AddrUniv', parent=univ_style, fontSize=8, fontName='Helvetica', textColor=colors.gray)))
    story.append(Spacer(1, 1.5 * cm))
    
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0F2C59'), spaceAfter=15))
    story.append(Paragraph("LAPORAN PROJECT UJIAN TENGAH SEMESTER (UTS)<br/>MATA KULIAH: AUTOMATION SYSTEMS", title_style))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Sistem Otomatisasi Scraping & Pengorganisasian Katalog Buku Digital<br/>(Studi Kasus: Penerbit Kakatua)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F2C59'), spaceBefore=15, spaceAfter=20))

    story.append(Spacer(1, 1.5 * cm))

    info_kelompok = [
        [Paragraph("<b>Dosen Pengampu</b>", body_style), Paragraph(": Anggi Muhammad Rifa’i, M.Kom", body_style)],
        [Paragraph("<b>Semester / TA</b>", body_style), Paragraph(": Semester Genap TA 2025 / 2026", body_style)],
        [Paragraph("<b>Tema Proyek</b>", body_style), Paragraph(": Online Book Catalog Organizer", body_style)],
        [Paragraph("<b>Nama Kelompok</b>", body_style), Paragraph(": Kelompok 01", body_style)],
        [Paragraph("<b>Anggota Kelompok</b>", body_style), Paragraph(": 1. [Nama Mahasiswa 1] - [NIM]<br/>2. [Nama Mahasiswa 2] - [NIM]<br/>3. [Nama Mahasiswa 3] - [NIM]", body_style)],
    ]
    t_info = Table(info_kelompok, colWidths=[4 * cm, 12 * cm])
    t_info.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_info)

    story.append(Spacer(1, 3.0 * cm))
    story.append(Paragraph("CIKARANG - BEKASI<br/>TAHUN 2026", ParagraphStyle('FootYear', parent=univ_style, fontSize=10)))
    story.append(PageBreak())

    # =========================================================================
    # BAB I: PENDAHULUAN
    # =========================================================================
    story.append(Paragraph("BAB I: PENDAHULUAN", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1E3E62'), spaceAfter=8))
    
    story.append(Paragraph("<b>1.1 Latar Belakang Masalah</b>", h2_style))
    story.append(Paragraph(
        "Di era ledakan informasi dan literasi digital, toko buku mandiri dan penerbit independen seperti <b>Penerbit Kakatua</b> (https://penerbitkakatua.com/) "
        "memiliki katalog literatur klasik dunia, filsafat, sastra, dan humaniora yang sangat berharga. Namun, proses pencarian, pencatatan data buku, "
        "pemantauan harga diskon, dan rekapitulasi inventaris secara manual membutuhkan waktu yang lama serta rawan kesalahan (human error). "
        "Oleh karena itu, diperlukan suatu aplikasi otomatisasi berbasis Python yang mampu mengekstraksi data secara terstruktur, membersihkan informasi, "
        "mengorganisasikan arsip secara sistematis, dan membuat pencadangan data otomatis.",
        body_style
    ))

    story.append(Paragraph("<b>1.2 Tujuan Proyek</b>", h2_style))
    story.append(Paragraph(
        "Tujuan utama dari proyek otomatisasi ini adalah:<br/>"
        "1. Membangun scraper berbasis HTML parsing menggunakan pustaka <i>requests</i> dan <i>BeautifulSoup</i> untuk mengambil minimal 30 record katalog buku tanpa menggunakan API pihak ketiga.<br/>"
        "2. Menerapkan minimal dua pola <i>Regular Expressions</i> (Regex) untuk ekstraksi harga angka Rupiah dan pemisahan otomatis nama pengarang serta judul buku.<br/>"
        "3. Menyimpan hasil ekstraksi secara terstruktur ke dalam file CSV dan laporan eksekutif TXT menggunakan modul <i>pathlib</i> dan <i>open()</i>.<br/>"
        "4. Mengimplementasikan antarmuka <i>Command Line Interface</i> (CLI) interaktif dengan argumen lengkap (argparse).<br/>"
        "5. Mengarsipkan hasil pemrosesan ke dalam file kompresi ZIP secara otomatis.",
        body_style
    ))
    story.append(Spacer(1, 0.5 * cm))

    # =========================================================================
    # BAB II: LANDASAN TEORI & INTEGRASI MATERI WAJIB
    # =========================================================================
    story.append(Paragraph("BAB II: INTEGRASI MATERI WAJIB (CH 9 - 13)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1E3E62'), spaceAfter=8))

    integrasi_data = [
        [Paragraph("<b>Bab Materi</b>", body_style), Paragraph("<b>Materi Wajib</b>", body_style), Paragraph("<b>Implementasi Nyata pada Proyek</b>", body_style)],
        [
            Paragraph("<b>Chapter 9</b>", body_style),
            Paragraph("Regular Expressions", body_style),
            Paragraph(r"Digunakan untuk: (1) Membersihkan string harga Rp dan diskon <code>r'Rp\s?([\d\.]+)'</code> menjadi integer murni; (2) Memisahkan nama Penulis dan Judul <code>r'^(.*?)\s*(?:[–—]|\s-\s)\s*(.*)$'</code>; (3) Ekstraksi ISBN/QRCBN dan jumlah halaman.", body_style)
        ],
        [
            Paragraph("<b>Chapter 10</b>", body_style),
            Paragraph("Reading & Writing Files", body_style),
            Paragraph("Menyimpan log mentah ke <code>data/raw_data.txt</code>, dataset hasil scraping ke <code>output/hasil_scraping.csv</code>, dan laporan statistik ke <code>output/laporan.txt</code> dengan encoding UTF-8.", body_style)
        ],
        [
            Paragraph("<b>Chapter 11</b>", body_style),
            Paragraph("Organizing Files", body_style),
            Paragraph("Menggunakan <code>pathlib.Path</code> untuk membuat direktori kerja otomatis (<code>mkdir(parents=True)</code>) dan modul <code>zipfile</code> untuk memaketkan arsip cadangan <code>backup/backup_data.zip</code>.", body_style)
        ],
        [
            Paragraph("<b>Chapter 12</b>", body_style),
            Paragraph("Command Line Programs", body_style),
            Paragraph("Mengimplementasikan <code>argparse</code> dengan opsi: <code>--url</code>, <code>--limit</code>, <code>--keyword</code>, <code>--category</code>, <code>--output</code>, dan <code>--backup</code>.", body_style)
        ],
        [
            Paragraph("<b>Chapter 13</b>", body_style),
            Paragraph("Web Scraping", body_style),
            Paragraph("Mengambil halaman HTML WooCommerce secara bertahap (paginasi multi-halaman) menggunakan <code>requests.get()</code> dan mem-parsing tag DOM menggunakan <code>BeautifulSoup(html, 'html.parser')</code> (Murni HTML, non-API).", body_style)
        ],
    ]
    t_materi = Table(integrasi_data, colWidths=[2.5 * cm, 3.5 * cm, 10.5 * cm])
    t_materi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8EDF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_materi)
    story.append(PageBreak())

    # =========================================================================
    # BAB III: PERANCANGAN SISTEM & KODE IMPLEMENTASI
    # =========================================================================
    story.append(Paragraph("BAB III: METODOLOGI & ARSITEKTUR PROGRAM", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1E3E62'), spaceAfter=8))

    story.append(Paragraph("<b>3.1 Alur Kerja Sistem (Flowchart)</b>", h2_style))
    story.append(Paragraph(
        "Alur program diawali dari CLI Parser (argparse) untuk membaca argumen dari terminal. "
        "Selanjutnya, modul pathlib memastikan direktori <code>data/</code>, <code>output/</code>, dan <code>backup/</code> tersedia. "
        "Aplikasi mengirimkan permintaan HTTP GET ke <code>https://penerbitkakatua.com/shop/</code> dan mem-parsing elemen HTML <code>.product_item</code>. "
        "Jika batas data (limit) belum tercapai, sistem secara cerdas melanjutkan paginasi ke <code>/shop/page/2/</code> dst. "
        "Setiap item buku diekstrak menggunakan RegEx untuk memisahkan pengarang, judul, serta harga diskon/asli. "
        "Terakhir, data disimpan ke format CSV dan TXT, lalu diarsipkan ke ZIP.",
        body_style
    ))

    story.append(Paragraph("<b>3.2 Struktur Direktori Proyek</b>", h2_style))
    story.append(Paragraph(
        "Struktur direktori pengumpulan dirancang sesuai standar ketentuan UTS:<br/>"
        "<font face='Courier' size='8'>"
        "UTS_Project_Kelompok_01/<br/>"
        "|-- main.py                # Script utama otomasi Python (CLI)<br/>"
        "|-- requirements.txt       # Daftar dependensi pustaka Python<br/>"
        "|-- README.md              # Petunjuk instalasi & demonstrasi program<br/>"
        "|-- data/<br/>"
        "|   +-- raw_data.txt       # Log data mentah hasil respon scraping<br/>"
        "|-- output/<br/>"
        "|   |-- hasil_scraping.csv # Dataset terstruktur (30+ baris data)<br/>"
        "|   +-- laporan.txt        # Laporan statistik & ringkasan eksekutif<br/>"
        "|-- backup/<br/>"
        "|   +-- backup_data.zip    # Arsip ZIP hasil kompresi data<br/>"
        "+-- dokumentasi/<br/>"
        "    +-- laporan_uts.pdf    # Dokumen laporan resmi UTS<br/>"
        "</font>",
        body_style
    ))

    story.append(Paragraph("<b>3.3 Penanganan Kesalahan (Error Handling & Robustness)</b>", h2_style))
    story.append(Paragraph(
        "Aplikasi dilengkapi penanganan error berlapis: "
        "(1) <i>ConnectionError & Timeout</i>: Menangani gangguan jaringan saat HTTP request; "
        "(2) <i>Data Kosong</i>: Menangani kondisi pencarian kata kunci yang tidak menemukan data dengan notifikasi ramah tanpa crash; "
        "(3) <i>File / Path Safety</i>: Penggunaan pathlib memastikan folder dibuat sebelum file ditulis sehingga bebas dari FileNotFoundError.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # BAB IV: HASIL PENGUJIAN DAN EVALUASI
    # =========================================================================
    story.append(Paragraph("BAB IV: HASIL PENGUJIAN & ANALISIS DATA", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1E3E62'), spaceAfter=8))

    story.append(Paragraph("<b>4.1 Pengujian Perintah CLI</b>", h2_style))
    story.append(Paragraph(
        "Perintah pengujian dijalankan pada terminal dengan konfigurasi:<br/>"
        "<font face='Courier' size='8.5'><b>python main.py --limit 30 --backup</b></font>",
        body_style
    ))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("<b>4.2 Ringkasan Hasil Scraping Buku</b>", h2_style))
    stats_data = [
        [Paragraph("<b>Metrik</b>", body_style), Paragraph("<b>Nilai Hasil Eksekusi</b>", body_style)],
        [Paragraph("Total Buku Diambil", body_style), Paragraph("30 judul buku (Minimal 30 record terpenuhi)", body_style)],
        [Paragraph("Rentang Harga Buku", body_style), Paragraph("Rp 42.750 s/d Rp 171.000", body_style)],
        [Paragraph("Rata-rata Harga Buku", body_style), Paragraph("Rp 70.142", body_style)],
        [Paragraph("Distribusi Kategori", body_style), Paragraph("Nonfiksi: 16 judul (53.3%), Fiksi: 13 judul (43.3%), Puisi: 1 judul (3.3%)", body_style)],
        [Paragraph("Status Ketersediaan", body_style), Paragraph("100% Tersedia (In Stock)", body_style)],
        [Paragraph("Status Backup ZIP", body_style), Paragraph("Berhasil terkompresi ke backup/backup_data.zip", body_style)],
    ]
    t_stats = Table(stats_data, colWidths=[5 * cm, 11 * cm])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8EDF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stats)
    story.append(PageBreak())

    # =========================================================================
    # BAB V: KESIMPULAN & PENUTUP
    # =========================================================================
    story.append(Paragraph("BAB V: KESIMPULAN & PENUTUP", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1E3E62'), spaceAfter=8))

    story.append(Paragraph("<b>5.1 Kesimpulan</b>", h2_style))
    story.append(Paragraph(
        "Berdasarkan hasil perancangan, implementasi, dan pengujian aplikasi otomatisasi scraping katalog Penerbit Kakatua, "
        "dapat disimpulkan bahwa:<br/>"
        "1. Aplikasi berhasil mengumpulkan 30+ record buku secara otomatis dari website berbasis HTML murni (BeautifulSoup) tanpa melanggar batasan akses API.<br/>"
        "2. Regular Expressions berhasil memisahkan entitas penulis dan judul buku secara akurat serta membersihkan format mata uang rupiah.<br/>"
        "3. Semua persyaratan integrasi materi silabus (Chapters 9 s/d 13) telah terpenuhi 100%, mencakup Regex, file handling, struktur folder pathlib, kompresi ZIP, dan antarmuka CLI argparse.<br/>"
        "4. Pengorganisasian berkas dan pembuatan laporan statistik memberikan kemudahan pemantauan inventaris buku bagi pihak manajemen.",
        body_style
    ))

    story.append(Paragraph("<b>5.2 Saran & Pengembangan Lanjutan</b>", h2_style))
    story.append(Paragraph(
        "Pengembangan berikutnya dapat mengintegrasikan penjadwalan otomatis berkala (cron job / Windows Task Scheduler) "
        "serta notifikasi peringatan harga buku diskon melalui email atau Telegram bot.",
        body_style
    ))
    story.append(Spacer(1, 1.0 * cm))

    story.append(Paragraph("<b>LEMBAR PENGESAHAN MAHASISWA</b>", h2_style))
    ttd_data = [
        [Paragraph("Disusun Oleh:<br/><b>Anggota Kelompok 1</b><br/><br/><br/>( ____________________ )", body_style),
         Paragraph("Mengetahui / Menguji:<br/><b>Dosen Pengampu</b><br/><br/><br/>( <b>Anggi Muhammad Rifa’i, M.Kom</b> )", body_style)]
    ]
    t_ttd = Table(ttd_data, colWidths=[8 * cm, 8 * cm])
    t_ttd.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_ttd)

    # Build the document
    doc.build(story)
    print(f"[+] Laporan PDF resmi berhasil dibuat: {filename}")

if __name__ == "__main__":
    build_pdf()
