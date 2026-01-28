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
            "site": {
                "title": "Muniz Distribuidora | Links",
                "subtitle": "Acesse nossos canais oficiais",
                "columns": 2
            },
            "tabs": [
                {"name": "Principais", "items": []}
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


# ----------------------------
# Logo helpers
# ----------------------------
def find_logo_path() -> str | None:
    # Seu GitHub está com logo.jpeg, então precisa considerar isso
    for name in ["logo.png", "logo.jpg", "logo.jpeg"]:
        if os.path.exists(name):
            return name
    return None


def read_file_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ----------------------------
# Admin auth
# ----------------------------
def get_admin_password() -> str:
    # 1) Streamlit Secrets (Cloud)
    try:
        if "ADMIN_PASSWORD" in st.secrets:
            return str(st.secrets["ADMIN_PASSWORD"])
    except Exception:
        pass
    # 2) Variável de ambiente (local)
    return os.getenv("ADMIN_PASSWORD", "")


def admin_gate() -> bool:
    """Retorna True se o admin foi autenticado nesta sessão."""
    if st.session_state.get("admin_ok"):
        return True

    admin_password = get_admin_password()
    if not admin_password:
        st.sidebar.error("Senha de admin não configurada (ADMIN_PASSWORD).")
        return False

    st.sidebar.subheader("🔒 Acesso Admin")
    typed = st.sidebar.text_input("Senha", type="password", placeholder="Digite a senha do admin")

    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        entrar = st.button("Entrar", use_container_width=True)
    with col2:
        limpar = st.button("Limpar", use_container_width=True)

    if limpar:
        st.session_state["admin_ok"] = False
        st.rerun()

    if entrar:
        if typed == admin_password:
            st.session_state["admin_ok"] = True
            st.sidebar.success("Acesso liberado.")
            st.rerun()
        else:
            st.sidebar.error("Senha incorreta.")
    return False


# ----------------------------
# UI helpers
# ----------------------------
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
title = site.get("title", "Muniz Distribuidora | Links")
subtitle = site.get("subtitle", "Acesse nossos canais oficiais")


# ----------------------------
# Styles (mais dourado e creme)
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
        background:
          radial-gradient(900px 450px at 50% 8%, rgba(237,158,31,0.22), rgba(0,0,0,0) 60%),
          radial-gradient(900px 500px at 50% 90%, rgba(246,231,203,0.07), rgba(0,0,0,0) 55%),
          var(--bg);
        color: var(--cream);
      }}

      .block-container {{
        padding-top: 1.6rem;
        padding-bottom: 2.4rem;
        max-width: 920px;
      }}

      h1, h2, h3, p, div, span, label {{
        color: var(--cream) !important;
      }}

      /* Logo */
      .logo-wrap {{
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
      }}
      .logo-wrap img {{
        width: 132px;
        height: 132px;
        object-fit: contain;
        border-radius: 999px;
        border: 2px solid rgba(237,158,31,0.85);
        box-shadow: 0 18px 40px rgba(0,0,0,0.45),
                    0 0 0 6px rgba(237,158,31,0.08);
        background: rgba(246,231,203,0.03);
        padding: 10px;
      }}

      /* Hero */
      .hero {{
        text-align: center;
        margin-bottom: 1.2rem;
      }}
      .hero h1 {{
        font-size: 2.05rem;
        margin: 0;
        line-height: 1.2;
        color: var(--accent) !important;
        text-shadow: 0 10px 25px rgba(0,0,0,0.55);
      }}
      .hero p {{
        margin: 0.45rem 0 0;
        opacity: 0.92;
        color: var(--cream) !important;
      }}

      /* Link cards */
      a.link-card {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 15px 16px;
        margin: 12px 0;
        border-radius: 18px;
        text-decoration: none !important;

        background: linear-gradient(180deg,
          rgba(246,231,203,0.07),
          rgba(11,7,6,0.55)
        );

        border: 1px solid rgba(237,158,31,0.30);
        box-shadow: 0 14px 34px rgba(0,0,0,0.42);
        transition: transform 140ms ease, border-color 140ms ease, box-shadow 140ms ease;
      }}

      a.link-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(237,158,31,0.70);
        box-shadow: 0 18px 42px rgba(0,0,0,0.55),
                    0 0 0 6px rgba(237,158,31,0.08);
      }}

      .link-icon {{
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 14px;

        background: rgba(237,158,31,0.26);
        border: 1px solid rgba(237,158,31,0.62);
        color: var(--cream);
        font-size: 18px;
      }}

      .link-text {{
        font-size: 1.03rem;
        font-weight: 750;
        color: var(--cream) !important;
        flex: 1;
      }}

      .link-arrow {{
        color: var(--accent) !important;
        font-weight: 900;
        opacity: 1;
      }}

      /* Sidebar */
      section[data-testid="stSidebar"] {{
        background: rgba(246,231,203,0.03);
        border-right: 1px solid rgba(237,158,31,0.18);
      }}

      /* Tabs */
      div[data-testid="stTabs"] button {{
        color: var(--cream) !important;
        opacity: 0.9;
      }}
      div[data-testid="stTabs"] button[aria-selected="true"] {{
        border-bottom: 3px solid var(--accent) !important;
        opacity: 1;
      }}

      .small-note {{
        text-align: center;
        opacity: 0.78;
        font-size: 0.9rem;
        margin-top: 1.25rem;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Sidebar (Admin protegido)
# ----------------------------
with st.sidebar:
    st.header("⚙️ Configurações")
    st.caption("Área pública: links. Área admin: protegida por senha.")

admin_mode = admin_gate()

if admin_mode:
    with st.sidebar:
        if st.button("Sair do Admin", use_container_width=True):
            st.session_state["admin_ok"] = False
            st.rerun()

# ----------------------------
# Logo + Hero
# ----------------------------
logo_path = find_logo_path()
if logo_path:
    mime = "png" if logo_path.endswith(".png") else "jpeg"
    b64 = read_file_base64(logo_path)
    st.markdown(
        f"""
        <div class="logo-wrap">
          <img src="data:image/{mime};base64,{b64}" alt="Logo Muniz" />
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
