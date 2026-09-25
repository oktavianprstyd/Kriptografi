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
# BAGIAN 1: LOGIKA PIPELINE SUPER ENKRIPSI (KOLABORASI 4 ORANG)
# ==============================================================================
def super_encrypt(plaintext: str, caesar_shift: int, vigenere_key: str, aes_key: str, rsa_e: int = 17, rsa_n: int = 3233):
    stages = []

    # 1. Caesar (Orang 1)
    c_out, _ = caesar_encrypt(plaintext, caesar_shift)
    stages.append({
        "stage": 1, "algo": "Caesar Cipher", "pic": "Orang 1",
        "key": f"k = {caesar_shift}", "output": c_out
    })

    # 2. Vigenère (Orang 2)
    v_out, _ = vigenere_encrypt(c_out, vigenere_key)
    stages.append({
        "stage": 2, "algo": "Vigenère Cipher", "pic": "Orang 2",
        "key": f"Kunci = '{vigenere_key}'", "output": v_out
    })

    # 3. AES-128 (Orang 3)
    aes_res = aes_encrypt(v_out.encode('utf-8'), aes_key, mode="CBC")
    stages.append({
        "stage": 3, "algo": "AES-128 (CBC)", "pic": "Orang 3",
        "key": f"Kunci = '{aes_key}'", "output": aes_res["hex_str"]
    })

    # 4. RSA (Orang 4)
    _, rsa_str, _ = rsa_encrypt(aes_res["hex_str"], rsa_e, rsa_n)
    stages.append({
        "stage": 4, "algo": "RSA Cipher", "pic": "Orang 4",
        "key": f"(e={rsa_e}, n={rsa_n})", "output": rsa_str
    })

    return {"final_cipher": rsa_str, "stages": stages}

def super_decrypt(ciphertext_input: str, caesar_shift: int, vigenere_key: str, aes_key: str, rsa_d: int = 2753, rsa_n: int = 3233):
    stages = []

    # 1. Dekripsi RSA (Orang 4)
    rec_hex, _ = rsa_decrypt(ciphertext_input, rsa_d, rsa_n)
    stages.append({"stage": 1, "algo": "Dekripsi RSA", "pic": "Orang 4", "output": rec_hex})

    # 2. Dekripsi AES-128 (Orang 3)
    aes_bytes = bytes.fromhex(rec_hex.strip())
    d_aes = aes_decrypt(aes_bytes, aes_key, mode="CBC")
    stages.append({"stage": 2, "algo": "Dekripsi AES-128", "pic": "Orang 3", "output": d_aes["text"]})

    # 3. Dekripsi Vigenère (Orang 2)
    rec_c, _ = vigenere_decrypt(d_aes["text"], vigenere_key)
    stages.append({"stage": 3, "algo": "Dekripsi Vigenère", "pic": "Orang 2", "output": rec_c})

    # 4. Dekripsi Caesar (Orang 1)
    original, _ = caesar_decrypt(rec_c, caesar_shift)
    stages.append({"stage": 4, "algo": "Dekripsi Caesar", "pic": "Orang 1", "output": original})

    return {"recovered_plaintext": original, "stages": stages}

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# ==============================================================================
def render_super_page():
    render_header(
        "5️⃣ Super Enkripsi (Kolaborasi Tim)",
        "Pipeline Terpadu 4 Tahap: Caesar ➔ Vigenère ➔ AES-128 ➔ RSA",
        "Penanggung Jawab: Seluruh Tim (Orang 1 s/d 4)",
        "Super Enkripsi",
        "badge-super"
    )

    tab_enc, tab_dec, tab_pipe, tab_theory = st.tabs([
        "🔒 Super Enkripsi", "🔓 Super Dekripsi", "🔄 Visualisasi Pipeline Bertingkat", "📖 Teori Super Enkripsi"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📝 Plainteks & Parameter Kunci 4 Orang")
            plain_super = st.text_area("Plainteks Asli:", value="BELAJAR KRIPTOGRAFI UNTUK INDONESIA MERDEKA DAN MAJU", height=90, key="sup_plain")
            k1, k2 = st.columns(2)
            with k1:
                k_c = st.number_input("Kunci Caesar (P1):", 1, 25, 18, key="sup_kc")
                k_aes_sup = st.text_input("Kunci AES-128 (P3):", value="KunciAESSuper128", key="sup_kaes")
            with k2:
                k_v = st.text_input("Kunci Vigenère (P2):", value="INFORMATIKA", key="sup_kv")
                k_rsa_e = st.number_input("RSA e (P4):", value=17, key="sup_ke")
                k_rsa_n = st.number_input("RSA n (P4):", value=3233, key="sup_kn")

            btn_sup_enc = st.button("🚀 Jalankan Super Enkripsi 4 Tahap", key="sup_btn_enc", use_container_width=True)

        with c2:
            if plain_super:
                sup_res = super_encrypt(plain_super, k_c, k_v, k_aes_sup, k_rsa_e, k_rsa_n)
                st.session_state["sup_res"] = sup_res
                st.markdown("##### 🎯 Hasil Akhir Super Ciphertext")
                st.text_area("Final Super Ciphertext (Deret Sandi RSA):", value=sup_res["final_cipher"], height=140)
                st.success("✅ Seluruh 4 Algoritma Berhasil Dieksekusi Beruntun!")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📥 Ciphertext & Parameter Kunci Pembalik")
            def_c = st.session_state["sup_res"]["final_cipher"] if "sup_res" in st.session_state else ""
            c_sup_in = st.text_area("Super Ciphertext Input:", value=def_c, height=90, key="sup_dec_in")

            k1, k2 = st.columns(2)
            with k1:
                d_c = st.number_input("Kunci Caesar (P1):", 1, 25, 18, key="sup_dec_kc")
                d_aes = st.text_input("Kunci AES-128 (P3):", value="KunciAESSuper128", key="sup_dec_kaes")
            with k2:
                d_v = st.text_input("Kunci Vigenère (P2):", value="INFORMATIKA", key="sup_dec_kv")
                d_rsa_d = st.number_input("RSA d (P4):", value=2753, key="sup_dec_kd")
                d_rsa_n = st.number_input("RSA n (P4):", value=3233, key="sup_dec_kn")

            btn_sup_dec = st.button("🔓 Jalankan Super Dekripsi", key="sup_btn_dec", use_container_width=True)

        with c2:
            if c_sup_in:
                try:
                    dec_sup = super_decrypt(c_sup_in, d_c, d_v, d_aes, d_rsa_d, d_rsa_n)
                    st.session_state["sup_dec"] = dec_sup
                    st.markdown("##### 🎯 Hasil Plainteks Rekonstruksi")
                    st.text_area("Original Plaintext:", value=dec_sup["recovered_plaintext"], height=140)
                    st.success("✅ Dekripsi Super Berhasil Memulihkan Pesan Asli!")
                except Exception as e:
                    st.error(f"Gagal mendekripsi: {str(e)}")

    with tab_pipe:
        st.markdown("#### 🔄 Tabel Transformasi di Setiap Stasiun Pipeline")
        if "sup_res" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["sup_res"]["stages"]), use_container_width=True)
        else:
            st.info("Jalankan Super Enkripsi untuk memuat pelacakan transformasi.")

    with tab_theory:
        st.markdown("""
        ### 📖 Konsep Super Enkripsi Terpadu (Materi 3 Slide 51)
        * **Kombinasi Algoritma**: Menggabungkan kekuatan cipher klasik (substitusi abjad) dan cipher modern (cipher blok AES & asimetris RSA).
        * **Alur Enkripsi**:
          $$\\text{Plainteks} \\xrightarrow{\\text{Caesar}} C_1 \\xrightarrow{\\text{Vigenère}} C_2 \\xrightarrow{\\text{AES-128}} C_3 \\xrightarrow{\\text{RSA}} \\text{Final Ciphertext}$$
        * **Alur Dekripsi (Prinsip LIFO)**:
          $$\\text{Final Ciphertext} \\xrightarrow{\\text{RSA}^{-1}} C_3 \\xrightarrow{\\text{AES}^{-1}} C_2 \\xrightarrow{\\text{Vigenère}^{-1}} C_1 \\xrightarrow{\\text{Caesar}^{-1}} \\text{Plainteks}$$
        """)

# Standalone runner
if __name__ == "__main__":
    st.set_page_config(page_title="Super Enkripsi", page_icon="🔐", layout="wide")
    load_global_css()
    render_super_page()
