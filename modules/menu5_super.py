import streamlit as st
import pandas as pd

try:
    from .ui_helper import render_header, load_global_css
    from .menu1_caesar import caesar_encrypt, caesar_decrypt
    from .menu2_vigenere import vigenere_encrypt, vigenere_decrypt
    from .menu3_aes import aes_encrypt, aes_decrypt
    from .menu4_vernam import vernam_encrypt, vernam_decrypt
except ImportError:
    from ui_helper import render_header, load_global_css
    from menu1_caesar import caesar_encrypt, caesar_decrypt
    from menu2_vigenere import vigenere_encrypt, vigenere_decrypt
    from menu3_aes import aes_encrypt, aes_decrypt
    from menu4_vernam import vernam_encrypt, vernam_decrypt

# ==============================================================================
# BAGIAN 1: LOGIKA PIPELINE SUPER ENKRIPSI (VERNAM TAHAP 3, AES TAHAP 4)
# Penanggung Jawab: Seluruh Tim (Orang 1 s/d 4)
# ==============================================================================

def super_encrypt(plaintext: str, caesar_shift: int, vigenere_key: str, vernam_key: str = "VERNAM_STREAM_KEY", aes_key: str = "KunciAESSuper12"):
    # 1. Caesar Cipher (Orang 1 - Klasik Monoalfabetik)
    c_out, c_steps = caesar_encrypt(plaintext, caesar_shift)

    # 2. Vigenère Cipher (Orang 2 - Klasik Polialfabetik)
    v_out, v_steps = vigenere_encrypt(c_out, vigenere_key)

    # 3. Vernam Stream Cipher (Orang 4 - Modern Aliran Bitwise XOR)
    c_bytes, vernam_hex, bin_res, vernam_steps = vernam_encrypt(v_out, vernam_key, mode="repeat")

    # 4. AES-128 Block Cipher (Orang 3 - Modern Blok)
    aes_res = aes_encrypt(vernam_hex, aes_key)
    aes_hex = aes_res.get("hex_str", vernam_hex)

    stages = [
        {"Tahap": 1, "Algoritma": "Caesar Cipher (Klasik Mono)", "Penanggung Jawab": "Orang 1", "Hasil Transformasi": str(c_out)},
        {"Tahap": 2, "Algoritma": "Vigenère Cipher (Klasik Poli)", "Penanggung Jawab": "Orang 2", "Hasil Transformasi": str(v_out)},
        {"Tahap": 3, "Algoritma": "Vernam Stream Cipher (Modern Aliran)", "Penanggung Jawab": "Orang 4 (Oktavian)", "Hasil Transformasi": str(vernam_hex)},
        {"Tahap": 4, "Algoritma": "AES-128 Block Cipher (Modern Blok)", "Penanggung Jawab": "Orang 3 (Adha)", "Hasil Transformasi": str(aes_hex)},
    ]
    return {
        "final_cipher": aes_hex,
        "stages": stages,
        "plaintext": plaintext,
        "caesar_shift": caesar_shift,
        "caesar_out": c_out,
        "caesar_steps": c_steps,
        "vigenere_key": vigenere_key,
        "vigenere_out": v_out,
        "vigenere_steps": v_steps,
        "vernam_key": vernam_key,
        "vernam_hex": vernam_hex,
        "vernam_bin": bin_res,
        "vernam_steps": vernam_steps,
        "aes_key": aes_key,
        "aes_hex": aes_hex,
        "aes_b64": aes_res.get("b64_str", ""),
        "aes_trace": aes_res.get("demo_trace", {})
    }


def super_decrypt(ciphertext_input: str, caesar_shift: int, vigenere_key: str, vernam_key: str = "VERNAM_STREAM_KEY", aes_key: str = "KunciAESSuper12"):
    # 4. Pembalik AES-128 (AES Dekripsi)
    aes_plain = aes_decrypt(ciphertext_input, aes_key)

    # 3. Pembalik Vernam (XOR Dekripsi)
    v_rec, _ = vernam_decrypt(aes_plain, vernam_key)

    # 2. Pembalik Vigenère (Vigenère Dekripsi)
    vig_plain, _ = vigenere_decrypt(v_rec, vigenere_key)

    # 1. Pembalik Caesar (Caesar Dekripsi)
    final_plain, _ = caesar_decrypt(vig_plain, caesar_shift)

    return final_plain


# ==============================================================================
# BAGIAN 2: TAMPILAN DASHBOARD STREAMLIT (GAYA DATAIN - BERSIH & RAPI)
# ==============================================================================

def render_super_page():
    render_header(
        title="Menu 5: Super Enkripsi",
        subtitle="Pipeline Terpadu 4 Tahap: Caesar ➔ Vigenère ➔ Vernam (Aliran) ➔ AES-128 (Blok)",
        pic_name="Penanggung Jawab: Seluruh Tim",
        category="Super Enkripsi Terpadu"
    )

    tab_enc, tab_dec, tab_pipe, tab_theory = st.tabs([
        "Super Enkripsi",
        "Super Dekripsi",
        "Visualisasi Transformasi Pipeline",
        "Teori Super Enkripsi"
    ])

    with tab_enc:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Input Plainteks & Parameter Kunci 4 Modul")
            plain_super = st.text_area("Masukkan teks plainteks:", value="BELAJAR KRIPTOGRAFI", height=90, key="sup_plain")
            k1, k2 = st.columns(2)
            with k1:
                k_c = st.number_input("Kunci Caesar Shift k (Orang 1):", 1, 25, 3, key="sup_kc")
                k_v = st.text_input("Kunci Vigenère (Orang 2):", value="INFORMATIKA", key="sup_kv")
            with k2:
                k_vernam_sup = st.text_input("Kunci Keystream Vernam (Orang 4):", value="VERNAM_STREAM_KEY", key="sup_kvernam")
                k_aes_sup = st.text_input("Kunci AES-128 (Orang 3):", value="KunciAESSuper12", key="sup_kaes")

            btn_sup_enc = st.button("Jalankan Super Enkripsi 4 Tahap", key="sup_btn_enc", type="primary", use_container_width=True)

        with c2:
            st.markdown("##### Hasil Akhir Super Cipherteks")
            if btn_sup_enc:
                try:
                    sup_res = super_encrypt(plain_super, k_c, k_v, k_vernam_sup, k_aes_sup)
                    st.session_state["sup_res"] = sup_res
                    st.markdown("**Final Super Cipherteks (Format Heksadesimal AES):**")
                    st.markdown(f'<div class="cipher-box" style="font-size: 0.9rem; word-break: break-all;">{sup_res["final_cipher"]}</div>', unsafe_allow_html=True)
                    st.success("Seluruh 4 algoritma berhasil dieksekusi secara berantai tanpa henti!")
                except Exception as ex:
                    st.error(f"Gagal memproses super enkripsi: {ex}")
            else:
                if "sup_res" in st.session_state and "final_cipher" in st.session_state["sup_res"]:
                    st.markdown("**Final Super Cipherteks Sebelumnya:**")
                    st.markdown(f'<div class="cipher-box" style="font-size: 0.9rem; word-break: break-all;">{st.session_state["sup_res"]["final_cipher"]}</div>', unsafe_allow_html=True)
                else:
                    st.info("Tekan tombol 'Jalankan Super Enkripsi 4 Tahap' untuk memproses.")

    with tab_dec:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Input Super Cipherteks & Kunci Pembalik (LIFO)")
            init_c_dec = st.session_state.get("sup_res", {}).get("final_cipher", "")
            c_sup_in = st.text_area("Masukkan teks super cipherteks (Hex):", value=init_c_dec, height=90, key="sup_dec_in")

            kd1, kd2 = st.columns(2)
            with kd1:
                kd_aes = st.text_input("Kunci AES Pembalik (Tahap 4):", value="KunciAESSuper12", key="sup_kdaes")
                kd_vernam = st.text_input("Kunci Vernam Pembalik (Tahap 3):", value="VERNAM_STREAM_KEY", key="sup_kdvernam")
            with kd2:
                kd_v = st.text_input("Kunci Vigenère Pembalik (Tahap 2):", value="INFORMATIKA", key="sup_kdv")
                kd_c = st.number_input("Kunci Caesar Pembalik (Tahap 1):", 1, 25, 3, key="sup_kdc")

            btn_sup_dec = st.button("Jalankan Super Dekripsi (Prinsip LIFO)", key="sup_btn_dec", type="primary", use_container_width=True)

        with c2:
            st.markdown("##### Hasil Plainteks Rekonstruksi")
            if btn_sup_dec:
                try:
                    dec_sup = super_decrypt(c_sup_in, kd_c, kd_v, kd_vernam, kd_aes)
                    st.markdown("**Plainteks Rekonstruksi Hasil Dekripsi LIFO:**")
                    st.markdown(f'<div class="cipher-box" style="font-size: 1.05rem; font-weight: 600;">{dec_sup}</div>', unsafe_allow_html=True)
                    st.success("Proses pembalikan pipeline 4 tahap berhasil diselesaikan!")
                except Exception as err:
                    st.error(f"Gagal memproses dekripsi: {err}")
            else:
                st.info("Tekan tombol 'Jalankan Super Dekripsi' untuk memproses.")

    with tab_pipe:
        # Sediakan data awal jika belum pernah dijalankan
        if "sup_res" not in st.session_state or "stages" not in st.session_state["sup_res"]:
            st.session_state["sup_res"] = super_encrypt(
                "BELAJAR KRIPTOGRAFI", 3, "INFORMATIKA", "VERNAM_STREAM_KEY", "KunciAESSuper12"
            )

        res_data = st.session_state["sup_res"]

        st.markdown("##### 1. Ikhtisar Alur Transformasi Pipeline 4 Stasiun")
        st.dataframe(pd.DataFrame(res_data["stages"]), width="stretch", hide_index=True)
        st.divider()

        st.markdown("##### 2. Pelacakan Transformasi Step-by-Step Setiap Algoritma")
        st.caption("Pilih tab di bawah untuk melihat rincian kalkulasi matematika dan pelacakan langkah demi langkah pada setiap stasiun:")

        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "Tahap 1: Caesar Cipher (Klasik)",
            "Tahap 2: Vigenère Cipher (Klasik)",
            "Tahap 3: Vernam Stream Cipher (Modern Aliran)",
            "Tahap 4: AES-128 Block Cipher (Modern Blok)"
        ])

        # TAB 1: CAESAR CIPHER STEP-BY-STEP
        with sub_tab1:
            st.markdown(f"""
            <div class="datain-card" style="margin-bottom: 1rem;">
                <span class="badge-category">Tahap 1</span>
                <span class="badge-pic">Penanggung Jawab: Orang 1</span>
                <p style="margin: 8px 0 4px 0; color: #1E3A5F; font-size: 0.95rem; line-height: 1.6;">
                    <b>Input Plainteks:</b> <code>{res_data.get('plaintext', '')}</code><br>
                    <b>Kunci Pergeseran (Shift k):</b> <code>{res_data.get('caesar_shift', 3)}</code><br>
                    <b>Rumus Modulo 26:</b> <code>C_i = (P_i + {res_data.get('caesar_shift', 3)}) mod 26</code><br>
                    <b>Output Sandi Caesar:</b> <code>{res_data.get('caesar_out', '')}</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

            c_steps = res_data.get("caesar_steps", [])
            if c_steps:
                st.markdown("**Tabel Kalkulasi Modulo 26 Karakter demi Karakter:**")
                st.dataframe(pd.DataFrame(c_steps), width="stretch", hide_index=True)

        # TAB 2: VIGENÈRE CIPHER STEP-BY-STEP
        with sub_tab2:
            st.markdown(f"""
            <div class="datain-card" style="margin-bottom: 1rem;">
                <span class="badge-category">Tahap 2</span>
                <span class="badge-pic">Penanggung Jawab: Orang 2</span>
                <p style="margin: 8px 0 4px 0; color: #1E3A5F; font-size: 0.95rem; line-height: 1.6;">
                    <b>Input (Output dari Caesar):</b> <code>{res_data.get('caesar_out', '')}</code><br>
                    <b>Kata Kunci Vigenère:</b> <code>{res_data.get('vigenere_key', '')}</code><br>
                    <b>Rumus Polialfabetik:</b> <code>C_i = (P_i + K_i) mod 26</code> (Berdasarkan Tabula Recta 26x26)<br>
                    <b>Output Sandi Vigenère:</b> <code>{res_data.get('vigenere_out', '')}</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

            v_steps = res_data.get("vigenere_steps", [])
            if v_steps:
                st.markdown("**Tabel Penjajaran Huruf Kunci dan Kalkulasi Polialfabetik:**")
                st.dataframe(pd.DataFrame(v_steps), width="stretch", hide_index=True)

        # TAB 3: VERNAM STREAM CIPHER STEP-BY-STEP
        with sub_tab3:
            st.markdown(f"""
            <div class="datain-card" style="margin-bottom: 1rem;">
                <span class="badge-category">Tahap 3</span>
                <span class="badge-pic">Penanggung Jawab: Orang 4 (Oktavian Prasetya Adi)</span>
                <p style="margin: 8px 0 4px 0; color: #1E3A5F; font-size: 0.95rem; line-height: 1.6;">
                    <b>Input (Output dari Vigenère):</b> <code>{res_data.get('vigenere_out', '')}</code><br>
                    <b>Kunci Keystream Vernam:</b> <code>{res_data.get('vernam_key', '')}</code><br>
                    <b>Operasi Logika Bit:</b> <code>c_i = p_i ⊕ k_i</code> (Bitwise XOR Aliran Byte/Bit)<br>
                    <b>Output Sandi Vernam (Hex):</b> <code>{res_data.get('vernam_hex', '')}</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

            vn_steps = res_data.get("vernam_steps", [])
            if vn_steps:
                st.markdown("**Tabel Pelacakan Bitwise XOR per Byte (ASCII ➔ Biner ➔ XOR ➔ Heksadesimal):**")
                st.dataframe(pd.DataFrame(vn_steps), width="stretch", hide_index=True)

        # TAB 4: AES-128 BLOCK CIPHER STEP-BY-STEP
        with sub_tab4:
            st.markdown(f"""
            <div class="datain-card" style="margin-bottom: 1rem;">
                <span class="badge-category">Tahap 4</span>
                <span class="badge-pic">Penanggung Jawab: Orang 3 (Adha)</span>
                <p style="margin: 8px 0 4px 0; color: #1E3A5F; font-size: 0.95rem; line-height: 1.6;">
                    <b>Input (Heksadesimal dari Vernam):</b> <code>{res_data.get('vernam_hex', '')}</code><br>
                    <b>Kunci Rahasia AES-128:</b> <code>{res_data.get('aes_key', '')}</code> (Expanded ke 10 Putaran)<br>
                    <b>Standar Industri:</b> FIPS 197 (CBC Mode, SubBytes, ShiftRows, MixColumns, AddRoundKey)<br>
                    <b>Output Akhir Super Cipherteks:</b> <code>{res_data.get('aes_hex', '')}</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

            aes_matrix = res_data.get("aes_trace", {}).get("State Matrix 4x4 (Blok Pertama)")
            if aes_matrix:
                st.markdown("**Visualisasi State Matrix 4×4 Blok Pertama (Representasi Heksadesimal NumPy):**")
                df_matrix = pd.DataFrame(
                    aes_matrix,
                    columns=["Kolom 0", "Kolom 1", "Kolom 2", "Kolom 3"],
                    index=["Baris 0", "Baris 1", "Baris 2", "Baris 3"]
                )
                st.dataframe(df_matrix, width="stretch")

            st.markdown("**Final Super Cipherteks (Base64):**")
            st.markdown(f'<div class="cipher-box" style="font-size: 0.85rem;">{res_data.get("aes_b64", "")}</div>', unsafe_allow_html=True)

    with tab_theory:
        st.markdown("##### Konsep Super Enkripsi Terpadu")
        st.markdown(r"""
        **Super Enkripsi** menggabungkan beberapa algoritma kriptografi secara beruntun (*pipelining*).
        Secara matematis, ini membentuk sebuah **Fungsi Komposisi**:

        $$E_{super}(P) = E_{aes}(E_{vernam}(E_{vig}(E_{caesar}(P))))$$

        * **Kombinasi Algoritma:**
          1. **Tahap 1 (Caesar Cipher):** Kriptografi Klasik (Aritmetika Modulo 26).
          2. **Tahap 2 (Vigenère Cipher):** Kriptografi Klasik (Substitusi Polialfabetik).
          3. **Tahap 3 (Vernam Stream Cipher):** Kriptografi Modern (Cipher Aliran Bitwise XOR Keystream).
          4. **Tahap 4 (AES-128 Rijndael):** Kriptografi Modern (Cipher Blok Matriks Galois Field $GF(2^8)$).

        * **Prinsip Dekripsi (LIFO - Teorema Invers Komposisi)**:
          Berdasarkan aturan invers fungsi komposisi $(f \circ g)^{-1} = g^{-1} \circ f^{-1}$, proses pembalikan harus dilakukan dengan urutan terbalik secara presisi:
          $$\text{Super Cipherteks} \xrightarrow{\text{AES}^{-1}} C_3 \xrightarrow{\text{Vernam}^{-1}} C_2 \xrightarrow{\text{Vigenère}^{-1}} C_1 \xrightarrow{\text{Caesar}^{-1}} \text{Plainteks}$$
        """)


# Standalone runner
if __name__ == "__main__":
    st.set_page_config(page_title="Super Enkripsi", layout="wide")
    load_global_css()
    render_super_page()
