import streamlit as st
import pandas as pd

from modules.ui_helper import load_global_css
from modules.menu1_caesar import render_caesar_page
from modules.menu2_vigenere import render_vigenere_page
from modules.menu3_aes import render_aes_page
from modules.menu4_vernam import render_vernam_page
from modules.menu5_super import render_super_page

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Aplikasi Kriptografi - UPN Veteran Yogyakarta",
    page_icon="https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_UPN_Veteran_Yogyakarta.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Memuat CSS Terpadu Bergaya DataIn
load_global_css()

# ==============================================================================
# SIDEBAR NAVIGASI (BERSIH, TANPA EMOJI, & INTERAKTIF)
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_UPN_Veteran_Yogyakarta.png", width=75)
    st.markdown("### UPN Veteran Yogyakarta")
    st.markdown("**Program Studi Informatika**")
    st.caption("Tugas Mata Kuliah Kriptografi")
    st.divider()

    menu = st.radio(
        "Menu Navigasi",
        [
            "Beranda: Ikhtisar Algoritma",
            "Menu 1: Caesar Cipher",
            "Menu 2: Vigenère Cipher",
            "Menu 3: AES-128 Block Cipher",
            "Menu 4: Vernam Stream Cipher",
            "Menu 5: Super Enkripsi",
            "Informasi Tim & Kontributor"
        ]
    )

# ==============================================================================
# 0. BERANDA: IKHTISAR ALGORITMA KRIPTOGRAFI
# ==============================================================================
if menu == "Beranda: Ikhtisar Algoritma":
    st.markdown('<div class="menu-title">Ikhtisar Algoritma Kriptografi</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="menu-desc">Platform Terpadu Pengujian dan Analisis Matematis Kriptografi Klasik, '
        'Modern, dan Super Enkripsi Pipeline.</div>',
        unsafe_allow_html=True
    )

    # 4 Kotak Kartu Algoritma (Grid 2x2)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="datain-card">
            <span class="badge-category">Kriptografi Klasik</span>
            <span class="badge-pic">Substitusi Monoalfabetik</span>
            <h4 style="margin-top: 8px; color: #1E3A5F; font-family: 'Outfit';">1. Caesar Cipher</h4>
            <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6; margin-bottom: 8px;">
                Algoritma tertua berbasis pergeseran posisi huruf alfabet standar. 
                Setiap karakter digeser secara siklis sejauh nilai kunci <b>k</b> dengan rumus modulo 26.
            </p>
            <div style="background: #FAF6F0; padding: 8px 12px; border-radius: 6px; border: 1px solid #D8CFC4; font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #002D80;">
                Formula: C = (P + k) mod 26 | P = (C - k) mod 26
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="datain-card">
            <span class="badge-category">Kriptografi Modern</span>
            <span class="badge-pic">Cipher Blok Simetris</span>
            <h4 style="margin-top: 8px; color: #1E3A5F; font-family: 'Outfit';">3. AES-128 (Rijndael)</h4>
            <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6; margin-bottom: 8px;">
                Standar enkripsi blok simetris internasional (FIPS 197). Memproses blok data 128 bit 
                dalam 10 putaran berbasis <i>Substitution-Permutation Network</i> (SPN) dan mode operasi CBC.
            </p>
            <div style="background: #FAF6F0; padding: 8px 12px; border-radius: 6px; border: 1px solid #D8CFC4; font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #002D80;">
                Putaran: SubBytes → ShiftRows → MixColumns → AddRoundKey
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="datain-card">
            <span class="badge-category">Kriptografi Klasik</span>
            <span class="badge-pic">Substitusi Polialfabetik</span>
            <h4 style="margin-top: 8px; color: #1E3A5F; font-family: 'Outfit';">2. Vigenère Cipher</h4>
            <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6; margin-bottom: 8px;">
                Pengembangan dari Caesar yang menggunakan kata kunci berulang periodik. 
                Setiap huruf memiliki pergeseran berbeda sehingga kebal dari analisis frekuensi huruf tunggal.
            </p>
            <div style="background: #FAF6F0; padding: 8px 12px; border-radius: 6px; border: 1px solid #D8CFC4; font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #002D80;">
                Formula: C_i = (P_i + K_i) mod 26 | Matriks: Tabula Recta 26x26
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="datain-card">
            <span class="badge-category">Kriptografi Modern</span>
            <span class="badge-pic">Cipher Aliran (Stream Cipher)</span>
            <h4 style="margin-top: 8px; color: #1E3A5F; font-family: 'Outfit';">4. Vernam Stream Cipher</h4>
            <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6; margin-bottom: 8px;">
                Algoritma cipher aliran modern berbasis operasi bitwise XOR (⊕) bit-per-bit dengan aliran bit kunci (keystream). 
                Mengadopsi konsep One-Time Pad (OTP) yang memberikan keamanan sempurna (unbreakable).
            </p>
            <div style="background: #FAF6F0; padding: 8px 12px; border-radius: 6px; border: 1px solid #D8CFC4; font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #002D80;">
                Formula: C_i = P_i ⊕ K_i | P_i = C_i ⊕ K_i (Involutori)
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Super Enkripsi Pipeline Overview
    st.markdown("##### Arsitektur Pipeline: Super Enkripsi 4 Tahap")
    st.markdown("""
    <div class="datain-card">
        <p style="color: #1E3A5F; font-size: 0.95rem; line-height: 1.6; margin-bottom: 12px;">
            <b>Super Enkripsi</b> mengombinasikan kekuatan algoritma substitusi klasik dengan standar cipher blok dan cipher aliran modern. 
            Output sandi dari setiap stasiun menjadi input bagi stasiun berikutnya:
        </p>
        <div style="background: #FAF6F0; border: 1px solid #D8CFC4; border-radius: 8px; padding: 14px; text-align: center; font-family: 'Outfit'; font-weight: 600; color: #002D80; margin-bottom: 12px;">
            Plainteks &nbsp; ➔ &nbsp; [Tahap 1: Caesar] &nbsp; ➔ &nbsp; [Tahap 2: Vigenère] &nbsp; ➔ &nbsp; [Tahap 3: AES-128] &nbsp; ➔ &nbsp; [Tahap 4: Vernam] &nbsp; ➔ &nbsp; Super Cipherteks
        </div>
        <p style="color: #4A709C; font-size: 0.88rem; margin: 0;">
            <b>Proses Dekripsi (Prinsip LIFO):</b> Dilakukan dengan urutan terbalik secara presisi: Vernam Dekripsi ➔ AES Dekripsi ➔ Vigenère Dekripsi ➔ Caesar Dekripsi ➔ Plainteks Asli.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabel Perbandingan Karakteristik Algoritma
    st.markdown("##### Tabel Komparasi Karakteristik Algoritma")
    comp_df = pd.DataFrame([
        {"Algoritma": "Caesar Cipher", "Kategori": "Klasik (Monoalfabetik)", "Tipe Kunci": "Simetris (Angka Shift k)", "Kompleksitas": "O(N)", "Ketahanan": "Rendah (25 Ruang Kunci)", "Fungsi Utama": "Pembelajaran Dasar Substitusi"},
        {"Algoritma": "Vigenère Cipher", "Kategori": "Klasik (Polialfabetik)", "Tipe Kunci": "Simetris (Kata Kunci)", "Kompleksitas": "O(N)", "Ketahanan": "Sedang (Polialfabetik)", "Fungsi Utama": "Pengacakan Frekuensi Karakter"},
        {"Algoritma": "AES-128", "Kategori": "Modern (Cipher Blok)", "Tipe Kunci": "Simetris (128-bit)", "Kompleksitas": "O(N) Blok", "Ketahanan": "Sangat Tinggi (2^128)", "Fungsi Utama": "Kerahasiaan Data Massal"},
        {"Algoritma": "Vernam Cipher", "Kategori": "Modern (Cipher Aliran)", "Tipe Kunci": "Simetris (Keystream Bit/Byte)", "Kompleksitas": "O(N) Bitwise", "Ketahanan": "Sempurna jika OTP (Unbreakable)", "Fungsi Utama": "Kerahasiaan Aliran Data Realtime"},
    ])
    st.dataframe(comp_df, width="stretch", hide_index=True)

# ==============================================================================
# MENU 1 - 5: MODUL KRIPTOGRAFI
# ==============================================================================
elif menu == "Menu 1: Caesar Cipher":
    render_caesar_page()

elif menu == "Menu 2: Vigenère Cipher":
    render_vigenere_page()

elif menu == "Menu 3: AES-128 Block Cipher":
    render_aes_page()

elif menu == "Menu 4: Vernam Stream Cipher":
    render_vernam_page()

elif menu == "Menu 5: Super Enkripsi":
    render_super_page()

# ==============================================================================
# 6. HALAMAN KHUSUS: INFORMASI TIM & KONTRIBUTOR
# ==============================================================================
elif menu == "Informasi Tim & Kontributor":
    st.markdown('<div class="menu-title">Informasi Tim Pengembang</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="menu-desc">Tugas Besar Mata Kuliah Kriptografi • Kelas Informatika H • '
        'Universitas Pembangunan Nasional "Veteran" Yogyakarta.</div>',
        unsafe_allow_html=True
    )

    # Inisialisasi default profil anggota di session state jika belum ada
    if "member_1_name" not in st.session_state:
        st.session_state["member_1_name"] = "Mahasiswa 1"
        st.session_state["member_1_nim"] = "123220001"
    if "member_2_name" not in st.session_state:
        st.session_state["member_2_name"] = "Mahasiswa 2"
        st.session_state["member_2_nim"] = "123220002"
    if "member_3_name" not in st.session_state:
        st.session_state["member_3_name"] = "Mahasiswa 3"
        st.session_state["member_3_nim"] = "123220003"
    if "member_4_name" not in st.session_state:
        st.session_state["member_4_name"] = "Oktavian Prasetya Adi"
        st.session_state["member_4_nim"] = "123220004"
    if "team_class" not in st.session_state:
        st.session_state["team_class"] = "Informatika - Kelas H"

    # Kartu Profil 4 Anggota Tim (Grid 2x2)
    t1, t2 = st.columns(2)
    with t1:
        st.markdown(f"""
        <div class="datain-card">
            <span class="badge-pic">Orang 1</span>
            <span class="badge-category">Kriptografi Klasik</span>
            <h3 style="margin: 8px 0 2px 0; color: #1E3A5F; font-family: 'Outfit';">{st.session_state['member_1_name']}</h3>
            <p style="color: #4A709C; font-size: 0.88rem; margin-bottom: 12px; font-family: 'JetBrains Mono';">NIM: {st.session_state['member_1_nim']}</p>
            <p style="color: #1E3A5F; font-size: 0.92rem; line-height: 1.5; margin-bottom: 6px;">
                <b>Tugas Utama:</b> Caesar Cipher (Enkripsi & Dekripsi)<br>
                <b>Tugas Tambahan:</b> Antarmuka Menu 1 & Kriptanalisis Brute-Force
            </p>
            <small style="color: #4A709C;">File Pengerjaan: <code>modules/menu1_caesar.py</code></small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="datain-card">
            <span class="badge-pic">Orang 3</span>
            <span class="badge-category">Kriptografi Modern</span>
            <h3 style="margin: 8px 0 2px 0; color: #1E3A5F; font-family: 'Outfit';">{st.session_state['member_3_name']}</h3>
            <p style="color: #4A709C; font-size: 0.88rem; margin-bottom: 12px; font-family: 'JetBrains Mono';">NIM: {st.session_state['member_3_nim']}</p>
            <p style="color: #1E3A5F; font-size: 0.92rem; line-height: 1.5; margin-bottom: 6px;">
                <b>Tugas Utama:</b> AES-128 Block Cipher (Enkripsi & Dekripsi CBC)<br>
                <b>Tugas Tambahan:</b> Antarmuka Menu 3 & Visualisasi State Matrix 4x4
            </p>
            <small style="color: #4A709C;">File Pengerjaan: <code>modules/menu3_aes.py</code></small>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown(f"""
        <div class="datain-card">
            <span class="badge-pic">Orang 2</span>
            <span class="badge-category">Kriptografi Klasik</span>
            <h3 style="margin: 8px 0 2px 0; color: #1E3A5F; font-family: 'Outfit';">{st.session_state['member_2_name']}</h3>
            <p style="color: #4A709C; font-size: 0.88rem; margin-bottom: 12px; font-family: 'JetBrains Mono';">NIM: {st.session_state['member_2_nim']}</p>
            <p style="color: #1E3A5F; font-size: 0.92rem; line-height: 1.5; margin-bottom: 6px;">
                <b>Tugas Utama:</b> Vigenère Cipher (Enkripsi & Dekripsi Polialfabetik)<br>
                <b>Tugas Tambahan:</b> Antarmuka Menu 2 & Matriks Tabula Recta 26x26
            </p>
            <small style="color: #4A709C;">File Pengerjaan: <code>modules/menu2_vigenere.py</code></small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="datain-card">
            <span class="badge-pic">Orang 4</span>
            <span class="badge-category">Kriptografi Modern - Cipher Aliran</span>
            <h3 style="margin: 8px 0 2px 0; color: #1E3A5F; font-family: 'Outfit';">{st.session_state['member_4_name']}</h3>
            <p style="color: #4A709C; font-size: 0.88rem; margin-bottom: 12px; font-family: 'JetBrains Mono';">NIM: {st.session_state['member_4_nim']}</p>
            <p style="color: #1E3A5F; font-size: 0.92rem; line-height: 1.5; margin-bottom: 6px;">
                <b>Tugas Utama:</b> Vernam Stream Cipher (Enkripsi & Dekripsi Bitwise XOR)<br>
                <b>Tugas Tambahan:</b> Antarmuka Menu 4 & Simulasi Aliran Bit One-Time Pad
            </p>
            <small style="color: #4A709C;">File Pengerjaan: <code>modules/menu4_vernam.py</code></small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Form Pengeditan Identitas Anggota Kelompok
    with st.expander("Perbarui Identitas Nama & NIM Kelompok", expanded=False):
        st.caption("Masukkan nama dan NIM lengkap anggota tim Anda untuk keperluan presentasi dan penilaian:")
        f1, f2 = st.columns(2)
        with f1:
            st.session_state["member_1_name"] = st.text_input("Nama Lengkap (Orang 1):", value=st.session_state["member_1_name"])
            st.session_state["member_1_nim"] = st.text_input("NIM (Orang 1):", value=st.session_state["member_1_nim"])
            st.session_state["member_3_name"] = st.text_input("Nama Lengkap (Orang 3):", value=st.session_state["member_3_name"])
            st.session_state["member_3_nim"] = st.text_input("NIM (Orang 3):", value=st.session_state["member_3_nim"])
        with f2:
            st.session_state["member_2_name"] = st.text_input("Nama Lengkap (Orang 2):", value=st.session_state["member_2_name"])
            st.session_state["member_2_nim"] = st.text_input("NIM (Orang 2):", value=st.session_state["member_2_nim"])
            st.session_state["member_4_name"] = st.text_input("Nama Lengkap (Orang 4):", value=st.session_state["member_4_name"])
            st.session_state["member_4_nim"] = st.text_input("NIM (Orang 4):", value=st.session_state["member_4_nim"])

        st.session_state["team_class"] = st.text_input("Kelas Perkuliahan:", value=st.session_state["team_class"])
        if st.button("Simpan Perubahan Identitas"):
            st.success("Identitas anggota tim berhasil diperbarui!")

st.divider()
st.caption("Tugas Mata Kuliah Kriptografi • UPN Veteran Yogyakarta • Program Studi Informatika")
