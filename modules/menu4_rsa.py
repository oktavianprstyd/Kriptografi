import streamlit as st
import pandas as pd
import math

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA RSA ASYMMETRIC CIPHER (ORANG 4)
# ==============================================================================
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e: int, phi: int) -> int:
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Invers modulo tidak ada!")
    return (x % phi + phi) % phi

def generate_rsa_keys(p: int, q: int, e: int = 65537):
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p dan q harus merupakan bilangan prima!")
    if p == q:
        raise ValueError("p dan q harus berbeda!")
    
    n = p * q
    phi = (p - 1) * (q - 1)

    if math.gcd(e, phi) != 1 or e >= phi:
        candidates = [3, 5, 17, 257, 65537]
        for c in candidates:
            if c < phi and math.gcd(c, phi) == 1:
                e = c
                break
        else:
            for c in range(3, phi, 2):
                if math.gcd(c, phi) == 1:
                    e = c
                    break

    d = mod_inverse(e, phi)
    return {
        "p": p, "q": q, "n": n, "phi": phi,
        "e": e, "d": d,
        "public_key": (e, n), "private_key": (d, n)
    }

def rsa_encrypt(text: str, e: int, n: int):
    cipher_nums = []
    steps = []
    for idx, char in enumerate(text):
        m_val = ord(char)
        if m_val >= n:
            raise ValueError(f"Karakter '{char}' (ASCII {m_val}) >= n ({n}). Gunakan prima p dan q yang lebih besar!")
        c_val = pow(m_val, e, n)
        cipher_nums.append(c_val)
        steps.append({
            "idx": idx + 1, "char": repr(char)[1:-1] if char == ' ' else char,
            "m_val": m_val, "formula": f"{m_val}^{e} mod {n} = {c_val}",
            "c_val": c_val
        })
    return cipher_nums, ",".join(map(str, cipher_nums)), steps

def rsa_decrypt(cipher_input, d: int, n: int):
    if isinstance(cipher_input, str):
        cleaned = cipher_input.replace("\n", " ").replace(";", ",").replace(" ", ",")
        cipher_nums = [int(x.strip()) for x in cleaned.split(",") if x.strip().isdigit()]
    elif isinstance(cipher_input, list):
        cipher_nums = cipher_input
    else:
        raise ValueError("Format input tidak valid.")

    recovered_chars = []
    steps = []
    for idx, c_val in enumerate(cipher_nums):
        m_val = pow(c_val, d, n)
        char = chr(m_val)
        recovered_chars.append(char)
        steps.append({
            "idx": idx + 1, "c_val": c_val,
            "formula": f"{c_val}^{d} mod {n} = {m_val}",
            "m_val": m_val, "char": repr(char)[1:-1] if char == ' ' else char
        })
    return "".join(recovered_chars), steps

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (ORANG 4)
# ==============================================================================
def render_rsa_page():
    render_header(
        "4️⃣ RSA Asymmetric Cipher",
        "Kriptografi Kunci Publik & Privat Berbasis Eksponensial Modulo Bilangan Prima",
        "Penanggung Jawab: Orang 4",
        "Kriptografi Modern",
        "badge-p4"
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
                p_in = st.number_input("Prima p:", 11, 997, 61, step=2, key="rsa_p_in")
            with cq:
                q_in = st.number_input("Prima q:", 11, 997, 53, step=2, key="rsa_q_in")

            try:
                keys = generate_rsa_keys(p_in, q_in)
                st.session_state["rsa_keys"] = keys
                st.success(f"Modulus n = {keys['n']} | Totient φ = {keys['phi']} | e = {keys['e']} | d = {keys['d']}")
                st.caption(f"Kunci Publik: `(e={keys['e']}, n={keys['n']})` | Kunci Privat: `(d={keys['d']}, n={keys['n']})`")
            except Exception as e:
                st.error(f"Error kunci: {str(e)}")

            st.markdown("##### 📝 2. Plaintext")
            p_text = st.text_area("Masukkan Plaintext:", value="KRIPTOGRAFI MAJU", height=100, key="rsa_p_text")
            btn_rsa_enc = st.button("🔒 Enkripsi Sekarang", key="rsa_btn_enc", use_container_width=True)

        with c2:
            if p_text and "rsa_keys" in st.session_state:
                try:
                    k = st.session_state["rsa_keys"]
                    nums, c_str, steps_rsa = rsa_encrypt(p_text, k["e"], k["n"])
                    st.session_state["rsa_steps"] = steps_rsa
                    st.text_area("Hasil Ciphertext (Deret Angka):", value=c_str, height=120)
                    st.info(f"Jumlah Angka Sandi: **{len(nums)}** | Enkripsi: $C = M^{k['e']} \\pmod{{{k['n']}}}$")
                except Exception as e:
                    st.error(f"Gagal mengenkripsi: {str(e)}")

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
            if c_rsa_in:
                try:
                    rec_rsa, _ = rsa_decrypt(c_rsa_in, d_in, n_in)
                    st.text_area("Hasil Plaintext Rekonstruksi:", value=rec_rsa, height=120)
                    st.success("Dekripsi RSA Sukses!")
                    st.code(f"Formula: M ≡ C^{d_in} mod {n_in}")
                except Exception as e:
                    st.error(f"Gagal mendekripsi: {str(e)}")

    with tab_trace:
        st.markdown("#### 🔍 Pelacakan Kalkulasi RSA")
        if "rsa_steps" in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state["rsa_steps"]), use_container_width=True, height=350)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk memuat tabel pelacakan.")

    with tab_theory:
        st.markdown("""
        ### 📖 Teori RSA Asymmetric Cipher
        * **Kategori**: Kriptografi Kunci Publik & Privat (*Public-Key Cryptography*).
        * **Rumus**:
          * $n = p \\times q$
          * $\\phi(n) = (p-1)(q-1)$
          * $e \\cdot d \\equiv 1 \\pmod{\\phi(n)}$
          * Enkripsi: $C = M^e \\pmod n$
          * Dekripsi: $M = C^d \\pmod n$
        * **Keamanan**: Bergantung pada sulitnya faktorisasi bilangan komposit besar (*Integer Factorization*).
        """)

# Standalone runner untuk pengujian mandiri Orang 4
if __name__ == "__main__":
    st.set_page_config(page_title="RSA Cipher - Orang 4", page_icon="🔐", layout="wide")
    load_global_css()
    render_rsa_page()
