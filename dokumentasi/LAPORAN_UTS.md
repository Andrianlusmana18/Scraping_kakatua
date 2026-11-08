# LAPORAN PROJECT UJIAN TENGAH SEMESTER (UTS)
## MATA KULIAH: AUTOMATION SYSTEMS (SEMESTER GENAP TA 2025/2026)
### PROGRAM STUDI TEKNIK INFORMATIKA - FAKULTAS TEKNIK - UNIVERSITAS PELITA BANGSA

---

* **Dosen Pengampu**: Anggi Muhammad Rifa’i, M.Kom  
* **Tema Proyek**: Online Book Catalog Organizer  
* **Objek / Sumber Data**: Katalog Buku Penerbit Kakatua (https://penerbitkakatua.com/shop/)  
* **Metode Pengambilan**: Murni HTML Scraping (Non-API)  
* **Kelompok**: Kelompok 01  
* **Anggota Kelompok**:
  1. `[Nama Mahasiswa 1]` - `[NIM 1]`
  2. `[Nama Mahasiswa 2]` - `[NIM 2]`
  3. `[Nama Mahasiswa 3]` - `[NIM 3]`

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang Masalah
Penerbit Kakatua merupakan salah satu penerbit independen di Indonesia yang berfokus pada buku-buku sastra klasik dunia, filsafat, nonfiksi kritis, dan humaniora. Data katalog buku yang disajikan di situs web resminya (`https://penerbitkakatua.com/shop/`) memiliki nilai informasi penting baik bagi pembaca, akademisi, maupun periset literatur.

Namun, pengumpulan informasi katalog, pencatatan harga diskon, pemantauan stok, dan rekapitulasi data masih kerap dilakukan secara manual melalui peramban web satu per satu. Kegiatan manual ini memakan waktu yang cukup besar dan rentan terhadap kesalahan manusia (*human error*). Melalui proyek ini, dibangun sebuah aplikasi otomatisasi berbasis Python yang mengintegrasikan teknik *web scraping* berbasis HTML parsing, ekstraksi pola dengan ekspresi reguler (*regex*), pengorganisasian file otomatis, serta penyediaan antarmuka baris perintah (*CLI*).

### 1.2 Rumusan Masalah
1. Bagaimana mengotomatisasi pengambilan data buku (minimal 30 judul) dari situs Penerbit Kakatua menggunakan teknik HTML scraping tanpa API?
2. Bagaimana memisahkan nama penulis, judul buku, dan membersihkan format harga mata uang menggunakan Regular Expressions (*Chapter 9*)?
3. Bagaimana mengorganisasikan folder output, menyimpan dataset CSV, membuat laporan ringkasan, dan memaketkan cadangan arsip ZIP secara otomatis (*Chapter 10 & 11*)?
4. Bagaimana merancang program agar fleksibel dan dapat dikendalikan dengan argumen baris perintah CLI (*Chapter 12*)?

### 1.3 Tujuan Proyek
1. Mengimplementasikan scraper berbasis pustaka `requests` dan `BeautifulSoup` yang mematuhi etika scraping dan mengambil data langsung dari dokumen HTML.
2. Menerapkan minimal dua pola Regular Expressions untuk ekstraksi harga angka Rupiah dan pemisahan pengarang-judul.
3. Menghasilkan dataset terstruktur dalam format CSV (`output/hasil_scraping.csv`) dan laporan ringkasan TXT (`output/laporan.txt`).
4. Menyediakan fitur pencadangan arsip otomatis (`backup/backup_data.zip`).
5. Menyediakan antarmuka CLI yang interaktif dan ramah pengguna dengan penanganan kesalahan (*error handling*) yang kuat.

---

## BAB II: INTEGRASI MATERI WAJIB (CHAPTER 9 - 13)

Sesuai silabus buku acuan *Automate the Boring Stuff with Python*, berikut adalah integrasi materi wajib yang diimplementasikan:

| Chapter | Materi Wajib | Implementasi Nyata pada Kode Program |
|---|---|---|
| **9** | **Regular Expressions** | Digunakan pada fungsi `bersihkan_harga()` dengan pola `r"Rp\s?([\d\.]+)"` untuk mengambil angka harga murni dan `re.sub(r"\D", "", ...)` untuk membersihkan pemisah ribuan titik. Serta fungsi `pisahkan_penulis_dan_judul()` dengan pola `r"^(.*?)\s*(?:[–—]\|\s-\s)\s*(.*)$"` untuk memisahkan pengarang dan judul tanpa memotong nama gabungan seperti *Jean-Paul*. |
| **10** | **Reading & Writing Files** | Menyimpan log data mentah ke `data/raw_data.txt`, dataset terstruktur ke `output/hasil_scraping.csv` menggunakan modul `csv.DictWriter`, dan laporan analisis teks ke `output/laporan.txt` menggunakan encoding UTF-8. |
| **11** | **Organizing Files** | Pembuatan direktori kerja (`data/`, `output/`, `backup/`, `dokumentasi/`) secara otomatis menggunakan objek `pathlib.Path.mkdir(parents=True, exist_ok=True)` dan pengarsipan hasil ke `backup/backup_data.zip` menggunakan `zipfile.ZipFile(..., compression=zipfile.ZIP_DEFLATED)`. |
| **12** | **Command Line Programs** | Membangun antarmuka terminal interaktif menggunakan `argparse.ArgumentParser` dengan argumen: `--url`, `--limit`, `--keyword`, `--category`, `--output`, `--backup`, dan `--detail`. |
| **13** | **Web Scraping** | Mengambil halaman web secara bertahap (paginasi multi-halaman WooCommerce `/shop/page/N/`) menggunakan `requests.get()` dengan `User-Agent` yang valid dan mengekstrak elemen DOM menggunakan parser HTML `BeautifulSoup(html, 'html.parser')`. |

---

## BAB III: METODOLOGI & ARSITEKTUR SISTEM

### 3.1 Alur Program (Workflow)
1. **Input**: Pengguna mengeksekusi perintah CLI pada terminal (misalnya `python main.py --limit 30 --backup`).
2. **Inisialisasi**: Modul `pathlib` mendeteksi dan membuat struktur folder yang dibutuhkan.
3. **Paginasi & HTTP Request**: Modul `requests` mengambil halaman HTML katalog secara berurutan.
4. **HTML Parsing**: `BeautifulSoup` membedah tag HTML `.product_item` untuk menemukan judul, link, harga, status ketersediaan, dan kategori.
5. **Pembersihan Data (Regex)**: Memisahkan penulis dan judul serta mengonversi harga ke format numerik integer.
6. **Penyimpanan**: Dataset disimpan ke format CSV dan laporan analisis diekspor ke TXT.
7. **Pencadangan**: File CSV dan TXT dikompresi ke dalam arsip `backup/backup_data.zip`.
8. **Output Terminal**: Menampilkan ringkasan eksekutif dan cuplikan 5 data buku pertama di layar terminal.

### 3.2 Struktur Pengumpulan Berkas
```
UTS_Project_Kelompok_01/
|-- main.py                # Script utama otomasi Python
|-- requirements.txt       # Daftar pustaka yang dibutuhkan
|-- README.md              # Dokumentasi lengkap petunjuk penggunaan
|-- data/
|   +-- raw_data.txt       # Log teks mentah hasil scraping
|-- output/
|   |-- hasil_scraping.csv # File dataset hasil scraping (minimal 30 data)
|   +-- laporan.txt        # Laporan ringkasan analisis data
|-- backup/
|   +-- backup_data.zip    # File cadangan ZIP hasil kompresi
+-- dokumentasi/
    |-- laporan_uts.pdf    # Laporan resmi UTS format PDF
    +-- LAPORAN_UTS.md     # Dokumen markdown laporan UTS
```

### 3.3 Penanganan Kesalahan (Error Handling)
* **Koneksi Jaringan**: Menangani `requests.exceptions.ConnectionError` dan `Timeout` dengan pesan informatif agar program tidak terhenti secara mendadak.
* **Data Kosong**: Jika kata kunci pencarian (`--keyword`) tidak menghasilkan buku, aplikasi menampilkan peringatan ramah tanpa crash.
* **Path & Folder**: Penggunaan `pathlib` memastikan direktori selalu terbuat sebelum penulisan berkas dilakukan, mencegah `FileNotFoundError`.

---

## BAB IV: HASIL PENGUJIAN DAN ANALISIS DATA

### 4.1 Eksekusi Perintah
```bash
python main.py --limit 30 --backup
```

### 4.2 Analisis Statistik Data Buku
Dari 30 record buku yang berhasil dikumpulkan secara otomatis dari Penerbit Kakatua:
* **Total Buku**: 30 judul
* **Harga Terendah**: Rp 42.750 (Buku *Chairil Anwar - Aku Mau Hidup Seribu Tahun Lagi* dan *Stefan Zweig - Pemain Catur*)
* **Harga Tertinggi**: Rp 171.000
* **Harga Rata-rata**: Rp 70.142
* **Distribusi Kategori**:
  * Nonfiksi: 16 judul (53,3%)
  * Fiksi: 13 judul (43,3%)
  * Puisi: 1 judul (3,3%)
* **Status Stok**: 100% Tersedia (*In Stock*)
* **Status Arsip Cadangan**: Berhasil dikompresi ke `backup/backup_data.zip` (ukuran: ~3.6 KB).

---

## BAB V: KESIMPULAN

1. Aplikasi otomasi scraping katalog Penerbit Kakatua berhasil dibangun dengan mengintegrasikan seluruh materi wajib (Chapters 9 sampai 13).
2. Scraping dilakukan murni berbasis struktur HTML tanpa menggunakan API, dan mematuhi etika scraping dengan jeda waktu (*polite delay*).
3. Penggunaan Regular Expressions memberikan hasil pembersihan dan pemisahan data yang presisi tinggi.
4. Berkas pengumpulan telah tersusun lengkap sesuai standar format penilaian UTS.

---
*Laporan ini disusun untuk memenuhi Ujian Tengah Semester (UTS) Mata Kuliah Automation Systems TA 2025/2026.*
