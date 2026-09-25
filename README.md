# 🔐 Aplikasi Enkripsi & Dekripsi Kriptografi (5 Menu)
> **Tugas Besar Mata Kuliah Kriptografi**  
> Program Studi Informatika — Universitas Pembangunan Nasional "Veteran" Yogyakarta

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)
![Cryptography](https://img.shields.io/badge/Security-AES%20%26%20RSA-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 1. Gambaran Umum Proyek
Aplikasi ini dikembangkan untuk memenuhi penugasan mata kuliah Kriptografi dengan arsitektur **5 Menu Terpadu**:
1. **Menu 1 (Klasik 1)**: Caesar Cipher (Substitusi Monoalfabetik)
2. **Menu 2 (Klasik 2)**: Vigenère Cipher (Substitusi Polialfabetik)
3. **Menu 3 (Modern 1)**: AES-128 Block Cipher (Cipher Blok Simetris)
4. **Menu 4 (Modern 2)**: RSA Asymmetric Cipher (Cipher Kunci Asimetris / Publik-Privat)
5. **Menu 5 (Super Enkripsi)**: Integrasi berantai dari ke-4 algoritma kriptografi.

Setiap menu dilengkapi dengan **halaman khusus visualisasi proses langkah demi langkah (*step-by-step trace*)** pada proses enkripsi dan dekripsi untuk keperluan presentasi di kelas.

---

## 👥 2. Pembagian Tugas Tim 4 Orang

Pembagian tugas kelompok dirancang terstruktur dan terbagi habis untuk 4 orang:

| Orang | Tugas Utama | Tugas Tambahan | Modul Terkait |
|---|---|---|---|
| **Orang 1** | **Caesar Cipher**: enkripsi + dekripsi | Tampilan Menu 1 + testing Caesar | `crypto/caesar.py` & Menu 1 `app.py` |
| **Orang 2** | **Vigenère Cipher**: enkripsi + dekripsi | Tampilan Menu 2 + testing Vigenère | `crypto/vigenere.py` & Menu 2 `app.py` |
| **Orang 3** | **AES**: enkripsi + dekripsi | Tampilan Menu 3 + testing AES | `crypto/aes.py` & Menu 3 `app.py` |
| **Orang 4** | **RSA**: enkripsi + dekripsi | Tampilan Menu 4 + testing RSA | `crypto/rsa_cipher.py` & Menu 4 `app.py` |
| **Bersama** | **Super Enkripsi**: Pipeline integrasi 4 tahap | Tampilan Menu 5 + testing integrasi | `crypto/super_cipher.py` & Menu 5 `app.py` |

---

## 🎨 3. Aturan Desain Konsisten (Design Guidelines)

Agar tampilan antarmuka (UI) tetap rapi, konsisten, dan seragam ketika dikerjakan oleh 4 orang yang berbeda, seluruh anggota **wajib mematuhi 4 pilar desain berikut**:

### 1. Struktur 4 Tab Wajib di Setiap Menu
Setiap menu algoritma (Menu 1 s/d 4) wajib memiliki 4 tab dengan penamaan dan urutan identik:
* **Tab 1 (`🔒 Enkripsi`)**: Untuk proses enkripsi pesan plainteks.
* **Tab 2 (`🔓 Dekripsi`)**: Untuk proses dekripsi ciphertext kembali ke plainteks.
* **Tab 3 (`🔍 Visualisasi Step-by-Step`)**: Tabel/matriks langkah perhitungan matematis karakter per karakter.
* **Tab 4 (`📖 Teori & Rumus`)**: Rangkuman rumus dan materi perkuliahan untuk bahan presentasi.

### 2. Standar Layout 2 Kolom (`st.columns([1, 1])`)
Pada Tab Enkripsi dan Dekripsi:
* **Kolom Kiri (Input)**:
  * Text area untuk Plaintext/Ciphertext input.
  * Input parameter kunci (slider untuk angka, text input untuk kata, number input untuk prima).
  * Tombol aksi penuh lebar (`use_container_width=True`) dengan warna primer.
* **Kolom Kanan (Output)**:
  * Text area untuk hasil enkripsi/dekripsi.
  * Komponen notifikasi status (`st.success` / `st.info`).
  * Rumus kalkulasi (`st.code`).

### 3. Konvensi Penamaan Prefix Widget Streamlit
Untuk mencegah terjadinya tabrakan session state antar halaman:
* **Orang 1 (Caesar)**: Gunakan prefix `c_` (contoh: `c_plain_in`, `c_shift_in`, `c_btn_enc`).
* **Orang 2 (Vigenère)**: Gunakan prefix `v_` (contoh: `v_plain`, `v_key_enc`, `v_btn_enc`).
* **Orang 3 (AES)**: Gunakan prefix `aes_` (contoh: `aes_plain_in`, `aes_key_in`, `aes_btn_enc`).
* **Orang 4 (RSA)**: Gunakan prefix `rsa_` (contoh: `rsa_plain_in`, `rsa_p`, `rsa_btn_enc`).
* **Menu 5 (Super)**: Gunakan prefix `sup_` (contoh: `sup_plain`, `sup_btn_enc`).

### 4. Skema Warna & Badge Penanggung Jawab
* Orang 1 (Caesar): Badge Biru Lembut (`badge-p1` `#DBEAFE`)
* Orang 2 (Vigenère): Badge Indigo Lembut (`badge-p2` `#E0E7FF`)
* Orang 3 (AES): Badge Hijau Lembut (`badge-p3` `#DCFCE7`)
* Orang 4 (RSA): Badge Kuning/Amber Lembut (`badge-p4` `#FEF3C7`)
* Super Enkripsi: Badge Ungu Elegan (`badge-super` `#F3E8FF`)

---

## 🎯 4. Rincian 5 Menu & Rumus Matematis

### 1️⃣ Menu 1: Caesar Cipher (Orang 1)
* **Enkripsi**: $C_i = (P_i + k) \pmod{26}$
* **Dekripsi**: $P_i = (C_i - k) \pmod{26}$
* **Fitur**: Slider pergeseran $k \in [1, 25]$, tabel kalkulasi modulo, peta abjad, dan **Kriptanalisis Brute-Force 25 kunci**.

### 2️⃣ Menu 2: Vigenère Cipher (Orang 2)
* **Enkripsi**: $C_i = (P_i + K_i) \pmod{26}$
* **Dekripsi**: $P_i = (C_i - K_i + 26) \pmod{26}$
* **Fitur**: Input kata kunci alfabetik, tabel perulangan kunci, dan **Tabula Recta 26×26**.

### 3️⃣ Menu 3: AES-128 Block Cipher (Orang 3)
* **Standar**: Rijndael 128-bit block cipher dengan mode CBC dan PKCS#7 Padding.
* **Fitur**: Visualisasi State Matrix 4×4, demonstrasi putaran (*SubBytes, ShiftRows, MixColumns, AddRoundKey*).

### 4️⃣ Menu 4: RSA Asymmetric Cipher (Orang 4)
* **Pembangkitan Kunci**:
  * Modulus: $n = p \times q$
  * Euler Totient: $\phi(n) = (p-1)(q-1)$
  * Kunci Publik: $(e, n)$, di mana $\gcd(e, \phi(n)) = 1$
  * Kunci Privat: $d \equiv e^{-1} \pmod{\phi(n)}$
* **Enkripsi & Dekripsi**:
  $$C_i = M_i^e \pmod n, \quad M_i = C_i^d \pmod n$$
* **Fitur**: Input bilangan prima $p$ dan $q$, penentuan otomatis $n, \phi(n), e, d$, dan tabel eksponensial modulo per karakter.

### 5️⃣ Menu 5: Super Enkripsi (Bersama)
* **Alur Enkripsi**:
  $$\text{Plainteks} \xrightarrow{\text{Caesar (P1)}} C_1 \xrightarrow{\text{Vigenère (P2)}} C_2 \xrightarrow{\text{AES (P3)}} C_3 \xrightarrow{\text{RSA (P4)}} \text{Final Super Ciphertext}$$
* **Alur Dekripsi (Prinsip LIFO)**:
  $$\text{Final Ciphertext} \xrightarrow{\text{RSA}^{-1}} C_3 \xrightarrow{\text{AES}^{-1}} C_2 \xrightarrow{\text{Vigenère}^{-1}} C_1 \xrightarrow{\text{Caesar}^{-1}} \text{Plainteks Asli}$$
* **Fitur**: Tabel stasiun transformasi data di setiap tahapan pipeline.

---

## 🚀 5. Cara Menjalankan Aplikasi

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/<USERNAME>/ProjekKripto.git
   cd ProjekKripto
   ```
2. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Aplikasi:**
   ```bash
   streamlit run app.py
   ```
   *(Atau klik 2x file `run.bat` di Windows)*

---

## 🧪 6. Testing & Verifikasi
Jalankan unit test otomatis untuk memvalidasi keempat modul:
```bash
python test_crypto.py
```
Hasil:
```text
[PASS] Orang 1: Caesar Cipher roundtrip verified.
[PASS] Orang 2: Vigenere Cipher roundtrip verified.
[PASS] Orang 3: AES-128 Block Cipher roundtrip verified.
[PASS] Orang 4: RSA Asymmetric Cipher roundtrip verified.
[PASS] Menu 5: Super Cipher (Caesar -> Vigenere -> AES -> RSA) roundtrip verified.

ALL CRYPTO TESTS PASSED SUCCESSFULLY!
```
