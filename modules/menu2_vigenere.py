import streamlit as st
import pandas as pd
import string

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA VIGENÈRE CIPHER (ORANG 2)
# ==============================================================================
def get_tabula_recta():
    alphabet = string.ascii_uppercase
    matrix = [list(alphabet[i:] + alphabet[:i]) for i in range(26)]
    return alphabet, matrix

def clean_key(key: str) -> str:
    filtered = "".join([c for c in key if c.isalpha()])
    return filtered.upper() if filtered else "A"

def vigenere_encrypt(text: str, key: str):
    key_clean = clean_key(key)
    result = []
    steps = []
    key_len = len(key_clean)
    key_ptr = 0

    for idx, char in enumerate(text):
        if char.isalpha():
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            p_val = ord(char) - base
            k_char = key_clean[key_ptr % key_len]
            k_val = ord(k_char) - ord('A')
            c_val = (p_val + k_val) % 26
            c_char = chr(c_val + base)
            result.append(c_char)
            steps.append({
                "index": idx + 1, "p_char": char, "p_val": p_val,
                "k_char": k_char, "k_val": k_val,
                "formula": f"({p_val} + {k_val}) mod 26 = {c_val}",
                "c_val": c_val, "c_char": c_char
            })
            key_ptr += 1
        else:
            result.append(char)
            steps.append({
                "index": idx + 1, "p_char": repr(char)[1:-1] if char == ' ' else char,
                "p_val": "-", "k_char": "-", "k_val": "-", "formula": "Tetap",
                "c_val": "-", "c_char": repr(char)[1:-1] if char == ' ' else char
            })
    return "".join(result), steps

def vigenere_decrypt(ciphertext: str, key: str):
    key_clean = clean_key(key)
    result = []
    steps = []
    key_len = len(key_clean)
    key_ptr = 0

    for idx, char in enumerate(ciphertext):
        if char.isalpha():
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            c_val = ord(char) - base
            k_char = key_clean[key_ptr % key_len]
            k_val = ord(k_char) - ord('A')
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + base)
            result.append(p_char)
            steps.append({
                "index": idx + 1, "c_char": char, "c_val": c_val,
                "k_char": k_char, "k_val": k_val,
                "formula": f"({c_val} - {k_val} + 26) mod 26 = {p_val}",
                "p_val": p_val, "p_char": p_char
            })
            key_ptr += 1
        else:
            result.append(char)
            steps.append({
                "index": idx + 1, "c_char": repr(char)[1:-1] if char == ' ' else char,
                "c_val": "-", "k_char": "-", "k_val": "-", "formula": "Tetap",
                "p_val": "-", "p_char": repr(char)[1:-1] if char == ' ' else char
            })
    return "".join(result), steps

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (ORANG 2)
# ==============================================================================
def render_vigenere_page():
    render_header(
        "2️⃣ Vigenère Cipher",
        "Substitusi Polialfabetik dengan Kata Kunci Berulang dan Tabula Recta",
        "Penanggung Jawab: Orang 2",
        "Kriptografi Klasik",
        "badge-p2"
    )

    tab_enc, tab_dec, tab_trace, tab_tabula, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi Step-by-Step", "📊 Tabula Recta", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            p_vig = st.text_area("Masukkan Plaintext:", value="BELAJAR KRIPTOGRAFI UNTUK INDONESIA MAJU", height=120, key="v_plain")
            k_vig = st.text_input("Kata Kunci (Alphabet Key):", value="INFORMATIKA", key="v_key_enc")
            btn_v_enc = st.button("🔒 Enkripsi Sekarang", key="v_btn_enc", use_container_width=True)
        with c2:
            if p_vig and k_vig:
                c_vig, steps_v = vigenere_encrypt(p_vig, k_vig)
                st.session_state["v_steps"] = steps_v
                st.text_area("Hasil Ciphertext:", value=c_vig, height=120)
                st.info(f"Panjang Teks: **{len(c_vig)}** | Kunci Diulang: **{k_vig.upper()}**")
                st.code("Formula: C_i = (P_i + K_i) mod 26")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            c_vig_in = st.text_area("Masukkan Ciphertext:", value="", height=120, key="v_cipher_in")
            k_vig_dec = st.text_input("Kata Kunci (Alphabet Key):", value="INFORMATIKA", key="v_key_dec")
            btn_v_dec = st.button("🔓 Dekripsi Sekarang", key="v_btn_dec", use_container_width=True)
        with c2:
            if c_vig_in and k_vig_dec:
                p_rec, _ = vigenere_decrypt(c_vig_in, k_vig_dec)
                st.text_area("Hasil Plaintext:", value=p_rec, height=120)
                st.success("Dekripsi Vigenère Selesai!")
                st.code("Formula: P_i = (C_i - K_i + 26) mod 26")

    with tab_trace:
        st.markdown("#### 🔍 Pelacakan Per Huruf & Kunci")
        if "v_steps" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["v_steps"]), use_container_width=True, height=350)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk memuat tabel pelacakan.")

    with tab_tabula:
        st.markdown("#### 📊 Bujursangkar Vigenère (Tabula Recta 26×26)")
        alpha, matrix = get_tabula_recta()
        st.dataframe(pd.DataFrame(matrix, index=list(alpha), columns=list(alpha)), use_container_width=True, height=420)

    with tab_theory:
        st.markdown("""
        ### 📖 Teori Vigenère Cipher (Materi 4)
        * **Kategori**: Cipher Substitusi Abjad-Majemuk (*Polyalphabetic Substitution*).
        * **Rumus Matematis**:
          $$C_i = (P_i + K_{i \\bmod m}) \\pmod{26}, \\quad P_i = (C_i - K_{i \\bmod m} + 26) \\pmod{26}$$
        * **Keunggulan**: Mengaburkan analisis frekuensi abjad tunggal.
        """)

# Standalone runner untuk pengujian mandiri Orang 2
if __name__ == "__main__":
    st.set_page_config(page_title="Vigenère Cipher - Orang 2", page_icon="🔐", layout="wide")
    load_global_css()
    render_vigenere_page()
