import streamlit as st
import pandas as pd

from modules.ui_helper import load_global_css
from modules.menu1_caesar import render_caesar_page
from modules.menu2_vigenere import render_vigenere_page
from modules.menu3_aes import render_aes_page
from modules.menu4_rsa import render_rsa_page
from modules.menu5_super import render_super_page

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Aplikasi Kriptografi - UPN 'Veteran' Yogyakarta",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Memuat CSS Terpadu
load_global_css()

# ==============================================================================
# SIDEBAR TIM & NAVIGASI
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_UPN_Veteran_Yogyakarta.png", width=90)
    st.markdown("### **UPN 'Veteran' Yogyakarta**")
    st.markdown("**Program Studi Informatika**")
    st.markdown("*Tugas Mata Kuliah Kriptografi*")
    st.divider()

    menu = st.radio(
        "Pilih Menu Navigasi:",
        [
            "🏠 Beranda & Pembagian Tim",
            "1️⃣ Menu 1: Caesar Cipher (Orang 1)",
            "2️⃣ Menu 2: Vigenère Cipher (Orang 2)",
            "3️⃣ Menu 3: AES-128 Block Cipher (Orang 3)",
            "4️⃣ Menu 4: RSA Asymmetric Cipher (Orang 4)",
            "5️⃣ Menu 5: Super Enkripsi (Kolaborasi Tim)"
        ]
    )

    st.divider()
    with st.expander("👥 Tim Pengembang (4 Orang)", expanded=True):
        st.markdown("**Orang 1: Caesar Cipher**")
        st.text_input("Nama / NIM 1", value="Mahasiswa 1 (NIM)", key="member_1")
        st.markdown("**Orang 2: Vigenère Cipher**")
        st.text_input("Nama / NIM 2", value="Mahasiswa 2 (NIM)", key="member_2")
        st.markdown("**Orang 3: AES-128**")
        st.text_input("Nama / NIM 3", value="Mahasiswa 3 (NIM)", key="member_3")
        st.markdown("**Orang 4: RSA**")
        st.text_input("Nama / NIM 4", value="Mahasiswa 4 (NIM)", key="member_4")
        st.divider()
        st.text_input("Kelas", value="Informatika - Kelas H", key="group_class")
    
    st.caption("Aplikasi Kriptografi Terintegrasi Python Streamlit")

# ==============================================================================
# ROUTER MENU UTAMA (PANGGIL FUNGSI MODUL MASING-MASING)
# ==============================================================================
if menu == "🏠 Beranda & Pembagian Tim":
    st.markdown('<div class="menu-title">🔐 Aplikasi Enkripsi & Dekripsi Kriptografi</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-desc">Implementasi 5 Menu Terpadu: 2 Kriptografi Klasik, 2 Kriptografi Modern, dan Super Enkripsi dengan Visualisasi Step-by-Step</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("### 📋 Pembagian Tugas Tim 4 Orang")
        team_df = pd.DataFrame([
            {"Orang": "Orang 1", "Tugas Utama": "Caesar Cipher: enkripsi + dekripsi", "Tugas Tambahan": "Tampilan Menu 1 + testing Caesar", "File": "modules/menu1_caesar.py"},
            {"Orang": "Orang 2", "Tugas Utama": "Vigenère Cipher: enkripsi + dekripsi", "Tugas Tambahan": "Tampilan Menu 2 + testing Vigenère", "File": "modules/menu2_vigenere.py"},
            {"Orang": "Orang 3", "Tugas Utama": "AES: enkripsi + dekripsi", "Tugas Tambahan": "Tampilan Menu 3 + testing AES", "File": "modules/menu3_aes.py"},
            {"Orang": "Orang 4", "Tugas Utama": "RSA: enkripsi + dekripsi", "Tugas Tambahan": "Tampilan Menu 4 + testing RSA", "File": "modules/menu4_rsa.py"},
        ])
        st.dataframe(team_df, use_container_width=True, hide_index=True)

        st.markdown("""
        #### 🎯 Menu ke-5: Super Enkripsi
        Mengintegrasikan seluruh modul yang dibuat oleh **Orang 1 s/d Orang 4** menjadi satu pipeline berantai:
        $$\\text{Plainteks} \\xrightarrow{\\text{Caesar (P1)}} C_1 \\xrightarrow{\\text{Vigenère (P2)}} C_2 \\xrightarrow{\\text{AES (P3)}} C_3 \\xrightarrow{\\text{RSA (P4)}} \\text{Super Ciphertext}$$
        """)

    with col2:
        st.markdown("""
        <div class="card-box">
            <h4>💡 Cara Kerja Tim di GitHub</h4>
            <ul>
                <li>Setiap anggota cukup mengedit <b>file miliknya sendiri di folder <code>modules/</code></b>.</li>
                <li>Bisa ditest sendiri dengan menjalankan: <br><code>streamlit run modules/menuX_xxx.py</code></li>
                <li>Bebas dari bentrok Git (*Zero merge conflict*).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "1️⃣ Menu 1: Caesar Cipher (Orang 1)":
    render_caesar_page()

elif menu == "2️⃣ Menu 2: Vigenère Cipher (Orang 2)":
    render_vigenere_page()

elif menu == "3️⃣ Menu 3: AES-128 Block Cipher (Orang 3)":
    render_aes_page()

elif menu == "4️⃣ Menu 4: RSA Asymmetric Cipher (Orang 4)":
    render_rsa_page()

elif menu == "5️⃣ Menu 5: Super Enkripsi (Kolaborasi Tim)":
    render_super_page()

st.divider()
st.caption("© 2026 Tugas Besar Kriptografi • UPN 'Veteran' Yogyakarta • Tim 4 Orang")
