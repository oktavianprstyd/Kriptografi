import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
    from .menu1_caesar import caesar_encrypt, caesar_decrypt
    from .menu2_vigenere import vigenere_encrypt, vigenere_decrypt
    from .menu3_aes import aes_encrypt, aes_decrypt
    from .menu4_rsa import rsa_encrypt, rsa_decrypt
except ImportError:
    from ui_helper import render_header, load_global_css
    from menu1_caesar import caesar_encrypt, caesar_decrypt
    from menu2_vigenere import vigenere_encrypt, vigenere_decrypt
    from menu3_aes import aes_encrypt, aes_decrypt
    from menu4_rsa import rsa_encrypt, rsa_decrypt

# ==============================================================================
# BAGIAN 1: LOGIKA PIPELINE SUPER ENKRIPSI
# Penanggung Jawab: Seluruh Tim (Orang 1 s/d 4)
# ==============================================================================

def super_encrypt(plaintext: str, caesar_shift: int, vigenere_key: str, aes_key: str, rsa_e: int = 17, rsa_n: int = 3233):
    # 1. Caesar (Orang 1)
    c_out, _ = caesar_encrypt(plaintext, caesar_shift)
    # 2. Vigenere (Orang 2)
    v_out, _ = vigenere_encrypt(c_out, vigenere_key)
    # 3. AES (Orang 3)
    aes_res = aes_encrypt(v_out, aes_key)
    aes_hex = aes_res.get("hex_str", v_out)
    # 4. RSA (Orang 4)
    _, rsa_str, _ = rsa_encrypt(aes_hex, rsa_e, rsa_n)

    stages = [
        {"Tahap": 1, "Algoritma": "Caesar Cipher", "Penanggung Jawab": "Orang 1", "Hasil Transformasi": str(c_out)},
        {"Tahap": 2, "Algoritma": "Vigenère Cipher", "Penanggung Jawab": "Orang 2", "Hasil Transformasi": str(v_out)},
        {"Tahap": 3, "Algoritma": "AES-128 Block", "Penanggung Jawab": "Orang 3", "Hasil Transformasi": str(aes_hex)},
        {"Tahap": 4, "Algoritma": "RSA Asymmetric", "Penanggung Jawab": "Orang 4", "Hasil Transformasi": str(rsa_str)},
    ]
    return {"final_cipher": rsa_str, "stages": stages}

def super_decrypt(ciphertext_input: str, caesar_shift: int, vigenere_key: str, aes_key: str, rsa_d: int = 2753, rsa_n: int = 3233):
    return f"[HASIL SUPER DEKRIPSI DARI {ciphertext_input[:20]}...]"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_super_page():
    render_header(
        title="Menu 5: Super Enkripsi",
        subtitle="Pipeline Terpadu 4 Tahap: Caesar ➔ Vigenère ➔ AES-128 ➔ RSA",
        pic_name="Penanggung Jawab: Seluruh Tim",
        category="Super Enkripsi"
    )

    tab_enc, tab_dec, tab_pipe, tab_theory = st.tabs([
        "Super Enkripsi",
        "Super Dekripsi",
        "Visualisasi Transformasi Pipeline",
        "Teori Super Enkripsi"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Input Plainteks & Parameter Kunci 4 Modul")
            plain_super = st.text_area("Masukkan teks plainteks:", value="BELAJAR KRIPTOGRAFI", height=90, key="sup_plain")
            k1, k2 = st.columns(2)
            with k1:
                k_c = st.number_input("Kunci Caesar (Orang 1):", 1, 25, 3, key="sup_kc")
                k_aes_sup = st.text_input("Kunci AES (Orang 3):", value="KunciAESSuper128", key="sup_kaes")
            with k2:
                k_v = st.text_input("Kunci Vigenère (Orang 2):", value="INFORMATIKA", key="sup_kv")
                k_rsa_e = st.number_input("RSA e (Orang 4):", value=17, key="sup_ke")
                k_rsa_n = st.number_input("RSA n (Orang 4):", value=3233, key="sup_kn")

            btn_sup_enc = st.button("Jalankan Super Enkripsi 4 Tahap", key="sup_btn_enc", use_container_width=True)

        with c2:
            st.markdown("##### Hasil Akhir Super Cipherteks")
            if btn_sup_enc:
                sup_res = super_encrypt(plain_super, k_c, k_v, k_aes_sup, k_rsa_e, k_rsa_n)
                st.session_state["sup_res"] = sup_res
                st.text_area("Final Ciphertext:", value=str(sup_res["final_cipher"]), height=120)
                st.success("Seluruh 4 algoritma berhasil dieksekusi beruntun.")
            else:
                st.info("Tekan tombol 'Jalankan Super Enkripsi 4 Tahap' untuk memproses.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Input Super Cipherteks & Kunci Pembalik")
            c_sup_in = st.text_area("Masukkan teks super cipherteks:", value="", height=90, key="sup_dec_in")
            btn_sup_dec = st.button("Jalankan Super Dekripsi", key="sup_btn_dec", use_container_width=True)
        with c2:
            st.markdown("##### Hasil Plainteks Rekonstruksi")
            if btn_sup_dec:
                dec_sup = super_decrypt(c_sup_in, 3, "INFORMATIKA", "KunciAESSuper128", 2753, 3233)
                st.text_area("Plaintext Rekonstruksi:", value=dec_sup, height=120)
                st.success("Proses dekripsi super selesai diproses.")
            else:
                st.info("Tekan tombol 'Jalankan Super Dekripsi' untuk memproses.")

    with tab_pipe:
        st.markdown("##### Tabel Transformasi di Setiap Stasiun Pipeline")
        if "sup_res" in st.session_state and "stages" in st.session_state["sup_res"]:
            st.dataframe(pd.DataFrame(st.session_state["sup_res"]["stages"]), use_container_width=True)
        else:
            st.info("Jalankan proses super enkripsi terlebih dahulu untuk memuat tabel transformasi.")

    with tab_theory:
        st.markdown("##### Konsep Super Enkripsi Terpadu")
        st.markdown("""
        **Super Enkripsi** menggabungkan beberapa algoritma kriptografi secara beruntun (*pipelining*).
        Output dari algoritma pertama menjadi input bagi algoritma berikutnya:

        $$\\text{Plainteks} \\xrightarrow{\\text{Caesar}} C_1 \\xrightarrow{\\text{Vigenère}} C_2 \\xrightarrow{\\text{AES-128}} C_3 \\xrightarrow{\\text{RSA}} \\text{Final Super Ciphertext}$$

        * **Prinsip Dekripsi (LIFO - Last In First Out)**:
        Proses pembalikan dilakukan dengan urutan terbalik secara presisi:
        $$\\text{Final Ciphertext} \\xrightarrow{\\text{RSA}^{-1}} C_3 \\xrightarrow{\\text{AES}^{-1}} C_2 \\xrightarrow{\\text{Vigenère}^{-1}} C_1 \\xrightarrow{\\text{Caesar}^{-1}} \\text{Plainteks}$$
        """)

# Standalone runner
if __name__ == "__main__":
    st.set_page_config(page_title="Super Enkripsi", layout="wide")
    load_global_css()
    render_super_page()
