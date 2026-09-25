import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA RSA ASYMMETRIC CIPHER
# Penanggung Jawab: Orang 4
# ==============================================================================

def generate_rsa_keys(p: int, q: int):
    """
    TODO: Tuliskan logika pembangkitan kunci RSA di sini.
    n = p * q
    phi = (p - 1) * (q - 1)
    d = e^(-1) mod phi
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
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
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    cipher_nums = [pow(ord(c), e, n) if n > 255 else ord(c) for c in plaintext]
    cipher_str = ",".join(map(str, cipher_nums))
    steps = [
        {"Karakter": c, "ASCII": ord(c), "Rumus": f"{ord(c)}^{e} mod {n}", "Cipher": pow(ord(c), e, n) if n > 255 else ord(c)}
        for c in plaintext[:5]
    ]
    return cipher_nums, cipher_str, steps

def rsa_decrypt(cipher_input: str, d: int, n: int):
    """
    TODO: Tuliskan logika dekripsi RSA di sini.
    M = C^d mod n
    """
    # [PLACEHOLDER - Silakan ganti dengan kodinganmu]
    return f"[HASIL DEKRIPSI RSA (d={d}, n={n})]"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# Penanggung Jawab: Orang 4
# ==============================================================================

def render_rsa_page():
    render_header(
        title="4️⃣ RSA Asymmetric Cipher",
        subtitle="Kriptografi Kunci Publik & Privat Berbasis Eksponensial Modulo Bilangan Prima",
        person_badge="Penanggung Jawab: Orang 4",
        algo_badge="Kriptografi Modern",
        badge_class="badge-p4"
    )

    tab_enc, tab_dec, tab_trace, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Pembangkitan Kunci & Kalkulasi", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 🔑 1. Parameter Bilangan Prima (p & q)")
            cp, cq = st.columns(2)
            with cp:
                p_in = st.number_input("Prima p:", min_value=11, max_value=997, value=61, step=2, key="rsa_p_in")
            with cq:
                q_in = st.number_input("Prima q:", min_value=11, max_value=997, value=53, step=2, key="rsa_q_in")

            keys = generate_rsa_keys(p_in, q_in)
            st.session_state["rsa_keys"] = keys
            st.success(f"Kunci Terbentuk: n = {keys['n']} | e = {keys['e']} | d = {keys['d']}")

            st.markdown("##### 📝 2. Plaintext")
            p_text = st.text_area("Masukkan Plaintext:", value="KRIPTOGRAFI", height=100, key="rsa_p_text")
            btn_rsa_enc = st.button("🔒 Enkripsi Sekarang", key="rsa_btn_enc", use_container_width=True)

        with c2:
            st.markdown("##### 🎯 Hasil Enkripsi")
            if btn_rsa_enc:
                k = st.session_state["rsa_keys"]
                nums, c_str, steps_rsa = rsa_encrypt(p_text, k["e"], k["n"])
                st.session_state["rsa_steps"] = steps_rsa
                st.text_area("Ciphertext (Deret Angka):", value=c_str, height=120)
                st.success("Enkripsi RSA berhasil diproses!")
            else:
                st.info("Klik tombol 'Enkripsi Sekarang' untuk melihat hasil.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 🔑 Parameter Kunci Privat")
            k_n = st.session_state["rsa_keys"]["n"] if "rsa_keys" in st.session_state else 3233
            k_d = st.session_state["rsa_keys"]["d"] if "rsa_keys" in st.session_state else 2753
            cd, cn = st.columns(2)
            with cd:
                d_in = st.number_input("Kunci Privat d:", min_value=1, value=k_d, key="rsa_d_in")
            with cn:
                n_in = st.number_input("Modulus n:", min_value=1, value=k_n, key="rsa_n_in")

            c_rsa_in = st.text_area("Masukkan Ciphertext (Angka dipisah koma):", value="", height=100, key="rsa_dec_in")
            btn_rsa_dec = st.button("🔓 Dekripsi Sekarang", key="rsa_btn_dec", use_container_width=True)

        with c2:
            st.markdown("##### 🎯 Hasil Dekripsi")
            if btn_rsa_dec:
                rec_rsa = rsa_decrypt(c_rsa_in, d_in, n_in)
                st.text_area("Plaintext Rekonstruksi:", value=rec_rsa, height=120)
                st.success("Dekripsi RSA berhasil diproses!")
            else:
                st.info("Klik tombol 'Dekripsi Sekarang' untuk melihat hasil.")

    with tab_trace:
        st.markdown("#### 🔍 Pelacakan Kalkulasi RSA")
        if "rsa_steps" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["rsa_steps"]), use_container_width=True)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk melihat langkah kalkulasi.")

    with tab_theory:
        st.markdown("""
        ### 📖 Teori RSA Asymmetric Cipher
        * **Kategori**: Kriptografi Kunci Asimetris (*Public-Key Cryptography*).
        * **Rumus**:
          * $n = p \\times q$
          * $\\phi(n) = (p-1)(q-1)$
          * Enkripsi: $C = M^e \\pmod n$
          * Dekripsi: $M = C^d \\pmod n$
        """)

# Standalone runner: Orang 4 bisa langsung menjalankan file ini saja
if __name__ == "__main__":
    st.set_page_config(page_title="RSA - Orang 4", page_icon="🔐", layout="wide")
    load_global_css()
    render_rsa_page()
