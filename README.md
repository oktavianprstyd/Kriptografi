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
3. **Menu 3 (Modern 1)**: Vernam Stream Cipher (Cipher Aliran Bitwise XOR & Autokey)
4. **Menu 4 (Modern 2)**: AES-128 Block Cipher (Cipher Blok Simetris Standar Matriks NumPy)
5. **Menu 5 (Super Enkripsi)**: Integrasi berantai 4 tahap dari seluruh algoritma (Caesar ➔ Vigenère ➔ Vernam ➔ AES-128).

Setiap modul memuat **logika algoritma murni tanpa library pihak ketiga untuk kripto inti, antarmuka Streamlit yang responsif, dan visualisasi proses langkah demi langkah (*step-by-step trace*)** secara mandiri.

---

## 👥 2. Pembagian Modul & Penanggung Jawab (Kelompok 3)

Setiap anggota tim bertanggung jawab penuh pada modul masing-masing di dalam folder `modules/`:

| No | Modul & Algoritma | Penanggung Jawab | NIM | **File yang Dikerjakan** |
|---|---|---|---|---|
| **Menu 1** | **Caesar Cipher** | Grace Rianty Butar Butar | `123240036` | [`modules/menu1_caesar.py`](modules/menu1_caesar.py) |
| **Menu 2** | **Vigenère Cipher** | Mirwan Qolyubi | `123240116` | [`modules/menu2_vigenere.py`](modules/menu2_vigenere.py) |
| **Menu 3** | **Vernam Stream Cipher** | Oktavian Prasetya Adi | `123240135` | [`modules/menu4_vernam.py`](modules/menu4_vernam.py) |
| **Menu 4** | **AES-128 Block Cipher** | Adhafa Joan Putranto | `123240069` | [`modules/menu3_aes.py`](modules/menu3_aes.py) |
| **Menu 5** | **Super Enkripsi (Pipeline)** | Kelompok 3 (Seluruh Anggota) | - | [`modules/menu5_super.py`](modules/menu5_super.py) |

---

## 📁 3. Struktur Berkas Repositori

```text
ProjekKripto/
├── app.py                      # Master Router / Menu Utama (~60 baris)
├── requirements.txt            # Dependensi pustaka Python
├── run.bat                     # Launcher otomatis satu-klik (Windows)
├── README.md                   # Dokumentasi proyek
├── CONTRIBUTING.md             # Panduan kolaborasi tim di GitHub
├── STYLE_GUIDE.md              # Standar desain UI dan estetika
├── Kripto .pdf                 # Slide materi & presentasi proyek
├── .streamlit/
│   └── config.toml             # Konfigurasi tema dan server Streamlit
└── modules/                    # Folder kerja tim (1 Modul = 1 File)
    ├── __init__.py
    ├── ui_helper.py            # Komponen desain, selector mode, & CSS bersama
    ├── menu1_caesar.py         # Grace (Caesar Cipher)
    ├── menu2_vigenere.py       # Mirwan (Vigenère Cipher)
    ├── menu3_aes.py            # Adhafa (AES-128 Block Cipher)
    ├── menu4_vernam.py         # Oktavian (Vernam Stream Cipher)
    └── menu5_super.py          # Bersama (Super Enkripsi 4 Tahap)
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
* Caesar: `streamlit run modules/menu1_caesar.py`
* Vigenère: `streamlit run modules/menu2_vigenere.py`
* AES-128: `streamlit run modules/menu3_aes.py`
* Vernam: `streamlit run modules/menu4_vernam.py`
* Super Enkripsi: `streamlit run modules/menu5_super.py`

---

## 🎨 5. Aturan Desain Konsisten
1. **Struktur 4 Tab Wajib**: `🔒 Enkripsi`, `🔓 Dekripsi`, `🔍 Visualisasi Step-by-Step`, `📖 Teori & Rumus`.
2. **Layout 2 Kolom**: Kiri (Input & Parameter Kunci) vs Kanan (Output & Statistik).
3. **Prefix Key Streamlit**: `c_` (Orang 1), `v_` (Orang 2), `aes_` (Orang 3), `rsa_` (Orang 4).
4. **Header Terpadu**: Menggunakan `render_header()` dari `ui_helper.py`.
