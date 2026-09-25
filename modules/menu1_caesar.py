import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# BAGIAN 1: LOGIKA CAESAR CIPHER

def caesar_encrypt(plaintext: str, shift: int):
    """
    Enkripsi Caesar Cipher.
    Rumus:
        C = (P + k) mod 26

    Huruf besar tetap besar.
    Huruf kecil tetap kecil.
    Spasi, angka, dan simbol tidak berubah.
    """

    ciphertext = ""
    steps = []

    no = 1

    for char in plaintext:

        # HURUF BESAR
        if char.isupper():

            old_pos = ord(char) - ord("A")
            new_pos = (old_pos + shift) % 26
            new_char = chr(new_pos + ord("A"))

            ciphertext += new_char

            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi": old_pos,
                "Kalkulasi": f"({old_pos} + {shift}) mod 26",
                "Hasil": new_char
            })

            no += 1

        # HURUF KECIL
        elif char.islower():

            old_pos = ord(char) - ord("a")
            new_pos = (old_pos + shift) % 26
            new_char = chr(new_pos + ord("a"))

            ciphertext += new_char

            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi": old_pos,
                "Kalkulasi": f"({old_pos} + {shift}) mod 26",
                "Hasil": new_char
            })

            no += 1

        # SPASI / ANGKA / SIMBOL
        else:

            ciphertext += char

            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi": "-",
                "Kalkulasi": "Tidak diproses",
                "Hasil": char
            })

            no += 1

    return ciphertext, steps


def caesar_decrypt(ciphertext: str, shift: int):
    """
    Dekripsi Caesar Cipher.
    Rumus:
        P = (C - k) mod 26
    """

    plaintext = ""
    steps = []

    no = 1

    for char in ciphertext:

        # HURUF BESAR
        if char.isupper():

            old_pos = ord(char) - ord("A")
            new_pos = (old_pos - shift) % 26
            new_char = chr(new_pos + ord("A"))

            plaintext += new_char

            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi": old_pos,
                "Kalkulasi": f"({old_pos} - {shift}) mod 26",
                "Hasil": new_char
            })

            no += 1

        # HURUF KECIL
        elif char.islower():

            old_pos = ord(char) - ord("a")
            new_pos = (old_pos - shift) % 26
            new_char = chr(new_pos + ord("a"))

            plaintext += new_char

            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi": old_pos,
                "Kalkulasi": f"({old_pos} - {shift}) mod 26",
                "Hasil": new_char
            })

            no += 1

        # SPASI / ANGKA / SIMBOL
        else:

            plaintext += char

            steps.append({
                "No": no,
                "Karakter": char,
                "Posisi": "-",
                "Kalkulasi": "Tidak diproses",
                "Hasil": char
            })

            no += 1

    return plaintext, steps


def caesar_bruteforce(ciphertext: str):
    """
    Mencoba seluruh kemungkinan shift Caesar Cipher.
    """

    results = []

    for shift in range(1, 26):

        plaintext, _ = caesar_decrypt(
            ciphertext,
            shift
        )

        results.append({
            "Shift": shift,
            "Hasil Dekripsi": plaintext
        })

    return results

# BAGIAN 2: DASHBOARD STREAMLIT
def render_caesar_page():

    render_header(
        title="1️⃣ Caesar Cipher",
        subtitle="Substitusi Monoalfabetik dengan Pergeseran Huruf Modulo 26",
        person_badge="Penanggung Jawab: Orang 1",
        algo_badge="Kriptografi Klasik",
        badge_class="badge-p1"
    )

    # TABS
    tab_main, tab_trace, tab_crypto, tab_theory = st.tabs([
        "🔐 Caesar Cipher",
        "🔍 Step-by-Step",
        "⚡ Brute-Force",
        "📖 Teori & Rumus"
    ])

    # TAB UTAMA
    with tab_main:

        st.markdown("##### 🔐 Caesar Cipher")

        # Pilihan Enkripsi / Dekripsi
        mode = st.radio(
            "Pilih Mode",
            ["🔒 Enkripsi", "🔓 Dekripsi"],
            horizontal=True
        )

        st.divider()

        # ----------------------------------------------------------------------
        # ENKRIPSI
        # ----------------------------------------------------------------------

        if mode == "🔒 Enkripsi":

            col1, col2 = st.columns([1, 1])

            with col1:

                st.markdown("##### 📝 Input Plaintext")

                plaintext = st.text_area(
                    "Masukkan plaintext",
                    value="Belajar Kriptografi",
                    height=100,
                    key="plaintext_input"
                )

                shift = st.slider(
                    "Kunci Pergeseran (Shift)",
                    min_value=1,
                    max_value=25,
                    value=3,
                    key="encrypt_shift"
                )

                encrypt_button = st.button(
                    "🔒 Enkripsi",
                    use_container_width=True,
                    key="encrypt_button"
                )

            with col2:

                st.markdown("##### Hasil Enkripsi")

                if encrypt_button:

                    if plaintext.strip() == "":
                        st.warning("Masukkan plaintext terlebih dahulu.")

                    else:

                        ciphertext, steps = caesar_encrypt(
                            plaintext,
                            shift
                        )

                        # Simpan hasil ke session
                        st.session_state["steps"] = steps
                        st.session_state["last_result"] = ciphertext

                        st.text_area(
                            "Ciphertext",
                            value=ciphertext,
                            height=100,
                            key="encrypt_result"
                        )

                        st.success("Enkripsi berhasil!")

                else:

                    st.info(
                        "Masukkan plaintext dan klik tombol Enkripsi."
                    )

        # DEKRIPSI
        else:

            col1, col2 = st.columns([1, 1])

            with col1:

                st.markdown("##### 📥 Input Ciphertext")

                ciphertext = st.text_area(
                    "Masukkan ciphertext",
                    value="",
                    height=100,
                    key="ciphertext_input"
                )

                shift = st.slider(
                    "Kunci Pergeseran (Shift)",
                    min_value=1,
                    max_value=25,
                    value=3,
                    key="decrypt_shift"
                )

                decrypt_button = st.button(
                    "🔓 Dekripsi",
                    use_container_width=True,
                    key="decrypt_button"
                )

            with col2:

                st.markdown("##### 🎯 Hasil Dekripsi")

                if decrypt_button:

                    if ciphertext.strip() == "":
                        st.warning("Masukkan ciphertext terlebih dahulu.")

                    else:

                        plaintext, steps = caesar_decrypt(
                            ciphertext,
                            shift
                        )

                        # Simpan hasil
                        st.session_state["steps"] = steps
                        st.session_state["last_result"] = plaintext

                        st.text_area(
                            "Plaintext",
                            value=plaintext,
                            height=100,
                            key="decrypt_result"
                        )

                        st.success("Dekripsi berhasil!")

                else:

                    st.info(
                        "Masukkan ciphertext dan klik tombol Dekripsi."
                    )


    # TAB STEP-BY-STEP
    with tab_trace:

        st.markdown("##### 🔍 Pelacakan Proses Caesar Cipher")

        if "steps" in st.session_state:

            st.dataframe(
                pd.DataFrame(
                    st.session_state["steps"]
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Lakukan enkripsi atau dekripsi terlebih dahulu "
                "untuk melihat prosesnya."
            )

    # TAB BRUTE FORCE
    with tab_crypto:

        st.markdown("##### ⚡ Kriptanalisis Brute-Force")

        st.caption(
            "Mencoba seluruh kemungkinan shift untuk menemukan plaintext."
        )

        target = st.text_area(
            "Masukkan Ciphertext",
            value="KHOOR ZRUOG",
            height=80,
            key="bruteforce_input"
        )

        brute_button = st.button(
            "🚀 Jalankan Brute-Force",
            use_container_width=True,
            key="brute_button"
        )

        if brute_button:

            if target.strip() == "":
                st.warning("Masukkan ciphertext terlebih dahulu.")

            else:

                results = caesar_bruteforce(target)

                st.dataframe(
                    pd.DataFrame(results),
                    use_container_width=True,
                    hide_index=True
                )

    # TAB TEORI
    with tab_theory:

        st.markdown("##### 📖 Teori Caesar Cipher")

        st.markdown("""
        **Caesar Cipher** merupakan algoritma kriptografi klasik
        yang menggunakan metode substitusi dengan menggeser posisi
        setiap huruf dalam alfabet.

        **Enkripsi:**

        $$C_i = (P_i + k) \\mod 26$$

        **Dekripsi:**

        $$P_i = (C_i - k) \\mod 26$$

        **Keterangan:**

        - **P** = Plaintext
        - **C** = Ciphertext
        - **k** = nilai shift/kunci
        - **26** = jumlah huruf alfabet

        **Contoh dengan k = 3:**

        `A → D`

        `B → E`

        `C → F`

        `X → A`

        `Y → B`

        `Z → C`

        Huruf besar dan kecil dipertahankan, sedangkan spasi,
        angka, dan simbol tidak mengalami perubahan.
        """)

# RUN APPLICATION

if __name__ == "__main__":

    st.set_page_config(
        page_title="Caesar Cipher",
        page_icon="🔐",
        layout="wide"
    )

    load_global_css()

    render_caesar_page()
