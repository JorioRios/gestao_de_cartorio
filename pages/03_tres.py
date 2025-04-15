import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder

if st.button("Clique Aqui Para Voltar", type='primary'):
    st.switch_page("main.py")

with st.container(border=True):
    st.markdown("""
    ### ✅ Principais Vantagens do Relatório de Tempo Real dos Protocolos

    📊 **Acompanhamento em tempo real** da quantidade de protocolos por etapa, colaborador e natureza, proporcionando uma visão completa do andamento dos trabalhos.

    ⚠️ **Redução de falhas operacionais**, evitando esquecimentos de baixas no sistema e garantindo maior confiabilidade nas informações.

    📂 **Controle eficaz dos documentos**, permitindo identificar rapidamente quais protocolos devem ser executados com prioridade, otimizando o fluxo de trabalho e o cumprimento de prazos.

    ⏱️ **Tomada de decisão imediata**, possibilitando, ao bater o olho, identificar gargalos e avaliar a necessidade de alocação de recursos extras, como hora extra ou redistribuição de tarefas.

    🔄 **Agilidade na gestão**, com relatórios dinâmicos que se atualizam automaticamente, facilitando reuniões rápidas e objetivas com base em dados concretos.
    """)

df = pd.read_excel('dados/previsao.xlsx', sheet_name='previsao')

protocolos = df.shape[0]
with st.container(border=True):
    st.markdown(f"### Previsão de Protocolo ({protocolos} Protocolos)")

a1, a2, a3, a4, a5 = st.columns(5, border=True)

with a1:
    filtro_0 = st.selectbox("Selecionar Etapa:", ["Todos"] + sorted(df['Etapa'].dropna().unique()), index=0)
    if filtro_0 != "Todos":
        df = df[df['Etapa'] == filtro_0]

with a2:
    filtro_1 = st.selectbox("Selecionar Nome:", ["Todos", "Vazios"] + sorted(df['Nome'].dropna().unique()), index=0)
    if filtro_1 == "Vazios":
        df = df[df['Nome'].isna() | (df['Nome'] == '')]
    elif filtro_1 != "Todos":
        df = df[df['Nome'] == filtro_1]

with a3:
    filtro_2 = st.selectbox("Selecionar Status:", ["Todos"] + sorted(df['Status'].dropna().unique()), index=0)
    if filtro_2 != "Todos":
        df = df[df['Status'] == filtro_2]

with a4:
    filtro_3 = st.selectbox("Selecionar Natureza:", ["Todos"] + sorted(df['Natureza'].dropna().unique()), index=0)
    if filtro_3 != "Todos":
        df = df[df['Natureza'] == filtro_3]

with a5:
    filtro_4 = st.text_input("Buscar texto:")
    if filtro_4 != "":
        df = df[df.apply(lambda row: row.astype(str).str.contains(filtro_4, case=False).any(), axis=1)]

# Reorganiza as etapas na ordem definida
ordem_etapas = ['Abertura', 'Análise/Registro', 'Conferência', 'Impressão/Certidão', 'Vistoria Certidão', 'Vistoria Impugnado']
df['Etapa'] = pd.Categorical(df['Etapa'], categories=ordem_etapas, ordered=True)
dias = ordem_etapas  # Mantém apenas as etapas na ordem desejada

series = []
legends = []
statuses = ["No Prazo", "Próximo do Vencimento", "Vencido Etapa", "Vencido Cliente"]

for classif, cor in zip(statuses, ["#1f663e", "#a3a318", "#94332c", "gray"]):
    etapa_status_counts = df[df["Status"] == classif].groupby("Etapa", observed=False).size().reindex(dias, fill_value=0)
    total_count = etapa_status_counts.sum()  # Calcula o total de cada status
    legends.append(f"{classif} ({total_count})")  # Adiciona a quantidade à legenda
    series.append({
        "name": f"{classif} ({total_count})",  # Nome da série também com total
        "type": "bar",
        "data": etapa_status_counts.tolist(),
        "itemStyle": {"color": cor},
        "barGap": "5%",
        "label": {
            "show": True,
            "position": "top",  # Define a posição do rótulo (em cima das barras)
            "formatter": "{c}",  # Exibe o valor da barra
            "fontSize": 12,      # Opcional: ajusta o tamanho da fonte
        },
    })

options = {
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
    },
    "legend": {"data": legends},
    "xAxis": {
        "type": "category",
        "data": dias,
        "axisPointer": {"type": "shadow"},
    },
    "yAxis": {"type": "value"},
    "grid": {
        "left": "3%",
        "right": "4%",
        "bottom": "3%",
        "containLabel": True,
    },
    "series": series,
}

events = {
    "click": "function(params) { return {seriesName: params.seriesName, name: params.name}; }",
}

# Inicializa o estado caso ainda não exista
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None

if "force_rerender" not in st.session_state:
    st.session_state.force_rerender = 0  # Controle de renderização

# Força o gráfico a ser rerenderizado (incrementa o estado do controle)
key_suffix = f"_{st.session_state.force_rerender}"

# Renderiza o gráfico com eventos
with st.container(border=True):
    selected_event = st_echarts(
        options=options, events=events, height=600, key=f"render_grouped_bar_events{key_suffix}"
    )

# Captura o evento selecionado
if selected_event:
    st.session_state.selected_event = selected_event

# Mostrar tabela com ou sem filtro
if st.session_state.selected_event and selected_event is not None:
    selected_period = selected_event["seriesName"].split(" (")[0]  # Período
    selected_day = selected_event["name"]  # Dia
    filtered_df = df[
        (df["Status"] == selected_period) & (df["Etapa"] == selected_day)
    ]
    data_to_display = filtered_df
    # Botão para limpar o evento
    col1, col2 = st.columns([1,2], vertical_alignment='center')
    with col1:
        st.write(f"**Filtro aplicado:** status = `{selected_period}`, etapa = `{selected_day}`")
    with col2:
        if st.button("Limpar Seleção"):
            # Redefine o estado e força a rerenderização
            st.session_state.selected_event = None
            st.session_state.force_rerender += 1
            st.rerun()
else:
    data_to_display = df

gb = GridOptionsBuilder.from_dataframe(data_to_display)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_default_column(filter="agTextColumnFilter", editable=False)

# Configurando filtros únicos para colunas específicas
for col in ["Etapa", "Nome", "Natureza", "Status"]:
    gb.configure_column(col, filter="agSetColumnFilter")

grid_options = gb.build()

AgGrid(data_to_display, gridOptions=grid_options, height=347, theme="streamlit", fit_columns_on_grid_load=True)

col1, col2, col3 = st.columns(3, border=True)

with col1:
    st.markdown("### Quantidade por Natureza")
    natureza_counts = data_to_display['Natureza'].value_counts().reset_index()
    natureza_counts.columns = ['Natureza', 'Quantidade']
    natureza_counts = natureza_counts.sort_values(by='Quantidade', ascending=False)
    st.dataframe(natureza_counts, hide_index=True, width=500, height=468)

with col2:
    st.markdown("### Quantidade por Usuário")
    nome_counts = data_to_display['Nome'].value_counts().reset_index()
    nome_counts.columns = ['Nome', 'Quantidade']
    nome_counts = nome_counts.sort_values(by='Quantidade', ascending=False)
    st.dataframe(nome_counts, hide_index=True, width=500, height=468)

with col3:
    st.markdown("### Quantidade por Etapa")
    etapa_counts = data_to_display['Etapa'].value_counts().reset_index()
    etapa_counts.columns = ['Etapa', 'Quantidade']
    etapa_counts = etapa_counts.sort_values(by='Quantidade', ascending=False)
    st.dataframe(etapa_counts, hide_index=True, width=500)