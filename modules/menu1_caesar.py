import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA CAESAR CIPHER
# Penanggung Jawab: Orang 1
# ==============================================================================

def caesar_encrypt(plaintext: str, shift: int):
    """
    TODO: Tuliskan logika enkripsi Caesar Cipher di sini.
    Rumus: C = (P + k) mod 26
    Kembalikan: (ciphertext, steps)
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    ciphertext = f"[HASIL ENKRIPSI CAESAR: {plaintext} (k={shift})]"
    steps = [
        {"No": 1, "Karakter": "Contoh", "Kalkulasi": f"(P + {shift}) mod 26", "Hasil": "C"}
    ]
    return ciphertext, steps

def caesar_decrypt(ciphertext: str, shift: int):
    """
    TODO: Tuliskan logika dekripsi Caesar Cipher di sini.
    Rumus: P = (C - k) mod 26
    Kembalikan: (plaintext, steps)
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    plaintext = f"[HASIL DEKRIPSI CAESAR: {ciphertext} (k={shift})]"
    steps = []
    return plaintext, steps

def caesar_bruteforce(ciphertext: str):
    """
    TODO (Fitur Tambahan): Coba ke-25 kemungkinan pergeseran kunci.
    """
    results = [{"shift": k, "decrypted_text": f"Contoh pergeseran k={k}"} for k in range(1, 26)]
    return results

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# Penanggung Jawab: Orang 1
# ==============================================================================

def render_caesar_page():
    render_header(
        title="1️⃣ Caesar Cipher",
        subtitle="Substitusi Monoalfabetik dengan Pergeseran Huruf Modulo 26",
        person_badge="Penanggung Jawab: Orang 1",
        algo_badge="Kriptografi Klasik",
        badge_class="badge-p1"
    )

    tab_enc, tab_dec, tab_trace, tab_crypto, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi Step-by-Step", "⚡ Kriptanalisis (Brute-Force)", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📝 Input Teks & Kunci")
            p_text = st.text_area("Masukkan Plaintext:", value="BELAJAR KRIPTOGRAFI", height=120, key="c_plain_in")
            k_val = st.slider("Kunci Pergeseran (Shift k):", min_value=1, max_value=25, value=3, key="c_shift_in")
            btn_enc = st.button("🔒 Enkripsi Sekarang", key="c_btn_enc", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Enkripsi")
            if btn_enc:
                c_res, steps = caesar_encrypt(p_text, k_val)
                st.session_state["c_steps"] = steps
                st.text_area("Ciphertext:", value=c_res, height=120)
                st.success("Enkripsi berhasil diproses!")
            else:
                st.info("Klik tombol 'Enkripsi Sekarang' untuk melihat hasil.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📥 Input Ciphertext & Kunci")
            c_input = st.text_area("Masukkan Ciphertext:", value="", height=120, key="c_cipher_in")
            k_dec = st.slider("Kunci Pergeseran (Shift k):", min_value=1, max_value=25, value=3, key="c_shift_dec")
            btn_dec = st.button("🔓 Dekripsi Sekarang", key="c_btn_dec", use_container_width=True)
        with c2:
            st.markdown("##### 🎯 Hasil Dekripsi")
            if btn_dec:
                p_res, _ = caesar_decrypt(c_input, k_dec)
                st.text_area("Plaintext Rekonstruksi:", value=p_res, height=120)
                st.success("Dekripsi berhasil diproses!")
            else:
                st.info("Klik tombol 'Dekripsi Sekarang' untuk melihat hasil.")

    with tab_trace:
        st.markdown("#### 🔍 Pelacakan Kalkulasi Langkah demi Langkah")
        if "c_steps" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["c_steps"]), use_container_width=True)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk melihat langkah kalkulasi.")

    with tab_crypto:
        st.markdown("#### ⚡ Kriptanalisis Otomatis: Brute-Force 25 Kunci")
        target = st.text_area("Ciphertext yang Ingin Dipecahkan:", value="KHOOR ZRUOG", height=90, key="c_bf_in")
        if st.button("🚀 Jalankan Brute-Force", key="c_btn_bf", use_container_width=True):
            res = caesar_bruteforce(target)
            st.dataframe(pd.DataFrame(res), use_container_width=True)

    with tab_theory:
        st.markdown("""
        ### 📖 Teori Caesar Cipher (Materi 3)
        * **Kategori**: Cipher Substitusi Abjad-Tunggal (*Monoalphabetic Substitution*).
        * **Rumus**:
          $$C_i = (P_i + k) \\pmod{26}, \\quad P_i = (C_i - k) \\pmod{26}$$
        """)

# Standalone runner: Orang 1 bisa langsung menjalankan file ini saja
if __name__ == "__main__":
    st.set_page_config(page_title="Caesar Cipher - Orang 1", page_icon="🔐", layout="wide")
    load_global_css()
    render_caesar_page()
