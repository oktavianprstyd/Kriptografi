import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA AES BLOCK CIPHER
# Penanggung Jawab: Orang 3
# ==============================================================================

def aes_encrypt(plaintext: str, key: str, mode: str = "CBC"):
    """
    TODO: Tuliskan logika enkripsi AES di sini.
    """
    hex_str = f"4145535F454E435259505445445F{len(plaintext):02X}"
    b64_str = "QUVTLUVOQ1JZUFRFRC1TQU1QTEU="
    demo_trace = {
        "State Matrix": [
            ["00", "04", "08", "0C"],
            ["01", "05", "09", "0D"],
            ["02", "06", "0A", "0E"],
            ["03", "07", "0B", "0F"]
        ]
    }
    return {
        "hex_str": hex_str,
        "b64_str": b64_str,
        "demo_trace": demo_trace
    }

def aes_decrypt(cipher_hex: str, key: str, mode: str = "CBC"):
    """
    TODO: Tuliskan logika dekripsi AES di sini.
    """
    return f"[HASIL DEKRIPSI AES dari {cipher_hex[:16]}...]"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_aes_page():
    render_header(
        title="Menu 3: AES-128 Block Cipher",
        subtitle="Standar Enkripsi Blok Modern 128-bit dengan Mode CBC & State Matrix 4×4",
        pic_name="Penanggung Jawab: Orang 3",
        category="Kriptografi Modern"
    )

    tab_main, tab_trace, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Visualisasi State Matrix & Round",
        "Teori & Formula"
    ])

    with tab_main:
        mode = st.radio(
            "Pilih Mode Operasi",
            ["Enkripsi Pesan", "Dekripsi Pesan"],
            horizontal=True,
            key="aes_mode"
        )
        st.divider()

        if mode == "Enkripsi Pesan":
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Plainteks & Parameter Kunci")
                p_aes = st.text_area("Masukkan teks plainteks:", value="BELAJAR KRIPTOGRAFI MODERN", height=110, key="aes_plain_in")
                k_aes = st.text_input("Kunci Rahasia AES (128-bit / Passphrase):", value="KunciSuperAman128", key="aes_key_in")
                mode_opt = st.selectbox("Mode Operasi Blok:", ["CBC (Cipher Block Chaining)", "ECB (Electronic Codebook)"], key="aes_mode_in")
                btn_aes_enc = st.button("Enkripsi Pesan", key="aes_btn_enc", use_container_width=True)
            with col2:
                st.markdown("##### Hasil Enkripsi")
                if btn_aes_enc:
                    aes_res = aes_encrypt(p_aes, k_aes, mode=mode_opt)
                    st.session_state["aes_trace"] = aes_res.get("demo_trace")
                    st.text_area("Cipherteks (Format Heksadesimal):", value=aes_res.get("hex_str", ""), height=80)
                    st.text_area("Cipherteks (Format Base64):", value=aes_res.get("b64_str", ""), height=60)
                    st.success("Proses enkripsi AES selesai diproses.")
                else:
                    st.info("Tekan tombol 'Enkripsi Pesan' untuk memproses teks.")

        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Cipherteks & Kunci")
                c_aes_in = st.text_area("Masukkan teks cipherteks (Heksadesimal):", value="", height=110, key="aes_dec_in")
                k_aes_dec = st.text_input("Kunci Rahasia AES:", value="KunciSuperAman128", key="aes_key_dec")
                btn_aes_dec = st.button("Dekripsi Pesan", key="aes_btn_dec", use_container_width=True)
            with col2:
                st.markdown("##### Hasil Dekripsi")
                if btn_aes_dec:
                    d_res = aes_decrypt(c_aes_in, k_aes_dec)
                    st.text_area("Teks Plainteks Rekonstruksi:", value=d_res, height=110)
                    st.success("Proses dekripsi AES selesai diproses.")
                else:
                    st.info("Tekan tombol 'Dekripsi Pesan' untuk memproses teks.")

    with tab_trace:
        st.markdown("##### Transformasi State Matrix 4×4")
        if "aes_trace" in st.session_state and st.session_state["aes_trace"]:
            st.write(st.session_state["aes_trace"])
        else:
            st.info("Lakukan proses enkripsi terlebih dahulu untuk memuat visualisasi State Matrix.")

    with tab_theory:
        st.markdown("##### Teori & Struktur AES (Advanced Encryption Standard)")
        st.markdown("""
        **AES-128** adalah cipher blok simetris yang memproses data dalam blok tetap berukuran 128 bit (16 byte)
        menggunakan struktur *Substitution-Permutation Network* (SPN) dalam 10 putaran (*rounds*).

        **4 Tahapan Inti per Putaran:**
        1. **SubBytes**: Substitusi non-linear per byte menggunakan tabel S-Box Rijndael.
        2. **ShiftRows**: Pergeseran siklis pada baris-baris State Matrix.
        3. **MixColumns**: Perkalian matriks setiap kolom dalam lapangan Galois $GF(2^8)$.
        4. **AddRoundKey**: Operasi bitwise XOR antara State Matrix dengan kunci putaran (*Round Key*).
        """)

# Standalone runner: Orang 3
if __name__ == "__main__":
    st.set_page_config(page_title="AES-128 - Orang 3", layout="wide")
    load_global_css()
    render_aes_page()
