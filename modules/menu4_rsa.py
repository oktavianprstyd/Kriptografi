import math
import random
import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css


# ==============================================================================
# BAGIAN 1: LOGIKA & MATEMATIKA RSA ASYMMETRIC CIPHER
# Penanggung Jawab: Orang 4
# ==============================================================================

def is_prime(n: int) -> bool:
    """Uji keprimaan deterministik untuk bilangan bulat positif."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def get_prime_presets() -> list[dict]:
    """Daftar pilihan bilangan prima ramah edukasi yang umum digunakan."""
    return [
        {"label": "Preset Standar Buku (p=61, q=53 -> n=3233, e=17)", "p": 61, "q": 53, "e": 17},
        {"label": "Preset Menengah (p=101, q=103 -> n=10403, e=17)", "p": 101, "q": 103, "e": 17},
        {"label": "Preset Nilai Prima Lebih Besar (p=137, q=149 -> n=20413, e=65537)", "p": 137, "q": 149, "e": 65537},
        {"label": "Preset Uji Kecil (p=17, q=19 -> n=323, e=5)", "p": 17, "q": 19, "e": 5},
    ]


def extended_euclidean(a: int, b: int):
    """
    Algoritma Euclidean Diperluas (Extended Euclidean Algorithm).
    Mencari gcd(a, b) serta koefisien s dan t sehingga: a*s + b*t = gcd(a, b).
    Menghasilkan rekaman langkah demi langkah untuk visualisasi edukasi.
    """
    trace_steps = []
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    step_no = 1

    while r1 != 0:
        q = r0 // r1
        r = r0 % r1
        s = s0 - q * s1
        t = t0 - q * t1

        trace_steps.append({
            "Langkah": step_no,
            "Persamaan Pembagian": f"{r0} = ({q} × {r1}) + {r}",
            "Quotient (q)": q,
            "Sisa (r)": r,
            "Koefisien s": s,
            "Koefisien t": t
        })

        r0, r1 = r1, r
        s0, s1 = s1, s
        t0, t1 = t1, t
        step_no += 1

    return r0, s0, t0, trace_steps


def mod_inverse(e: int, phi: int):
    """
    Menghitung invers perkalian modulo: d = e^(-1) mod phi.
    Menggunakan Algoritma Euclidean Diperluas.
    """
    gcd, x, _, trace_steps = extended_euclidean(e, phi)
    if gcd != 1:
        raise ValueError(f"Invers modulo tidak ada karena gcd({e}, {phi}) = {gcd} != 1. Pilih eksponen publik 'e' lain!")
    d = (x % phi + phi) % phi
    return d, trace_steps


def square_and_multiply(base: int, exp: int, mod: int):
    """
    Simulasi Eksponensial Modulo Cepat (Square-and-Multiply / Binary Exponentiation).
    Menghitung (base^exp) mod mod dengan kompleksitas O(log exp).
    Menghasilkan rekaman kalkulasi per bit biner.
    """
    binary_exp = bin(exp)[2:]
    accum = 1
    trace = []

    for idx, bit in enumerate(binary_exp):
        prev_accum = accum
        accum = (accum * accum) % mod
        operation_desc = f"Kuadrat: ({prev_accum}² mod {mod}) = {accum}"

        if bit == '1':
            accum_before = accum
            accum = (accum * base) % mod
            operation_desc += f" ➔ Kalikan Basis: ({accum_before} × {base} mod {mod}) = {accum}"

        trace.append({
            "Iterasi": idx + 1,
            "Bit Biner (e)": bit,
            "Operasi Kalkulasi": operation_desc,
            "Hasil Sementara": accum
        })

    return accum, trace


def generate_rsa_keys(p: int, q: int, e_preferred: int = 17):
    """
    Membangkitkan sepasang Kunci Publik (e, n) dan Kunci Privat (d, n) RSA:
    1. Validasi keprimaan p dan q
    2. n = p * q
    3. phi = (p - 1) * (q - 1)
    4. Cari / validasi e relatif prima terhadap phi
    5. Hitung d = e^(-1) mod phi
    """
    if not is_prime(p):
        raise ValueError(f"Nilai p = {p} bukan bilangan prima!")
    if not is_prime(q):
        raise ValueError(f"Nilai q = {q} bukan bilangan prima!")
    if p == q:
        raise ValueError(f"Nilai p dan q tidak boleh bernilai sama ({p})! RSA mewajibkan dua prima yang berbeda.")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Validasi atau cari e yang valid
    candidate_e = e_preferred
    if math.gcd(candidate_e, phi) != 1 or candidate_e >= phi or candidate_e <= 1:
        # Coba daftar kandidat eksponen publik standar
        standard_candidates = [17, 65537, 3, 5, 257, 7, 11, 13]
        found = False
        for cand in standard_candidates:
            if cand < phi and math.gcd(cand, phi) == 1:
                candidate_e = cand
                found = True
                break
        if not found:
            for cand in range(3, min(phi, 1000), 2):
                if math.gcd(cand, phi) == 1:
                    candidate_e = cand
                    found = True
                    break

    d, eea_trace = mod_inverse(candidate_e, phi)

    return {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": candidate_e,
        "d": d,
        "public_key": (candidate_e, n),
        "private_key": (d, n),
        "eea_trace": eea_trace
    }


def parse_cipher_input(cipher_input) -> list[int]:
    """
    Mem-parsing input cipherteks RSA secara fleksibel:
    Mendukung format koma (597, 1859), spasi, baris baru, format list [597, 1859], ataupun list integer langsung.
    """
    if isinstance(cipher_input, list):
        return [int(x) for x in cipher_input]
    if isinstance(cipher_input, str):
        cleaned = (
            cipher_input.replace("[", " ")
            .replace("]", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("\n", " ")
        )
        tokens = [t.strip() for t in cleaned.split() if t.strip()]
        numbers = []
        for tok in tokens:
            if tok.isdigit() or (tok.startswith("-") and tok[1:].isdigit()):
                numbers.append(int(tok))
            elif tok.lower().startswith("0x"):
                try:
                    numbers.append(int(tok, 16))
                except ValueError:
                    pass
        return numbers
    return []


def rsa_encrypt(plaintext: str, e: int, n: int):
    """
    Enkripsi RSA per karakter teks:
    C = M^e mod n, di mana M = ord(char)
    Mengembalikan: (cipher_nums, cipher_str, steps)
    """
    cipher_nums = []
    steps = []

    for idx, char in enumerate(plaintext):
        m_val = ord(char)
        if m_val >= n:
            raise ValueError(
                f"Karakter '{char}' memiliki kode ASCII {m_val} >= modulus n ({n}). "
                f"Modulus RSA (p × q) wajib lebih besar dari 255 agar seluruh karakter ASCII dapat dienkripsi dengan aman."
            )

        c_val = pow(m_val, e, n)
        cipher_nums.append(c_val)
        steps.append({
            "No": idx + 1,
            "Karakter": repr(char)[1:-1] if char == " " else char,
            "ASCII (M)": m_val,
            "Formula Modulo": f"{m_val}^{e} mod {n}",
            "Hasil Cipher (C)": c_val,
            "Format Hex": f"0x{c_val:04X}"
        })

    cipher_str = ", ".join(map(str, cipher_nums))
    return cipher_nums, cipher_str, steps


def rsa_decrypt(cipher_input, d: int, n: int):
    """
    Dekripsi RSA per angka sandi:
    M = C^d mod n, di mana karakter = chr(M)
    Mengembalikan: (recovered_text, steps)
    """
    cipher_nums = parse_cipher_input(cipher_input)
    if not cipher_nums:
        return "", []

    recovered_chars = []
    steps = []

    for idx, c_val in enumerate(cipher_nums):
        m_val = pow(c_val, d, n)
        try:
            char = chr(m_val)
        except (ValueError, OverflowError):
            char = "?"

        recovered_chars.append(char)
        steps.append({
            "No": idx + 1,
            "Cipher (C)": c_val,
            "Formula Modulo": f"{c_val}^{d} mod {n}",
            "Nilai ASCII (M)": m_val,
            "Karakter Plain": repr(char)[1:-1] if char == " " else char
        })

    recovered_text = "".join(recovered_chars)
    return recovered_text, steps


def rsa_sign(message: str, d: int, n: int):
    """
    Pembuatan Tanda Tangan Digital (Digital Signature) dengan RSA:
    S = M^d mod n (menggunakan Kunci Privat d)
    """
    sig_nums = []
    for char in message:
        m_val = ord(char)
        s_val = pow(m_val, d, n)
        sig_nums.append(s_val)
    sig_str = ", ".join(map(str, sig_nums))
    return sig_nums, sig_str


def rsa_verify(message: str, signature_input, e: int, n: int):
    """
    Verifikasi Tanda Tangan Digital dengan RSA:
    M' = S^e mod n (menggunakan Kunci Publik e)
    Jika M' == M untuk seluruh karakter, maka tanda tangan valid & otentik.
    """
    sig_nums = parse_cipher_input(signature_input)
    if len(sig_nums) != len(message):
        return False, []

    verified_chars = []
    steps = []
    is_valid = True

    for idx, (char, s_val) in enumerate(zip(message, sig_nums)):
        m_expected = ord(char)
        m_recovered = pow(s_val, e, n)
        match = (m_expected == m_recovered)
        if not match:
            is_valid = False

        verified_chars.append(chr(m_recovered) if m_recovered < 1114112 else "?")
        steps.append({
            "No": idx + 1,
            "Karakter Pesan": char,
            "ASCII Pesan (M)": m_expected,
            "Tanda Tangan (S)": s_val,
            "Formula Verifikasi": f"{s_val}^{e} mod {n}",
            "Hasil Rekonstruksi (M')": m_recovered,
            "Status Cocok": "VALID" if match else "TIDAK VALID"
        })

    return is_valid, steps


# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - WARM CREAM & DEEP NAVY)
# ==============================================================================

def render_rsa_page():
    render_header(
        title="Menu 4: RSA Asymmetric Cipher",
        subtitle="Kriptografi Kunci Publik & Privat Berbasis Faktorisasi Bilangan Prima dan Eksponensial Modulo",
        pic_name="Penanggung Jawab: Orang 4",
        category="Kriptografi Modern"
    )

    # Inisialisasi default kunci di session_state jika belum ada
    if "rsa_keys" not in st.session_state:
        st.session_state["rsa_keys"] = generate_rsa_keys(61, 53, 17)
    if "rsa_cipher_result" not in st.session_state:
        st.session_state["rsa_cipher_result"] = ""
    if "rsa_steps" not in st.session_state:
        st.session_state["rsa_steps"] = []
    if "rsa_dec_steps" not in st.session_state:
        st.session_state["rsa_dec_steps"] = []

    tab_main, tab_trace, tab_sign, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pelacakan Proses Step-by-Step",
        "Digital Signature & Integritas Pesan",
        "Teori & Landasan Matematis"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: OPERASI ENKRIPSI & DEKRIPSI
    # --------------------------------------------------------------------------
    with tab_main:
        # Panel Pembangkitan Kunci RSA Interaktif
        st.markdown("##### 1. Konfigurasi Kunci Asimetris RSA")
        with st.expander("Panel Pemilihan & Pembangkitan Kunci Prima (p & q)", expanded=True):
            col_preset, col_custom = st.columns([1, 1])

            presets = get_prime_presets()
            preset_labels = [p["label"] for p in presets] + ["Kustom Manual (Masukkan p & q Sendiri)"]

            with col_preset:
                selected_preset = st.selectbox(
                    "Pilih Preset Bilangan Prima:",
                    preset_labels,
                    index=0,
                    key="rsa_preset_choice"
                )

            if selected_preset != "Kustom Manual (Masukkan p & q Sendiri)":
                chosen_preset = next(p for p in presets if p["label"] == selected_preset)
                p_val = chosen_preset["p"]
                q_val = chosen_preset["q"]
                e_default = chosen_preset["e"]
            else:
                p_val = 61
                q_val = 53
                e_default = 17

            col_p, col_q, col_e = st.columns(3)
            with col_p:
                p_in = st.number_input("Bilangan Prima p:", min_value=3, max_value=9999, value=p_val, step=1, key="rsa_p_input")
            with col_q:
                q_in = st.number_input("Bilangan Prima q:", min_value=3, max_value=9999, value=q_val, step=1, key="rsa_q_input")
            with col_e:
                e_in = st.number_input("Eksponen Publik e:", min_value=3, max_value=65537, value=e_default, step=1, key="rsa_e_input")

            # Tombol generate / update kunci
            if st.button("Bangkitkan Pasangan Kunci RSA", key="rsa_btn_gen_keys"):
                try:
                    new_keys = generate_rsa_keys(int(p_in), int(q_in), int(e_in))
                    st.session_state["rsa_keys"] = new_keys
                    st.success(f"Kunci RSA berhasil diperbarui! Modulus n = {new_keys['n']}, e = {new_keys['e']}, d = {new_keys['d']}")
                except ValueError as err:
                    st.error(f"Gagal membentuk kunci: {err}")

            # Kartu Info Kunci Aktif
            curr_keys = st.session_state["rsa_keys"]
            n_status = "Aman untuk ASCII (> 255)" if curr_keys["n"] > 255 else "Peringatan: n <= 255 (Hanya huruf kecil/angka terbatas)"

            col_k1, col_k2 = st.columns(2)
            with col_k1:
                st.markdown(f"""
                <div class="datain-card" style="margin-bottom: 0.5rem; padding: 1rem;">
                    <span class="badge-category">Kunci Publik (Public Key)</span>
                    <p style="margin: 6px 0 2px 0; color: #1E3A5F; font-size: 0.95rem;">
                        <b>Pasangan Kunci (e, n):</b> <code style="color: #002D80;">({curr_keys['e']}, {curr_keys['n']})</code>
                    </p>
                    <small style="color: #4A709C;">Digunakan oleh siapapun untuk mengenkripsi pesan dan memverifikasi tanda tangan.</small>
                </div>
                """, unsafe_allow_html=True)
            with col_k2:
                st.markdown(f"""
                <div class="datain-card" style="margin-bottom: 0.5rem; padding: 1rem;">
                    <span class="badge-category">Kunci Privat (Private Key)</span>
                    <p style="margin: 6px 0 2px 0; color: #1E3A5F; font-size: 0.95rem;">
                        <b>Pasangan Kunci (d, n):</b> <code style="color: #002D80;">({curr_keys['d']}, {curr_keys['n']})</code>
                    </p>
                    <small style="color: #4A709C;">Wajib dirahasiakan pemilik untuk mendekripsi pesan dan menandatangani dokumen.</small>
                </div>
                """, unsafe_allow_html=True)

            st.caption(f"Status Modulus: n = {curr_keys['n']} ({n_status}) | Totient phi(n) = {curr_keys['phi']}")

        st.markdown("---")

        # Mode Operasi (Enkripsi vs Dekripsi)
        mode = st.radio(
            "Pilih Mode Operasi",
            ["Enkripsi Pesan", "Dekripsi Pesan"],
            horizontal=True,
            key="rsa_op_mode"
        )
        st.divider()

        # MODE ENKRIPSI
        if mode == "Enkripsi Pesan":
            c_inp, c_out = st.columns([1, 1])

            with c_inp:
                st.markdown("##### Input Teks Plainteks")
                plain_input = st.text_area(
                    "Masukkan pesan teks yang ingin dienkripsi:",
                    value="KRIPTOGRAFI INFORMATIKA UPN",
                    height=130,
                    key="rsa_enc_plain_text"
                )
                btn_encrypt = st.button("Jalankan Enkripsi RSA", key="rsa_run_encrypt")

            with c_out:
                st.markdown("##### Hasil Enkripsi RSA")
                if btn_encrypt:
                    k = st.session_state["rsa_keys"]
                    try:
                        c_nums, c_str, enc_steps = rsa_encrypt(plain_input, k["e"], k["n"])
                        st.session_state["rsa_cipher_result"] = c_str
                        st.session_state["rsa_steps"] = enc_steps

                        st.markdown("**Cipherteks (Deret Angka Modulo):**")
                        st.markdown(f'<div class="cipher-box">{c_str}</div>', unsafe_allow_html=True)

                        hex_repr = " ".join([f"0x{num:04X}" for num in c_nums])
                        st.markdown("**Representasi Heksadesimal:**")
                        st.markdown(f'<div class="cipher-box" style="font-size: 0.85rem;">{hex_repr}</div>', unsafe_allow_html=True)

                        st.success(f"Enkripsi berhasil diproses! ({len(c_nums)} karakter terenkripsi)")
                    except ValueError as ex:
                        st.error(f"Kesalahan enkripsi: {ex}")
                else:
                    if st.session_state["rsa_cipher_result"]:
                        st.markdown("**Cipherteks Sebelumnya:**")
                        st.markdown(f'<div class="cipher-box">{st.session_state["rsa_cipher_result"]}</div>', unsafe_allow_html=True)
                    else:
                        st.info("Tekan tombol 'Jalankan Enkripsi RSA' untuk memproses teks.")

        # MODE DEKRIPSI
        else:
            c_dec_inp, c_dec_out = st.columns([1, 1])

            with c_dec_inp:
                st.markdown("##### Input Cipherteks & Kunci Privat")
                col_d, col_n = st.columns(2)
                curr_k = st.session_state["rsa_keys"]
                with col_d:
                    d_input = st.number_input("Kunci Privat d:", min_value=1, value=curr_k["d"], key="rsa_dec_d")
                with col_n:
                    n_input = st.number_input("Modulus n:", min_value=1, value=curr_k["n"], key="rsa_dec_n")

                cipher_val_init = st.session_state.get("rsa_cipher_result", "597, 1859, 1486, 2933, 2159, 1307, 669, 1859, 2790, 325, 1486")
                cipher_input = st.text_area(
                    "Masukkan deret angka cipherteks (pisahkan dengan koma atau spasi):",
                    value=cipher_val_init,
                    height=130,
                    key="rsa_dec_cipher_text"
                )
                btn_decrypt = st.button("Jalankan Dekripsi RSA", key="rsa_run_decrypt")

            with c_dec_out:
                st.markdown("##### Hasil Rekonstruksi Plainteks")
                if btn_decrypt:
                    try:
                        recovered_msg, dec_steps = rsa_decrypt(cipher_input, int(d_input), int(n_input))
                        st.session_state["rsa_dec_steps"] = dec_steps

                        st.markdown("**Plainteks Rekonstruksi:**")
                        st.markdown(f'<div class="cipher-box" style="font-weight: 600; font-size: 1.05rem;">{recovered_msg}</div>', unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="datain-card" style="margin-top: 1rem; padding: 0.85rem;">
                            <span class="badge-category">Verifikasi Dekripsi</span>
                            <p style="margin: 6px 0 0 0; color: #1E3A5F; font-size: 0.9rem;">
                                Seluruh deret cipherteks berhasil dikembalikan ke karakter teks semula menggunakan formula: 
                                <code>M = C^d mod n</code>.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.success(f"Dekripsi berhasil diselesaikan! ({len(dec_steps)} blok sandi didekripsi)")
                    except Exception as err:
                        st.error(f"Kesalahan dekripsi: {err}")
                else:
                    st.info("Tekan tombol 'Jalankan Dekripsi RSA' untuk memulihkan pesan asli.")

    # --------------------------------------------------------------------------
    # TAB 2: PELACAKAN PROSES STEP-BY-STEP
    # --------------------------------------------------------------------------
    with tab_trace:
        st.markdown("##### 1. Tabel Pelacakan Enkripsi per Karakter (M^e mod n)")
        if st.session_state.get("rsa_steps"):
            df_enc = pd.DataFrame(st.session_state["rsa_steps"])
            st.dataframe(df_enc, width="stretch", hide_index=True)
        else:
            st.info("Lakukan enkripsi di Tab 'Operasi Enkripsi & Dekripsi' untuk melihat tabel kalkulasi ini.")

        st.markdown("---")

        st.markdown("##### 2. Pembuktian Kunci Privat d: Extended Euclidean Algorithm (EEA)")
        st.markdown(
            "Perhitungan nilai $d$ merupakan invers perkalian modular dari $e$ modulo $\\phi(n)$, yaitu "
            "$e \\times d \\equiv 1 \\pmod{\\phi(n)}$. Tabel di bawah menampilkan langkah algoritma pembagian Euclidean diperluas:"
        )
        curr_keys = st.session_state["rsa_keys"]
        if curr_keys.get("eea_trace"):
            df_eea = pd.DataFrame(curr_keys["eea_trace"])
            st.dataframe(df_eea, width="stretch", hide_index=True)
            st.caption(f"Hasil Pembuktian Invers: e = {curr_keys['e']}, phi(n) = {curr_keys['phi']} ➔ d = {curr_keys['d']}")

        st.markdown("---")

        st.markdown("##### 3. Simulasi Algoritma Square-and-Multiply (Fast Modular Exponentiation)")
        st.markdown(
            "Dalam implementasi komputer riil, perhitungan $M^e \\pmod n$ tidak dilakukan dengan menghitung angka $M^e$ raksasa terlebih dahulu, "
            "melainkan menggunakan metode *Square-and-Multiply* berbasis representasi biner dari eksponen $e$:"
        )

        sample_char = "K"
        sample_m = ord(sample_char)
        sample_e = curr_keys["e"]
        sample_n = curr_keys["n"]

        sample_res, sample_trace = square_and_multiply(sample_m, sample_e, sample_n)

        col_sm_info, col_sm_table = st.columns([1, 2])
        with col_sm_info:
            st.markdown(f"""
            <div class="datain-card" style="padding: 1rem;">
                <span class="badge-pic">Contoh Sampel Karakter</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">'{sample_char}' (ASCII: {sample_m})</h4>
                <p style="color: #4A709C; font-size: 0.9rem; line-height: 1.5; margin-bottom: 8px;">
                    Eksponen e = <b>{sample_e}</b><br>
                    Representasi Biner: <code>{bin(sample_e)[2:]}</code><br>
                    Modulus n = <b>{sample_n}</b>
                </p>
                <div style="background: #FAF6F0; padding: 6px 10px; border-radius: 6px; border: 1px solid #D8CFC4; font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #002D80;">
                    Hasil Akhir: {sample_res}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_sm_table:
            df_sm = pd.DataFrame(sample_trace)
            st.dataframe(df_sm, width="stretch", hide_index=True)

    # --------------------------------------------------------------------------
    # TAB 3: DIGITAL SIGNATURE & INTEGRITAS PESAN
    # --------------------------------------------------------------------------
    with tab_sign:
        st.markdown("##### Konsep Tanda Tangan Digital (Digital Signature)")
        st.markdown("""
        RSA memiliki sifat simetri matematis yang unik: selain digunakan untuk **Kerahasiaan (*Confidentiality*)**, 
        RSA juga merupakan standar industri untuk **Tanda Tangan Digital (*Authenticity & Non-Repudiation*)**.
        
        * **Penandatanganan Dokumen:** Pengirim mengenkripsi pesan menggunakan **Kunci Privat ($d$)**:
          $$S \\equiv M^d \\pmod n$$
        * **Verifikasi Dokumen:** Siapapun dapat memverifikasi keaslian pengirim menggunakan **Kunci Publik ($e$)**:
          $$M' \\equiv S^e \\pmod n$$
        * Jika $M' == M$, maka dokumen **pasti berasal dari pemilik kunci privat asli** dan belum mengalami modifikasi sedikitpun!
        """)

        st.divider()

        cs_sign, cs_verify = st.columns([1, 1])
        curr_k = st.session_state["rsa_keys"]

        with cs_sign:
            st.markdown("##### 1. Pembuatan Tanda Tangan Digital")
            sign_input = st.text_input("Teks Pesan Dokumen:", value="SURAT KEPUTUSAN RESMI", key="rsa_doc_sign_in")
            btn_gen_sig = st.button("Tandatangani Dokumen (Sign with Private Key d)", key="rsa_btn_sign")

            if btn_gen_sig:
                sig_nums, sig_str = rsa_sign(sign_input, curr_k["d"], curr_k["n"])
                st.session_state["rsa_last_sig"] = sig_str
                st.session_state["rsa_last_doc"] = sign_input

                st.markdown("**Nilai Tanda Tangan Digital (Signature):**")
                st.markdown(f'<div class="cipher-box" style="font-size: 0.85rem;">{sig_str}</div>', unsafe_allow_html=True)
                st.success("Tanda tangan digital berhasil dibuat menggunakan Kunci Privat (d)!")

        with cs_verify:
            st.markdown("##### 2. Verifikasi Keabsahan Tanda Tangan")
            init_v_doc = st.session_state.get("rsa_last_doc", "SURAT KEPUTUSAN RESMI")
            init_v_sig = st.session_state.get("rsa_last_sig", "")

            v_doc_input = st.text_input("Dokumen yang Diterima:", value=init_v_doc, key="rsa_doc_v_in")
            v_sig_input = st.text_area("Tanda Tangan Digital yang Diterima:", value=init_v_sig, height=90, key="rsa_sig_v_in")
            btn_verify_sig = st.button("Verifikasi Tanda Tangan (Verify with Public Key e)", key="rsa_btn_verify")

            if btn_verify_sig:
                if not v_sig_input.strip():
                    st.warning("Masukkan tanda tangan digital terlebih dahulu.")
                else:
                    is_valid, v_steps = rsa_verify(v_doc_input, v_sig_input, curr_k["e"], curr_k["n"])
                    if is_valid:
                        st.markdown("""
                        <div class="datain-card" style="border-color: #2E7D32; background-color: #E8F5E9; padding: 1rem;">
                            <h4 style="color: #2E7D32; margin: 0 0 6px 0;">TANDA TANGAN OTENTIK & VALID</h4>
                            <p style="color: #1B5E20; margin: 0; font-size: 0.92rem;">
                                Dokumen terbukti 100% otentik dibuat oleh pemilik kunci privat asli dan isi pesan tidak pernah diubah!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="datain-card" style="border-color: #C62828; background-color: #FFEBEE; padding: 1rem;">
                            <h4 style="color: #C62828; margin: 0 0 6px 0;">PERINGATAN: TANDA TANGAN TIDAK VALID!</h4>
                            <p style="color: #B71C1C; margin: 0; font-size: 0.92rem;">
                                Isi dokumen telah dimanipulasi atau tanda tangan tidak dibuat menggunakan kunci privat yang sesuai!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    if v_steps:
                        with st.expander("Lihat Rincian Verifikasi per Karakter"):
                            st.dataframe(pd.DataFrame(v_steps), width="stretch", hide_index=True)

    # --------------------------------------------------------------------------
    # TAB 4: TEORI & LANDASAN MATEMATIS
    # --------------------------------------------------------------------------
    with tab_theory:
        st.markdown("##### Landasan Teori Algoritma RSA (Rivest-Shamir-Adleman)")
        st.markdown("""
        **RSA** diperkenalkan pada tahun 1977 oleh **Ron Rivest, Adi Shamir, dan Leonard Adleman** di MIT. 
        RSA merupakan algoritma kriptografi kunci asimetris modern yang paling banyak digunakan di dunia, 
        termasuk pada protokol TLS/SSL (HTTPS), SSH, dan sertifikat digital.
        """)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Fondasi Keamanan</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">Faktorisasi Bilangan Bulat (IFP)</h4>
                <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6;">
                    Keamanan RSA bertumpu pada <i>One-Way Trapdoor Function</i>:
                    Mengalikan dua bilangan prima raksasa (<i>p × q = n</i>) sangat mudah dihitung oleh komputer, 
                    namun memfaktorkan kembali <i>n</i> menjadi <i>p</i> dan <i>q</i> secara komputasi hampir mustahil 
                    jika ukuran prima mencapai 2048 atau 4096 bit.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Fungsi Totient Euler</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">Teorema Euler & Modulo</h4>
                <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6;">
                    Fungsi Totient Euler φ(n) menghitung banyaknya bilangan positif kurang dari <i>n</i> yang relatif prima terhadap <i>n</i>:
                    <br><code>φ(n) = (p - 1) × (q - 1)</code><br>
                    Berdasarkan Teorema Euler: <code>M^φ(n) ≡ 1 (mod n)</code>, sehingga berlaku <code>M^(e × d) ≡ M (mod n)</code>.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_t2:
            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Ringkasan Tahapan Matematis</span>
                <ol style="color: #1E3A5F; font-size: 0.9rem; line-height: 1.7; padding-left: 20px; margin: 8px 0;">
                    <li><b>Pilih Prima:</b> Tentukan dua bilangan prima rahasia <i>p</i> dan <i>q</i>.</li>
                    <li><b>Hitung Modulus:</b> <code>n = p × q</code>.</li>
                    <li><b>Hitung Totient:</b> <code>φ(n) = (p - 1)(q - 1)</code>.</li>
                    <li><b>Pilih Eksponen Publik e:</b> Memenuhi <code>1 < e < φ(n)</code> dan <code>gcd(e, φ(n)) = 1</code>.</li>
                    <li><b>Hitung Kunci Privat d:</b> <code>d ≡ e^(-1) (mod φ(n))</code> menggunakan Extended Euclidean.</li>
                    <li><b>Enkripsi:</b> <code>C ≡ M^e (mod n)</code>.</li>
                    <li><b>Dekripsi:</b> <code>M ≡ C^d (mod n)</code>.</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Analisis Keamanan & Serangan</span>
                <p style="color: #4A709C; font-size: 0.9rem; line-height: 1.6; margin: 8px 0;">
                    <b>1. Faktorisasi Fermat:</b> Berbahaya jika selisih <code>|p - q|</code> terlalu kecil.<br>
                    <b>2. Wiener's Attack:</b> Dapat membongkar kunci jika nilai <code>d < 1/3 n^(1/4)</code>.<br>
                    <b>3. Standar Industri:</b> RSA di dunia nyata wajib menggunakan padding aman seperti <b>OAEP</b> 
                    (Optimal Asymmetric Encryption Padding) untuk mencegah serangan chosen-ciphertext.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# STANDALONE RUNNER: ORANG 4
# ==============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="RSA Asymmetric Cipher - Orang 4",
        page_icon="https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_UPN_Veteran_Yogyakarta.png",
        layout="wide"
    )
    load_global_css()
    render_rsa_page()
