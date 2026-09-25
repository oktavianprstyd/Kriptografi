import streamlit as st

def load_global_css():
    """Memuat CSS global agar seluruh halaman memiliki gaya visual yang seragam."""
    st.markdown("""
    <style>
        .menu-title {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.1rem;
        }
        .menu-desc {
            font-size: 1rem;
            color: #4B5563;
            margin-bottom: 1.2rem;
        }
        .badge-p1 {
            background-color: #DBEAFE;
            color: #1E40AF;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            margin-right: 6px;
        }
        .badge-p2 {
            background-color: #E0E7FF;
            color: #3730A3;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            margin-right: 6px;
        }
        .badge-p3 {
            background-color: #DCFCE7;
            color: #166534;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            margin-right: 6px;
        }
        .badge-p4 {
            background-color: #FEF3C7;
            color: #92400E;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            margin-right: 6px;
        }
        .badge-super {
            background-color: #F3E8FF;
            color: #6B21A8;
            padding: 5px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }
        .card-box {
            background-color: #F8FAFC;
            border-radius: 10px;
            padding: 1.2rem;
            border: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str, person_badge: str, algo_badge: str, badge_class: str):
    """Menampilkan header terpadu di setiap halaman modul."""
    st.markdown(f'<div class="menu-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="{badge_class}">{person_badge}</span> <span class="{badge_class}">{algo_badge}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="menu-desc" style="margin-top: 0.6rem;">{subtitle}</div>', unsafe_allow_html=True)
