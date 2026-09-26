import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css, render_mode_selector
except ImportError:
    from ui_helper import render_header, load_global_css, render_mode_selector

# ==============================================================================
# BAGIAN 1: LOGIKA VIGENÈRE CIPHER
# Penanggung Jawab: Orang 2
# ==============================================================================

def vigenere_encrypt(plaintext: str, key: str):
    """
    Melakukan enkripsi Vigenère Cipher.
    Rumus: C_i = (P_i + K_i) mod 26
    Kembalikan: (ciphertext, steps)
    """
    # Bersihkan input: hanya huruf alfabet, uppercase
    plaintext_clean = ''.join(ch for ch in plaintext.upper() if ch.isalpha())
    key_clean = ''.join(ch for ch in key.upper() if ch.isalpha())

    if not key_clean:
        raise ValueError("Kunci harus berisi minimal satu huruf alfabet.")

    ciphertext = ""
    steps = []

    for i, p_char in enumerate(plaintext_clean):
        k_char = key_clean[i % len(key_clean)]
        p_val = ord(p_char) - ord('A')
        k_val = ord(k_char) - ord('A')
        c_val = (p_val + k_val) % 26
        c_char = chr(c_val + ord('A'))
        ciphertext += c_char

        steps.append({
            "No": i + 1,
            "Plainteks": p_char,
            "Kunci": k_char,
            "P (angka)": p_val,
            "K (angka)": k_val,
            "Rumus": f"({p_val} + {k_val}) mod 26 = {c_val}",
            "Hasil Sandi": c_char
        })

    return ciphertext, steps

def vigenere_decrypt(ciphertext: str, key: str):
    """
    Melakukan dekripsi Vigenère Cipher.
    Rumus: P_i = (C_i - K_i + 26) mod 26
    Kembalikan: (plaintext, steps)
    """
    ciphertext_clean = ''.join(ch for ch in ciphertext.upper() if ch.isalpha())
    key_clean = ''.join(ch for ch in key.upper() if ch.isalpha())

    if not key_clean:
        raise ValueError("Kunci harus berisi minimal satu huruf alfabet.")

    plaintext = ""
    steps = []

    for i, c_char in enumerate(ciphertext_clean):
        k_char = key_clean[i % len(key_clean)]
        c_val = ord(c_char) - ord('A')
        k_val = ord(k_char) - ord('A')
        p_val = (c_val - k_val + 26) % 26
        p_char = chr(p_val + ord('A'))
        plaintext += p_char

        steps.append({
            "No": i + 1,
            "Cipherteks": c_char,
            "Kunci": k_char,
            "C (angka)": c_val,
            "K (angka)": k_val,
            "Rumus": f"({c_val} - {k_val} + 26) mod 26 = {p_val}",
            "Hasil Plainteks": p_char
        })
    
    return plaintext, steps

def get_tabula_recta():
    """Matriks Tabula Recta 26x26 untuk visualisasi."""
    import string
    alphabet = string.ascii_uppercase
    matrix = [list(alphabet[i:] + alphabet[:i]) for i in range(26)]
    return alphabet, matrix

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_vigenere_page():
    render_header(
        title="Menu 2: Vigenère Cipher",
        subtitle="Substitusi Polialfabetik dengan Kata Kunci Berulang dan Tabula Recta",
        pic_name="Penanggung Jawab: Orang 2",
        category="Kriptografi Klasik"
    )

    tab_main, tab_trace, tab_tabula, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pelacakan Proses (Step-by-Step)",
        "Tabel Tabula Recta",
        "Teori & Formula"
    ])

    with tab_main:
        mode = render_mode_selector(session_state_key="v_mode", key_prefix="vig")

        if mode == "Enkripsi Pesan":
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Plainteks & Kata Kunci")
                p_vig = st.text_area("Masukkan teks plainteks:", value="BELAJAR KRIPTOGRAFI", height=110, key="v_plain")
                k_vig = st.text_input("Kata Kunci (Huruf Alfabet):", value="INFORMATIKA", key="v_key_enc")
                btn_v_enc = st.button("Jalankan Enkripsi Vigenère", key="v_btn_enc", use_container_width=True, type="primary")
            with col2:
                st.markdown("##### Hasil Enkripsi")
                if btn_v_enc:
                    c_vig, steps_v = vigenere_encrypt(p_vig, k_vig)
                    st.session_state["v_steps"] = steps_v
                    st.text_area("Teks Cipherteks:", value=c_vig, height=110)
                    st.success("Proses enkripsi Vigenère selesai diproses.")
                else:
                    st.info("Tekan tombol 'Jalankan Enkripsi Vigenère' untuk memproses teks.")

        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Cipherteks & Kata Kunci")
                c_vig_in = st.text_area("Masukkan teks cipherteks:", value="", height=110, key="v_cipher_in")
                k_vig_dec = st.text_input("Kata Kunci (Huruf Alfabet):", value="INFORMATIKA", key="v_key_dec")
                btn_v_dec = st.button("Jalankan Dekripsi Vigenère", key="v_btn_dec", use_container_width=True, type="primary")
            with col2:
                st.markdown("##### Hasil Dekripsi")
                if btn_v_dec:
                    p_rec, _ = vigenere_decrypt(c_vig_in, k_vig_dec)
                    st.text_area("Teks Plainteks Rekonstruksi:", value=p_rec, height=110)
                    st.success("Proses dekripsi Vigenère selesai diproses.")
                else:
                    st.info("Tekan tombol 'Jalankan Dekripsi Vigenère' untuk memproses teks.")

    with tab_trace:
        st.markdown("##### Pelacakan Transformasi Per Karakter dan Kunci")
        if "v_steps" in st.session_state and st.session_state["v_steps"]:
            st.dataframe(pd.DataFrame(st.session_state["v_steps"]), use_container_width=True)
        else:
            st.info("Lakukan proses enkripsi atau dekripsi terlebih dahulu untuk memuat langkah.")

    with tab_tabula:
        st.markdown("##### Matriks Bujursangkar Vigenère (Tabula Recta 26×26)")
        alpha, matrix = get_tabula_recta()
        st.dataframe(pd.DataFrame(matrix, index=list(alpha), columns=list(alpha)), use_container_width=True, height=420)

    with tab_theory:
        st.markdown("##### Teori & Formula Vigenère Cipher")
        st.markdown("""
        **Vigenère Cipher** adalah algoritma substitusi polialfabetik (*polyalphabetic substitution*) 
        yang menggunakan kata kunci berulang untuk menentukan besar pergeseran pada setiap karakter teks terang.

        * **Formula Enkripsi**:
          $$C_i = (P_i + K_{i \\bmod m}) \\pmod{26}$$

        * **Formula Dekripsi**:
          $$P_i = (C_i - K_{i \\bmod m} + 26) \\pmod{26}$$

        **Keterangan Notasi:**
        * $P_i$ = Indeks posisi huruf plainteks ($0 - 25$)
        * $K_i$ = Indeks posisi huruf kunci pada iterasi ke-$i$
        * $m$ = Panjang karakter kata kunci
        """)

# Standalone runner: Orang 2
if __name__ == "__main__":
    st.set_page_config(page_title="Vigenère Cipher - Orang 2", layout="wide")
    load_global_css()
    render_vigenere_page()
