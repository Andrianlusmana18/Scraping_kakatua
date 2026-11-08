# Penerbit Kakatua - Online Book Catalog Scraper & Organizer

Proyek Otomatisasi Scraping Katalog Buku Digital untuk memenuhi **Ujian Tengah Semester (UTS) Mata Kuliah Automation Systems**, Semester Genap TA 2025/2026, Program Studi Teknik Informatika, Fakultas Teknik, **Universitas Pelita Bangsa**.

Dosen Pengampu: **Anggi Muhammad Rifa’i, M.Kom**  
Tema Proyek: **Online Book Catalog Organizer**  
Target Website: [Penerbit Kakatua](https://penerbitkakatua.com/shop/) (Murni HTML Scraping, Non-API)

---

## 📋 Daftar Isi
1. [Deskripsi Proyek](#-deskripsi-proyek)
2. [Fitur Utama & Pemenuhan Syarat UTS](#-fitur-utama--pemenuhan-syarat-uts)
3. [Integrasi Materi Silabus (Chapter 9 - 13)](#-integrasi-materi-silabus-chapter-9---13)
4. [Struktur Berkas Proyek](#-struktur-berkas-proyek)
5. [Instalasi & Persiapan](#-instalasi--persiapan)
6. [Panduan Penggunaan (CLI)](#-panduan-penggunaan-cli)
7. [Contoh Output Program](#-contoh-output-program)
8. [Panduan Demonstrasi & Presentasi UTS](#-panduan-demonstrasi--presentasi-uts)

---

## 📖 Deskripsi Proyek
Penerbit Kakatua adalah penerbit buku independen yang menyediakan karya sastra klasik dunia, filsafat, dan humaniora. Proyek ini mengotomatisasi pengambilan data buku dari halaman katalog web, mengekstrak dan memvalidasi informasi menggunakan Regular Expressions, menyimpan dataset terstruktur ke CSV, menyusun laporan ringkasan otomatis, serta mengompresi hasil ke dalam arsip ZIP cadangan melalui Command Line Interface (CLI).

---

## ✨ Fitur Utama & Pemenuhan Syarat UTS

| No | Persyaratan Teknis UTS | Status | Keterangan Implementasi |
|:--:|---|:--:|---|
| 1 | Minimal 30 record dari sumber | ✅ Terpenuhi | Mengambil 30+ data buku lengkap dengan judul, pengarang, harga, diskon, stok, dan URL. |
| 2 | Sedikitnya dua pola Regular Expressions | ✅ Terpenuhi | **Pola 1**: Pembersihan & konversi harga `r'Rp\s?([\d\.]+)'`<br/>**Pola 2**: Pemisahan Penulis & Judul `r'^(.*?)\s*(?:[–—]\|\s-\s)\s*(.*)$'`<br/>**Pola 3**: Ekstraksi ISBN/QRCBN `r'(?:ISBN\|QRCBN)\s*[:\-]?\s*([0-9Xx\-]+)'` |
| 3 | Menyimpan data format `.txt` atau `.csv` | ✅ Terpenuhi | Tersimpan ke `output/hasil_scraping.csv`, `output/laporan.txt`, dan `data/raw_data.txt`. |
| 4 | Folder otomatis dibuat via `pathlib` | ✅ Terpenuhi | Fungsi `siapkan_direktori_kerja()` menggunakan `pathlib.Path.mkdir(parents=True, exist_ok=True)`. |
| 5 | Backup hasil pemrosesan format `.zip` | ✅ Terpenuhi | Otomatis dibuat di `backup/backup_data.zip` via modul `zipfile`. |
| 6 | Minimal tiga argumen CLI (`argparse`) | ✅ Terpenuhi | Tersedia `--url`, `--limit`, `--keyword`, `--category`, `--output`, `--backup`, dan `--detail`. |
| 7 | Penanganan kegagalan (Error Handling) | ✅ Terpenuhi | Menangani `requests.exceptions.ConnectionError`, `Timeout`, data kosong, dan penanganan path aman. |
| 8 | Ringkasan pemrosesan di terminal | ✅ Terpenuhi | Menampilkan statistik total data, rentang harga, path file keluaran, dan cuplikan tabel data. |

---

## 🧠 Integrasi Materi Silabus (Chapter 9 - 13)
Proyek ini mengacu pada buku pegangan *Automate the Boring Stuff with Python*:

- **Chapter 9: Regular Expressions**  
  Digunakan untuk mengekstrak angka harga numerik dari teks berformat Rupiah, menghitung persentase diskon, dan memisahkan pengarang serta judul buku secara akurat.
- **Chapter 10: Reading and Writing Files**  
  Membaca dan menulis file log mentah (`data/raw_data.txt`), menyimpan dataset tabel menggunakan `csv.DictWriter`, serta menulis laporan ringkasan teks ber-encoding UTF-8.
- **Chapter 11: Organizing Files**  
  Manajemen struktur folder secara otomatis dengan `pathlib.Path` dan pemaketan arsip cadangan terkompresi menggunakan `zipfile.ZipFile(..., compression=zipfile.ZIP_DEFLATED)`.
- **Chapter 12: Command Line Programs**  
  Implementasi antarmuka terminal yang fleksibel dengan modul `argparse`, dilengkapi dokumentasi bantuan (`--help`) dan nilai bawaan (*default values*).
- **Chapter 13: Web Scraping**  
  Pengambilan data murni berbasis dokumen HTML web menggunakan `requests` dan `BeautifulSoup` (`html.parser`), mendukung paginasi multi-halaman WooCommerce (`/shop/page/N/`) tanpa menggunakan API pihak ketiga.

---

## 📁 Struktur Berkas Proyek

```text
c:/kumpulan projek/scraping kakatua/
│
├── main.py                     # Script utama aplikasi otomasi CLI
├── generate_pdf_report.py      # Script pembuat dokumen PDF laporan resmi UTS
├── requirements.txt            # Daftar dependensi modul Python
├── README.md                   # Petunjuk instalasi & dokumentasi program
│
├── data/
│   └── raw_data.txt            # Catatan mentah teks hasil proses scraping
│
├── output/
│   ├── hasil_scraping.csv      # Dataset terstruktur (30+ data buku)
│   └── laporan.txt             # Laporan eksekutif statistik harga & kategori
│
├── backup/
│   └── backup_data.zip         # File arsip cadangan (ZIP)
│
└── dokumentasi/
    ├── laporan_uts.pdf         # Laporan resmi UTS format PDF siap kumpul
    └── LAPORAN_UTS.md          # Dokumen laporan versi Markdown
```

---

## 🚀 Instalasi & Persiapan

### 1. Prasyarat
Pastikan Python 3.8 atau yang lebih baru sudah terpasang di sistem operasi Anda. Periksa dengan perintah:
```bash
python --version
```

### 2. Pasang Dependensi
Buka terminal / PowerShell di direktori proyek, lalu jalankan perintah:
```bash
pip install -r requirements.txt
```

---

## 💻 Panduan Penggunaan (CLI)

### 1. Menjalankan Scraping Standar (Minimal 30 Data & Backup ZIP)
```bash
python main.py --limit 30 --backup
```

### 2. Mengambil Lebih Banyak Data (Contoh: 50 Buku)
```bash
python main.py --limit 50
```

### 3. Menyaring Berdasarkan Kata Kunci (Keyword)
Mencari buku yang berkaitan dengan kata kunci tertentu (misal: "filsafat" atau nama penulis):
```bash
python main.py --keyword "filsafat" --limit 20
```

### 4. Menyaring Berdasarkan Kategori
```bash
python main.py --category "Nonfiksi" --limit 30
```

### 5. Mengubah Lokasi File Output CSV
```bash
python main.py --output "output/katalog_pilihan.csv" --limit 30
```

### 6. Menjalankan Mode Detail (ISBN & Halaman dari Laman Produk)
```bash
python main.py --limit 30 --detail
```

### 7. Melihat Panduan Bantuan Lengkap Argumen CLI
```bash
python main.py --help
```

---

## 📊 Contoh Output Program

### Tampilan Terminal:
```text
======================================================================
                  RINGKASAN PEMROSESAN APLIKASI
======================================================================
[*] Total Record Terkumpul : 30 buku
[*] Rentang Harga Buku      : Rp 42,750 s/d Rp 171,000
[*] Estimasi Rata-rata      : Rp 70,142
----------------------------------------------------------------------
[+] File Dataset CSV       : output/hasil_scraping.csv
[+] File Laporan TXT       : output/laporan.txt
[+] File Raw Scraping      : data/raw_data.txt
[+] File Backup Arsip ZIP  : backup/backup_data.zip (3.62 KB)
======================================================================

Cuplikan 5 Data Pertama yang Berhasil Dikumpulkan:
No  | Kategori     | Penulis            | Judul                     | Harga       
---------------------------------------------------------------------------
1   | Nonfiksi     | Edward W. Said     | Representasi Intelektual  | Rp 66,500   
2   | Nonfiksi     | Bertrand Russell   | Persoalan-Persoalan Fi..  | Rp 66,500   
3   | Nonfiksi     | Nawal El Saadawi   | Perempuan Arab dalam S..  | Rp 90,250   
4   | Fiksi        | Virginia Woolf     | Orlando                   | Rp 90,250   
5   | Fiksi        | Stefan Zweig       | Pemain Catur              | Rp 42,750   
===========================================================================
[SUCCESS] Otomatisasi Scraping & Pengorganisasian File Selesai!
```

---

## 🎤 Panduan Demonstrasi & Presentasi UTS (15 Menit)

Saat presentasi di hadapan dosen pengampu (**Anggi Muhammad Rifa'i, M.Kom**), bagi alokasi waktu sebagai berikut:

1. **5 Menit - Penjelasan Masalah dan Alur Solusi**:
   - Jelaskan latar belakang mengapa scraping katalog Penerbit Kakatua penting (pengorganisasian data buku secara otomatis).
   - Tunjukkan slide/diagram alur kerja dari pembacaan CLI, HTTP requests, parsing HTML, Regex, hingga file saving dan ZIP backup.
   - Jelaskan integrasi Chapters 9-13 pada kode.
2. **7 Menit - Demonstrasi Langsung (Live Demo)**:
   - Buka terminal dan jalankan:
     ```bash
     python main.py --limit 30 --backup
     ```
   - Tunjukkan proses scraping multi-halaman yang berjalan.
   - Buka file `output/hasil_scraping.csv` di Excel/VS Code untuk memperlihatkan data terstruktur minimal 30 baris.
   - Buka file `output/laporan.txt` untuk memperlihatkan analisis ringkasan dan distribusi kategori.
   - Buka file `backup/backup_data.zip` untuk menunjukkan fungsi kompresi file cadangan.
   - Tunjukkan opsi fleksibel CLI lainnya, misalnya pencarian filter:
     ```bash
     python main.py --keyword "Sartre"
     ```
3. **3 Menit - Tanya Jawab Individu**:
   - Kuasai fungsi Regular Expressions di `main.py` (`RE_HARGA_RP` dan `RE_PENULIS_JUDUL`).
   - Pahami perbedaan metode HTML scraping (`BeautifulSoup`) dibanding API.
   - Pahami modul `pathlib` dan `zipfile` yang digunakan.

---
*Sukses untuk Ujian Tengah Semester (UTS) Automation Systems!*
