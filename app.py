import json
import os
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


# ----------------------------
# Data
# ----------------------------
def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {
            "site": {"title": "Muniz Distribuidora | Links", "subtitle": "Acesse nossos canais oficiais", "columns": 2},
            "tabs": [{"name": "Principais", "items": []}],
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


# ----------------------------
# Files
# ----------------------------
def find_logo_path() -> str | None:
    for name in ["logo.png", "logo.webp", "logo.jpg", "logo.jpeg"]:
        if os.path.exists(name):
            return name
    return None


def guess_mime_from_path(path: str) -> str:
    p = path.lower()
    if p.endswith(".png"):
        return "image/png"
    if p.endswith(".jpg") or p.endswith(".jpeg"):
        return "image/jpeg"
    if p.endswith(".webp"):
        return "image/webp"
    if p.endswith(".svg"):
        return "image/svg+xml"
    return "application/octet-stream"


def read_file_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_data_uri(path: str) -> str | None:
    if not path:
        return None
    # aceita também "./icons/..."
    p = path
    if not os.path.exists(p) and os.path.exists("./" + p):
        p = "./" + p
    if not os.path.exists(p):
        return None
    mime = guess_mime_from_path(p)
    b64 = read_file_base64(p)
    return f"data:{mime};base64,{b64}"


# ----------------------------
# Admin auth
# ----------------------------
def get_admin_password() -> str:
    try:
        if "ADMIN_PASSWORD" in st.secrets:
            return str(st.secrets["ADMIN_PASSWORD"])
    except Exception:
        pass
    return os.getenv("ADMIN_PASSWORD", "")


def admin_login_ui() -> bool:
    if st.session_state.get("admin_ok"):
        return True

    admin_password = get_admin_password()
    if not admin_password:
        st.warning("Senha de admin não configurada (ADMIN_PASSWORD).")
        return False

    typed = st.text_input("Senha do Admin", type="password", placeholder="Digite a senha")
    c1, c2 = st.columns([1, 1])
    with c1:
        entrar = st.button("Entrar", use_container_width=True)
    with c2:
        limpar = st.button("Limpar", use_container_width=True)

    if limpar:
        st.session_state["admin_ok"] = False
        st.rerun()

    if entrar:
        if typed == admin_password:
            st.session_state["admin_ok"] = True
            st.success("Acesso liberado.")
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False


# ----------------------------
# UI
# ----------------------------
def render_button(label: str, url: str, arquivo: str | None):
    label = (label or "").strip()
    url = (url or "").strip()

    data_uri = build_data_uri(arquivo) if arquivo else None
    icon_html = "<span class='link-icon-fallback'>🔗</span>"
    if data_uri:
        icon_html = f'<img class="link-icon-img" src="{data_uri}" alt="{label}"/>'

    st.markdown(
        f"""
        <a class="link-card" href="{url}" target="_blank" rel="noopener noreferrer">
            <span class="link-icon">{icon_html}</span>
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
title = site.get("title", "Muniz Distribuidora | Links")
subtitle = site.get("subtitle", "Acesse nossos canais oficiais")


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

      header[data-testid="stHeader"] {{
        background: transparent !important;
      }}

      .block-container {{
        padding-top: 2.8rem !important;
        padding-bottom: 2.2rem;
        max-width: 920px;
      }}
      @media (max-width: 640px) {{
        .block-container {{
          padding-top: 4.2rem !important;
        }}
      }}

      .stApp {{
        background:
          radial-gradient(1000px 520px at 50% 8%, rgba(237,158,31,0.45), rgba(0,0,0,0) 62%),
          radial-gradient(900px 500px at 18% 70%, rgba(135,58,28,0.30), rgba(0,0,0,0) 62%),
          linear-gradient(180deg,
            rgba(237,158,31,0.28) 0%,
            rgba(135,58,28,0.38) 34%,
            rgba(11,7,6,1) 80%,
            rgba(11,7,6,1) 100%
          );
        color: var(--cream);
      }}

      h1, h2, h3, p, div, span, label {{
        color: var(--cream) !important;
      }}

      /* LOGO: círculo perfeito */
      .logo-wrap {{
        display: flex;
        justify-content: center;
        margin: 0 0 12px 0;
      }}
      .logo-circle {{
        width: 170px;
        height: 170px;
        border-radius: 999px;
        overflow: hidden;
        border: 2px solid rgba(237,158,31,0.65);
        background: rgba(11,7,6,0.55);
        box-shadow: 0 18px 44px rgba(0,0,0,0.45);
      }}
      .logo-circle img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }}
      @media (max-width: 640px) {{
        .logo-circle {{
          width: 150px;
          height: 150px;
        }}
      }}

      .hero {{
        text-align: center;
        margin-bottom: 1.15rem;
      }}
      .hero h1 {{
        font-size: 2.05rem;
        margin: 0;
        line-height: 1.2;
        color: var(--cream) !important;
        text-shadow: 0 10px 25px rgba(0,0,0,0.55);
      }}
      .hero p {{
        margin: 0.45rem 0 0;
        opacity: 0.95;
      }}

      /* Cards */
      a.link-card {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 16px;
        margin: 12px 0;
        border-radius: 18px;
        text-decoration: none !important;
        background: linear-gradient(180deg,
          rgba(246,231,203,0.10),
          rgba(135,58,28,0.24),
          rgba(11,7,6,0.62)
        );
        border: 1px solid rgba(237,158,31,0.42);
        box-shadow: 0 14px 34px rgba(0,0,0,0.45);
        transition: transform 140ms ease, border-color 140ms ease, box-shadow 140ms ease;
      }}
      a.link-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(237,158,31,0.92);
        box-shadow: 0 18px 46px rgba(0,0,0,0.60),
                    0 0 0 7px rgba(237,158,31,0.10);
      }}

      /* ✅ ÍCONE: fundo MARROM com degradê (pra logo preta aparecer) */
      .link-icon {{
        width: 52px;
        height: 52px;
        display: grid;
        place-items: center;
        border-radius: 16px;
        overflow: hidden;

        background: radial-gradient(circle at 30% 30%,
          rgba(237,158,31,0.25),
          rgba(135,58,28,0.98) 55%,
          rgba(11,7,6,0.90) 100%) !important;

        border: 1px solid rgba(237,158,31,0.95);
        box-shadow: inset 0 0 0 1px rgba(0,0,0,0.35);
      }}

      .link-icon-img {{
        width: 82%;
        height: 82%;
        object-fit: contain;
        display: block;
        filter: drop-shadow(0 2px 6px rgba(0,0,0,0.55));
      }}

      .link-text {{
        font-size: 1.04rem;
        font-weight: 780;
        flex: 1;
      }}
      .link-arrow {{
        color: var(--accent) !important;
        font-weight: 900;
      }}

      /* Sidebar */
      section[data-testid="stSidebar"] {{
        background: rgba(11,7,6,0.92);
        border-right: 1px solid rgba(237,158,31,0.22);
      }}

      /* Tabs */
      div[data-testid="stTabs"] button[aria-selected="true"] {{
        border-bottom: 3px solid var(--accent) !important;
      }}

      /* Footer/Admin no final */
      .footer-admin {{
        margin-top: 26px;
        padding-top: 18px;
        border-top: 1px solid rgba(237,158,31,0.22);
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("⚙️ Configurações")
    st.caption("A lateral abre pelo botão (>>) no topo.")
    if st.session_state.get("admin_ok"):
        if st.button("Sair do Admin", use_container_width=True):
            st.session_state["admin_ok"] = False
            st.rerun()

# ----------------------------
# Logo + Hero
# ----------------------------
logo_path = find_logo_path()
if logo_path:
    logo_uri = build_data_uri(logo_path)
    if logo_uri:
        st.markdown(
            f"""
            <div class="logo-wrap">
              <div class="logo-circle">
                <img src="{logo_uri}" alt="Logo Muniz" />
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
# Tabs
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
            arquivo = item.get("arquivo")
            with cols[i % columns]:
                if is_valid_url(url):
                    render_button(label, url, arquivo)
                else:
                    st.warning(f"URL inválida em: {label}")

# ----------------------------
# Footer/Admin no final
# ----------------------------
st.markdown('<div class="footer-admin">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 2])
with c1:
    if st.button("🔒 Área do Admin", use_container_width=True):
        st.session_state["show_admin"] = True
with c2:
    st.caption("Acesso protegido por senha.")
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("show_admin") and not st.session_state.get("admin_ok"):
    st.subheader("🔒 Login Admin")
    admin_login_ui()
    st.divider()

if st.session_state.get("admin_ok"):
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

    current_tab["name"] = st.text_input("Nome da aba", value=current_tab.get("name", tab_to_edit)).strip() or "Aba"

    edited = st.data_editor(
        current_tab.get("items", []),
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "label": st.column_config.TextColumn("Título", required=True),
            "url": st.column_config.TextColumn("URL", required=True),
            "arquivo": st.column_config.TextColumn("Arquivo imagem (ex: icons/instagram.png)", required=False),
        },
        hide_index=True,
    )
    current_tab["items"] = edited

    if st.button("💾 Salvar alterações", use_container_width=True):
        data["tabs"] = tabs
        save_data(data)
        st.success("Salvo em links.json!")
        st.rerun()
