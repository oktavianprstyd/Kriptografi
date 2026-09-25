import streamlit as st

def load_global_css():
    """
    Menyuntikkan sistem desain terpadu bergaya DataIn (Warm Cream & Deep Navy).
    Font: Outfit (Heading) & Plus Jakarta Sans (Body)
    Palet Warna:
      - Primary Navy: #002D80
      - Text Navy: #1E3A5F
      - Slate Blue: #4A709C
      - Warm Cream Background: #FAF6F0
      - Container Warm Dark: #F4F0EA
      - Border Taupe: #D8CFC4
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* 1. Global Typography & Colors */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #1E3A5F;
            letter-spacing: -0.01em;
        }

        .stApp {
            background-color: #FAF6F0;
        }

        /* 2. Headings (Outfit) */
        h1, h2, h3, h4, h5, h6, .menu-title {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            letter-spacing: -0.02em;
            color: #1E3A5F !important;
            font-weight: 700;
        }

        .menu-title {
            font-size: 2rem;
            margin-bottom: 0.2rem;
        }

        .menu-desc {
            font-size: 0.98rem;
            color: #4A709C;
            margin-bottom: 1.2rem;
            line-height: 1.5;
        }

        /* 3. DataIn Card Component */
        .datain-card {
            background-color: #FFFFFF;
            border: 1px solid #D8CFC4;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 20px -5px rgba(0, 45, 128, 0.08);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .datain-card:hover {
            border-color: #002D80;
            box-shadow: 0 12px 28px -6px rgba(0, 45, 128, 0.12);
        }

        /* 4. Minimalist Badges (Tanpa Emoji) */
        .badge-category {
            background-color: #EBF0F7;
            color: #002D80;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            display: inline-block;
            margin-right: 6px;
            border: 1px solid #D1DFEE;
        }

        .badge-pic {
            background-color: #FFFFFF;
            color: #1E3A5F;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-block;
            border: 1px solid #D8CFC4;
        }

        /* 5. Custom Button Styling (Solid Navy Main) */
        .stButton > button {
            background-color: #002D80 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 0.55rem 1.2rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(0, 45, 128, 0.15) !important;
        }

        .stButton > button:hover {
            background-color: #142742 !important;
            box-shadow: 0 4px 14px rgba(0, 45, 128, 0.25) !important;
            transform: translateY(-1px);
        }

        /* 6. Form Inputs & Text Areas */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #FFFFFF !important;
            border: 1px solid #D8CFC4 !important;
            border-radius: 8px !important;
            color: #1E3A5F !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #002D80 !important;
            box-shadow: 0 0 0 1px #002D80 !important;
        }

        /* 7. Monospace Output Box (For Ciphers, Hashes, Matrix) */
        .cipher-box {
            font-family: 'JetBrains Mono', monospace !important;
            background-color: #FFFFFF;
            border: 1px solid #D8CFC4;
            border-radius: 8px;
            padding: 0.85rem;
            font-size: 0.92rem;
            color: #002D80;
            word-break: break-all;
        }

        /* 8. Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            border-bottom: 1px solid #D8CFC4;
        }

        .stTabs [data-baseweb="tab"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            color: #4A709C !important;
            padding: 8px 16px !important;
            border-radius: 6px 6px 0 0 !important;
        }

        .stTabs [aria-selected="true"] {
            color: #002D80 !important;
            border-bottom: 2px solid #002D80 !important;
            background-color: transparent !important;
        }

        /* 9. Sidebar Clean Background */
        [data-testid="stSidebar"] {
            background-color: #F4F0EA !important;
            border-right: 1px solid #D8CFC4 !important;
        }

        /* 10. Sidebar Interactive Block Navigation (Gaya Card Menu Interaktif) */
        [data-testid="stSidebar"] div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding-top: 4px;
        }

        /* Block Box Card untuk setiap pilihan menu */
        [data-testid="stSidebar"] div[role="radiogroup"] > label {
            background-color: #FFFFFF !important;
            border: 1px solid #D8CFC4 !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            margin: 0 !important;
            width: 100% !important;
            cursor: pointer !important;
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 45, 128, 0.04) !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Sembunyikan lingkaran radio default agar menjadi murni blok kartu */
        [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Teks di dalam kartu menu */
        [data-testid="stSidebar"] div[role="radiogroup"] > label p {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.94rem !important;
            color: #1E3A5F !important;
            margin: 0 !important;
            transition: color 0.2s ease !important;
        }

        /* EFEK HOVER: Saat kursor mendekat, blok berubah jadi warna biru elegan */
        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background-color: #002D80 !important;
            border-color: #002D80 !important;
            transform: translateX(6px) !important;
            box-shadow: 0 6px 18px rgba(0, 45, 128, 0.22) !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover p {
            color: #FFFFFF !important;
        }

        /* EFEK AKTIF (MENU YANG SEDANG DIPILIH) */
        [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
            background-color: #002D80 !important;
            border-color: #002D80 !important;
            box-shadow: 0 6px 18px rgba(0, 45, 128, 0.25) !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* 11. Dataframe / Table refinement */
        .stDataFrame {
            border: 1px solid #D8CFC4;
            border-radius: 8px;
            background-color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str, pic_name: str, category: str):
    """
    Menampilkan header terpadu bergaya DataIn: bersih, elegan, dan tanpa emotikon berlebihan.
    """
    st.markdown(f'<div class="menu-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="badge-category">{category}</span> '
        f'<span class="badge-pic">{pic_name}</span>',
        unsafe_allow_html=True
    )
    st.markdown(f'<div class="menu-desc" style="margin-top: 0.5rem;">{subtitle}</div>', unsafe_allow_html=True)
