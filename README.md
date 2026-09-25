# 🔐 Aplikasi Enkripsi & Dekripsi Kriptografi (5 Menu)
> **Tugas Besar Mata Kuliah Kriptografi**  
> Program Studi Informatika — Universitas Pembangunan Nasional "Veteran" Yogyakarta

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20(1%20Person%201%20File)-purple)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 1. Gambaran Umum Proyek
Aplikasi ini dikembangkan untuk memenuhi penugasan mata kuliah Kriptografi dengan arsitektur **Modular Terpadu (1 Orang = 1 File)**:
1. **Menu 1 (Klasik 1)**: Caesar Cipher (Substitusi Monoalfabetik)
2. **Menu 2 (Klasik 2)**: Vigenère Cipher (Substitusi Polialfabetik)
3. **Menu 3 (Modern 1)**: AES-128 Block Cipher (Cipher Blok Simetris)
4. **Menu 4 (Modern 2)**: RSA Asymmetric Cipher (Cipher Kunci Asimetris / Publik-Privat)
5. **Menu 5 (Super Enkripsi)**: Integrasi berantai dari ke-4 algoritma kriptografi.

Setiap modul memuat **logika algoritma, antarmuka Streamlit, dan visualisasi proses langkah demi langkah (*step-by-step trace*)** secara mandiri.

---

## 👥 2. Pembagian File & Tugas Tim 4 Orang

Setiap anggota tim bertanggung jawab penuh pada file masing-masing di dalam folder `modules/`:

| Orang | Tugas Utama | Tugas Tambahan | **File yang Dikerjakan** |
|---|---|---|---|
| **Orang 1** | **Caesar Cipher**: enkripsi + dekripsi | Tampilan Menu 1 + testing Caesar | [`modules/menu1_caesar.py`](modules/menu1_caesar.py) |
| **Orang 2** | **Vigenère Cipher**: enkripsi + dekripsi | Tampilan Menu 2 + testing Vigenère | [`modules/menu2_vigenere.py`](modules/menu2_vigenere.py) |
| **Orang 3** | **AES**: enkripsi + dekripsi | Tampilan Menu 3 + testing AES | [`modules/menu3_aes.py`](modules/menu3_aes.py) |
| **Orang 4** | **RSA**: enkripsi + dekripsi | Tampilan Menu 4 + testing RSA | [`modules/menu4_rsa.py`](modules/menu4_rsa.py) |
| **Bersama** | **Super Enkripsi**: Pipeline 4 tahap | Tampilan Menu 5 + testing integrasi | [`modules/menu5_super.py`](modules/menu5_super.py) |

---

## 📁 3. Struktur Berkas Repositori

```text
ProjekKripto/
├── app.py                      # Master Router / Menu Utama (~60 baris)
├── requirements.txt            # Dependensi pustaka Python
├── run.bat                     # Launcher otomatis satu-klik (Windows)
├── README.md                   # Dokumentasi proyek
├── CONTRIBUTING.md             # Panduan kolaborasi tim di GitHub
└── modules/                    # Folder kerja tim (1 Orang = 1 File)
    ├── __init__.py
    ├── ui_helper.py            # Komponen desain, warna badge, & CSS bersama
    ├── menu1_caesar.py         # File kerja Orang 1 (Algoritma + UI Caesar)
    ├── menu2_vigenere.py       # File kerja Orang 2 (Algoritma + UI Vigenère)
    ├── menu3_aes.py            # File kerja Orang 3 (Algoritma + UI AES-128)
    ├── menu4_rsa.py            # File kerja Orang 4 (Algoritma + UI RSA)
    └── menu5_super.py          # File kerja Bersama (Super Enkripsi 4 Tahap)
```

---

## 🚀 4. Cara Menjalankan Aplikasi

### Menjalankan Seluruh Aplikasi (Dashboard Utama):
```bash
streamlit run app.py
```
*(Atau di Windows cukup klik 2x file `run.bat`)*

### Menjalankan Halaman Mandiri (Standalone Test):
Tiap anggota bisa langsung mengetes kodenya sendiri tanpa membuka menu utama:
* Orang 1: `streamlit run modules/menu1_caesar.py`
* Orang 2: `streamlit run modules/menu2_vigenere.py`
* Orang 3: `streamlit run modules/menu3_aes.py`
* Orang 4: `streamlit run modules/menu4_rsa.py`
* Menu 5: `streamlit run modules/menu5_super.py`

---

## 🎨 5. Aturan Desain Konsisten
1. **Struktur 4 Tab Wajib**: `🔒 Enkripsi`, `🔓 Dekripsi`, `🔍 Visualisasi Step-by-Step`, `📖 Teori & Rumus`.
2. **Layout 2 Kolom**: Kiri (Input & Parameter Kunci) vs Kanan (Output & Statistik).
3. **Prefix Key Streamlit**: `c_` (Orang 1), `v_` (Orang 2), `aes_` (Orang 3), `rsa_` (Orang 4).
4. **Header Terpadu**: Menggunakan `render_header()` dari `ui_helper.py`.
