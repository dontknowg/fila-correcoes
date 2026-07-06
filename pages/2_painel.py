import streamlit as st
import pandas as pd
from supabase import create_client, Client
import urllib.parse
from datetime import datetime, date

st.set_page_config(page_title="Painel | Projeto de Correções", layout="wide")

# CSS alinhado corretamente (removido o recuo extra)
st.markdown(
    """
    <style>
    /* Esconde o menu/rodapé padrão do Streamlit */
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }

    /* Trava de Segurança: Oculta completamente a barra lateral e o botão de colapso */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

TABELA = "fila"

@st.cache_resource
def init_connection() -> Client:
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = init_connection()

# ... (resto das suas funções continua exatamente igual)

def carregar_dados(filtro_status=None) -> pd.DataFrame:
    query = supabase.table(TABELA).select("*")
    if filtro_status:
        query = query.eq("status", filtro_status).order("data_hora", desc=False)
    else:
        query = query.order("data_hora", desc=True)
    response = query.execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=["id", "data_hora", "nome", "contato", "turma", "tema", "status"])

def atualizar_status(id_aluno: str, novo_status: str):
    supabase.table(TABELA).update({"status": novo_status}).eq("id", id_aluno).execute()

def contar_por_status(dados: pd.DataFrame, status: str) -> int:
    if dados.empty:
        return 0
    return len(dados[dados["status"] == status])

def gerar_link_whatsapp(contato: str, nome: str) -> str:
    numero = "".join(filter(str.isdigit, str(contato)))
    texto = f"Olá, {nome}! É a sua vez no Projeto de Correções. Dirija-se à mesa do corretor."
    return f"https://wa.me/55{numero}?text={urllib.parse.quote(texto)}"

# ---------- AUTENTICAÇÃO ----------

if not st.session_state.get("autenticado"):
    col_vazia_e, col_login, col_vazia_d = st.columns([1, 2, 1])
    with col_login:
        st.title("Acesso Restrito")
        st.markdown("Insira a senha para acessar o painel de correções.")
        with st.form("form_login"):
            senha = st.text_input("Senha", type="password", label_visibility="collapsed", placeholder="Senha de acesso")
            if st.form_submit_button("Entrar", use_container_width=True):
                if senha == st.secrets.get("SENHA_CORRETOR", "corretor123"):
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    st.stop()

# ---------- PAINEL DO CORRETOR ----------
# O restante do seu código abaixo permanece igual, apenas garanta que 
# os níveis de indentação estejam alinhados (Tabulação padrão)
st.title("Painel de Correções")
# ... restante do seu código
