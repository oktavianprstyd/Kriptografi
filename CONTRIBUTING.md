# 🤝 Panduan Kolaborasi Tim (4 Orang) & Standar Desain

Dokumen ini adalah acuan kerja bersama agar seluruh 4 anggota tim dapat mengembangkan modul masing-masing di GitHub dengan lancar, rapi, serta memiliki **tampilan antarmuka (UI) yang seragam dan konsisten 100%**.

---

## 👥 1. Pembagian Tugas Tim (Sesuai Kesepakatan)

| Orang | Tugas Utama | Tugas Tambahan | File yang Dikerjakan |
|---|---|---|---|
| **Orang 1** | **Caesar Cipher**: enkripsi + dekripsi | Tampilan Menu 1 + testing Caesar | `crypto/caesar.py` & Bagian Menu 1 di `app.py` |
| **Orang 2** | **Vigenère Cipher**: enkripsi + dekripsi | Tampilan Menu 2 + testing Vigenère | `crypto/vigenere.py` & Bagian Menu 2 di `app.py` |
| **Orang 3** | **AES**: enkripsi + dekripsi | Tampilan Menu 3 + testing AES | `crypto/aes.py` & Bagian Menu 3 di `app.py` |
| **Orang 4** | **RSA**: enkripsi + dekripsi | Tampilan Menu 4 + testing RSA | `crypto/rsa_cipher.py` & Bagian Menu 4 di `app.py` |

---

## 🎨 2. Standar Desain Konsisten (Design Consistency Contract)

Ketika 4 orang mengerjakan menu yang berbeda, sangat rawan terjadi inkonsistensi (misalnya ada yang membuat tombol kecil, warna berbeda, susunan tab acak-acakan). Untuk mencegah hal tersebut, ikuti aturan standar berikut:

### Aturan 1: Header Menggunakan Fungsi Terpadu
Gunakan helper `render_header` di baris pertama setiap menu:
```python
render_header(
    "1️⃣ Nama Algoritma",
    "Deskripsi singkat algoritma dalam satu kalimat",
    "Penanggung Jawab: Orang X",
    "Kriptografi Klasik / Modern",
    "badge-pX"  # Gunakan badge-p1, badge-p2, badge-p3, atau badge-p4
)
```

### Aturan 2: Wajib 4 Tab Seragam
Setiap menu algoritma memiliki 4 tab dengan nama persis:
```python
tab_enc, tab_dec, tab_trace, tab_theory = st.tabs([
    "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi Step-by-Step", "📖 Teori & Rumus"
])
```

### Aturan 3: Layout 2 Kolom Seimbang (50% - 50%)
Pada tab `🔒 Enkripsi` dan `🔓 Dekripsi`, gunakan layout 2 kolom:
```python
c1, c2 = st.columns([1, 1])
with c1:
    # INPUT: Text area plainteks & input kunci/parameter
    # Tombol Enkripsi penuh: st.button("🔒 Enkripsi Sekarang", use_container_width=True)
with c2:
    # OUTPUT: Text area hasil sandi & st.info statistik
```

### Aturan 4: Prefiks Kunci Widget Streamlit
Setiap anggota **WAJIB** memberikan `key` unik dengan prefiks huruf modul agar tidak terjadi tabrakan *session state*:
* Orang 1 (Caesar): `key="c_..."` (contoh: `c_plain`, `c_shift`, `c_btn_enc`)
* Orang 2 (Vigenère): `key="v_..."` (contoh: `v_plain`, `v_key`, `v_btn_enc`)
* Orang 3 (AES): `key="aes_..."` (contoh: `aes_plain`, `aes_key`, `aes_btn_enc`)
* Orang 4 (RSA): `key="rsa_..."` (contoh: `rsa_plain`, `rsa_p`, `rsa_btn_enc`)

---

## 🌿 3. Alur Kerja Git & GitHub

### 1. Cabang Fitur (Branch)
Setiap anggota wajib bekerja di branch masing-masing, **DILARANG LANGSUNG PUSH KE MAIN**:
* Orang 1: `git checkout -b feature/caesar-orang1`
* Orang 2: `git checkout -b feature/vigenere-orang2`
* Orang 3: `git checkout -b feature/aes-orang3`
* Orang 4: `git checkout -b feature/rsa-orang4`

### 2. Pengujian Kode Lokal Sebelum Commit
Sebelum melakukan commit, selalu jalankan verifikasi:
```bash
python test_crypto.py
streamlit run app.py
```

### 3. Commit & Push
```bash
git add .
git commit -m "feat(caesar): menambahkan visualisasi pergeseran abjad"
git push -u origin feature/<nama-branch-kamu>
```

### 4. Membuat Pull Request (PR)
1. Masuk ke halaman GitHub repositori.
2. Klik tombol **"Compare & pull request"**.
3. Berikan judul dan penjelasan ringkas fitur yang dikerjakan.
4. Minta rekan kelompok untuk meninjau dan klik **Merge** ke `main`.
