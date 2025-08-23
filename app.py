import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="Projetos Financeiros", layout="wide")

# Inicializar storage na sessão
if "projetos" not in st.session_state:
    st.session_state.projetos = []

# Função para adicionar ou editar projeto
def salvar_projeto(data, codigo, receita, depe, ressarcimento, doa, edit_id=None):
    if edit_id:
        for p in st.session_state.projetos:
            if p["id"] == edit_id:
                p.update({
                    "data": data,
                    "codigo": codigo,
                    "receita": receita,
                    "depe": depe,
                    "ressarcimento": ressarcimento,
                    "doa": doa
                })
                break
    else:
        st.session_state.projetos.append({
            "id": str(uuid.uuid4()),
            "data": data,
            "codigo": codigo,
            "receita": receita,
            "depe": depe,
            "ressarcimento": ressarcimento,
            "doa": doa,
        })

# Sidebar - cadastro
st.sidebar.header("Novo Projeto")

with st.sidebar.form("cadastro"):
    data = st.date_input("Data")
    codigo = st.text_input("Código do projeto")
    receita = st.number_input("Receita", min_value=0.0, step=100.0)

    # Cálculo automático
    depe_default = receita * 0.10
    ress_default = receita * 0.03
    doa_default = receita * 0.10

    depe = st.number_input("DEPE (10%)", min_value=0.0, value=depe_default, step=10.0)
    ressarcimento = st.number_input("Ressarcimento (3%)", min_value=0.0, value=ress_default, step=10.0)
    doa = st.number_input("DOA (10%)", min_value=0.0, value=doa_default, step=10.0)

    submitted = st.form_submit_button("Salvar")
    if submitted:
        if not codigo:
            st.warning("Informe o código do projeto!")
        else:
            salvar_projeto(str(data), codigo, receita, depe, ressarcimento, doa)
            st.success("Projeto salvo com sucesso!")

# Exibir tabela de projetos
st.title("📊 Projetos Financeiros")

if st.session_state.projetos:
    df = pd.DataFrame(st.session_state.projetos)
    st.dataframe(df.drop(columns=["id"]), use_container_width=True)

    # Totais
    st.subheader("Totais")
    totais = df[["receita", "depe", "ressarcimento", "doa"]].sum()
    st.write(totais)
else:
    st.info("Nenhum projeto cadastrado ainda.")
