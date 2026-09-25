import streamlit as st
import pandas as pd
import string

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA CAESAR CIPHER (ORANG 1)
# ==============================================================================
def get_caesar_mapping(shift: int):
    shift = shift % 26
    upper_orig = string.ascii_uppercase
    upper_shifted = upper_orig[shift:] + upper_orig[:shift]
    return {
        "shift": shift,
        "upper_orig": list(upper_orig),
        "upper_shifted": list(upper_shifted)
    }

def caesar_encrypt(text: str, shift: int):
    shift = shift % 26
    result = []
    steps = []
    for idx, char in enumerate(text):
        if 'A' <= char <= 'Z':
            p_val = ord(char) - ord('A')
            c_val = (p_val + shift) % 26
            c_char = chr(c_val + ord('A'))
            result.append(c_char)
            steps.append({
                "index": idx + 1, "char": char, "type": "Huruf Besar",
                "p_val": p_val, "formula": f"({p_val} + {shift}) mod 26 = {c_val}",
                "c_val": c_val, "result_char": c_char
            })
        elif 'a' <= char <= 'z':
            p_val = ord(char) - ord('a')
            c_val = (p_val + shift) % 26
            c_char = chr(c_val + ord('a'))
            result.append(c_char)
            steps.append({
                "index": idx + 1, "char": char, "type": "Huruf Kecil",
                "p_val": p_val, "formula": f"({p_val} + {shift}) mod 26 = {c_val}",
                "c_val": c_val, "result_char": c_char
            })
        else:
            result.append(char)
            steps.append({
                "index": idx + 1, "char": repr(char)[1:-1] if char == ' ' else char,
                "type": "Spasi/Simbol", "p_val": "-", "formula": "Tetap",
                "c_val": "-", "result_char": repr(char)[1:-1] if char == ' ' else char
            })
    return "".join(result), steps

def caesar_decrypt(ciphertext: str, shift: int):
    shift = shift % 26
    result = []
    steps = []
    for idx, char in enumerate(ciphertext):
        if 'A' <= char <= 'Z':
            c_val = ord(char) - ord('A')
            p_val = (c_val - shift) % 26
            p_char = chr(p_val + ord('A'))
            result.append(p_char)
            steps.append({
                "index": idx + 1, "char": char, "type": "Huruf Besar",
                "c_val": c_val, "formula": f"({c_val} - {shift}) mod 26 = {p_val}",
                "p_val": p_val, "result_char": p_char
            })
        elif 'a' <= char <= 'z':
            c_val = ord(char) - ord('a')
            p_val = (c_val - shift) % 26
            p_char = chr(p_val + ord('a'))
            result.append(p_char)
            steps.append({
                "index": idx + 1, "char": char, "type": "Huruf Kecil",
                "c_val": c_val, "formula": f"({c_val} - {shift}) mod 26 = {p_val}",
                "p_val": p_val, "result_char": p_char
            })
        else:
            result.append(char)
            steps.append({
                "index": idx + 1, "char": repr(char)[1:-1] if char == ' ' else char,
                "type": "Spasi/Simbol", "c_val": "-", "formula": "Tetap",
                "p_val": "-", "result_char": repr(char)[1:-1] if char == ' ' else char
            })
    return "".join(result), steps

def caesar_bruteforce(ciphertext: str):
    results = []
    indonesian_words = {"dan", "yang", "untuk", "pada", "di", "ke", "dari", "ini", "itu", "dengan", "informatika", "kriptografi", "mahasiswa"}
    for shift in range(1, 26):
        decrypted, _ = caesar_decrypt(ciphertext, shift)
        words = decrypted.lower().split()
        match_count = sum(1 for w in words if w.strip(".,!?;:()[]{}'\"") in indonesian_words)
        results.append({"shift": shift, "decrypted_text": decrypted, "match_score": match_count})
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (ORANG 1)
# ==============================================================================
def render_caesar_page():
    render_header(
        "1️⃣ Caesar Cipher",
        "Substitusi Monoalfabetik dengan Pergeseran Huruf Modulo 26",
        "Penanggung Jawab: Orang 1",
        "Kriptografi Klasik",
        "badge-p1"
    )

    tab_enc, tab_dec, tab_trace, tab_crypto, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi Step-by-Step", "⚡ Kriptanalisis (Brute-Force)", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            p_text = st.text_area("Masukkan Plaintext:", value="BELAJAR KRIPTOGRAFI UNTUK INDONESIA MAJU", height=120, key="c_plain_in")
            k_val = st.slider("Kunci Pergeseran (Shift k):", 1, 25, 18, key="c_shift_in")
            btn_enc = st.button("🔒 Enkripsi Sekarang", key="c_btn_enc", use_container_width=True)
        with c2:
            if p_text:
                c_res, steps = caesar_encrypt(p_text, k_val)
                st.session_state["c_steps"] = steps
                st.text_area("Hasil Ciphertext:", value=c_res, height=120)
                st.info(f"Panjang Karakter: **{len(c_res)}** | Kunci Pergeseran: **{k_val}**")
                st.code(f"Formula: C ≡ (P + {k_val}) mod 26")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            c_input = st.text_area("Masukkan Ciphertext:", value="TWDSFWYSJS VA WJS YDGTSD", height=120, key="c_cipher_in")
            k_dec = st.slider("Kunci Pergeseran (Shift k):", 1, 25, 18, key="c_shift_dec")
            btn_dec = st.button("🔓 Dekripsi Sekarang", key="c_btn_dec", use_container_width=True)
        with c2:
            if c_input:
                p_res, _ = caesar_decrypt(c_input, k_dec)
                st.text_area("Hasil Plaintext:", value=p_res, height=120)
                st.success(f"Dekripsi Sukses dengan k = **{k_dec}**")
                st.code(f"Formula: P ≡ (C - {k_dec}) mod 26")

    with tab_trace:
        st.markdown("#### 🔍 Pelacakan Kalkulasi Per Karakter")
        if "c_steps" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["c_steps"]), use_container_width=True, height=350)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk memuat tabel pelacakan.")
        st.markdown("#### 🔤 Peta Pergeseran Abjad")
        mapping = get_caesar_mapping(k_val if 'k_val' in locals() else 18)
        st.dataframe(pd.DataFrame({
            "Abjad Asli": mapping["upper_orig"],
            f"Abjad Tergeser (Shift {mapping['shift']})": mapping["upper_shifted"]
        }).T, use_container_width=True)

    with tab_crypto:
        st.markdown("#### ⚡ Kriptanalisis Otomatis (Brute-Force 25 Kunci)")
        target = st.text_area("Ciphertext Target:", value="Ewfbsva hjgyjse klmva Afxgjeslacs qsfy mfyymd...", height=90, key="c_bf_in")
        if st.button("🚀 Jalankan Brute-Force", key="c_btn_bf", use_container_width=True):
            res = caesar_bruteforce(target)
            st.success(f"Kunci terbaik terdeteksi: **Shift k = {res[0]['shift']}**")
            st.dataframe(pd.DataFrame(res), use_container_width=True, height=300)

    with tab_theory:
        st.markdown("""
        ### 📖 Teori Caesar Cipher (Materi 3)
        * **Kategori**: Cipher Substitusi Abjad-Tunggal (*Monoalphabetic Substitution*).
        * **Rumus Matematis**:
          $$C_i = (P_i + k) \\pmod{26}, \\quad P_i = (C_i - k) \\pmod{26}$$
        * **Karakteristik**: Sangat mudah dipecahkan karena ruang kunci hanya 25 kemungkinan ($26 - 1$).
        """)

# Standalone runner untuk pengujian mandiri Orang 1
if __name__ == "__main__":
    st.set_page_config(page_title="Caesar Cipher - Orang 1", page_icon="🔐", layout="wide")
    load_global_css()
    render_caesar_page()
