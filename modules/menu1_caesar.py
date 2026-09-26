import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css, render_mode_selector
except ImportError:
    from ui_helper import render_header, load_global_css, render_mode_selector

# ==============================================================================
# BAGIAN 1: LOGIKA CAESAR CIPHER (ORANG 1)
# ==============================================================================

def caesar_encrypt(plaintext: str, shift: int):
    """
    Enkripsi Caesar Cipher:
    C = (P + k) mod 26
    """
    ciphertext = ""
    steps = []
    no = 1

    for char in plaintext:
        if char.isupper():
            old_pos = ord(char) - ord("A")
            new_pos = (old_pos + shift) % 26
            new_char = chr(new_pos + ord("A"))
            ciphertext += new_char
            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi (0-25)": str(old_pos),
                "Kalkulasi Modulo": f"({old_pos} + {shift}) mod 26",
                "Hasil Sandi": new_char
            })
            no += 1
        elif char.islower():
            old_pos = ord(char) - ord("a")
            new_pos = (old_pos + shift) % 26
            new_char = chr(new_pos + ord("a"))
            ciphertext += new_char
            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi (0-25)": str(old_pos),
                "Kalkulasi Modulo": f"({old_pos} + {shift}) mod 26",
                "Hasil Sandi": new_char
            })
            no += 1
        else:
            ciphertext += char
            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi (0-25)": "-",
                "Kalkulasi Modulo": "Karakter tidak diubah",
                "Hasil Sandi": char
            })
            no += 1

    return ciphertext, steps


def caesar_decrypt(ciphertext: str, shift: int):
    """
    Dekripsi Caesar Cipher:
    P = (C - k) mod 26
    """
    plaintext = ""
    steps = []
    no = 1

    for char in ciphertext:
        if char.isupper():
            old_pos = ord(char) - ord("A")
            new_pos = (old_pos - shift) % 26
            new_char = chr(new_pos + ord("A"))
            plaintext += new_char
            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi (0-25)": str(old_pos),
                "Kalkulasi Modulo": f"({old_pos} - {shift}) mod 26",
                "Hasil Plain": new_char
            })
            no += 1
        elif char.islower():
            old_pos = ord(char) - ord("a")
            new_pos = (old_pos - shift) % 26
            new_char = chr(new_pos + ord("a"))
            plaintext += new_char
            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi (0-25)": str(old_pos),
                "Kalkulasi Modulo": f"({old_pos} - {shift}) mod 26",
                "Hasil Plain": new_char
            })
            no += 1
        else:
            plaintext += char
            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi (0-25)": "-",
                "Kalkulasi Modulo": "Karakter tidak diubah",
                "Hasil Plain": char
            })
            no += 1

    return plaintext, steps


def caesar_bruteforce(ciphertext: str):
    """
    Mencoba seluruh 25 kemungkinan shift untuk kriptanalisis.
    """
    results = []
    for shift in range(1, 26):
        plaintext, _ = caesar_decrypt(ciphertext, shift)
        results.append({
            "Kunci Shift (k)": shift,
            "Hasil Dekripsi Plainteks": plaintext
        })
    return results

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_caesar_page():
    render_header(
        title="Menu 1: Caesar Cipher",
        subtitle="Substitusi Monoalfabetik dengan Pergeseran Abjad Modulo 26",
        pic_name="Penanggung Jawab: Orang 1",
        category="Kriptografi Klasik"
    )

    tab_main, tab_trace, tab_crypto, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pelacakan Proses (Step-by-Step)",
        "Kriptanalisis Brute-Force",
        "Teori & Formula"
    ])

    with tab_main:
        mode = render_mode_selector(session_state_key="c_mode", key_prefix="caesar")

        if mode == "Enkripsi Pesan":
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Plainteks")
                plaintext = st.text_area(
                    "Masukkan teks yang akan dienkripsi:",
                    value="Belajar Kriptografi",
                    height=110,
                    key="plaintext_input"
                )
                shift = st.slider(
                    "Kunci Pergeseran (Shift k):",
                    min_value=1,
                    max_value=25,
                    value=3,
                    key="encrypt_shift"
                )
                encrypt_button = st.button(
                    "Jalankan Enkripsi Caesar",
                    use_container_width=True,
                    key="encrypt_button",
                    type="primary"
                )

            with col2:
                st.markdown("##### Hasil Enkripsi")
                if encrypt_button:
                    if plaintext.strip() == "":
                        st.warning("Silakan masukkan teks plainteks terlebih dahulu.")
                    else:
                        ciphertext, steps = caesar_encrypt(plaintext, shift)
                        st.session_state["steps"] = steps
                        st.session_state["last_result"] = ciphertext
                        st.text_area(
                            "Teks Cipherteks:",
                            value=ciphertext,
                            height=110,
                            key="encrypt_result"
                        )
                        st.success("Proses enkripsi berhasil diselesaikan.")
                else:
                    st.info("Tekan tombol 'Jalankan Enkripsi Caesar' untuk memproses teks.")

        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Cipherteks")
                ciphertext = st.text_area(
                    "Masukkan teks cipherteks yang akan didekripsi:",
                    value="",
                    height=110,
                    key="ciphertext_input"
                )
                shift = st.slider(
                    "Kunci Pergeseran (Shift k):",
                    min_value=1,
                    max_value=25,
                    value=3,
                    key="decrypt_shift"
                )
                decrypt_button = st.button(
                    "Jalankan Dekripsi Caesar",
                    use_container_width=True,
                    key="decrypt_button",
                    type="primary"
                )

            with col2:
                st.markdown("##### Hasil Dekripsi")
                if decrypt_button:
                    if ciphertext.strip() == "":
                        st.warning("Silakan masukkan teks cipherteks terlebih dahulu.")
                    else:
                        plaintext, steps = caesar_decrypt(ciphertext, shift)
                        st.session_state["steps"] = steps
                        st.session_state["last_result"] = plaintext
                        st.text_area(
                            "Teks Plainteks Rekonstruksi:",
                            value=plaintext,
                            height=110,
                            key="decrypt_result"
                        )
                        st.success("Proses dekripsi berhasil diselesaikan.")
                else:
                    st.info("Tekan tombol 'Dekripsi Pesan' untuk memproses teks.")

    with tab_trace:
        st.markdown("##### Pelacakan Transformasi Karakter demi Karakter")
        if "steps" in st.session_state and st.session_state["steps"]:
            st.dataframe(
                pd.DataFrame(st.session_state["steps"]),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Lakukan proses enkripsi atau dekripsi terlebih dahulu untuk memuat tabel langkah.")

    with tab_crypto:
        st.markdown("##### Analisis Kunci: Brute-Force 25 Shift")
        st.caption("Mencoba seluruh kemungkinan nilai pergeseran abjad dari k = 1 hingga k = 25.")
        target = st.text_area(
            "Masukkan Cipherteks Target:",
            value="KHOOR ZRUOG",
            height=90,
            key="bruteforce_input"
        )
        brute_button = st.button(
            "Jalankan Analisis Brute-Force",
            use_container_width=True,
            key="brute_button"
        )

        if brute_button:
            if target.strip() == "":
                st.warning("Silakan masukkan cipherteks target terlebih dahulu.")
            else:
                results = caesar_bruteforce(target)
                st.dataframe(
                    pd.DataFrame(results),
                    use_container_width=True,
                    hide_index=True
                )

    with tab_theory:
        st.markdown("##### Teori & Formula Caesar Cipher")
        st.markdown("""
        **Caesar Cipher** adalah algoritma kriptografi klasik bertipe substitusi abjad-tunggal (*monoalphabetic substitution*).
        Setiap huruf pada teks terang (*plaintext*) digantikan oleh huruf lain dengan selisih pergeseran posisi tetap sebesar $k$.

        * **Formula Enkripsi**:
          $$C_i = (P_i + k) \\pmod{26}$$

        * **Formula Dekripsi**:
          $$P_i = (C_i - k) \\pmod{26}$$

        **Keterangan Notasi:**
        * $P_i$ = Indeks posisi huruf plainteks ($A=0, B=1, \\dots, Z=25$)
        * $C_i$ = Indeks posisi huruf cipherteks
        * $k$ = Nilai kunci pergeseran (*shift key*)
        * $26$ = Jumlah total abjad alfabet standar
        """)

# Standalone runner: Orang 1 bisa menjalankan file ini saja
if __name__ == "__main__":
    st.set_page_config(
        page_title="Caesar Cipher - Orang 1",
        layout="wide"
    )
    load_global_css()
    render_caesar_page()
