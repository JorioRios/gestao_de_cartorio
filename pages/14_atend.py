import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.button("Clique Aqui Para Voltar", type='primary'):
    if st.session_state["logged_in"] == False:
        st.switch_page("main.py")
    else:
        st.switch_page("pages/10_apresent.py")

@st.cache_data
def carregar_dados():
    return pd.read_excel('dados/previsao.xlsx', sheet_name='atendimento')
df = carregar_dados()

# Widget para seleção de filtro
a1, a2, a3 = st.columns(3, border=True)

with a1:
    filtro_valor = st.selectbox("Selecionar Setor:", sorted(df['tipo'].dropna().unique()), index=None, placeholder="Todos Selecionados")
    if filtro_valor is None:
        df = df
    else:
        df = df[df['tipo'] == filtro_valor]

with a2:
    filtro0 = st.selectbox("Selecionar Status:", sorted(df['status'].dropna().unique()), index=None, placeholder="Todos Selecionados")
    if filtro0 is None:
        df = df
    else:
        df = df[df['status'] == filtro0]

with a3:
    filtro1 = st.selectbox("Selecionar Ano/Mês:", sorted(df['mes_ano'].unique(),reverse=True), index=None, placeholder="Mês Atual")
    if filtro1 is None:
        filtro1 = '2024-12'
        df_filtrado = df[df['mes_ano'] == filtro1]
    else:
        df_filtrado = df[df['mes_ano'] == filtro1]

contagem = df_filtrado.groupby(['Dia', 'Hora']).size().reset_index(name='Contagem')
df_pivot = contagem.pivot(index='Hora', columns='Dia', values='Contagem')

col11, col12, col13, col14, col15, col16 = st.columns([2,1,1,1,1,1], vertical_alignment='center', border=True)
with col11:
    st.title(f'{filtro1} Métricas')
with col12:
    st.metric("**Senhas emitidas**", df_filtrado.shape[0])
with col13:
    st.metric("**Senhas atrasadas**", df_filtrado[df_filtrado['status'] == 'atrasado'].shape[0])
with col14:
    num_atrasos = df_filtrado[df_filtrado['status'] == 'atrasado'].shape[0]
    total_registros = df_filtrado.shape[0]
    perc_atraso = (num_atrasos / total_registros) * 100
    st.metric("**Percentual Atraso**", f"{perc_atraso:.2f}%")
with col15:
    tempo_medio_espera = df_filtrado['Tempo espera'].mean()
    total_seconds = int(tempo_medio_espera * 3600)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    tempo_formatado = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    st.metric("**Tempo de espera**", tempo_formatado)
with col16:
    tempo_medio_espera = df_filtrado['Tempo atendimento'].mean()
    total_seconds = int(tempo_medio_espera * 3600)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    tempo_formatado1 = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    st.metric("**Tempo de atendimento**", tempo_formatado1)

df_filt = df[df['mes_ano'] != datetime.now().strftime('%Y-%m')]
df_grouped = df_filt.groupby(['mes_ano']).agg(
                                    Qtd_Atendimento=('Tempo espera', 'count'),
                                    Média_Espera=('Tempo espera', 'mean'),
                                    Total_Atrasados=('status', lambda x: (x == 'atrasado').sum())                                        
                                    ).reset_index()
df_grouped['Percentual_Atrasados'] = ((df_grouped['Total_Atrasados'] / df_grouped['Qtd_Atendimento']) * 100).round(2)
df_grouped['Média_Espera'] = (df_grouped['Média_Espera'] * 60).round(2)
df_sorted = df_grouped.sort_values(by='mes_ano', ascending=False)

def add_icon(val, col):
    rank = df_sorted[col].rank(method='min', ascending=(col == 'Média_Espera' or col == 'Percentual_Atrasados')).loc[df_sorted[df_sorted[col] == val].index[0]]
    if rank == 1:
        return '🏆'  # Troféu para o 1º lugar
    elif rank == 2:
        return '🥈'  # Medalha de prata para o 2º lugar
    elif rank == 3:
        return '🥉'  # Medalha de bronze para o 3º lugar
    else:
        return ''

# Selecionar apenas as colunas desejadas
df_filtered = df_sorted[['mes_ano', 'Qtd_Atendimento', 'Média_Espera', 'Percentual_Atrasados']]

# Renomear as colunas
df_filtered = df_filtered.rename(columns={
    'mes_ano': 'Ano/Mês',
    'Qtd_Atendimento': 'Total Atendimento',
    'Média_Espera': 'Média Espera (min)',
    'Percentual_Atrasados': 'Perc. Atraso (%)'
})

styled_df = df_filtered.style \
    .background_gradient(subset=['Total Atendimento'], cmap='RdYlGn') \
    .background_gradient(subset=['Média Espera (min)', 'Perc. Atraso (%)'], cmap='RdYlGn_r') \
    .format({
        'Total Atendimento': lambda x: f"{add_icon(x, 'Qtd_Atendimento')} {x}",
        'Média Espera (min)': lambda x: f"{add_icon(x, 'Média_Espera')} {x:.2f}",
        'Perc. Atraso (%)': lambda x: f"{add_icon(x, 'Percentual_Atrasados')} {x:.2f}"
    })

col1, col2 = st.columns([1,1], border=True)

with col1:
    st.title('Histórico Mensal')
    st.dataframe(styled_df, hide_index=True, height=310)
with col2:
    st.title(f'{filtro1} Horário de Pico')
    df_agrupado = df_filtrado.groupby('Hora').size().reset_index(name='Quantidade')
    fig = px.bar(df_agrupado, x='Hora', y='Quantidade', labels={'Hora': 'Hora', 'Quantidade': 'Quantidade'}, color='Quantidade', text='Quantidade',  height=350)
    fig.update_layout(yaxis=dict(range=[df_agrupado['Quantidade'].min() - 5, df_agrupado['Quantidade'].max() + df_agrupado['Quantidade'].max()*0.15]),
                    xaxis=dict(tickmode='linear', tick0=df_agrupado['Hora'].min(), dtick=1))
    fig.update_traces(textposition='outside', textfont=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

def background_gradient(s, cmap='RdYlGn_r'):
    norm = mcolors.Normalize(s.min(), s.max())
    colors = [mcolors.to_hex(c) for c in plt.colormaps[cmap](norm(s.values))]
    return ['background-color: %s' % color for color in colors]

# Aplicar a formatação condicional ao DataFrame por coluna
styled_df = df_pivot.style.apply(lambda x: background_gradient(x, cmap='RdYlGn_r'), axis=0)
styled_df = styled_df.format("{:.0f}")

with st.container(border=True):
    st.title(f"{filtro1} Senhas emitidas por Hora/Dia")
    st.dataframe(styled_df)

col1, col2 = st.columns(2, border=True)
with col1:
    st.title(f"{filtro1} Por usuário")
    result = df_filtrado.groupby('Nome').agg(
        Quantidade=('Tempo atendimento', 'size'),
        Media_Tempo_Atendimento=('Tempo atendimento', 'mean')
    ).reset_index()

    def hours_to_hms(hours):
        total_seconds = int(hours * 3600)
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f'{h:02}:{m:02}:{s:02}'

    result['Media_Tempo_Atendimento'] = result['Media_Tempo_Atendimento'].apply(hours_to_hms)

    st.dataframe(result, hide_index=True)

with col2:
    st.title(f"{filtro1} Atraso de Senhas")
    df_filtrado_atrasado = df_filtrado[df_filtrado['status'] == 'atrasado']
    agrupado_por_tipo = df_filtrado_atrasado.groupby('tipo').size().reset_index(name='quantidade')
    st.dataframe(agrupado_por_tipo, hide_index=True)

df['ano'] = pd.to_datetime(df['DtCriacao']).dt.year

with st.container(border=True):
    st.title('Indicador Anual Planejamento Estratégico')

    resultados = []
    for ano, grupo in df.groupby("ano"):
        total_registros = grupo.shape[0]
        num_atrasos = grupo[grupo["status"] == "atrasado"].shape[0]
        perc_atraso = (num_atrasos / total_registros) * 100
        tempo_medio_espera = grupo["Tempo espera"].mean()

        total_seconds = int(tempo_medio_espera * 3600)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        tempo_formatado = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        resultados.append({
            "Ano": ano,
            "Total Registros": total_registros,
            "Atrasados": num_atrasos,
            "Percentual Atraso (%)": round(perc_atraso, 2),
            "Tempo Sem formatar": total_seconds/60,
            "Tempo Médio de Espera": tempo_formatado,
        })

    # Convertendo para DataFrame para exibição
    df_resultados = pd.DataFrame(resultados)

    # Exibindo os resultados no Streamlit
    st.dataframe(df_resultados, hide_index=True)