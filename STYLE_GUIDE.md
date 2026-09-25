# Panduan Gaya Desain Antarmuka (Style Guide) — DataIn Aesthetic

Panduan ini dibuat agar seluruh anggota tim (Orang 1 s/d Orang 4) memiliki tampilan halaman yang **100% seragam, rapi, dan terlihat profesional seperti aplikasi web modern (ala DataIn)** tanpa bentrok desain.

---

## 1. Aturan Utama Desain (DOs & DON'Ts)

| Hal yang Diwajibkan (DO) | Hal yang Dilarang (DON'T) |
|---|---|
| Gunakan teks bahasa Indonesia baku & formal (contoh: `Enkripsi Pesan`, `Dekripsi Pesan`). | **Hindari emoji berlebihan** (seperti 🔒, 🔓, 🔍, ⚡, 🚀, 🎯, 1️⃣, 2️⃣). |
| Gunakan layout 2 kolom seimbang: `col1, col2 = st.columns([1, 1])`. | Jangan menumpuk input dan output memanjang ke bawah dalam satu kolom. |
| Gunakan helper `render_header()` yang sudah disiapkan di `modules/ui_helper.py`. | Jangan membuat judul manual dengan warna dan font acak. |
| Beri awalan `key` unik pada setiap input/tombol (contoh: `key="v_plain"`). | Jangan gunakan key generic seperti `key="input"` (akan tabrakan state). |

---

## 2. Palet Warna Resmi (DataIn Warm & Navy Palette)

Semua komponen sudah terhubung otomatis ke CSS global, tetapi jika ingin menambahkan elemen visual khusus, gunakan kode warna berikut:

* **Background Utama**: `#FAF6F0` *(Warm Cream)*
* **Background Sidebar**: `#F4F0EA` *(Warm Dark)*
* **Teks & Judul**: `#1E3A5F` *(Deep Navy)*
* **Tombol Utama (Action Button)**: `#002D80` *(Navy Main)*
* **Border & Garis**: `#D8CFC4` *(Border Taupe)*
* **Aksen / Subteks**: `#4A709C` *(Slate Blue)*
* **Kartu Kontainer**: Putih murni (`#FFFFFF`) dengan border `#D8CFC4`

---

## 3. Struktur Standar File Modul (Template Siap Pakai)

Setiap file di `modules/menuX_xxx.py` mengikuti struktur 3 bagian berikut:

```python
import streamlit as st
import pandas as pd

# 1. Import helper desain
try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: RUMUS / LOGIKA ALGORITMA
# ==============================================================================
def algoritma_encrypt(plaintext, key):
    # Tulis fungsi matematikamu di sini
    return ciphertext, steps

def algoritma_decrypt(ciphertext, key):
    # Tulis fungsi dekripsimu di sini
    return plaintext, steps

# ==============================================================================
# BAGIAN 2: TAMPILAN STREAMLIT (UI)
# ==============================================================================
def render_nama_page():
    # Header seragam tanpa emoji
    render_header(
        title="Menu X: Nama Algoritma",
        subtitle="Penjelasan ringkas cara kerja algoritma dalam satu kalimat",
        pic_name="Penanggung Jawab: Orang X",
        category="Kriptografi Klasik / Modern"
    )

    # 4 Tab Standar
    tab_main, tab_trace, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pelacakan Proses (Step-by-Step)",
        "Teori & Formula"
    ])

    with tab_main:
        # Pilihan Mode (Radio button bersih)
        mode = st.radio("Pilih Mode Operasi", ["Enkripsi Pesan", "Dekripsi Pesan"], horizontal=True, key="x_mode")
        st.divider()

        # Layout 2 Kolom Seimbang: Kiri (Input) vs Kanan (Output)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("##### Input Teks & Parameter Kunci")
            # Input teks & tombol
            btn = st.button("Enkripsi Pesan", use_container_width=True, key="x_btn")
            
        with col2:
            st.markdown("##### Hasil Enkripsi")
            # Output teks

# ==============================================================================
# BAGIAN 3: STANDALONE RUNNER
# ==============================================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Nama Algoritma", layout="wide")
    load_global_css()
    render_nama_page()
```

---

## 4. Cara Mengetes Halaman Sendiri
Cukup buka terminal dan jalankan:
```bash
streamlit run modules/menuX_xxx.py
```
Halaman milikmu akan langsung terbuka di browser dengan tema DataIn yang bersih dan rapi!
