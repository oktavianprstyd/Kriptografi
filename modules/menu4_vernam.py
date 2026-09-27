import secrets
import string
import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css, render_mode_selector
except ImportError:
    from ui_helper import render_header, load_global_css, render_mode_selector


# ==============================================================================
# BAGIAN 1: LOGIKA & MATEMATIKA VERNAM STREAM CIPHER
# Penanggung Jawab: Oktavian Prasetya Adi (123240135)
# ==============================================================================

def generate_otp_key(length: int) -> str:
    """
    Membangkitkan aliran kunci acak murni (One-Time Pad / Truly Random).
    Panjang kunci persis sama dengan panjang teks plainteks.
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(max(1, length)))


def vernam_encrypt(plaintext: str, key: str, mode: str = "repeat"):
    """
    Enkripsi Vernam Stream Cipher berbasis bitwise XOR:
    c_i = p_i ⊕ k_i
    
    Parameter:
      - plaintext: teks asli yang akan disandikan
      - key: kunci teks keystream
      - mode: 'repeat' (kunci diulang periodik) atau 'otp' (kunci acak sepanjang teks)
    
    Mengembalikan: (cipher_bytes, hex_string, bin_string, steps)
    """
    p_bytes = plaintext.encode("utf-8")
    k_bytes = key.encode("utf-8")

    if not k_bytes:
        raise ValueError("Kunci keystream tidak boleh kosong!")

    # Bentuk keystream penuh sepanjang data
    if mode == "repeat":
        keystream = bytearray(k_bytes[i % len(k_bytes)] for i in range(len(p_bytes)))
    else:
        # One-Time Pad mode: potong atau pad
        if len(k_bytes) < len(p_bytes):
            raise ValueError(
                f"Mode One-Time Pad (OTP) mewajibkan panjang kunci ({len(k_bytes)} byte) "
                f"minimal sama dengan panjang plainteks ({len(p_bytes)} byte)!"
            )
        keystream = k_bytes[:len(p_bytes)]

    c_bytes = bytearray()
    steps = []

    for i, (p_byte, k_byte) in enumerate(zip(p_bytes, keystream)):
        c_byte = p_byte ^ k_byte
        c_bytes.append(c_byte)

        p_bin = format(p_byte, "08b")
        k_bin = format(k_byte, "08b")
        c_bin = format(c_byte, "08b")

        steps.append({
            "No": i + 1,
            "Karakter (P)": repr(chr(p_byte))[1:-1] if 32 <= p_byte <= 126 else f"\\x{p_byte:02x}",
            "ASCII (P)": p_byte,
            "Biner Plain (P)": p_bin,
            "Karakter (K)": repr(chr(k_byte))[1:-1] if 32 <= k_byte <= 126 else f"\\x{k_byte:02x}",
            "Biner Kunci (K)": k_bin,
            "Operasi XOR (P ⊕ K)": f"{p_bin} ⊕ {k_bin}",
            "Biner Cipher (C)": c_bin,
            "Hex": f"0x{c_byte:02X}"
        })

    hex_string = " ".join(f"{b:02X}" for b in c_bytes)
    bin_string = " ".join(format(b, "08b") for b in c_bytes)

    return c_bytes, hex_string, bin_string, steps


def vernam_decrypt(cipher_hex_input: str, key: str, mode: str = "repeat"):
    """
    Dekripsi Vernam Stream Cipher:
    Karena sifat involutori XOR: (P ⊕ K) ⊕ K = P ⊕ (K ⊕ K) = P ⊕ 0 = P
    Maka dekripsi persis sama dengan enkripsi:
    p_i = c_i ⊕ k_i
    
    Mengembalikan: (recovered_text, steps)
    """
    cleaned_hex = (
        cipher_hex_input.replace("0x", "")
        .replace(" ", "")
        .replace(":", "")
        .replace("-", "")
        .replace("\n", "")
        .strip()
    )

    if not cleaned_hex:
        return "", []

    try:
        c_bytes = bytes.fromhex(cleaned_hex)
    except ValueError as err:
        raise ValueError(f"Format cipherteks heksadesimal tidak valid: {err}")

    k_bytes = key.encode("utf-8")
    if not k_bytes:
        raise ValueError("Kunci keystream dekripsi tidak boleh kosong!")

    if mode == "repeat":
        keystream = bytearray(k_bytes[i % len(k_bytes)] for i in range(len(c_bytes)))
    else:
        if len(k_bytes) < len(c_bytes):
            raise ValueError(f"Panjang kunci ({len(k_bytes)}) lebih pendek dari cipherteks ({len(c_bytes)}) pada mode OTP!")
        keystream = k_bytes[:len(c_bytes)]

    p_bytes = bytearray()
    steps = []

    for i, (c_byte, k_byte) in enumerate(zip(c_bytes, keystream)):
        p_byte = c_byte ^ k_byte
        p_bytes.append(p_byte)

        c_bin = format(c_byte, "08b")
        k_bin = format(k_byte, "08b")
        p_bin = format(p_byte, "08b")

        steps.append({
            "No": i + 1,
            "Cipher (Hex)": f"0x{c_byte:02X}",
            "Biner Cipher (C)": c_bin,
            "Biner Kunci (K)": k_bin,
            "Operasi XOR (C ⊕ K)": f"{c_bin} ⊕ {k_bin}",
            "Biner Plain (P)": p_bin,
            "ASCII (P)": p_byte,
            "Karakter Pulih": repr(chr(p_byte))[1:-1] if 32 <= p_byte <= 126 else f"\\x{p_byte:02x}"
        })

    recovered_text = p_bytes.decode("utf-8", errors="replace")
    return recovered_text, steps


def vernam_bit_simulation(plain_bits: str, key_bits: str):
    """
    Simulasi Aliran Bit Murni dengan operasi bitwise XOR:
    Plainteks : 1100101
    Keystream : 1000110
    Cipherteks: 0100011
    """
    clean_p = "".join(b for b in plain_bits if b in ("0", "1"))
    clean_k = "".join(b for b in key_bits if b in ("0", "1"))

    if not clean_p or not clean_k:
        return "", []

    # Ulangi kunci bit jika lebih pendek
    full_key_bits = (clean_k * ((len(clean_p) // len(clean_k)) + 1))[:len(clean_p)]

    cipher_bits = []
    bit_steps = []

    for i, (pb, kb) in enumerate(zip(clean_p, full_key_bits)):
        cb = "1" if pb != kb else "0"
        cipher_bits.append(cb)
        bit_steps.append({
            "Posisi Bit": i + 1,
            "Bit Plainteks (p_i)": pb,
            "Bit Keystream (k_i)": kb,
            "Operasi XOR": f"{pb} ⊕ {kb}",
            "Bit Cipherteks (c_i)": cb
        })

    return "".join(cipher_bits), bit_steps


# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - WARM CREAM & DEEP NAVY)
# ==============================================================================

def render_vernam_page():
    render_header(
        title="Menu 3: Vernam Stream Cipher",
        subtitle="Kriptografi Modern Cipher Aliran (Stream Cipher) Berbasis Bitwise XOR (⊕) dan One-Time Pad",
        pic_name="Penanggung Jawab: Oktavian Prasetya Adi (123240135)",
        category="Kriptografi Modern - Cipher Aliran • Kelompok 3"
    )

    # Inisialisasi default session state
    if "vernam_mode" not in st.session_state:
        st.session_state["vernam_mode"] = "Enkripsi Pesan"
    if "vernam_last_hex" not in st.session_state:
        st.session_state["vernam_last_hex"] = ""
    if "vernam_last_key" not in st.session_state:
        st.session_state["vernam_last_key"] = "KUNCI"
    if "vernam_steps" not in st.session_state:
        st.session_state["vernam_steps"] = []
    if "vernam_dec_steps" not in st.session_state:
        st.session_state["vernam_dec_steps"] = []

    tab_main, tab_trace, tab_bits, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pelacakan Bitwise XOR Step-by-Step",
        "Simulasi Aliran Bit Murni",
        "Teori & 3 Kasus Keystream"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: OPERASI ENKRIPSI & DEKRIPSI
    # --------------------------------------------------------------------------
    with tab_main:
        mode_op = render_mode_selector(session_state_key="vernam_mode", key_prefix="vernam")

        # MODE ENKRIPSI
        if mode_op == "Enkripsi Pesan":
            c_inp, c_out = st.columns([1, 1])

            with c_inp:
                st.markdown("##### 1. Masukan Plainteks & Konfigurasi Keystream")
                p_text = st.text_area(
                    "Masukkan teks plainteks:",
                    value="BELAJAR",
                    height=100,
                    key="vernam_p_in"
                )

                keystream_mode = st.selectbox(
                    "Tipe Pembangkit Keystream:",
                    [
                        "Keystream Periodik (Kunci Teks Berulang)",
                        "Keystream Acak Sempurna / One-Time Pad (OTP)"
                    ],
                    key="vernam_ks_type"
                )

                is_otp = "One-Time Pad" in keystream_mode

                if is_otp:
                    st.caption("Mode OTP: Panjang kunci keystream wajib dibuat minimal sama panjang dengan plainteks.")
                    req_len = max(len(p_text.encode("utf-8")), 1)

                    # Inisialisasi default OTP jika belum ada di state
                    if "vernam_key_otp_in" not in st.session_state or not st.session_state["vernam_key_otp_in"]:
                        initial_otp = generate_otp_key(req_len)
                        st.session_state["vernam_key_otp_in"] = initial_otp
                        st.session_state["vernam_last_key"] = initial_otp

                    col_gen_k, col_k_field = st.columns([1.2, 2])
                    with col_gen_k:
                        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("Generate Kunci OTP Acak", key="vernam_gen_otp_btn", use_container_width=True):
                            new_otp = generate_otp_key(req_len)
                            st.session_state["vernam_key_otp_in"] = new_otp
                            st.session_state["vernam_last_key"] = new_otp
                            st.rerun()

                    with col_k_field:
                        key_val = st.text_input(
                            "Kunci Keystream OTP:",
                            key="vernam_key_otp_in"
                        )
                        st.session_state["vernam_last_key"] = key_val

                    # Info validasi panjang byte
                    p_bytes_len = len(p_text.encode("utf-8"))
                    k_bytes_len = len(key_val.encode("utf-8"))
                    if k_bytes_len < p_bytes_len:
                        st.warning(
                            f"Panjang kunci OTP ({k_bytes_len} byte) lebih pendek dari plainteks ({p_bytes_len} byte)! "
                            f"Silakan klik tombol 'Generate Kunci OTP Acak'."
                        )
                    else:
                        st.caption(f"Status Kunci: Valid untuk OTP ({k_bytes_len} byte >= {p_bytes_len} byte plainteks).")
                else:
                    if "vernam_key_rep_in" not in st.session_state:
                        st.session_state["vernam_key_rep_in"] = "INFORMATIKA"
                    key_val = st.text_input(
                        "Kunci Teks Keystream (diulang periodik):",
                        key="vernam_key_rep_in"
                    )
                    st.session_state["vernam_last_key"] = key_val

                btn_enc = st.button("Jalankan Enkripsi Vernam (XOR)", key="vernam_btn_enc", type="primary", use_container_width=True)

            with c_out:
                st.markdown("##### 2. Hasil Cipherteks Aliran")
                if btn_enc:
                    try:
                        k_mode_param = "otp" if is_otp else "repeat"
                        c_bytes, hex_res, bin_res, steps_res = vernam_encrypt(p_text, key_val, mode=k_mode_param)
                        st.session_state["vernam_last_hex"] = hex_res
                        st.session_state["vernam_last_key"] = key_val
                        st.session_state["vernam_steps"] = steps_res
                        st.session_state["vernam_hex_dec_in"] = hex_res
                        st.session_state["vernam_dec_key_in"] = key_val

                        st.markdown("**Cipherteks Format Heksadesimal (Standar Industri):**")
                        st.markdown(f'<div class="cipher-box">{hex_res}</div>', unsafe_allow_html=True)

                        st.markdown("**Aliran Bit Biner Cipherteks:**")
                        st.markdown(f'<div class="cipher-box" style="font-size: 0.82rem;">{bin_res}</div>', unsafe_allow_html=True)

                        st.success(f"Enkripsi berhasil diproses! ({len(c_bytes)} byte data dialirkan)")
                    except ValueError as ex:
                        st.error(f"Kesalahan enkripsi: {ex}")
                else:
                    if st.session_state.get("vernam_last_hex"):
                        st.markdown("**Cipherteks Sebelumnya (Hex):**")
                        st.markdown(f'<div class="cipher-box">{st.session_state["vernam_last_hex"]}</div>', unsafe_allow_html=True)
                    else:
                        st.info("Tekan tombol 'Jalankan Enkripsi Vernam (XOR)' untuk memproses data.")

        # MODE DEKRIPSI
        else:
            c_dec_inp, c_dec_out = st.columns([1, 1])

            with c_dec_inp:
                st.markdown("##### 1. Masukan Cipherteks & Kunci Keystream")
                if st.session_state.get("vernam_last_hex") and st.session_state.get("vernam_last_key"):
                    if st.button("Gunakan Cipherteks & Kunci dari Sesi Enkripsi Terakhir", key="vernam_btn_sync_enc", use_container_width=True):
                        st.session_state["vernam_hex_dec_in"] = st.session_state["vernam_last_hex"]
                        st.session_state["vernam_dec_key_in"] = st.session_state["vernam_last_key"]
                        st.rerun()

                if "vernam_hex_dec_in" not in st.session_state:
                    st.session_state["vernam_hex_dec_in"] = st.session_state.get(
                        "vernam_last_hex",
                        "09 0B 0A 0E 05 0E 1B 65 02 1C 07 1F 1A 00 1D 0E 09 06 65 04 01 0B 0A 1D 07 65 1E 1F 01"
                    )
                dec_hex_input = st.text_area(
                    "Masukkan cipherteks format Heksadesimal (Hex):",
                    key="vernam_hex_dec_in",
                    height=110
                )

                if "vernam_dec_key_in" not in st.session_state:
                    st.session_state["vernam_dec_key_in"] = st.session_state.get("vernam_last_key", "INFORMATIKA")

                dec_key = st.text_input(
                    "Kunci Keystream Dekripsi:",
                    key="vernam_dec_key_in"
                )

                btn_dec = st.button("Jalankan Dekripsi Vernam", key="vernam_btn_dec", type="primary", use_container_width=True)

            with c_dec_out:
                st.markdown("##### 2. Hasil Rekonstruksi Plainteks")
                if btn_dec:
                    try:
                        recovered_msg, dec_steps = vernam_decrypt(dec_hex_input, dec_key, mode="repeat")
                        st.session_state["vernam_dec_steps"] = dec_steps

                        st.markdown("**Plainteks Rekonstruksi:**")
                        st.markdown(f'<div class="cipher-box" style="font-weight: 600; font-size: 1.05rem;">{recovered_msg}</div>', unsafe_allow_html=True)

                        st.markdown("""
                        <div class="datain-card" style="margin-top: 1rem; padding: 0.85rem;">
                            <span class="badge-category">Sifat Involutori XOR Terpenuhi</span>
                            <p style="margin: 6px 0 0 0; color: #1E3A5F; font-size: 0.9rem;">
                                Karena <code>(P ⊕ K) ⊕ K = P</code>, operasi XOR kedua dengan kunci yang sama 
                                langsung memulihkan data asli secara sempurna.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.success("Dekripsi berhasil dipulihkan secara 100% presisi!")
                    except Exception as err:
                        st.error(f"Gagal memproses dekripsi: {err}")
                else:
                    st.info("Tekan tombol 'Jalankan Dekripsi Vernam' untuk memulihkan teks asli.")

    # --------------------------------------------------------------------------
    # TAB 2: PELACAKAN BITWISE XOR STEP-BY-STEP
    # --------------------------------------------------------------------------
    with tab_trace:
        st.markdown("##### Tabel Pelacakan Bitwise XOR per Karakter (p_i ⊕ k_i = c_i)")
        st.markdown(
            "Tabel di bawah memperlihatkan proses bit-per-bit konversi kode ASCII setiap karakter ke representasi biner 8-bit, "
            "kemudian dilakukan operasi logika **XOR bitwise** dengan bit kunci keystream:"
        )

        if st.session_state.get("vernam_steps"):
            df_trace = pd.DataFrame(st.session_state["vernam_steps"])
            st.dataframe(df_trace, width="stretch", hide_index=True)
        else:
            st.info("Lakukan proses enkripsi di Tab 1 untuk memuat rincian tabel pelacakan bitwise XOR.")

    # --------------------------------------------------------------------------
    # TAB 3: SIMULASI ALIRAN BIT MURNI
    # --------------------------------------------------------------------------
    with tab_bits:
        st.markdown("##### Simulasi Aliran Bit Biner Murni")
        st.markdown("""
        Demonstrasi manipulasi bit biner langsung tanpa melalui teks ASCII:
        * Plainteks: `1100101`
        * Keystream: `1000110`
        * Cipherteks: `0100011`
        """)

        cb1, cb2 = st.columns(2)
        with cb1:
            bit_p_in = st.text_input("Deret Bit Plainteks (0 dan 1):", value="1100101", key="v_bit_p")
            bit_k_in = st.text_input("Deret Bit Keystream (0 dan 1):", value="1000110", key="v_bit_k")
            btn_bit_sim = st.button("Hitung Operasi Bit XOR", key="v_bit_sim_btn")

        with cb2:
            st.markdown("##### Hasil Aliran Bit Sandi")
            c_bits_res, b_steps = vernam_bit_simulation(bit_p_in, bit_k_in)
            if c_bits_res:
                st.markdown(f'<div class="cipher-box" style="font-size: 1.2rem; font-weight: 700; letter-spacing: 2px;">{c_bits_res}</div>', unsafe_allow_html=True)
                st.caption(f"Panjang bit: {len(c_bits_res)} bit")

        if b_steps:
            st.markdown("##### Rincian Operasi Bit per Bit")
            st.dataframe(pd.DataFrame(b_steps), width="stretch", hide_index=True)

        st.markdown("---")
        st.markdown("##### Tabel Kebenaran Logika Operasi XOR (Exclusive-OR)")
        xor_truth = pd.DataFrame([
            {"Bit Plainteks (p)": 0, "Bit Keystream (k)": 0, "Formula": "0 ⊕ 0", "Bit Cipherteks (c)": 0, "Penjelasan": "Sama -> 0"},
            {"Bit Plainteks (p)": 0, "Bit Keystream (k)": 1, "Formula": "0 ⊕ 1", "Bit Cipherteks (c)": 1, "Penjelasan": "Beda -> 1"},
            {"Bit Plainteks (p)": 1, "Bit Keystream (k)": 0, "Formula": "1 ⊕ 0", "Bit Cipherteks (c)": 1, "Penjelasan": "Beda -> 1"},
            {"Bit Plainteks (p)": 1, "Bit Keystream (k)": 1, "Formula": "1 ⊕ 1", "Bit Cipherteks (c)": 0, "Penjelasan": "Sama -> 0"},
        ])
        st.dataframe(xor_truth, width="stretch", hide_index=True)

    # ==============================================================================
    # TAB 4: TEORI & 3 KASUS KEYSTREAM
    # ==============================================================================
    with tab_theory:
        st.markdown("##### Teori & Karakteristik Vernam Cipher")
        
        # Tambahkan huruf 'r' di depan tanda kutip tiga untuk membuat raw string
        st.markdown(r"""
        **Vernam Cipher** adalah algoritma kriptografi simetris yang mengenkripsi plaintext dengan melakukan operasi XOR terhadap key. Proses dekripsi menggunakan operasi XOR yang sama.

        ---

        ##### Karakteristik Utama:
        1. **Symmetric-Key Cipher**: Menggunakan kunci yang sama untuk proses enkripsi dan dekripsi.
        2. **Operasi Bitwise XOR**: Pengacakan dilakukan pada tingkat bit atau byte menggunakan gerbang logika $\oplus$ (Modulo-2).
        3. **Konsep One-Time Pad (OTP)**: Jika kunci memiliki panjang yang sama dengan plaintext dan benar-benar acak, konsepnya menjadi One-Time Pad dengan tingkat keamanan sempurna (*unbreakable*).
        4. **Efisiensi Tinggi**: Proses komputasi sangat sederhana, cepat, dan bersifat *involutori* (algoritma enkripsi dan dekripsi identik).

        ---

        ##### Formula Matematis & Sifat Involutori:
        * **Enkripsi**:
          $$C = P \oplus K$$
        * **Dekripsi**:
          $$P = C \oplus K$$
        * **Pembuktian Pembalikan (Involutori XOR)**:
          $$(P \oplus K) \oplus K = P \oplus (K \oplus K) = P \oplus 0 = P$$

        ---

        ##### Contoh Perhitungan Biner:
        * **Plainteks**: `10110010`
        * **Key**: `01101100`
        * **Enkripsi**:
          $$\begin{array}{rl}           & 10110010 \\           \oplus & 01101100 \\           \hline           & \mathbf{11011110}           \end{array}$$
        * **Dekripsi**:
          $$\begin{array}{rl}           & 11011110 \\           \oplus & 01101100 \\           \hline           & \mathbf{10110010}           \end{array}$$

        ---

        ##### Tinjauan 3 Kasus Pembangkit Keystream:
        """)

        c_k1, c_k2, c_k3 = st.columns(3)
        with c_k1:
            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Kasus 1</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">Keystream Seluruhnya 0</h4>
                <p style="color: #4A709C; font-size: 0.88rem; line-height: 1.5;">
                    Jika pembangkit mengeluarkan aliran bit kunci yang seluruhnya 0, maka:<br>
                    <code>c_i = p_i ⊕ 0 = p_i</code><br>
                    <b>Status Keamanan:</b> Tak-berarti (Cipherteks persis sama dengan Plainteks).
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_k2:
            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Kasus 2</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">Keystream Periodik Berulang</h4>
                <p style="color: #4A709C; font-size: 0.88rem; line-height: 1.5;">
                    Jika keystream berulang secara siklis mengikuti panjang kata kunci (seperti Vigenère biner):<br>
                    <code>c_i = p_i ⊕ k_(i mod m)</code><br>
                    <b>Status Keamanan:</b> Rendah/Mudah dipecahkan dengan analisis frekuensi Kasiski.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_k3:
            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Kasus 3</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">One-Time Pad (Truly Random)</h4>
                <p style="color: #4A709C; font-size: 0.88rem; line-height: 1.5;">
                    Jika keystream benar-benar acak murni dan panjangnya sama dengan panjang plainteks:<br>
                    <b>Status Keamanan:</b> Sempurna (<i>Perfect Secrecy / Unbreakable Cipher</i> Claude Shannon).
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="datain-card" style="margin-top: 1rem;">
            <h4 style="color: #1E3A5F; margin-top: 0;">Kesimpulan Tingkat Keamanan</h4>
            <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6; margin-bottom: 0;">
                Tingkat keamanan cipher aliran terletak di antara algoritma XOR sederhana (Kasus 2) dengan One-Time Pad (Kasus 3). 
                Semakin acak keluaran yang dihasilkan oleh <i>keystream generator</i>, semakin sulit bagi kriptanalis untuk memecahkan cipherteks.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# STANDALONE RUNNER
# ==============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="Vernam Stream Cipher - Oktavian Prasetya Adi",
        page_icon="https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_UPN_Veteran_Yogyakarta.png",
        layout="wide"
    )
    load_global_css()
    render_vernam_page()
