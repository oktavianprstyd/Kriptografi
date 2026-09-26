import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
    from .menu1_caesar import caesar_encrypt, caesar_decrypt
    from .menu2_vigenere import vigenere_encrypt, vigenere_decrypt
    from .menu3_aes import aes_encrypt, aes_decrypt
    from .menu4_vernam import vernam_encrypt, vernam_decrypt
except ImportError:
    from ui_helper import render_header, load_global_css
    from menu1_caesar import caesar_encrypt, caesar_decrypt
    from menu2_vigenere import vigenere_encrypt, vigenere_decrypt
    from menu3_aes import aes_encrypt, aes_decrypt
    from menu4_vernam import vernam_encrypt, vernam_decrypt

# ==============================================================================
# BAGIAN 1: LOGIKA PIPELINE SUPER ENKRIPSI
# Penanggung Jawab: Seluruh Tim (Orang 1 s/d 4)
# ==============================================================================

def super_encrypt(plaintext: str, caesar_shift: int, vigenere_key: str, aes_key: str, vernam_key: str = "VERNAM_SUPER"):
    # 1. Caesar Cipher (Orang 1 - Klasik Monoalfabetik)
    c_out, _ = caesar_encrypt(plaintext, caesar_shift)

    # 2. Vigenère Cipher (Orang 2 - Klasik Polialfabetik)
    v_out, _ = vigenere_encrypt(c_out, vigenere_key)

    # 3. AES-128 Block Cipher (Orang 3 - Modern Blok)
    aes_res = aes_encrypt(v_out, aes_key)
    aes_hex = aes_res.get("hex_str", v_out)

    # 4. Vernam Stream Cipher (Orang 4 - Modern Aliran Bitwise XOR)
    _, vernam_hex, _, _ = vernam_encrypt(aes_hex, vernam_key)

    stages = [
        {"Tahap": 1, "Algoritma": "Caesar Cipher (Klasik)", "Penanggung Jawab": "Orang 1", "Hasil Transformasi": str(c_out)},
        {"Tahap": 2, "Algoritma": "Vigenère Cipher (Klasik)", "Penanggung Jawab": "Orang 2", "Hasil Transformasi": str(v_out)},
        {"Tahap": 3, "Algoritma": "AES-128 Block Cipher (Modern Blok)", "Penanggung Jawab": "Orang 3", "Hasil Transformasi": str(aes_hex)},
        {"Tahap": 4, "Algoritma": "Vernam Stream Cipher (Modern Aliran)", "Penanggung Jawab": "Orang 4 (Oktavian)", "Hasil Transformasi": str(vernam_hex)},
    ]
    return {"final_cipher": vernam_hex, "stages": stages}


def super_decrypt(ciphertext_input: str, caesar_shift: int, vigenere_key: str, aes_key: str, vernam_key: str = "VERNAM_SUPER"):
    # 4. Pembalik Vernam (XOR Dekripsi)
    v_rec, _ = vernam_decrypt(ciphertext_input, vernam_key)

    # 3. Pembalik AES-128 (AES Dekripsi)
    a_rec = aes_decrypt(v_rec, aes_key)
    aes_plain = a_rec.get("text", v_rec)

    # 2. Pembalik Vigenère (Vigenère Dekripsi)
    vig_plain, _ = vigenere_decrypt(aes_plain, vigenere_key)

    # 1. Pembalik Caesar (Caesar Dekripsi)
    final_plain, _ = caesar_decrypt(vig_plain, caesar_shift)

    return final_plain


# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_super_page():
    render_header(
        title="Menu 5: Super Enkripsi",
        subtitle="Pipeline Terpadu 4 Tahap: Caesar ➔ Vigenère ➔ AES-128 (Blok) ➔ Vernam (Aliran)",
        pic_name="Penanggung Jawab: Seluruh Tim",
        category="Super Enkripsi Terpadu"
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
                k_c = st.number_input("Kunci Caesar Shift k (Orang 1):", 1, 25, 3, key="sup_kc")
                k_aes_sup = st.text_input("Kunci AES-128 (Orang 3):", value="KunciAESSuper128", key="sup_kaes")
            with k2:
                k_v = st.text_input("Kunci Vigenère (Orang 2):", value="INFORMATIKA", key="sup_kv")
                k_vernam_sup = st.text_input("Kunci Keystream Vernam (Orang 4):", value="VERNAM_STREAM_KEY", key="sup_kvernam")

            btn_sup_enc = st.button("Jalankan Super Enkripsi 4 Tahap", key="sup_btn_enc", width="stretch")

        with c2:
            st.markdown("##### Hasil Akhir Super Cipherteks")
            if btn_sup_enc:
                try:
                    sup_res = super_encrypt(plain_super, k_c, k_v, k_aes_sup, k_vernam_sup)
                    st.session_state["sup_res"] = sup_res
                    st.markdown("**Final Super Cipherteks (Hex):**")
                    st.markdown(f'<div class="cipher-box" style="font-size: 0.9rem;">{sup_res["final_cipher"]}</div>', unsafe_allow_html=True)
                    st.success("Seluruh 4 algoritma berhasil dieksekusi secara berantai tanpa henti!")
                except Exception as ex:
                    st.error(f"Gagal memproses super enkripsi: {ex}")
            else:
                if "sup_res" in st.session_state and "final_cipher" in st.session_state["sup_res"]:
                    st.markdown("**Final Super Cipherteks Sebelumnya:**")
                    st.markdown(f'<div class="cipher-box" style="font-size: 0.9rem;">{st.session_state["sup_res"]["final_cipher"]}</div>', unsafe_allow_html=True)
                else:
                    st.info("Tekan tombol 'Jalankan Super Enkripsi 4 Tahap' untuk memproses.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Input Super Cipherteks & Kunci Pembalik")
            init_c_dec = st.session_state.get("sup_res", {}).get("final_cipher", "")
            c_sup_in = st.text_area("Masukkan teks super cipherteks (Hex):", value=init_c_dec, height=90, key="sup_dec_in")

            kd1, kd2 = st.columns(2)
            with kd1:
                kd_c = st.number_input("Kunci Caesar Pembalik:", 1, 25, 3, key="sup_kdc")
                kd_aes = st.text_input("Kunci AES Pembalik:", value="KunciAESSuper128", key="sup_kdaes")
            with kd2:
                kd_v = st.text_input("Kunci Vigenère Pembalik:", value="INFORMATIKA", key="sup_kdv")
                kd_vernam = st.text_input("Kunci Vernam Pembalik:", value="VERNAM_STREAM_KEY", key="sup_kdvernam")

            btn_sup_dec = st.button("Jalankan Super Dekripsi (Prinsip LIFO)", key="sup_btn_dec", width="stretch")

        with c2:
            st.markdown("##### Hasil Plainteks Rekonstruksi")
            if btn_sup_dec:
                try:
                    dec_sup = super_decrypt(c_sup_in, kd_c, kd_v, kd_aes, kd_vernam)
                    st.markdown("**Plainteks Rekonstruksi Hasil Dekripsi LIFO:**")
                    st.markdown(f'<div class="cipher-box" style="font-size: 1.05rem; font-weight: 600;">{dec_sup}</div>', unsafe_allow_html=True)
                    st.success("Proses pembalikan pipeline 4 tahap berhasil diselesaikan!")
                except Exception as err:
                    st.error(f"Gagal memproses dekripsi: {err}")
            else:
                st.info("Tekan tombol 'Jalankan Super Dekripsi' untuk memproses.")

    with tab_pipe:
        st.markdown("##### Tabel Transformasi di Setiap Stasiun Pipeline")
        if "sup_res" in st.session_state and "stages" in st.session_state["sup_res"]:
            st.dataframe(pd.DataFrame(st.session_state["sup_res"]["stages"]), width="stretch", hide_index=True)
        else:
            st.info("Jalankan proses super enkripsi terlebih dahulu untuk memuat tabel transformasi.")

    with tab_theory:
        st.markdown("##### Konsep Super Enkripsi Terpadu")
        st.markdown("""
        **Super Enkripsi** menggabungkan beberapa algoritma kriptografi secara beruntun (*pipelining*).
        Output dari algoritma pertama menjadi input bagi algoritma berikutnya:

        $$\\text{Plainteks} \\xrightarrow{\\text{Tahap 1: Caesar}} C_1 \\xrightarrow{\\text{Tahap 2: Vigenère}} C_2 \\xrightarrow{\\text{Tahap 3: AES-128}} C_3 \\xrightarrow{\\text{Tahap 4: Vernam}} \\text{Final Super Cipherteks}$$

        * **Kombinasi Algoritma:**
          1. **Tahap 1 (Caesar Cipher):** Kriptografi Klasik Substitusi Monoalfabetik.
          2. **Tahap 2 (Vigenère Cipher):** Kriptografi Klasik Substitusi Polialfabetik.
          3. **Tahap 3 (AES-128 Rijndael):** Kriptografi Modern Cipher Blok Simetris 10 Putaran SPN.
          4. **Tahap 4 (Vernam Stream Cipher):** Kriptografi Modern Cipher Aliran Bitwise XOR Keystream.

        * **Prinsip Dekripsi (LIFO - Last In First Out)**:
          Proses pembalikan dilakukan dengan urutan terbalik secara presisi:
          $$\\text{Super Cipherteks} \\xrightarrow{\\text{Vernam}^{-1}} C_3 \\xrightarrow{\\text{AES}^{-1}} C_2 \\xrightarrow{\\text{Vigenère}^{-1}} C_1 \\xrightarrow{\\text{Caesar}^{-1}} \\text{Plainteks}$$
        """)


# Standalone runner
if __name__ == "__main__":
    st.set_page_config(page_title="Super Enkripsi", layout="wide")
    load_global_css()
    render_super_page()
