import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA RSA ASYMMETRIC CIPHER
# Penanggung Jawab: Orang 4
# ==============================================================================

def generate_rsa_keys(p: int, q: int):
    """
    TODO: Tuliskan logika pembangkitan kunci RSA di sini.
    n = p * q
    phi = (p - 1) * (q - 1)
    d = e^(-1) mod phi
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = 2753
    return {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}

def rsa_encrypt(plaintext: str, e: int, n: int):
    """
    TODO: Tuliskan logika enkripsi RSA di sini.
    C = M^e mod n
    """
    cipher_nums = [pow(ord(c), e, n) if n > 255 else ord(c) for c in plaintext]
    cipher_str = ",".join(map(str, cipher_nums))
    steps = [
        {"Karakter": c, "ASCII (M)": ord(c), "Formula": f"{ord(c)}^{e} mod {n}", "Hasil Cipher (C)": pow(ord(c), e, n) if n > 255 else ord(c)}
        for c in plaintext[:6]
    ]
    return cipher_nums, cipher_str, steps

def rsa_decrypt(cipher_input: str, d: int, n: int):
    """
    TODO: Tuliskan logika dekripsi RSA di sini.
    M = C^d mod n
    """
    return f"[HASIL DEKRIPSI RSA (d={d}, n={n})]"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_rsa_page():
    render_header(
        title="Menu 4: RSA Asymmetric Cipher",
        subtitle="Kriptografi Kunci Publik & Privat Berbasis Eksponensial Modulo Bilangan Prima",
        pic_name="Penanggung Jawab: Orang 4",
        category="Kriptografi Modern"
    )

    tab_main, tab_trace, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pembangkitan Kunci & Langkah Kalkulasi",
        "Teori & Formula"
    ])

    with tab_main:
        mode = st.radio(
            "Pilih Mode Operasi",
            ["Enkripsi Pesan", "Dekripsi Pesan"],
            horizontal=True,
            key="rsa_mode"
        )
        st.divider()

        if mode == "Enkripsi Pesan":
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Parameter Bilangan Prima (p & q)")
                cp, cq = st.columns(2)
                with cp:
                    p_in = st.number_input("Prima p:", min_value=11, max_value=997, value=61, step=2, key="rsa_p_in")
                with cq:
                    q_in = st.number_input("Prima q:", min_value=11, max_value=997, value=53, step=2, key="rsa_q_in")

                keys = generate_rsa_keys(p_in, q_in)
                st.session_state["rsa_keys"] = keys
                st.caption(f"Kunci Terbentuk: n = {keys['n']} | e = {keys['e']} | d = {keys['d']}")

                st.markdown("##### Input Plainteks")
                p_text = st.text_area("Masukkan teks plainteks:", value="KRIPTOGRAFI", height=100, key="rsa_p_text")
                btn_rsa_enc = st.button("Enkripsi Pesan", key="rsa_btn_enc", use_container_width=True)

            with col2:
                st.markdown("##### Hasil Enkripsi")
                if btn_rsa_enc:
                    k = st.session_state["rsa_keys"]
                    nums, c_str, steps_rsa = rsa_encrypt(p_text, k["e"], k["n"])
                    st.session_state["rsa_steps"] = steps_rsa
                    st.text_area("Cipherteks (Deret Angka Sandi):", value=c_str, height=120)
                    st.success("Proses enkripsi RSA selesai diproses.")
                else:
                    st.info("Tekan tombol 'Enkripsi Pesan' untuk memproses teks.")

        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Parameter Kunci Privat Dekripsi")
                k_n = st.session_state["rsa_keys"]["n"] if "rsa_keys" in st.session_state else 3233
                k_d = st.session_state["rsa_keys"]["d"] if "rsa_keys" in st.session_state else 2753
                cd, cn = st.columns(2)
                with cd:
                    d_in = st.number_input("Kunci Privat d:", min_value=1, value=k_d, key="rsa_d_in")
                with cn:
                    n_in = st.number_input("Modulus n:", min_value=1, value=k_n, key="rsa_n_in")

                c_rsa_in = st.text_area("Masukkan deret angka cipherteks:", value="", height=100, key="rsa_dec_in")
                btn_rsa_dec = st.button("Dekripsi Pesan", key="rsa_btn_dec", use_container_width=True)

            with col2:
                st.markdown("##### Hasil Dekripsi")
                if btn_rsa_dec:
                    rec_rsa = rsa_decrypt(c_rsa_in, d_in, n_in)
                    st.text_area("Teks Plainteks Rekonstruksi:", value=rec_rsa, height=120)
                    st.success("Proses dekripsi RSA selesai diproses.")
                else:
                    st.info("Tekan tombol 'Dekripsi Pesan' untuk memproses teks.")

    with tab_trace:
        st.markdown("##### Pelacakan Kalkulasi Eksponensial Modulo")
        if "rsa_steps" in st.session_state and st.session_state["rsa_steps"]:
            st.dataframe(pd.DataFrame(st.session_state["rsa_steps"]), use_container_width=True)
        else:
            st.info("Lakukan proses enkripsi terlebih dahulu untuk memuat langkah.")

    with tab_theory:
        st.markdown("##### Teori & Formula RSA (Rivest-Shamir-Adleman)")
        st.markdown("""
        **RSA** adalah algoritma kriptografi kunci asimetris (*public-key cryptography*) yang menggunakan 
        sepasang kunci: **Kunci Publik** $(e, n)$ untuk enkripsi dan **Kunci Privat** $(d, n)$ untuk dekripsi.

        * **Pembentukan Kunci**:
          1. Pilih dua bilangan prima: $p$ dan $q$
          2. Hitung modulus: $n = p \\times q$
          3. Hitung totient: $\\phi(n) = (p-1)(q-1)$
          4. Tentukan eksponen publik $e$ dan hitung invers modulo $d \\equiv e^{-1} \\pmod{\\phi(n)}$

        * **Formula Enkripsi**:
          $$C \\equiv M^e \\pmod n$$

        * **Formula Dekripsi**:
          $$M \\equiv C^d \\pmod n$$
        """)

# Standalone runner: Orang 4
if __name__ == "__main__":
    st.set_page_config(page_title="RSA Cipher - Orang 4", layout="wide")
    load_global_css()
    render_rsa_page()
