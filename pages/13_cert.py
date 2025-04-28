import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"] == False:
    st.switch_page("main.py")

if st.button("Clique Aqui Para Voltar", type='primary'):
    if st.session_state["logged_in"] == False:
        st.switch_page("main.py")
    else:
        st.switch_page("pages/10_apresent.py")

def carregar_dados():
    return pd.read_excel('dados/previsao.xlsx', sheet_name='onr')
df = carregar_dados()

# Principal
a1, a2 = st.columns([1,2], border=True)

with a1:
    st.subheader('Previsão ONR Inteiro Teor da Matrícula')

    df_sorted = df.sort_values(by='horas_uteis',ascending=False)

    def highlight_rows(row):
        if row['horas_uteis'] > 3:
            return ['background-color: lightcoral' for _ in row]
        elif row['horas_uteis'] <= 3 and row['horas_uteis'] > 2:
            return ['background-color: lightyellow' for _ in row]
        else:
            return ['background-color: lightgreen' for _ in row]    

    # Aplicar o estilo ao DataFrame
    styled_df = df_sorted.style.apply(highlight_rows, axis=1)

    # Exibir o DataFrame estilizado no Streamlit
    styled_df = styled_df.format({'horas_uteis': '{:.2f}'})
    st.dataframe(styled_df, hide_index=True)

def carregar_dados1():
    return pd.read_excel('dados/previsao.xlsx', sheet_name='certidao')
df = carregar_dados1()

certidoes = df.shape[0]

with a2:
    st.subheader(f'Previsão de Certidão ({certidoes} Certidões)')

    # Agrupar os dados
    df_grouped_filtrado = df.groupby(['Etapa', 'Situação']).size().reset_index(name='Count')

    # Preparar as etapas únicas
    etapas = df_grouped_filtrado['Etapa'].unique().tolist()
    situacoes = df_grouped_filtrado['Situação'].unique().tolist()

    # Definir as cores para cada situação
    cores = {
        'Vencido Cliente': 'gray',
        'Vencido Etapa': '#94332c',
        'Próximo do Vencimento': '#a3a318',
        'No Prazo': '#1f663e'
    }

    # Calcular total de cada situação
    totais = df_grouped_filtrado.groupby('Situação')['Count'].sum().to_dict()

    # Atualizar legenda com total
    legenda_data = [f"{situacao} ({totais.get(situacao, 0)})" for situacao in situacoes]

    # Construir a estrutura de dados para ECharts
    series = []
    for situacao in situacoes:
        dados = []
        for etapa in etapas:
            count = df_grouped_filtrado[
                (df_grouped_filtrado['Etapa'] == etapa) & 
                (df_grouped_filtrado['Situação'] == situacao)
            ]['Count']
            if not count.empty:
                dados.append(int(count.values[0]))
            else:
                dados.append(0)
        
        series.append({
            "name": f"{situacao} ({totais.get(situacao, 0)})",  # Atualizar também o name no series
            "type": "bar",
            "label": {
                "show": True,
                "position": "top",
                "fontWeight": "bold"
            },
            "emphasis": {
                "focus": "series"
            },
            "itemStyle": {
                "color": cores.get(situacao, "#000000")
            },
            "data": dados
        })

    # Configuração do gráfico
    options = {
        "backgroundColor": "white",
        "tooltip": {"trigger": "axis"},
        "legend": {
            "show": True,
            "data": legenda_data
        },
        "xAxis": {
            "type": "category",
            "data": etapas,
            "axisLabel": {"rotate": 0}
        },
        "yAxis": {
            "type": "value"
        },
        "series": series,
        "grid": {
            "left": 0,
            "right": 20,
            "top": 40,
            "bottom": 0,
            "containLabel": True
        }
    }

    st_echarts(options=options, height="300px")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)  # Configura 10 linhas por página
grid_options = gb.build()

AgGrid(df, gridOptions=grid_options,  height=347, theme="streamlit", fit_columns_on_grid_load=True)