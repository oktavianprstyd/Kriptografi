import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA AES BLOCK CIPHER
# Penanggung Jawab: Orang 3
# ==============================================================================

def aes_encrypt(plaintext: str, key: str, mode: str = "CBC"):
    """
    TODO: Tuliskan logika enkripsi AES di sini (misal menggunakan library cryptography atau manual).
    Input: Teks plainteks & string kunci
    Kembalikan: dict berisi hex_str, b64_str, demo_trace, dll.
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    hex_str = f"4145535F454E435259505445445F{len(plaintext):02X}"
    b64_str = "[PLACEHOLDER_BASE64]"
    demo_trace = {
        "round": "Contoh State Matrix 4x4",
        "data": [["00", "01", "02", "03"], ["04", "05", "06", "07"], ["08", "09", "0A", "0B"], ["0C", "0D", "0E", "0F"]]
    }
    return {
        "hex_str": hex_str,
        "b64_str": b64_str,
        "demo_trace": demo_trace
    }

def aes_decrypt(cipher_hex_or_bytes: str, key: str, mode: str = "CBC"):
    """
    TODO: Tuliskan logika dekripsi AES di sini.
    Kembalikan: plainteks hasil rekonstruksi
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    return f"[HASIL DEKRIPSI AES dari {cipher_hex_or_bytes[:16]}...]"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# Penanggung Jawab: Orang 3
# ==============================================================================

def render_aes_page():
    render_header(
        title="3️⃣ AES-128 Block Cipher",
        subtitle="Standar Enkripsi Blok Modern 128-bit dengan Mode CBC & State Matrix 4×4",
        person_badge="Penanggung Jawab: Orang 3",
        algo_badge="Kriptografi Modern",
        badge_class="badge-p3"
    )

    tab_enc, tab_dec, tab_trace, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi State Matrix & Round", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📝 Input Teks & Kunci")
            p_aes = st.text_area("Masukkan Plaintext:", value="BELAJAR KRIPTOGRAFI MODERN", height=120, key="aes_plain_in")
            k_aes = st.text_input("Kunci Rahasia AES:", value="KunciSuperAman128", key="aes_key_in")
            mode_opt = st.selectbox("Mode Operasi:", ["CBC (Cipher Block Chaining)", "ECB (Electronic Codebook)"], key="aes_mode_in")
            btn_aes_enc = st.button("🔒 Enkripsi Sekarang", key="aes_btn_enc", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Enkripsi")
            if btn_aes_enc:
                aes_res = aes_encrypt(p_aes, k_aes, mode=mode_opt)
                st.session_state["aes_trace"] = aes_res.get("demo_trace")
                st.text_area("Ciphertext (Hex):", value=aes_res.get("hex_str", ""), height=80)
                st.text_area("Ciphertext (Base64):", value=aes_res.get("b64_str", ""), height=60)
                st.success("Enkripsi AES berhasil diproses!")
            else:
                st.info("Klik tombol 'Enkripsi Sekarang' untuk melihat hasil.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📥 Input Ciphertext & Kunci")
            c_aes_in = st.text_area("Masukkan Ciphertext (Hex):", value="", height=120, key="aes_dec_in")
            k_aes_dec = st.text_input("Kunci Rahasia AES:", value="KunciSuperAman128", key="aes_key_dec")
            btn_aes_dec = st.button("🔓 Dekripsi Sekarang", key="aes_btn_dec", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Dekripsi")
            if btn_aes_dec:
                d_res = aes_decrypt(c_aes_in, k_aes_dec)
                st.text_area("Plaintext Rekonstruksi:", value=d_res, height=120)
                st.success("Dekripsi AES berhasil diproses!")
            else:
                st.info("Klik tombol 'Dekripsi Sekarang' untuk melihat hasil.")

    with tab_trace:
        st.markdown("#### 🧱 Transformasi State Matrix 4×4")
        if "aes_trace" in st.session_state and st.session_state["aes_trace"]:
            t = st.session_state["aes_trace"]
            st.write(t)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk melihat visualisasi State Matrix.")

    with tab_theory:
        st.markdown("""
        ### 📖 Teori AES (Advanced Encryption Standard)
        * **Kategori**: Cipher Blok Simetris (*Symmetric Block Cipher*).
        * **Operasi Inti per Round**: *SubBytes*, *ShiftRows*, *MixColumns*, *AddRoundKey*.
        """)

# Standalone runner: Orang 3 bisa langsung menjalankan file ini saja
if __name__ == "__main__":
    st.set_page_config(page_title="AES - Orang 3", page_icon="🔐", layout="wide")
    load_global_css()
    render_aes_page()
