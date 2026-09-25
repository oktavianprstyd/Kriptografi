import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA VIGENÈRE CIPHER
# Penanggung Jawab: Orang 2
# ==============================================================================

def vigenere_encrypt(plaintext: str, key: str):
    """
    TODO: Tuliskan logika enkripsi Vigenère Cipher di sini.
    Rumus: C_i = (P_i + K_i) mod 26
    Kembalikan: (ciphertext, steps)
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    ciphertext = f"[HASIL ENKRIPSI VIGENERE: {plaintext} (Kunci: {key})]"
    steps = [
        {"No": 1, "Plainteks": "P", "Kunci": "K", "Rumus": "(P + K) mod 26", "Cipher": "C"}
    ]
    return ciphertext, steps

def vigenere_decrypt(ciphertext: str, key: str):
    """
    TODO: Tuliskan logika dekripsi Vigenère Cipher di sini.
    Rumus: P_i = (C_i - K_i + 26) mod 26
    Kembalikan: (plaintext, steps)
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    plaintext = f"[HASIL DEKRIPSI VIGENERE: {ciphertext} (Kunci: {key})]"
    steps = []
    return plaintext, steps

def get_tabula_recta():
    """
    TODO: Buat matriks Tabula Recta 26x26 untuk visualisasi.
    """
    import string
    alphabet = string.ascii_uppercase
    matrix = [list(alphabet[i:] + alphabet[:i]) for i in range(26)]
    return alphabet, matrix

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# Penanggung Jawab: Orang 2
# ==============================================================================

def render_vigenere_page():
    render_header(
        title="2️⃣ Vigenère Cipher",
        subtitle="Substitusi Polialfabetik dengan Kata Kunci Berulang dan Tabula Recta",
        person_badge="Penanggung Jawab: Orang 2",
        algo_badge="Kriptografi Klasik",
        badge_class="badge-p2"
    )

    tab_enc, tab_dec, tab_trace, tab_tabula, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi Step-by-Step", "📊 Tabula Recta", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📝 Input Teks & Kunci")
            p_vig = st.text_area("Masukkan Plaintext:", value="BELAJAR KRIPTOGRAFI", height=120, key="v_plain")
            k_vig = st.text_input("Kata Kunci (Alphabet):", value="INFORMATIKA", key="v_key_enc")
            btn_v_enc = st.button("🔒 Enkripsi Sekarang", key="v_btn_enc", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Enkripsi")
            if btn_v_enc:
                c_vig, steps_v = vigenere_encrypt(p_vig, k_vig)
                st.session_state["v_steps"] = steps_v
                st.text_area("Ciphertext:", value=c_vig, height=120)
                st.success("Enkripsi Vigenère berhasil diproses!")
            else:
                st.info("Klik tombol 'Enkripsi Sekarang' untuk melihat hasil.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📥 Input Ciphertext & Kunci")
            c_vig_in = st.text_area("Masukkan Ciphertext:", value="", height=120, key="v_cipher_in")
            k_vig_dec = st.text_input("Kata Kunci (Alphabet):", value="INFORMATIKA", key="v_key_dec")
            btn_v_dec = st.button("🔓 Dekripsi Sekarang", key="v_btn_dec", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Dekripsi")
            if btn_v_dec:
                p_rec, _ = vigenere_decrypt(c_vig_in, k_vig_dec)
                st.text_area("Plaintext Rekonstruksi:", value=p_rec, height=120)
                st.success("Dekripsi Vigenère berhasil diproses!")
            else:
                st.info("Klik tombol 'Dekripsi Sekarang' untuk melihat hasil.")

    with tab_trace:
        st.markdown("#### 🔍 Pelacakan Per Huruf & Kunci")
        if "v_steps" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["v_steps"]), use_container_width=True)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk melihat langkah kalkulasi.")

    with tab_tabula:
        st.markdown("#### 📊 Bujursangkar Vigenère (Tabula Recta 26×26)")
        alpha, matrix = get_tabula_recta()
        st.dataframe(pd.DataFrame(matrix, index=list(alpha), columns=list(alpha)), use_container_width=True, height=400)

    with tab_theory:
        st.markdown("""
        ### 📖 Teori Vigenère Cipher (Materi 4)
        * **Kategori**: Cipher Substitusi Abjad-Majemuk (*Polyalphabetic Substitution*).
        * **Rumus**:
          $$C_i = (P_i + K_{i \\bmod m}) \\pmod{26}, \\quad P_i = (C_i - K_{i \\bmod m} + 26) \\pmod{26}$$
        """)

# Standalone runner: Orang 2 bisa langsung menjalankan file ini saja
if __name__ == "__main__":
    st.set_page_config(page_title="Vigenère Cipher - Orang 2", page_icon="🔐", layout="wide")
    load_global_css()
    render_vigenere_page()
