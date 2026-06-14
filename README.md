# 📡 Network Tools Analyzer

**Network Tools Analyzer** adalah aplikasi desktop berkinerja tinggi berbasis Python dan PyQt6 yang dirancang khusus untuk membantu *RF Engineer* dan *Network Administrator* dalam mengolah data telekomunikasi.

Aplikasi ini berfungsi sebagai "Hub" terpusat yang saat ini memiliki dua modul utama: **RSSI & SNR Calculation** (Kalkulasi hasil *Drive Test*) dan **Radio Editor** (Pengolahan data parameter *Access Point* / Radio).

## ✨ Fitur Utama

### 📊 Modul 1: RSSI & SNR Calculation

Modul ini digunakan untuk memproses data mentah hasil *Drive Test* dengan sangat cepat (mendukung ribuan baris data tanpa *freeze*).

* **Clipboard Integration:** Langsung *Paste* data dari Microsoft Excel tanpa perlu *upload* file.
* **Auto-Calculation:** Menghitung otomatis nilai **SNR** berdasarkan *Average Field Strength* dan mengelompokkannya ke dalam kategori (*Excellent, Good, Fair, Poor*).
* **Custom Columns:** Menambahkan kolom baru dengan formula matematika kustom secara dinamis.
* **Smart Averaging:** Menghitung rata-rata dari seluruh kolom numerik dengan satu klik.
* **Export Dashboard to PNG:** Menghasilkan laporan visual (*Pie Chart* & Tabel Rekap) menggunakan Matplotlib dan menyimpannya sebagai file gambar.
* **Database History:** Menyimpan riwayat kalkulasi secara otomatis ke SQLite (bisa dimuat ulang atau dihapus kapan saja).

### 📻 Modul 2: Radio Editor

Modul untuk mem-parsing dan merapikan data konfigurasi Radio (*dump file* CSV) menjadi tabel siap lapor sesuai standar dokumentasi *Enterprise*.

* **Smart CSV Parsing:** Mengelompokkan data berdasarkan *AP Name* dan otomatis memetakan frekuensi (Radio 0 ke 2.4GHz, Radio 1 & 2 ke 5GHz).
* **5GHz Channel Merging:** Otomatis mendeteksi *channel* atas dan bawah, merapikannya menjadi format `High` dan `Low` dalam satu sel.
* **Bulk SSID Assignment:** Fitur *checkbox dropdown* untuk menerapkan satu atau beberapa SSID secara serentak ke data yang difilter.
* **Live Search Filter:** Pencarian data *real-time* berdasarkan *AP Name* atau *SSID*.
* **Bulletproof HTML Export:** Tombol khusus untuk menyalin tabel dengan format HTML *Rich Text* (Calibri 11pt, Header Merah, Border Hitam Tegas). Saat di-*paste* ke MS Word/Excel, format tidak akan pecah.

---

## 🛠️ Prasyarat (Prerequisites)

Pastikan Anda telah menginstal **Python 3.8** (atau versi lebih baru) di sistem operasi Anda (Windows / macOS / Linux).

---

## 🚀 Cara Instalasi

1. **Clone repositori ini** ke direktori lokal Anda:
```bash
git clone https://github.com/username-anda/network-tools-analyzer.git
cd network-tools-analyzer

```


2. **Instal library yang dibutuhkan** melalui file `requirements.txt`:
```bash
pip install -r requirements.txt

```


3. **Jalankan aplikasi**:
```bash
python main.py

```



---

## 📖 Panduan Penggunaan

### Menggunakan RSSI & SNR Calculation

1. Buka file Excel yang berisi data hasil *Drive Test*.
2. Blok (*highlight*) data yang ingin diproses (pastikan tidak menyertakan baris judul/header), lalu `Ctrl+C` (*Copy*).
3. Buka aplikasi, masuk ke menu **RSSI & SNR Calculation**, dan klik tombol **📋 Paste Data**.
4. Klik **📊 Hitung Rata-Rata** jika ingin memunculkan baris AVG di bawah tabel.
5. Klik **🖼️ Preview Laporan (PNG)** untuk melihat grafik distribusi *Excellent/Good/Fair/Poor* dan menyimpannya.

### Menggunakan Radio Editor

1. Ekspor data Radio Info dari sistem ke format `.csv`.
2. Masuk ke menu **Radio Editor Module** di aplikasi.
3. Klik **📂 Upload CSV** dan pilih file yang baru saja diekspor.
4. Gunakan bar **🔍 Cari Data** untuk mencari *AP Name* tertentu.
5. Gunakan dropdown **🎯 Set SSID** dengan mencentang (*checklist*) SSID yang diinginkan untuk diterapkan langsung ke tabel.
6. Klik **📑 Copy Tabel (Word/Excel)**, lalu buka Microsoft Word dan tekan `Ctrl+V`. Format tabel akan tersalin dengan sempurna.

---

## 📁 Struktur Folder Proyek

Aplikasi ini dibangun menggunakan arsitektur modular MVC (*Model-View-Component*) agar mudah dikembangkan (*scalable*):

```text
network-tools-analyzer/
│
├── main.py                  # Entry point utama aplikasi
├── requirements.txt         # Daftar dependency Python
├── drivetest_history.db     # (Auto-generated) Database SQLite lokal
│
├── database/                # Manajemen SQLite
│   ├── __init__.py
│   └── db_manager.py
│
├── components/              # Elemen UI yang dapat digunakan kembali (Dialog/Pop-up)
│   ├── __init__.py
│   ├── history_dialog.py    # GUI Riwayat kalkulasi
│   └── preview_dialog.py    # GUI Penampil grafik Matplotlib
│
└── views/                   # Tampilan Jendela Utama (Windows)
    ├── __init__.py
    ├── home_window.py       # Jendela Menu Utama
    ├── main_window.py       # Modul RSSI & SNR
    └── radio_window.py      # Modul Radio Editor

```

---

## 🧰 Teknologi yang Digunakan

* **Bahasa Pemrograman:** [Python 3](https://www.python.org/)
* **GUI Framework:** [PyQt6](https://pypi.org/project/PyQt6/)
* **Data Visualization:** [Matplotlib](https://matplotlib.org/)
* **Database:** SQLite3 (Bawaan Python)

---

## 📄 Lisensi

Didistribusikan di bawah lisensi MIT License. Lihat file `LICENSE` untuk informasi lebih lanjut.
