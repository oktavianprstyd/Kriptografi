import secrets
import string
import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css


# ==============================================================================
# BAGIAN 1: LOGIKA & MATEMATIKA VERNAM STREAM CIPHER
# Penanggung Jawab: Orang 4 (Oktavian Prasetya Adi)
# Mengacu pada: Materi 5 Kriptografi Modern (Slide 15 - 23)
# ==============================================================================

def generate_otp_key(length: int) -> str:
    """
    Membangkitkan aliran kunci acak murni (One-Time Pad / Kasus 3 Slide 22).
    Panjang kunci persis sama dengan panjang teks plainteks.
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    return "".join(secrets.choice(alphabet) for _ in range(max(1, length)))


def vernam_encrypt(plaintext: str, key: str, mode: str = "repeat"):
    """
    Enkripsi Vernam Stream Cipher berbasis bitwise XOR:
    c_i = p_i ⊕ k_i
    (Slide 18 & 19 Materi 5)
    
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
    (Slide 18 Materi 5)
    
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
    Simulasi Aliran Bit Murni persis seperti contoh Slide 19 Materi 5:
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
        pic_name="Penanggung Jawab: Orang 4 (Oktavian Prasetya Adi)",
        category="Kriptografi Modern - Cipher Aliran"
    )

    # Inisialisasi default session state
    if "vernam_last_hex" not in st.session_state:
        st.session_state["vernam_last_hex"] = ""
    if "vernam_last_key" not in st.session_state:
        st.session_state["vernam_last_key"] = "RAHASIA"
    if "vernam_steps" not in st.session_state:
        st.session_state["vernam_steps"] = []
    if "vernam_dec_steps" not in st.session_state:
        st.session_state["vernam_dec_steps"] = []

    tab_main, tab_trace, tab_bits, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Pelacakan Bitwise XOR Step-by-Step",
        "Simulasi Aliran Bit Murni (Slide 19)",
        "Teori & 3 Kasus Keystream"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: OPERASI ENKRIPSI & DEKRIPSI
    # --------------------------------------------------------------------------
    with tab_main:
        mode_op = st.radio(
            "Pilih Mode Operasi",
            ["Enkripsi Pesan", "Dekripsi Pesan"],
            horizontal=True,
            key="vernam_mode_choice"
        )
        st.divider()

        # MODE ENKRIPSI
        if mode_op == "Enkripsi Pesan":
            c_inp, c_out = st.columns([1, 1])

            with c_inp:
                st.markdown("##### 1. Masukan Plainteks & Konfigurasi Keystream")
                p_text = st.text_area(
                    "Masukkan teks plainteks:",
                    value="BELAJAR KRIPTOGRAFI MODERN UPN",
                    height=100,
                    key="vernam_p_in"
                )

                keystream_mode = st.selectbox(
                    "Tipe Pembangkit Keystream (Slide 20-22):",
                    [
                        "Keystream Periodik (Kunci Teks Berulang / Kasus 2 Slide 21)",
                        "Keystream Acak Sempurna / One-Time Pad (OTP / Kasus 3 Slide 22)"
                    ],
                    key="vernam_ks_type"
                )

                is_otp = "One-Time Pad" in keystream_mode

                if is_otp:
                    st.caption("Mode OTP: Panjang kunci keystream wajib dibuat minimal sama panjang dengan plainteks.")
                    col_gen_k, col_k_field = st.columns([1, 2])
                    with col_gen_k:
                        if st.button("Generate Kunci OTP Acak", key="vernam_gen_otp_btn"):
                            st.session_state["vernam_last_key"] = generate_otp_key(len(p_text.encode("utf-8")))
                    with col_k_field:
                        key_val = st.text_input(
                            "Kunci Keystream OTP:",
                            value=st.session_state.get("vernam_last_key", generate_otp_key(len(p_text))),
                            key="vernam_key_otp_in"
                        )
                else:
                    key_val = st.text_input(
                        "Kunci Teks Keystream (diulang periodik):",
                        value=st.session_state.get("vernam_last_key", "INFORMATIKA"),
                        key="vernam_key_rep_in"
                    )

                btn_enc = st.button("Jalankan Enkripsi Vernam (XOR)", key="vernam_btn_enc")

            with c_out:
                st.markdown("##### 2. Hasil Cipherteks Aliran")
                if btn_enc:
                    try:
                        k_mode_param = "otp" if is_otp else "repeat"
                        c_bytes, hex_res, bin_res, steps_res = vernam_encrypt(p_text, key_val, mode=k_mode_param)
                        st.session_state["vernam_last_hex"] = hex_res
                        st.session_state["vernam_last_key"] = key_val
                        st.session_state["vernam_steps"] = steps_res

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
                init_hex = st.session_state.get("vernam_last_hex", "09 0B 0A 0E 05 0E 1B 65 02 1C 07 1F 1A 00 1D 0E 09 06 65 04 01 0B 0A 1D 07 65 1E 1F 01")
                dec_hex_input = st.text_area(
                    "Masukkan cipherteks format Heksadesimal (Hex):",
                    value=init_hex,
                    height=110,
                    key="vernam_hex_dec_in"
                )

                dec_key = st.text_input(
                    "Kunci Keystream Dekripsi:",
                    value=st.session_state.get("vernam_last_key", "INFORMATIKA"),
                    key="vernam_dec_key_in"
                )

                btn_dec = st.button("Jalankan Dekripsi Vernam", key="vernam_btn_dec")

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
    # TAB 3: SIMULASI ALIRAN BIT MURNI (SLIDE 19 MATERI 5)
    # --------------------------------------------------------------------------
    with tab_bits:
        st.markdown("##### Simulasi Aliran Bit Biner Murni (Persis Contoh Slide 19 Materi 5)")
        st.markdown("""
        Pada Slide 19 perkuliahan, dicontohkan manipulasi bit biner langsung tanpa melalui teks ASCII:
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

    # --------------------------------------------------------------------------
    # TAB 4: TEORI & 3 KASUS KEYSTREAM
    # --------------------------------------------------------------------------
    with tab_theory:
        st.markdown("##### Teori Vernam Cipher & 3 Kasus Keystream (Materi 5 Slide 15–23)")
        st.markdown("""
        **Vernam Cipher** diperkenalkan oleh **Gilbert S. Vernam** pada tahun 1917 untuk teleprinter telegraf. 
        Vernam mengadopsi prinsip *One-Time Pad* (OTP) di mana karakter dikonversi menjadi representasi bit (0 atau 1) 
        dan digabungkan menggunakan gerbang logika modulo-2 atau **Exclusive-OR (XOR)**.
        """)

        st.markdown("##### Tinjauan 3 Kasus Pembangkit Keystream (Slide 20–22):")

        c_k1, c_k2, c_k3 = st.columns(3)
        with c_k1:
            st.markdown("""
            <div class="datain-card">
                <span class="badge-category">Kasus 1 (Slide 20)</span>
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
                <span class="badge-category">Kasus 2 (Slide 21)</span>
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
                <span class="badge-category">Kasus 3 (Slide 22)</span>
                <h4 style="margin: 8px 0; color: #1E3A5F;">One-Time Pad (Truly Random)</h4>
                <p style="color: #4A709C; font-size: 0.88rem; line-height: 1.5;">
                    Jika keystream benar-benar acak murni dan panjangnya sama dengan panjang plainteks:<br>
                    <b>Status Keamanan:</b> Sempurna (<i>Perfect Secrecy / Unbreakable Cipher</i> Claude Shannon).
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="datain-card" style="margin-top: 1rem;">
            <h4 style="color: #1E3A5F; margin-top: 0;">Kesimpulan Tingkat Keamanan (Slide 23)</h4>
            <p style="color: #4A709C; font-size: 0.92rem; line-height: 1.6; margin-bottom: 0;">
                Tingkat keamanan cipher aliran terletak di antara algoritma XOR sederhana (Kasus 2) dengan One-Time Pad (Kasus 3). 
                Semakin acak keluaran yang dihasilkan oleh <i>keystream generator</i>, semakin sulit bagi kriptanalis untuk memecahkan cipherteks.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# STANDALONE RUNNER: ORANG 4
# ==============================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="Vernam Stream Cipher - Orang 4",
        page_icon="https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_UPN_Veteran_Yogyakarta.png",
        layout="wide"
    )
    load_global_css()
    render_vernam_page()
