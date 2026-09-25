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

def super_encrypt(plaintext: str, caesar_shift: int, vigenere_key: str, aes_key: str, rsa_e: int, rsa_n: int):
    """
    TODO: Gabungkan ke-4 algoritma secara berurutan:
    Plaintext -> Caesar -> Vigenere -> AES -> RSA -> Super Ciphertext
    """
    # 1. Caesar (Orang 1)
    c_out, _ = caesar_encrypt(plaintext, caesar_shift)
    # 2. Vigenere (Orang 2)
    v_out, _ = vigenere_encrypt(c_out, vigenere_key)
    # 3. AES (Orang 3)
    aes_res = aes_encrypt(v_out, aes_key)
    # 4. RSA (Orang 4)
    _, rsa_str, _ = rsa_encrypt(aes_res.get("hex_str", v_out), rsa_e, rsa_n)

    stages = [
        {"Tahap": 1, "Algoritma": "Caesar", "PIC": "Orang 1", "Hasil": str(c_out)},
        {"Tahap": 2, "Algoritma": "Vigenère", "PIC": "Orang 2", "Hasil": str(v_out)},
        {"Tahap": 3, "Algoritma": "AES", "PIC": "Orang 3", "Hasil": str(aes_res.get("hex_str", ""))},
        {"Tahap": 4, "Algoritma": "RSA", "PIC": "Orang 4", "Hasil": str(rsa_str)},
    ]
    return {"final_cipher": rsa_str, "stages": stages}

def super_decrypt(ciphertext_input: str, caesar_shift: int, vigenere_key: str, aes_key: str, rsa_d: int, rsa_n: int):
    """
    TODO: Dekripsi secara berurutan terbalik (LIFO):
    Ciphertext -> RSA -> AES -> Vigenere -> Caesar -> Original Plaintext
    """
    # [PLACEHOLDER - Silakan lengkapi logika pembalikannya]
    return f"[HASIL SUPER DEKRIPSI DARI {ciphertext_input[:20]}...]"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# ==============================================================================

def render_super_page():
    render_header(
        title="5️⃣ Super Enkripsi (Kolaborasi Tim)",
        subtitle="Pipeline Terpadu 4 Tahap: Caesar ➔ Vigenère ➔ AES-128 ➔ RSA",
        person_badge="Penanggung Jawab: Seluruh Tim (Orang 1 s/d 4)",
        algo_badge="Super Enkripsi",
        badge_class="badge-super"
    )

    tab_enc, tab_dec, tab_pipe, tab_theory = st.tabs([
        "🔒 Super Enkripsi", "🔓 Super Dekripsi", "🔄 Visualisasi Pipeline Bertingkat", "📖 Teori Super Enkripsi"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📝 Plainteks & Parameter Kunci 4 Orang")
            plain_super = st.text_area("Plainteks Asli:", value="BELAJAR KRIPTOGRAFI", height=90, key="sup_plain")
            k1, k2 = st.columns(2)
            with k1:
                k_c = st.number_input("Kunci Caesar (P1):", 1, 25, 3, key="sup_kc")
                k_aes_sup = st.text_input("Kunci AES (P3):", value="KunciAESSuper128", key="sup_kaes")
            with k2:
                k_v = st.text_input("Kunci Vigenère (P2):", value="INFORMATIKA", key="sup_kv")
                k_rsa_e = st.number_input("RSA e (P4):", value=17, key="sup_ke")
                k_rsa_n = st.number_input("RSA n (P4):", value=3233, key="sup_kn")

            btn_sup_enc = st.button("🚀 Jalankan Super Enkripsi 4 Tahap", key="sup_btn_enc", use_container_width=True)

        with c2:
            st.markdown("##### 🎯 Hasil Akhir Super Ciphertext")
            if btn_sup_enc:
                sup_res = super_encrypt(plain_super, k_c, k_v, k_aes_sup, k_rsa_e, k_rsa_n)
                st.session_state["sup_res"] = sup_res
                st.text_area("Final Super Ciphertext:", value=str(sup_res["final_cipher"]), height=120)
                st.success("✅ Seluruh 4 Algoritma Berhasil Dieksekusi Beruntun!")
            else:
                st.info("Klik tombol 'Jalankan Super Enkripsi' untuk melihat hasil.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📥 Ciphertext & Parameter Kunci Pembalik")
            c_sup_in = st.text_area("Super Ciphertext Input:", value="", height=90, key="sup_dec_in")
            btn_sup_dec = st.button("🔓 Jalankan Super Dekripsi", key="sup_btn_dec", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Plainteks Rekonstruksi")
            if btn_sup_dec:
                dec_sup = super_decrypt(c_sup_in, 3, "INFORMATIKA", "KunciAESSuper128", 2753, 3233)
                st.text_area("Original Plaintext:", value=dec_sup, height=120)
                st.success("Dekripsi Super selesai diproses!")
            else:
                st.info("Klik tombol 'Jalankan Super Dekripsi' untuk melihat hasil.")

    with tab_pipe:
        st.markdown("#### 🔄 Tabel Transformasi di Setiap Stasiun Pipeline")
        if "sup_res" in st.session_state and "stages" in st.session_state["sup_res"]:
            st.dataframe(pd.DataFrame(st.session_state["sup_res"]["stages"]), use_container_width=True)
        else:
            st.info("Jalankan Super Enkripsi terlebih dahulu untuk melihat tahapan pipeline.")

    with tab_theory:
        st.markdown("""
        ### 📖 Konsep Super Enkripsi Terpadu (Materi 3 Slide 51)
        * Menggabungkan 4 algoritma secara berurutan: Caesar -> Vigenère -> AES -> RSA.
        * Dekripsi membalik urutan secara presisi (LIFO): RSA -> AES -> Vigenère -> Caesar.
        """)

# Standalone runner
if __name__ == "__main__":
    st.set_page_config(page_title="Super Enkripsi - Bersama", page_icon="🔐", layout="wide")
    load_global_css()
    render_super_page()
