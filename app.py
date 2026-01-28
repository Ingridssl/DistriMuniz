import json
import os
import re
import base64
from urllib.parse import urlparse

import streamlit as st

DATA_FILE = "links.json"

PALETTE = {
    "accent": "#ed9e1f",  # dourado
    "bg": "#0b0706",      # preto
    "brown": "#873a1c",   # marrom
    "cream": "#f6e7cb",   # creme
}


def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {
            "site": {
                "title": "Muniz Distribuidora | Links",
                "subtitle": "Acesse nossos canais oficiais",
                "columns": 2
            },
            "tabs": [
                {
                    "name": "Principais",
                    "items": [
                        {"label": "WhatsApp", "url": "https://wa.me/5591999999999", "icon": "💬"},
                        {"label": "Instagram", "url": "https://instagram.com/suaempresa", "icon": "📷"},
                        {"label": "iFood", "url": "https://www.ifood.com.br/delivery/sua-loja", "icon": "🍔"},
                        {"label": "Zé Delivery", "url": "https://www.ze.delivery/", "icon": "🍺"},
                    ],
                }
            ],
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_valid_url(url: str) -> bool:
    try:
        p = urlparse((url or "").strip())
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def read_logo_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_button(label: str, url: str, icon: str):
    label = (label or "").strip()
    url = (url or "").strip()
    icon = (icon or "🔗").strip()

    st.markdown(
        f"""
        <a class="link-card" href="{url}" target="_blank" rel="noopener noreferrer">
            <span class="link-icon">{icon}</span>
            <span class="link-text">{label}</span>
            <span class="link-arrow">↗</span>
        </a>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Muniz | Links", page_icon="🔗", layout="centered")

data = load_data()
site = data.get("site", {})
tabs = data.get("tabs", [])

columns = int(site.get("columns", 2))
title = site.get("title", "Links")
subtitle = site.get("subtitle", "")

# ----------------------------
# Styles
# ----------------------------
st.markdown(
    f"""
    <style>
      :root {{
        --accent: {PALETTE["accent"]};
        --bg: {PALETTE["bg"]};
        --brown: {PALETTE["brown"]};
        --cream: {PALETTE["cream"]};
      }}

      .stApp {{
        background: var(--bg);
        color: var(--cream);
      }}

      .block-container {{
        padding-top: 2.0rem;
        padding-bottom: 2.5rem;
        max-width: 860px;
      }}

      h1, h2, h3, p, div, span, label {{
        color: var(--cream) !important;
      }}

      .logo-wrap {{
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
      }}
      .logo-wrap img {{
        width: 120px;
        height: 120px;
        object-fit: contain;
        border-radius: 999px;
        border: 2px solid rgba(237,158,31,0.70);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        background: rgba(255,255,255,0.02);
        padding: 10px;
      }}

      .hero {{
        text-align: center;
        margin-bottom: 1.25rem;
      }}
      .hero h1 {{
        font-size: 2.0rem;
        margin: 0;
        line-height: 1.2;
      }}
      .hero p {{
        margin: 0.4rem 0 0;
        opacity: 0.92;
      }}

      a.link-card {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        margin: 10px 0;
        border-radius: 16px;
        text-decoration: none !important;

        background: linear-gradient(
          180deg,
          rgba(255,255,255,0.04),
          rgba(255,255,255,0.02)
        );

        border: 1px solid rgba(246,231,203,0.12);
        transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
      }}
      a.link-card:hover {{
        transform: translateY(-1px);
        border-color: rgba(237,158,31,0.55);
        box-shadow: 0 12px 28px rgba(0,0,0,0.35);
      }}

      .link-icon {{
        width: 40px;
        height: 40px;
        display: grid;
        place-items: center;
        border-radius: 14px;

        background: rgba(237,158,31,0.18);
        border: 1px solid rgba(237,158,31,0.30);
        font-size: 18px;
      }}

      .link-text {{
        font-size: 1.02rem;
        font-weight: 650;
        color: var(--cream) !important;
        flex: 1;
      }}

      .link-arrow {{
        color: var(--accent) !important;
        font-weight: 800;
        opacity: 0.95;
      }}

      section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.03);
        border-right: 1px solid rgba(246,231,203,0.10);
      }}

      div[data-testid="stTabs"] button {{
        color: var(--cream) !important;
      }}
      div[data-testid="stTabs"] button[aria-selected="true"] {{
        border-bottom: 2px solid var(--accent) !important;
      }}

      .small-note {{
        text-align: center;
        opacity: 0.75;
        font-size: 0.9rem;
        margin-top: 1.25rem;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Sidebar admin
# ----------------------------
with st.sidebar:
    st.header("⚙️ Configurações")
    admin_mode = st.toggle("Modo Admin", value=False, help="Ative para editar links e abas")
    st.caption("Deixe desativado para uso público.")


# ----------------------------
# Top logo + hero
# ----------------------------
if os.path.exists("logo.png"):
    b64 = read_logo_base64("logo.png")
    st.markdown(f'<div class="logo-wrap"><img src="data:image/png;base64,{b64}"/></div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="hero">
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Tabs view
# ----------------------------
if not tabs:
    tabs = [{"name": "Principais", "items": []}]

tab_names = [t.get("name", "Aba") for t in tabs]
tab_objs = st.tabs(tab_names)

for idx, tab in enumerate(tabs):
    items = tab.get("items", [])
    with tab_objs[idx]:
        cols = st.columns(columns)
        for i, item in enumerate(items):
            label = item.get("label", "Link")
            url = item.get("url", "")
            icon = item.get("icon", "🔗")
            with cols[i % columns]:
                if is_valid_url(url):
                    render_button(label, url, icon)
                else:
                    st.warning(f"URL inválida em: {label}")

# ----------------------------
# Admin panel
# ----------------------------
if admin_mode:
    st.divider()
    st.subheader("🛠️ Painel Admin")

    with st.expander("Aparência", expanded=False):
        site["title"] = st.text_input("Título", value=site.get("title", "Muniz Distribuidora | Links"))
        site["subtitle"] = st.text_input("Subtítulo", value=site.get("subtitle", "Acesse nossos canais oficiais"))
        site["columns"] = st.slider("Colunas de botões", 1, 3, int(site.get("columns", 2)))
        data["site"] = site

    st.markdown("### Abas e Links")
    tab_to_edit = st.selectbox("Editar aba", options=tab_names, index=0)
    tab_index = tab_names.index(tab_to_edit)
    current_tab = tabs[tab_index]

    col_a, col_b = st.columns([2, 1])

    with col_a:
        current_tab["name"] = st.text_input("Nome da aba", value=current_tab.get("name", tab_to_edit)).strip() or "Aba"

        edited = st.data_editor(
            current_tab.get("items", []),
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "label": st.column_config.TextColumn("Título do botão", required=True),
                "url": st.column_config.TextColumn("URL (https://...)", required=True),
                "icon": st.column_config.TextColumn("Ícone (emoji)", required=False),
            },
            hide_index=True,
        )
        current_tab["items"] = edited

    with col_b:
        st.markdown("#### Ações")
        if st.button("➕ Criar nova aba"):
            tabs.append({"name": "Nova Aba", "items": []})
            st.success("Nova aba criada!")
            st.rerun()

        if len(tabs) > 1 and st.button("🗑️ Excluir esta aba"):
            tabs.pop(tab_index)
            st.success("Aba excluída.")
            st.rerun()

        st.markdown("---")
        if st.button("💾 Salvar alterações"):
            errors = []
            for t in tabs:
                if not (t.get("name") or "").strip():
                    errors.append("Existe uma aba sem nome.")
                for it in t.get("items", []):
                    u = (it.get("url") or "").strip()
                    if u and not is_valid_url(u):
                        errors.append(f"URL inválida: {it.get('label','(sem título)')} → {u}")

            if errors:
                st.error("Corrija antes de salvar:\n- " + "\n- ".join(errors))
            else:
                data["tabs"] = tabs
                save_data(data)
                st.success("Salvo em links.json!")
                st.rerun()

st.markdown('<div class="small-note">🔗 Muniz Distribuidora — Página de links</div>', unsafe_allow_html=True)
