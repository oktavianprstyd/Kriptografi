# 🤝 Panduan Kolaborasi Tim (4 Orang) - 1 Orang = 1 File

Dokumen ini adalah acuan kerja bersama agar seluruh 4 anggota tim dapat mengembangkan modul masing-masing di GitHub dengan lancar, rapi, serta memiliki **tampilan antarmuka (UI) yang seragam dan konsisten 100%**.

---

## 📁 1. Dimana Saya Menulis Kode? (1 Orang = 1 File)

Setiap anggota memiliki **1 file khusus di dalam folder `modules/`**. File tersebut sudah memuat:
1. **Bagian 1: Rumus/Logika Algoritma** (Enkripsi, Dekripsi, Step-by-Step).
2. **Bagian 2: Tampilan Dashboard Streamlit** (`def render_xxx_page()`).
3. **Bagian 3: Standalone Runner** (Bisa dites langsung sendiri).

| Orang | Tugas Utama | Tugas Tambahan | **File yang Diedit** |
|---|---|---|---|
| **Orang 1** | **Caesar Cipher**: enkripsi + dekripsi | Tampilan Menu 1 + testing Caesar | [`modules/menu1_caesar.py`](modules/menu1_caesar.py) |
| **Orang 2** | **Vigenère Cipher**: enkripsi + dekripsi | Tampilan Menu 2 + testing Vigenère | [`modules/menu2_vigenere.py`](modules/menu2_vigenere.py) |
| **Orang 3** | **AES**: enkripsi + dekripsi | Tampilan Menu 3 + testing AES | [`modules/menu3_aes.py`](modules/menu3_aes.py) |
| **Orang 4** | **RSA**: enkripsi + dekripsi | Tampilan Menu 4 + testing RSA | [`modules/menu4_rsa.py`](modules/menu4_rsa.py) |
| **Bersama** | **Super Enkripsi**: Pipeline 4 tahap | Tampilan Menu 5 + testing integrasi | [`modules/menu5_super.py`](modules/menu5_super.py) |

> 💡 **PENTING**: Kamu **TIDAK PERLU** mengedit file `app.py`. File `app.py` otomatis memanggil file kamu! Kamu hanya perlu mengedit dan mempercantik file milikmu sendiri di folder `modules/`.

---

## 🚀 2. Cara Menjalankan & Mengetes File Sendiri (Standalone Test)

Kamu bisa menjalankan dan melihat tampilan filemu sendiri secara langsung di browser tanpa perlu menjalankan menu utama:

* **Orang 1 (Caesar)**:
  ```bash
  streamlit run modules/menu1_caesar.py
  ```
* **Orang 2 (Vigenère)**:
  ```bash
  streamlit run modules/menu2_vigenere.py
  ```
* **Orang 3 (AES)**:
  ```bash
  streamlit run modules/menu3_aes.py
  ```
* **Orang 4 (RSA)**:
  ```bash
  streamlit run modules/menu4_rsa.py
  ```

---

## 🎨 3. Standar Desain Konsisten (Design Consistency)

Agar aplikasi saat digabungkan terlihat rapi dan senada:

1. **Header Seragam**: Panggil fungsi `render_header()` yang sudah disediakan di bagian atas fungsi render.
2. **4 Tab Wajib**: Pertahankan 4 tab seragam:
   * `🔒 Enkripsi`
   * `🔓 Dekripsi`
   * `🔍 Visualisasi Step-by-Step`
   * `📖 Teori & Rumus`
3. **Layout 2 Kolom**:
   * Kolom Kiri: Input teks & parameter kunci + tombol aksi (`use_container_width=True`).
   * Kolom Kanan: Output teks sandi & notifikasi info/sukses.
4. **Prefiks Key Streamlit**: Berikan prefiks huruf pada setiap `key` widget:
   * Orang 1: `c_...`
   * Orang 2: `v_...`
   * Orang 3: `aes_...`
   * Orang 4: `rsa_...`

---

## 🌿 4. Alur Kerja Git & GitHub

1. **Tarik Kode Terbaru:**
   ```bash
   git pull origin main
   ```
2. **Buat Branch Tugasmu:**
   ```bash
   git checkout -b feature/<nama-kamu-dan-algoritma>
   ```
3. **Edit Filemu di Folder `modules/`** dan tes lokal via `streamlit run modules/...`.
4. **Simpan & Unggah (Commit & Push):**
   ```bash
   git add modules/menuX_xxx.py
   git commit -m "feat: perbarui visualisasi enkripsi"
   git push -u origin feature/<nama-kamu-dan-algoritma>
   ```
5. **Buat Pull Request (PR) di GitHub** untuk digabungkan ke branch `main`.
