import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
from datetime import datetime

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"] == False:
    st.switch_page("main.py")

if st.button("Clique Aqui Para Voltar", type='primary'):
    if st.session_state["logged_in"] == False:
        st.switch_page("main.py")
    else:
        st.switch_page("pages/10_apresent.py")

@st.cache_data
def carregar_dados():
    return pd.read_excel('dados/previsao.xlsx', sheet_name='rendimento')
df = carregar_dados()

# Função para aplicar a escala de cores por coluna
def color_scale(val, min_val, max_val):
    cmap = sns.color_palette("RdYlGn", as_cmap=True)  # Paleta de cores
    norm = plt.Normalize(min_val, max_val)
    color = cmap(norm(val))
    r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Calcular a luminosidade percebida
    text_color = 'white' if brightness < 128 else 'black'
    return f'background-color: rgb({r}, {g}, {b}); color: {text_color}'

# Função para aplicar a escala de cores ao DataFrame
def apply_columnwise_color_scale(df):
    styled_df = df.style
    for column in df.columns:
        if column.lower() == 'total':  # Ignora a coluna 'Total'
            continue
        min_val = df[column].min()
        max_val = df[column].max()
        styled_df = styled_df.map(lambda val: color_scale(val, min_val, max_val), subset=[column])
    return styled_df

a1, a2, a3= st.columns(3, border=True, vertical_alignment='center')

filtro0 = None
filtro1 = None

with a1:
    filtro2 = st.selectbox("Selecionar Setor:", sorted(df['departamento'].dropna().unique()), index=None, placeholder="Todos Selecionados")
    if filtro2 is None:
        df = df
    else:
        df = df[df['departamento'] == filtro2]

with a2:
    filtro1 = st.selectbox("Selecionar Nome:", sorted(df['nome'].dropna().unique()), index=None, placeholder="Todos Selecionados")
    if filtro1 is None:
        df = df
    else:
        df = df[df['nome'] == filtro1]

with a3:
    filtro3 = st.selectbox("Selecionar Tipo:", sorted(df['tipo'].dropna().unique()), index=None, placeholder="Todos Selecionados")
    if filtro3 is None:
        df = df
    else:
        df = df[df['tipo'] == filtro3]   

a1, a2 = st.columns([1,1.5])

with a1:
    df_pivot = df.pivot_table(index='ano_mes', columns='tipo', aggfunc='size', fill_value=0)
    fig = px.line(df_pivot, markers=True, labels={'value': 'Quantidade', 'ano_mes': 'Ano/Mês', 'variable': 'Tipo'}, height=500)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=df_pivot.index, ticktext=[str(val) for val in df_pivot.index]))

    with st.container(border=True):
        if filtro1 is not None:
            st.subheader(f"Rendimento por Mês de {filtro1}")
        else:
            if filtro2 is None:
                st.subheader("Rendimento por Mês de Todos Setores")
            else:
                st.subheader(f"Rendimento por Mês do Setor {filtro2}")

        st.plotly_chart(fig)

with a2:
    tabela_pivot = df.pivot_table(
        index="nome",
        columns="ano_mes", 
        values="tipo",
        aggfunc="count",
        fill_value=0
    )

    tabela_pivot["Total"] = tabela_pivot.sum(axis=1)
    tabela_pivot = tabela_pivot.sort_values(by="Total", ascending=False)

    df_protocolo_styled = apply_columnwise_color_scale(tabela_pivot)
    st.dataframe(df_protocolo_styled, height=595, width=2000)