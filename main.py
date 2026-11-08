#!/usr/bin/env python3
"""
=============================================================================
UJIAN TENGAH SEMESTER (UTS) - AUTOMATION SYSTEMS
PROGRAM STUDI TEKNIK INFORMATIKA - UNIVERSITAS PELITA BANGSA

Judul Proyek : Online Book Catalog Scraper & Organizer (Penerbit Kakatua)
Sumber Data  : https://penerbitkakatua.com/shop/
Metode       : HTML Web Scraping (BeautifulSoup & Requests) - Murni HTML (Non-API)

Integrasi Materi Otomatisasi (Automate the Boring Stuff with Python):
- Chapter 9  : Regular Expressions (Ekstraksi harga, pemisahan Penulis & Judul, ISBN/QRCBN, Halaman)
- Chapter 10 : Reading and Writing Files (Membaca/menyimpan raw data, CSV, dan laporan ringkasan)
- Chapter 11 : Organizing Files (Pengelolaan direktori otomatis dengan pathlib dan backup arsip ZIP)
- Chapter 12 : Command Line Programs (Antarmuka CLI interaktif menggunakan argparse)
- Chapter 13 : Web Scraping (Scraping multi-halaman HTML menggunakan requests dan BeautifulSoup)
=============================================================================
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, List, Optional
import zipfile

import requests
from bs4 import BeautifulSoup

# =============================================================================
# KONFIGURASI GLOBAL & DEFAULT
# =============================================================================
DEFAULT_TARGET_URL = "https://penerbitkakatua.com/shop/"
DEFAULT_LIMIT = 30
DEFAULT_OUTPUT_CSV = Path("output/hasil_scraping.csv")
DEFAULT_RAW_DATA = Path("data/raw_data.txt")
DEFAULT_SUMMARY_TXT = Path("output/laporan.txt")
DEFAULT_BACKUP_ZIP = Path("backup/backup_data.zip")

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
}

# =============================================================================
# CHAPTER 9: REGULAR EXPRESSIONS (Pembersihan, Ekstraksi & Validasi Pola)
# =============================================================================
# Pola Regex 1: Ekstraksi angka harga Rupiah (contoh: 'Rp70.000' -> ['70.000'])
RE_HARGA_RP = re.compile(r"Rp\s?([\d\.]+)", re.IGNORECASE)

# Pola Regex 2: Pemisahan Nama Penulis dan Judul Buku dari format katalog 'Penulis - Judul'
# Mendukung en-dash (–), em-dash (—), atau tanda hubung berkasi spasi ( - ) agar nama seperti Jean-Paul tidak terpotong
RE_PENULIS_JUDUL = re.compile(r"^(.*?)\s*(?:[–—]|\s-\s)\s*(.*)$")

# Pola Regex 3: Ekstraksi kode ISBN atau QRCBN dari teks deskripsi buku
RE_ISBN_QRCBN = re.compile(
    r"(?:ISBN|QRCBN)\s*[:\-]?\s*([0-9Xx\-]+)", re.IGNORECASE
)

# Pola Regex 4: Ekstraksi informasi tebal halaman buku (contoh: 'Halaman: vi + 141')
RE_HALAMAN = re.compile(r"Halaman\s*[:\-]?\s*([^\n\r<]+)", re.IGNORECASE)

# Pola Regex 5: Ekstraksi persentase diskon (contoh: '-5%' -> '5%')
RE_DISKON = re.compile(r"(\d+)%")


def bersihkan_harga(teks_harga: str) -> tuple[int, int, str]:
    """Menggunakan Regular Expressions (Chapter 9) untuk membersihkan format harga

    dan menentukan harga diskon, harga asli, serta persentase potongan.
    """
    if not teks_harga:
        return 0, 0, "0%"

    cocok_harga = RE_HARGA_RP.findall(teks_harga)
    angka_bersih = []
    for item in cocok_harga:
        # Hapus titik pemisah ribuan
        angka_str = re.sub(r"\D", "", item)
        if angka_str.isdigit():
            angka_bersih.append(int(angka_str))

    if len(angka_bersih) >= 2:
        # Format WooCommerce saat diskon: <del>Rp Asli</del> <ins>Rp Diskon</ins>
        harga_asli = max(angka_bersih)
        harga_diskon = min(angka_bersih)
        persen = (
            round(((harga_asli - harga_diskon) / harga_asli) * 100)
            if harga_asli > 0
            else 0
        )
        return harga_diskon, harga_asli, f"{persen}%"
    elif len(angka_bersih) == 1:
        harga = angka_bersih[0]
        return harga, harga, "0%"
    else:
        return 0, 0, "0%"


def pisahkan_penulis_dan_judul(teks_judul: str) -> tuple[str, str]:
    """Menggunakan Regular Expressions (Chapter 9) untuk memisahkan nama penulis

    dan judul buku yang lazim digabungkan dengan tanda strip (- / – / —).
    """
    teks_judul = teks_judul.strip()
    match = RE_PENULIS_JUDUL.match(teks_judul)
    if match:
        penulis = match.group(1).strip()
        judul = match.group(2).strip()
        return penulis, judul
    return "-", teks_judul


def ekstrak_detail_buku(html_content: str) -> tuple[str, str]:
    """Menggunakan Regular Expressions (Chapter 9) untuk mengekstrak ISBN/QRCBN

    dan jumlah halaman dari HTML tab deskripsi halaman produk.
    """
    isbn = "-"
    halaman = "-"

    match_isbn = RE_ISBN_QRCBN.search(html_content)
    if match_isbn:
        isbn = match_isbn.group(1).strip()

    match_hal = RE_HALAMAN.search(html_content)
    if match_hal:
        halaman = match_hal.group(1).strip()

    return isbn, halaman


# =============================================================================
# CHAPTER 11: ORGANIZING FILES (Pengelolaan Folder & Backup ZIP)
# =============================================================================
def siapkan_direktori_kerja() -> None:
    """Membuat struktur folder kerja yang dibutuhkan secara otomatis menggunakan pathlib (Chapter 11 & 10)."""
    folders = [Path("data"), Path("output"), Path("backup"), Path("dokumentasi")]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def buat_arsip_backup(
    file_list: List[Path], zip_path: Path = DEFAULT_BACKUP_ZIP
) -> Optional[Path]:
    """Membuat arsip cadangan (ZIP file) dari hasil pemrosesan (Chapter 11).

    Menyimpan file hasil ke dalam direktori backup/.
    """
    try:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(
            zip_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zipf:
            for file_path in file_list:
                if file_path.exists():
                    zipf.write(file_path, arcname=file_path.name)
        return zip_path
    except Exception as e:
        print(f"[!] Gagal membuat arsip backup ZIP: {e}")
        return None


# =============================================================================
# CHAPTER 13: WEB SCRAPING (Mengambil data website menggunakan BeautifulSoup & Requests)
# =============================================================================
def ambil_halaman_html(
    url: str, timeout: int = 15
) -> Optional[BeautifulSoup]:
    """Mengambil halaman web berbasis HTTP GET dan mem-parsing dokumen HTML

    menggunakan BeautifulSoup (Murni HTML parser, BUKAN API).
    """
    try:
        response = requests.get(
            url, headers=REQUEST_HEADERS, timeout=timeout
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Koneksi ke {url} mengalami batas waktu (Timeout).")
    except requests.exceptions.ConnectionError:
        print(
            f"[ERROR] Gagal terhubung ke {url}. Silakan periksa koneksi internet Anda."
        )
    except requests.exceptions.HTTPError as err:
        print(f"[ERROR] Respons HTTP Error: {err}")
    except Exception as e:
        print(f"[ERROR] Terjadi kegagalan saat mengambil halaman {url}: {e}")
    return None


def ambil_detail_produk(product_url: str) -> tuple[str, str]:
    """Mengunjungi URL detail produk untuk mengekstrak ISBN/QRCBN dan tebal halaman."""
    try:
        soup = ambil_halaman_html(product_url, timeout=10)
        if not soup:
            return "-", "-"
        desc_panel = soup.select_one(
            "#tab-description, .woocommerce-Tabs-panel--description, .woocommerce-product-details__short-description"
        )
        if desc_panel:
            text_desc = desc_panel.get_text(separator=" ", strip=True)
            return ekstrak_detail_buku(text_desc)
    except Exception:
        pass
    return "-", "-"


def scrape_katalog_kakatua(
    base_url: str = DEFAULT_TARGET_URL,
    limit: int = DEFAULT_LIMIT,
    keyword: Optional[str] = None,
    category_filter: Optional[str] = None,
    fetch_details: bool = False,
    raw_file_path: Path = DEFAULT_RAW_DATA,
) -> List[Dict[str, Any]]:
    """Fungsi utama untuk melakukan scraping katalog buku Penerbit Kakatua

    dengan dukungan paginasi, ekstraksi Regex, dan filter kata kunci.
    """
    print(f"\n[*] Memulai proses Web Scraping:")
    print(f"    - URL Sumber : {base_url}")
    print(f"    - Target Data: Minimal {limit} buku")
    if keyword:
        print(f"    - Filter Kata Kunci: '{keyword}'")
    if category_filter:
        print(f"    - Filter Kategori  : '{category_filter}'")

    buku_terkumpul: List[Dict[str, Any]] = []
    page = 1
    raw_text_logs = []

    while len(buku_terkumpul) < limit:
        # Menentukan URL paginasi WooCommerce
        if page == 1:
            page_url = (
                base_url
                if base_url.endswith("/")
                else f"{base_url}/"
            )
        else:
            clean_base = base_url.rstrip("/")
            page_url = f"{clean_base}/page/{page}/"

        print(
            f"[*] Mengunduh Halaman {page} ({page_url})...",
            end=" ",
            flush=True,
        )
        soup = ambil_halaman_html(page_url)
        if not soup:
            print("[Gagal]")
            break

        # Selector HTML WooCommerce pada template The Retailer milik Penerbit Kakatua
        item_produk = soup.select(".product_item, li.product")
        if not item_produk:
            print("[Tidak ada produk lagi]")
            break

        print(f"[Ditemukan {len(item_produk)} produk]")
        raw_text_logs.append(
            f"=== HALAMAN {page} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n"
        )

        for item in item_produk:
            if len(buku_terkumpul) >= limit:
                break

            # 1. Judul & Tautan
            title_el = item.select_one(".product-title a") or item.select_one(
                "h2.woocommerce-loop-product__title, h3 a"
            )
            raw_title = title_el.get_text(strip=True) if title_el else "-"
            product_url = (
                title_el.get("href")
                if title_el and title_el.has_attr("href")
                else "-"
            )

            # 2. Kategori
            cat_el = item.select_one("h3 a")
            kategori = cat_el.get_text(strip=True) if cat_el else "-"

            # 3. Regular Expression: Pemisahan Penulis & Judul
            penulis, judul = pisahkan_penulis_dan_judul(raw_title)

            # 4. Harga & Diskon (Regular Expression)
            price_el = item.select_one(".price")
            raw_price_str = (
                price_el.get_text(" ", strip=True) if price_el else ""
            )
            harga_diskon, harga_asli, diskon_persen = bersihkan_harga(
                raw_price_str
            )

            # 5. Status Stok
            classes = item.get("class", [])
            if "instock" in classes:
                status_stok = "Tersedia"
            elif "outofstock" in classes:
                status_stok = "Habis"
            else:
                status_stok = "Tersedia"

            # 6. Filter Keyword jika diberikan oleh pengguna
            if keyword:
                keyword_lower = keyword.lower()
                if (
                    keyword_lower not in raw_title.lower()
                    and keyword_lower not in penulis.lower()
                    and keyword_lower not in kategori.lower()
                ):
                    continue

            # 7. Filter Kategori jika diberikan
            if (
                category_filter
                and category_filter.lower() not in kategori.lower()
            ):
                continue

            # 8. Opsional: Detail Tambahan (ISBN, Tebal Halaman)
            isbn, halaman = "-", "-"
            if fetch_details and product_url != "-":
                isbn, halaman = ambil_detail_produk(product_url)
                time.sleep(0.3)  # Jeda sopan (polite delay) agar server ramah

            record = {
                "No": len(buku_terkumpul) + 1,
                "Kategori": kategori,
                "Penulis": penulis,
                "Judul": judul,
                "Harga_Diskon_Rp": harga_diskon,
                "Harga_Asli_Rp": harga_asli,
                "Diskon": diskon_persen,
                "Status_Stok": status_stok,
                "ISBN_QRCBN": isbn,
                "Halaman": halaman,
                "URL": product_url,
            }
            buku_terkumpul.append(record)
            raw_text_logs.append(
                f"{record['No']}. [{kategori}] {penulis} - {judul} | Rp {harga_diskon} | {status_stok}\n"
            )

        page += 1
        time.sleep(0.5)  # Jeda antar halaman

    # CHAPTER 10: Reading & Writing Files (Menyimpan data mentah)
    try:
        raw_file_path.parent.mkdir(parents=True, exist_ok=True)
        raw_file_path.write_text(
            "".join(raw_text_logs), encoding="utf-8"
        )
    except Exception as e:
        print(f"[!] Gagal menulis file raw_data.txt: {e}")

    return buku_terkumpul


# =============================================================================
# CHAPTER 10: READING & WRITING FILES (Penyimpanan CSV & Pembuatan Laporan TXT)
# =============================================================================
def simpan_ke_csv(
    data: List[Dict[str, Any]], target_file: Path = DEFAULT_OUTPUT_CSV
) -> bool:
    """Menyimpan dataset hasil scraping ke dalam format CSV menggunakan modul csv (Chapter 10)."""
    if not data:
        print("[!] Data kosong, tidak ada baris yang disimpan ke CSV.")
        return False

    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(data[0].keys())

        with open(
            target_file, "w", newline="", encoding="utf-8-sig"
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return True
    except Exception as e:
        print(f"[ERROR] Gagal menulis ke file CSV {target_file}: {e}")
        return False


def buat_laporan_ringkasan(
    data: List[Dict[str, Any]],
    target_file: Path = DEFAULT_SUMMARY_TXT,
    url_target: str = DEFAULT_TARGET_URL,
    filter_keyword: Optional[str] = None,
) -> bool:
    """Membuat laporan ringkasan pemrosesan dan statistik data dalam format TXT (Chapter 10)."""
    if not data:
        return False

    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)

        total_buku = len(data)
        daftar_harga = [
            b["Harga_Diskon_Rp"]
            for b in data
            if b["Harga_Diskon_Rp"] > 0
        ]
        harga_terendah = min(daftar_harga) if daftar_harga else 0
        harga_tertinggi = max(daftar_harga) if daftar_harga else 0
        rata_rata = (
            sum(daftar_harga) / len(daftar_harga) if daftar_harga else 0
        )

        # Hitung statistik per kategori
        kategori_count: Dict[str, int] = {}
        for b in data:
            kat = b["Kategori"]
            kategori_count[kat] = kategori_count.get(kat, 0) + 1

        buku_tersedia = sum(
            1 for b in data if b["Status_Stok"] == "Tersedia"
        )
        buku_habis = sum(1 for b in data if b["Status_Stok"] == "Habis")

        laporan_text = f"""================================================================================
LAPORAN RINGKASAN HASIL WEB SCRAPING - PENERBIT KAKATUA
Tugas UTS Automation Systems - Teknik Informatika Universitas Pelita Bangsa
================================================================================
Waktu Eksekusi    : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} WIB
Sumber Data       : {url_target}
Kata Kunci Filter : {filter_keyword if filter_keyword else '(Semua Buku)'}
Total Data Buku   : {total_buku} judul

STATISTIK HARGA:
- Harga Terendah  : Rp {harga_terendah:,.0f}
- Harga Tertinggi : Rp {harga_tertinggi:,.0f}
- Harga Rata-rata : Rp {rata_rata:,.0f}

STATISTIK KETERSEDIAAN STOK:
- Buku Tersedia   : {buku_tersedia} judul
- Buku Habis      : {buku_habis} judul

DISTRIBUSI KATEGORI:
"""
        for kat, jml in sorted(
            kategori_count.items(), key=lambda x: x[1], reverse=True
        ):
            laporan_text += (
                f"- {kat:<25}: {jml:>3} judul ({jml/total_buku*100:.1f}%)\n"
            )

        laporan_text += """
================================================================================
SAMPLE DATA BUKU HASIL SCRAPING (10 Data Pertama):
================================================================================
"""
        for item in data[:10]:
            laporan_text += f"[{item['No']:02d}] {item['Penulis']} - {item['Judul']}\n"
            laporan_text += f"     Kategori: {item['Kategori']} | Harga: Rp {item['Harga_Diskon_Rp']:,} (Diskon: {item['Diskon']}) | Stok: {item['Status_Stok']}\n"
            laporan_text += f"     Tautan  : {item['URL']}\n\n"

        target_file.write_text(laporan_text, encoding="utf-8")
        return True
    except Exception as e:
        print(f"[ERROR] Gagal membuat file laporan ringkasan: {e}")
        return False


# =============================================================================
# RINGKASAN TERMINAL (Tampilan Elegan CLI)
# =============================================================================
def tampilkan_ringkasan_terminal(
    data: List[Dict[str, Any]],
    csv_path: Path,
    summary_path: Path,
    zip_path: Optional[Path],
) -> None:
    """Menampilkan ringkasan pemrosesan pada terminal sesuai Persyaratan Teknis No. 8."""
    print("\n" + "=" * 70)
    print(" " * 18 + "RINGKASAN PEMROSESAN APLIKASI")
    print("=" * 70)

    total = len(data)
    print(f"[*] Total Record Terkumpul : {total} buku")

    if data:
        daftar_harga = [
            b["Harga_Diskon_Rp"]
            for b in data
            if b["Harga_Diskon_Rp"] > 0
        ]
        min_p = min(daftar_harga) if daftar_harga else 0
        max_p = max(daftar_harga) if daftar_harga else 0
        avg_p = sum(daftar_harga) / len(daftar_harga) if daftar_harga else 0

        print(
            f"[*] Rentang Harga Buku      : Rp {min_p:,.0f} s/d Rp {max_p:,.0f}"
        )
        print(f"[*] Estimasi Rata-rata      : Rp {avg_p:,.0f}")

    print("-" * 70)
    print(f"[+] File Dataset CSV       : {csv_path.resolve()}")
    print(f"[+] File Laporan TXT       : {summary_path.resolve()}")
    print(f"[+] File Raw Scraping      : {DEFAULT_RAW_DATA.resolve()}")
    if zip_path and zip_path.exists():
        print(
            f"[+] File Backup Arsip ZIP  : {zip_path.resolve()} ({zip_path.stat().st_size / 1024:.2f} KB)"
        )
    print("=" * 70)

    # Tampilkan cuplikan 5 data pertama
    print("\nCuplikan 5 Data Pertama yang Berhasil Dikumpulkan:")
    print(f"{'No':<3} | {'Kategori':<12} | {'Penulis':<18} | {'Judul':<25} | {'Harga':<12}")
    print("-" * 75)
    for b in data[:5]:
        p_penulis = (
            (b["Penulis"][:15] + "..")
            if len(b["Penulis"]) > 18
            else b["Penulis"]
        )
        p_judul = (
            (b["Judul"][:22] + "..")
            if len(b["Judul"]) > 25
            else b["Judul"]
        )
        print(
            f"{b['No']:<3} | {b['Kategori'][:12]:<12} | {p_penulis:<18} | {p_judul:<25} | Rp {b['Harga_Diskon_Rp']:<9,}"
        )
    print("=" * 75)
    print("[SUCCESS] Otomatisasi Scraping & Pengorganisasian File Selesai!\n")


# =============================================================================
# CHAPTER 12: COMMAND LINE PROGRAMS (Antarmuka Argumen CLI via argparse)
# =============================================================================
def parse_arguments() -> argparse.Namespace:
    """Mengonfigurasi dan mem-parsing parameter CLI (Chapter 12)."""
    parser = argparse.ArgumentParser(
        description="Aplikasi Otomatisasi Web Scraping Katalog Buku Penerbit Kakatua",
        epilog="Contoh pemanggilan: python main.py --limit 30 --backup",
    )

    parser.add_argument(
        "--url",
        type=str,
        default=DEFAULT_TARGET_URL,
        help=f"URL halaman katalog target (default: {DEFAULT_TARGET_URL})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Jumlah minimal buku yang ingin diambil (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default=None,
        help="Filter pencarian buku berdasarkan kata kunci pada judul/penulis",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter kategori buku (contoh: Nonfiksi, Fiksi)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT_CSV),
        help=f"Lokasi path output CSV (default: {DEFAULT_OUTPUT_CSV})",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Membuat arsip ZIP backup di folder backup/ (default: True)",
    )
    parser.add_argument(
        "--no-backup",
        dest="backup",
        action="store_false",
        help="Menonaktifkan pembuatan arsip backup ZIP",
    )
    parser.add_argument(
        "--detail",
        action="store_true",
        default=False,
        help="Scrape mendalam ke laman produk untuk mengambil ISBN dan tebal halaman",
    )

    return parser.parse_args()


# =============================================================================
# TITIK MASUK UTAMA (ENTRY POINT)
# =============================================================================
def main():
    print("""
    ==================================================================
           PENERBIT KAKATUA - BOOK CATALOG SCRAPER & ORGANIZER
          Mata Kuliah: Automation Systems - Univ. Pelita Bangsa
    ==================================================================
    """)

    # 1. Parsing argumen CLI (Chapter 12)
    args = parse_arguments()

    # 2. Persiapan direktori otomatis menggunakan pathlib (Chapter 11)
    siapkan_direktori_kerja()

    target_csv = Path(args.output)

    # 3. Eksekusi Web Scraping (Chapter 13 & 9)
    try:
        daftar_buku = scrape_katalog_kakatua(
            base_url=args.url,
            limit=args.limit,
            keyword=args.keyword,
            category_filter=args.category,
            fetch_details=args.detail,
        )
    except KeyboardInterrupt:
        print("\n[!] Scraping dibatalkan secara manual oleh pengguna.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] Gagal menjalankan proses scraping: {e}")
        sys.exit(1)

    if not daftar_buku:
        print("\n[!] Tidak ada data buku yang berhasil diambil atau cocok dengan filter.")
        sys.exit(0)

    # 4. Menyimpan data ke format CSV dan TXT (Chapter 10)
    print(f"\n[*] Menyimpan {len(daftar_buku)} record data ke {target_csv}...")
    simpan_ke_csv(daftar_buku, target_csv)

    print(f"[*] Menulis laporan ringkasan statistik ke {DEFAULT_SUMMARY_TXT}...")
    buat_laporan_ringkasan(
        daftar_buku,
        DEFAULT_SUMMARY_TXT,
        url_target=args.url,
        filter_keyword=args.keyword,
    )

    # 5. Membuat arsip backup ZIP (Chapter 11)
    zip_path = None
    if args.backup:
        print(f"[*] Mengompresi file hasil ke arsip cadangan {DEFAULT_BACKUP_ZIP}...")
        files_to_backup = [
            target_csv,
            DEFAULT_SUMMARY_TXT,
            DEFAULT_RAW_DATA,
        ]
        zip_path = buat_arsip_backup(files_to_backup, DEFAULT_BACKUP_ZIP)

    # 6. Menampilkan ringkasan pemrosesan di terminal
    tampilkan_ringkasan_terminal(
        daftar_buku, target_csv, DEFAULT_SUMMARY_TXT, zip_path
    )


if __name__ == "__main__":
    main()
