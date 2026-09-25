import streamlit as st
import pandas as pd
import base64
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

try:
    from .ui_helper import render_header, load_global_css
except ImportError:
    from ui_helper import render_header, load_global_css

# ==============================================================================
# BAGIAN 1: LOGIKA ALGORITMA AES-128 BLOCK CIPHER (ORANG 3)
# ==============================================================================
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5e, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

def derive_16byte_key(key_input: str) -> bytes:
    raw = key_input if isinstance(key_input, bytes) else str(key_input).encode('utf-8')
    return hashlib.sha256(raw).digest()[:16]

def bytes_to_matrix(b: bytes):
    return [[b[r + 4 * c] for c in range(4)] for r in range(4)]

def matrix_to_hex_table(matrix):
    return [[f"{val:02X}" for val in row] for row in matrix]

def sub_bytes(state):
    return [[S_BOX[state[r][c]] for c in range(4)] for r in range(4)]

def shift_rows(state):
    return [
        state[0][:],
        state[1][1:] + state[1][:1],
        state[2][2:] + state[2][:2],
        state[3][3:] + state[3][:3]
    ]

def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

def mix_single_column(col):
    t = col[0] ^ col[1] ^ col[2] ^ col[3]
    u = col[0]
    return [
        col[0] ^ t ^ xtime(col[0] ^ col[1]),
        col[1] ^ t ^ xtime(col[1] ^ col[2]),
        col[2] ^ t ^ xtime(col[2] ^ col[3]),
        col[3] ^ t ^ xtime(col[3] ^ u)
    ]

def mix_columns(state):
    new_state = [[0] * 4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        mixed = mix_single_column(col)
        for r in range(4):
            new_state[r][c] = mixed[r]
    return new_state

def add_round_key(state, round_key_matrix):
    return [[state[r][c] ^ round_key_matrix[r][c] for c in range(4)] for r in range(4)]

def get_aes_round_demo(block_16bytes: bytes, key_16bytes: bytes):
    if len(block_16bytes) < 16:
        block_16bytes = block_16bytes.ljust(16, b'\x00')
    else:
        block_16bytes = block_16bytes[:16]

    state = bytes_to_matrix(block_16bytes)
    key_mat = bytes_to_matrix(key_16bytes)

    state_after_ark0 = add_round_key(state, key_mat)
    state_sub = sub_bytes(state_after_ark0)
    state_shift = shift_rows(state_sub)
    state_mix = mix_columns(state_shift)
    state_round1_final = add_round_key(state_mix, key_mat)

    return {
        "initial_state": matrix_to_hex_table(state),
        "key_matrix": matrix_to_hex_table(key_mat),
        "round0_ark": matrix_to_hex_table(state_after_ark0),
        "round1_subbytes": matrix_to_hex_table(state_sub),
        "round1_shiftrows": matrix_to_hex_table(state_shift),
        "round1_mixcolumns": matrix_to_hex_table(state_mix),
        "round1_ark": matrix_to_hex_table(state_round1_final)
    }

def aes_encrypt(data_bytes: bytes, key_str: str, mode: str = "CBC"):
    key_16 = derive_16byte_key(key_str)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data_bytes) + padder.finalize()

    if mode.upper() == "CBC":
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key_16), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        full_ciphertext = iv + encrypted
    else:
        iv = b""
        cipher = Cipher(algorithms.AES(key_16), modes.ECB())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        full_ciphertext = encrypted

    hex_str = full_ciphertext.hex().upper()
    b64_str = base64.b64encode(full_ciphertext).decode('utf-8')
    demo_trace = get_aes_round_demo(padded_data[:16], key_16)

    return {
        "cipher_bytes": full_ciphertext,
        "hex_str": hex_str,
        "b64_str": b64_str,
        "iv_hex": iv.hex().upper() if iv else "None (ECB)",
        "key_hex": key_16.hex().upper(),
        "block_count": len(padded_data) // 16,
        "demo_trace": demo_trace
    }

def aes_decrypt(cipher_bytes: bytes, key_str: str, mode: str = "CBC"):
    key_16 = derive_16byte_key(key_str)
    if mode.upper() == "CBC":
        if len(cipher_bytes) < 32 or len(cipher_bytes) % 16 != 0:
            raise ValueError("Ciphertext tidak valid untuk AES-128-CBC.")
        iv = cipher_bytes[:16]
        encrypted = cipher_bytes[16:]
        cipher = Cipher(algorithms.AES(key_16), modes.CBC(iv))
    else:
        if len(cipher_bytes) % 16 != 0:
            raise ValueError("Ciphertext tidak valid untuk AES-128-ECB.")
        iv = b""
        encrypted = cipher_bytes
        cipher = Cipher(algorithms.AES(key_16), modes.ECB())

    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    original_data = unpadder.update(padded_data) + unpadder.finalize()
    try:
        text = original_data.decode('utf-8')
    except UnicodeDecodeError:
        text = original_data.decode('latin-1', errors='replace')

    return {"plain_bytes": original_data, "text": text}

# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (ORANG 3)
# ==============================================================================
def render_aes_page():
    render_header(
        "3️⃣ AES-128 Block Cipher",
        "Standar Enkripsi Blok Modern 128-bit dengan Mode CBC & State Matrix 4×4",
        "Penanggung Jawab: Orang 3",
        "Kriptografi Modern",
        "badge-p3"
    )

    tab_enc, tab_dec, tab_trace, tab_theory = st.tabs([
        "🔒 Enkripsi", "🔓 Dekripsi", "🔍 Visualisasi State Matrix & Round", "📖 Teori & Rumus"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            p_aes = st.text_area("Masukkan Plaintext:", value="BELAJAR KRIPTOGRAFI UNTUK INDONESIA MAJU", height=120, key="aes_plain_in")
            k_aes = st.text_input("Kunci Rahasia AES:", value="KunciSuperAman128", key="aes_key_in")
            mode_opt = st.selectbox("Mode Operasi:", ["CBC (Cipher Block Chaining - Standar)", "ECB (Electronic Codebook)"], key="aes_mode_in")
            btn_aes_enc = st.button("🔒 Enkripsi Sekarang", key="aes_btn_enc", use_container_width=True)
        with c2:
            if p_aes and k_aes:
                m_str = "CBC" if "CBC" in mode_opt else "ECB"
                aes_res = aes_encrypt(p_aes.encode('utf-8'), k_aes, mode=m_str)
                st.session_state["aes_trace"] = aes_res["demo_trace"]
                st.text_area("Ciphertext (Heksadesimal):", value=aes_res["hex_str"], height=80)
                st.text_area("Ciphertext (Base64):", value=aes_res["b64_str"], height=60)
                ca, cb = st.columns(2)
                ca.metric("Jumlah Blok 128-bit", f"{aes_res['block_count']} Blok")
                cb.metric("Derived Key (16 Bytes)", aes_res["key_hex"][:12] + "...")
                st.caption(f"IV: `{aes_res['iv_hex']}`")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            c_aes_in = st.text_area("Masukkan Ciphertext (Hex atau Base64):", value="", height=120, key="aes_dec_in")
            k_aes_dec = st.text_input("Kunci Rahasia AES:", value="KunciSuperAman128", key="aes_key_dec")
            mode_dec_opt = st.selectbox("Mode Operasi:", ["CBC (Cipher Block Chaining - Standar)", "ECB (Electronic Codebook)"], key="aes_mode_dec")
            fmt_opt = st.radio("Format Input:", ["Heksadesimal (Hex)", "Base64"], horizontal=True, key="aes_fmt")
            btn_aes_dec = st.button("🔓 Dekripsi Sekarang", key="aes_btn_dec", use_container_width=True)
        with c2:
            if c_aes_in and k_aes_dec:
                try:
                    clean = c_aes_in.strip().replace(" ", "").replace("\n", "")
                    raw = bytes.fromhex(clean) if fmt_opt == "Heksadesimal (Hex)" else base64.b64decode(clean)
                    m_dec_str = "CBC" if "CBC" in mode_dec_opt else "ECB"
                    d_res = aes_decrypt(raw, k_aes_dec, mode=m_dec_str)
                    st.text_area("Hasil Plaintext:", value=d_res["text"], height=120)
                    st.success("Dekripsi AES-128 Sukses!")
                except Exception as e:
                    st.error(f"Gagal mendekripsi: {str(e)}")

    with tab_trace:
        st.markdown("#### 🧱 Transformasi State Matrix 4×4 (Round 1)")
        if "aes_trace" in st.session_state:
            t = st.session_state["aes_trace"]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**1. Initial State Matrix (Input Block):**")
                st.dataframe(pd.DataFrame(t["initial_state"]), use_container_width=True)
                st.markdown("**3. State Setelah SubBytes (S-Box):**")
                st.dataframe(pd.DataFrame(t["round1_subbytes"]), use_container_width=True)
                st.markdown("**5. State Setelah MixColumns (GF(2^8)):**")
                st.dataframe(pd.DataFrame(t["round1_mixcolumns"]), use_container_width=True)
            with c2:
                st.markdown("**2. State Setelah Pre-Round AddRoundKey:**")
                st.dataframe(pd.DataFrame(t["round0_ark"]), use_container_width=True)
                st.markdown("**4. State Setelah ShiftRows (Siklis):**")
                st.dataframe(pd.DataFrame(t["round1_shiftrows"]), use_container_width=True)
                st.markdown("**6. Output Final Round 1:**")
                st.dataframe(pd.DataFrame(t["round1_ark"]), use_container_width=True)
        else:
            st.info("Lakukan enkripsi terlebih dahulu untuk memuat visualisasi State Matrix.")

    with tab_theory:
        st.markdown("""
        ### 📖 Teori AES-128 (Materi 5)
        * **Kategori**: Cipher Blok Simetris (*Symmetric Block Cipher*) berbasis *Substitution-Permutation Network*.
        * **Struktur 10 Putaran (*Rounds*)**:
          1. **SubBytes**: Substitusi non-linear per byte menggunakan tabel S-Box Rijndael.
          2. **ShiftRows**: Pergeseran siklis byte pada baris State Matrix.
          3. **MixColumns**: Transformasi kolom matriks dalam lapangan Galois $GF(2^8)$.
          4. **AddRoundKey**: Operasi XOR antara State Matrix dengan kunci putaran (*Round Key*).
        """)

# Standalone runner untuk pengujian mandiri Orang 3
if __name__ == "__main__":
    st.set_page_config(page_title="AES-128 - Orang 3", page_icon="🔐", layout="wide")
    load_global_css()
    render_aes_page()
