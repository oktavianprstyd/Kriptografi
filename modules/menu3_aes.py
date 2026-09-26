import streamlit as st
import pandas as pd
import base64
import numpy as np

try:
    from .ui_helper import render_header, load_global_css, render_mode_selector
except ImportError:
    from ui_helper import render_header, load_global_css, render_mode_selector

# ==============================================================================
# BAGIAN 1: MATEMATIKA MURNI AES-128
# ==============================================================================

# Tabel S-Box untuk Vektorisasi Vektor / Matriks
SBOX = np.array([
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
], dtype=np.uint8)

INV_SBOX = np.array([
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
], dtype=np.uint8)

RCON = np.array([0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36], dtype=np.uint8)

# Matriks Transformasi FIPS 197 untuk MixColumns
MIX_COL_MATRIX = np.array([
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
], dtype=np.uint8)

INV_MIX_COL_MATRIX = np.array([
    [0x0e, 0x0b, 0x0d, 0x09],
    [0x09, 0x0e, 0x0b, 0x0d],
    [0x0d, 0x09, 0x0e, 0x0b],
    [0x0b, 0x0d, 0x09, 0x0e]
], dtype=np.uint8)

# Operasi Matematis Galois Field GF(2^8)
def gf_mult(a, b):
    a, b = int(a), int(b)
    p = 0
    for _ in range(8):
        if b & 1: p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set: a ^= 0x1B
        b >>= 1
    return p % 256

# Fungsi Konversi Cepat (Buffer Array)
def text_to_matrix(text_bytes):
    # Mengubah stream byte menjadi Matriks NumPy 4x4
    return np.frombuffer(text_bytes, dtype=np.uint8).reshape(4, 4).copy()

def matrix_to_text(matrix):
    # Matriks kembali ke stream byte
    return matrix.tobytes()

# ======================= TAHAPAN ROUND AES =======================

def sub_bytes(state, inv=False):
    # Vektorisasi O(1): NumPy memetakan seluruh matriks sekaligus ke dalam tabel SBOX
    box = INV_SBOX if inv else SBOX
    return box[state]

def shift_rows(state, inv=False):
    # Optimasi Shift menggunakan operasi perputaran array np.roll
    for i in range(1, 4):
        shift = -i if not inv else i
        state[i, :] = np.roll(state[i, :], shift)
    return state

def mix_columns(state, inv=False):
    # Matriks Dot Product di Galois Field
    # State = Matriks FIPS * Matriks State
    M = INV_MIX_COL_MATRIX if inv else MIX_COL_MATRIX
    new_state = np.empty_like(state)
    
    for i in range(4): # Baris Matriks M
        for j in range(4): # Kolom Matriks State
            val = 0
            for k in range(4):
                val ^= gf_mult(M[i, k], state[k, j])
            new_state[i, j] = val
    return new_state

def add_round_key(state, key_matrix):
    # Operasi matriks bitwise XOR O(1) di NumPy
    return state ^ key_matrix

# ======================= EKSPANSI KUNCI =======================

def expand_key(key):
    key_bytes = list(key)
    key_words = [key_bytes[i:i+4] for i in range(0, 16, 4)]
    
    for i in range(4, 44):
        temp = key_words[i-1][:]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1] # RotWord
            temp = [SBOX[b] for b in temp] # SubWord
            temp[0] ^= RCON[i//4] # Rcon XOR
            
        word = [key_words[i-4][j] ^ temp[j] for j in range(4)]
        key_words.append(word)
    
    # Kelompokkan menjadi List of NumPy Matrices (4x4)
    round_keys = []
    for r in range(11):
        rmatrix = np.array([key_words[r*4 + c] for c in range(4)], dtype=np.uint8)
        round_keys.append(rmatrix)
    return round_keys

# ======================= FUNGSI UTAMA =======================

def encrypt_block(pt_bytes, round_keys):
    state = text_to_matrix(pt_bytes)
    state = add_round_key(state, round_keys[0])
    for round_num in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round_num])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])
    return matrix_to_text(state), state

def decrypt_block(ct_bytes, round_keys):
    state = text_to_matrix(ct_bytes)
    state = add_round_key(state, round_keys[10])
    for round_num in range(9, 0, -1):
        state = shift_rows(state, inv=True)
        state = sub_bytes(state, inv=True)
        state = add_round_key(state, round_keys[round_num])
        state = mix_columns(state, inv=True)
    state = shift_rows(state, inv=True)
    state = sub_bytes(state, inv=True)
    state = add_round_key(state, round_keys[0])
    return matrix_to_text(state)

# Padding PKCS#7
def pad(text_bytes):
    padding_len = 16 - (len(text_bytes) % 16)
    return text_bytes + bytes([padding_len] * padding_len)

def unpad(text_bytes):
    padding_len = text_bytes[-1]
    return text_bytes[:-padding_len]

def format_state(state):
    return [[f"{b:02X}" for b in row] for row in state]

def aes_encrypt(plaintext: str, key: str, mode: str = "CBC"):
    pt_bytes = pad(plaintext.encode('utf-8'))
    k_bytes = pad(key.encode('utf-8'))[:16] # Paksa 128-bit
    round_keys = expand_key(k_bytes)
    
    iv = bytes([0] * 16)
    ct_bytes = b""
    prev_block = iv
    demo_state = None
    
    for i in range(0, len(pt_bytes), 16):
        block = pt_bytes[i:i+16]
        
        # CBC Mode - Operasi Array Cepat menggunakan bitwise NumPy
        if mode == "CBC":
            arr_block = np.frombuffer(block, dtype=np.uint8)
            arr_prev = np.frombuffer(prev_block, dtype=np.uint8)
            block = (arr_block ^ arr_prev).tobytes()
        
        enc_block, state = encrypt_block(block, round_keys)
        ct_bytes += enc_block
        prev_block = enc_block
        if i == 0: demo_state = format_state(state)
            
    hex_str = ct_bytes.hex().upper()
    b64_str = base64.b64encode(ct_bytes).decode('utf-8')
    
    return {
        "hex_str": hex_str,
        "b64_str": b64_str,
        "demo_trace": {"State Matrix 4x4 (Blok Pertama)": demo_state}
    }

def aes_decrypt(cipher_hex: str, key: str, mode: str = "CBC"):
    try:
        ct_bytes = bytes.fromhex(cipher_hex)
        k_bytes = pad(key.encode('utf-8'))[:16]
        round_keys = expand_key(k_bytes)
        
        iv = bytes([0] * 16)
        pt_bytes = b""
        prev_block = iv
        
        for i in range(0, len(ct_bytes), 16):
            block = ct_bytes[i:i+16]
            dec_block = decrypt_block(block, round_keys)
            
            # CBC Un-Mode
            if mode == "CBC":
                arr_dec = np.frombuffer(dec_block, dtype=np.uint8)
                arr_prev = np.frombuffer(prev_block, dtype=np.uint8)
                dec_block = (arr_dec ^ arr_prev).tobytes()
            
            pt_bytes += dec_block
            prev_block = block
            
        return unpad(pt_bytes).decode('utf-8', errors='replace')
    except Exception as e:
        return f"[ERROR DEKRIPSI]: Format tidak valid atau kunci salah. Detail: {str(e)}"

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT
# ==============================================================================

def render_aes_page():
    render_header(
        title="Menu 4: AES-128 Block Cipher",
        subtitle="Standar Enkripsi Blok 128-bit (Implementasi Operasi Matriks Murni dengan NumPy)",
        pic_name="Penanggung Jawab: Orang 3",
        category="Kriptografi Modern - Cipher Blok"
    )

    tab_main, tab_trace, tab_theory = st.tabs([
        "Operasi Enkripsi & Dekripsi",
        "Visualisasi State Matrix 4x4",
        "Teori Matematis & Vektorisasi"
    ])

    with tab_main:
        mode = render_mode_selector(session_state_key="aes_mode", key_prefix="aes")

        if mode == "Enkripsi Pesan":
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Plainteks & Parameter Kunci")
                p_aes = st.text_area("Masukkan teks plainteks:", value="BELAJAR KRIPTOGRAFI MODERN", height=110, key="aes_plain_in")
                k_aes = st.text_input("Kunci Rahasia AES (Otomatis di-pad ke 128-bit):", value="KunciSuperAman12", key="aes_key_in")
                mode_opt = st.selectbox("Mode Operasi Blok:", ["CBC", "ECB"], key="aes_mode_in")
                btn_aes_enc = st.button("Jalankan Enkripsi AES-128", key="aes_btn_enc", use_container_width=True, type="primary")
            with col2:
                st.markdown("##### Hasil Enkripsi")
                if btn_aes_enc:
                    aes_res = aes_encrypt(p_aes, k_aes, mode=mode_opt)
                    st.session_state["aes_trace"] = aes_res.get("demo_trace")
                    st.session_state["aes_last_hex"] = aes_res.get("hex_str", "")
                    st.text_area("Cipherteks (Format Heksadesimal):", value=aes_res.get("hex_str", ""), height=80)
                    st.text_area("Cipherteks (Format Base64):", value=aes_res.get("b64_str", ""), height=60)
                    st.success("Proses enkripsi AES (Operasi Matriks) berhasil diselesaikan.")
                else:
                    st.info("Tekan tombol 'Jalankan Enkripsi AES-128' untuk memproses teks.")

        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### Input Cipherteks & Kunci")
                if "aes_last_hex" in st.session_state and st.session_state["aes_last_hex"]:
                    if st.button("Salin Cipherteks dari Hasil Enkripsi", key="aes_btn_sync_enc"):
                        st.session_state["aes_dec_in"] = st.session_state["aes_last_hex"]
                        st.rerun()
                c_aes_in = st.text_area("Masukkan teks cipherteks (Heksadesimal):", value=st.session_state.get("aes_dec_in", ""), height=110, key="aes_dec_in")
                k_aes_dec = st.text_input("Kunci Rahasia AES:", value="KunciSuperAman12", key="aes_key_dec")
                mode_opt_dec = st.selectbox("Mode Operasi Blok:", ["CBC", "ECB"], key="aes_mode_dec_in")
                btn_aes_dec = st.button("Jalankan Dekripsi AES-128", key="aes_btn_dec", use_container_width=True, type="primary")
            with col2:
                st.markdown("##### Hasil Dekripsi")
                if btn_aes_dec:
                    if not c_aes_in.strip():
                        st.warning("Masukkan cipherteks terlebih dahulu.")
                    else:
                        d_res = aes_decrypt(c_aes_in, k_aes_dec, mode=mode_opt_dec)
                        st.text_area("Teks Plainteks Rekonstruksi:", value=d_res, height=110)
                        st.success("Proses dekripsi pembalikan matriks AES selesai.")
                else:
                    st.info("Tekan tombol 'Jalankan Dekripsi AES-128' untuk memproses teks.")

    with tab_trace:
        st.markdown("##### Transformasi State Matrix 4×4")
        
        # Inisialisasi otomatis jika belum ada data agar tab langsung memuat visualisasi
        is_demo = False
        if "aes_trace" not in st.session_state or not st.session_state["aes_trace"]:
            demo_res = aes_encrypt("BELAJAR KRIPTOGRAFI MODERN", "KunciSuperAman12", mode="CBC")
            st.session_state["aes_trace"] = demo_res.get("demo_trace")
            is_demo = True

        if is_demo:
            st.info("Menampilkan State Matrix dari contoh teks default ('BELAJAR KRIPTOGRAFI MODERN'). Lakukan enkripsi teks Anda di tab 'Operasi Enkripsi & Dekripsi' untuk memperbarui tabel.")

        trace_data = st.session_state.get("aes_trace", {})
        matrix_data = trace_data.get("State Matrix 4x4 (Blok Pertama)")

        if matrix_data:
            st.markdown("""
            <div class="datain-card" style="margin-bottom: 1.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span class="badge-category">FIPS 197 Standard</span>
                    <span class="badge-pic">Blok Pertama (16 Byte / 128 Bit)</span>
                </div>
                <p style="margin: 0; color: #1E3A5F; font-size: 0.95rem; line-height: 1.5;">
                    Visualisasi <b>State Matrix 4×4</b> setelah operasi transformasi round AES. Setiap sel merepresentasikan 1 byte dalam format heksadesimal <code>0xXX</code>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 1. Tabel Utama State Matrix 4x4 (Standar FIPS-197)
            st.markdown("**Tabel State Matrix 4×4 (Format Heksadesimal):**")
            df_matrix = pd.DataFrame(
                [[f"0x{cell}" for cell in row] for row in matrix_data],
                columns=["Kolom 0", "Kolom 1", "Kolom 2", "Kolom 3"],
                index=["Baris 0", "Baris 1", "Baris 2", "Baris 3"]
            )
            st.table(df_matrix)

            # 2. Tabel Rincian 16 Byte Elemen Matriks
            st.markdown("**Tabel Rincian 16 Byte Elemen State Matrix:**")
            
            # Peta nama karakter kontrol ASCII (0-31 dan 127)
            CONTROL_NAMES = {
                0: "NUL (Null)", 1: "SOH (Start of Header)", 2: "STX (Start of Text)",
                3: "ETX (End of Text)", 4: "EOT (End of Transmission)", 5: "ENQ (Enquiry)",
                6: "ACK (Acknowledge)", 7: "BEL (Bell)", 8: "BS (Backspace)",
                9: "HT (Horizontal Tab)", 10: "LF (Line Feed / Enter)", 11: "VT (Vertical Tab)",
                12: "FF (Form Feed)", 13: "CR (Carriage Return)", 14: "SO (Shift Out)",
                15: "SI (Shift In)", 16: "DLE (Data Link Escape)", 17: "DC1 (Dev Ctrl 1)",
                18: "DC2 (Dev Ctrl 2)", 19: "DC3 (Dev Ctrl 3)", 20: "DC4 (Dev Ctrl 4)",
                21: "NAK (Negative Ack)", 22: "SYN (Sync Idle)", 23: "ETB (End Trans Block)",
                24: "CAN (Cancel)", 25: "EM (End of Medium)", 26: "SUB (Substitute)",
                27: "ESC (Escape)", 28: "FS (File Separator)", 29: "GS (Group Separator)",
                30: "RS (Record Separator)", 31: "US (Unit Separator)", 127: "DEL (Delete)"
            }

            byte_rows = []
            for r_idx, row in enumerate(matrix_data):
                for c_idx, cell in enumerate(row):
                    byte_idx = r_idx * 4 + c_idx
                    dec_val = int(cell, 16)
                    bin_val = f"{dec_val:08b}"
                    
                    if 32 <= dec_val <= 126:
                        repr_char = f"'{chr(dec_val)}'"
                        tipe_byte = "Teks ASCII Printable"
                    elif dec_val in CONTROL_NAMES:
                        repr_char = CONTROL_NAMES[dec_val]
                        tipe_byte = "Control Byte (Non-printable)"
                    else:
                        repr_char = f"Biner Tinggi (0x{cell})"
                        tipe_byte = "Extended Byte (Non-printable)"

                    byte_rows.append({
                        "No": byte_idx + 1,
                        "Posisi": f"Baris {r_idx}, Kolom {c_idx}",
                        "Nilai Hex": f"0x{cell}",
                        "Nilai Desimal": dec_val,
                        "Biner (8-bit)": bin_val,
                        "Representasi Karakter": repr_char,
                        "Escape Python": f"\\x{cell.lower()}",
                        "Kategori Byte": tipe_byte
                    })

            st.dataframe(pd.DataFrame(byte_rows), width="stretch", hide_index=True)

            # Penjelasan Ilmiah / Solusi Kriptografi Standar
            st.info("""
            💡 **Mengapa Byte Cipherteks AES Bersifat Non-Printable?**
            * **Sifat Matematis Galois Field $GF(2^8)$**: AES memetakan teks ke dalam 256 nilai biner murni ($0$ s/d $255$). 
            * **Keterbatasan Standar ASCII**: Rentang karakter ASCII yang dapat dicetak (*printable*) hanya bernilai **32 (Spasi) sampai 126 (`~`)**, yaitu hanya **95 karakter (~37%)**. Sebanyak **161 nilai lainnya (~63%)** adalah kode biner/kontrol yang tidak memiliki representasi huruf.
            * **Solusi Baku Industri Kriptografi**: Cipherteks AES **tidak boleh disimpan atau dikirim sebagai string teks mentah** karena dapat rusak (*corrupted*). Standar dunia menyelesaikannya dengan mengonversi stream biner ke format teks aman:
              1. **Format Heksadesimal (Hex/Base16)**: Mengubah tiap byte menjadi 2 digit hex (tersedia di tab hasil enkripsi).
              2. **Format Base64 (RFC 4648)**: Mengubah setiap 3 byte menjadi 4 karakter ASCII aman untuk protokol jaringan HTTP/Email.
            """)
        else:
            st.info("Lakukan proses enkripsi terlebih dahulu untuk memuat visualisasi State Matrix.")

    with tab_theory:
        st.markdown("##### Teori Implementasi Matematis & Aljabar Linier (NumPy)")
        st.markdown("""
        Implementasi ini dibangun secara **matematis murni dari nol** tanpa menggunakan *library* kriptografi siap pakai. Menggunakan arsitektur matriks 2D NumPy, algoritma ini menirukan persis operasi matematika standar FIPS-197:

        1. **SubBytes (Pemetaan Matriks $1 \\to 1$)**: 
           Matriks `state` langsung dipetakan (*mapping*) ke dalam array S-Box menggunakan operasi indeks vektorisasi: `state = SBOX[state]`.
        2. **ShiftRows (Rotasi Siklis Baris)**: 
           Menggunakan operasi pergeseran array sirkuler matematis: `np.roll(baris, -i)`.
        3. **MixColumns (Perkalian Matriks *Galois Field*)**: 
           Ini adalah bentuk murni dari *Dot Product* matriks. Matriks FIPS standar $M$ dikalikan dengan matriks *State* menggunakan operasi aritmetika polinomial $GF(2^8)$.
        4. **AddRoundKey (Penjumlahan Modulo 2 / Matriks XOR)**: 
           Matriks Kunci ditambahkan (XOR bitwise paralel) langsung ke matriks *State*: `state ^ key`.
        """)

if __name__ == "__main__":
    st.set_page_config(page_title="AES-128 - Orang 3", layout="wide")
    load_global_css()
    render_aes_page()