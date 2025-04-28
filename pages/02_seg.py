import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.button("Clique Aqui Para Voltar", type='primary'):
    if st.session_state["logged_in"] == False:
        st.switch_page("main.py")
    else:
        st.switch_page("pages/10_apresent.py")

with st.container(border=True):
    if st.session_state["logged_in"] == False:
        st.markdown("""
        ### 🧾 Vantagens do Relatório de Indicador do Registro

        📈 **Histórico completo da performance**, mostrando mês a mês a quantidade de protocolos feitos, os atrasos e o tempo médio até o registro ou impugnação, permitindo visualizar claramente a evolução e identificar tendências.

        📌 **Identificação precisa das naturezas com maior atraso**, possibilitando ações corretivas direcionadas, como revisão de fluxos, reforço de equipe ou priorização de certos tipos de serviço.

        🟢 **Incentivo à melhoria contínua**, com dados que demonstram se o percentual de atraso está diminuindo e se os dias para registro estão dentro de uma média aceitável, fortalecendo a cultura de excelência.

        📊 **Comparativo visual entre prazos cumpridos e vencidos**, através de gráficos intuitivos que facilitam a tomada de decisão estratégica e a comunicação dos resultados à equipe.

        🔍 **Acesso detalhado aos protocolos com atraso**, com possibilidade de identificar exatamente quais foram os registros fora do prazo — preservando a privacidade no relatório geral, mas disponível para análise interna quando necessário.

        📂 **Base sólida para reuniões de desempenho**, auditorias e planejamento, com números confiáveis que ajudam na definição de metas realistas e no reconhecimento de boas práticas.
        """)

@st.cache_data
def carregar_dados():
    return pd.read_excel('dados/previsao.xlsx', sheet_name='protocolo')
df = carregar_dados()

protocolos = df.shape[0]

a1, a2 = st.columns([5.1,1], border=True) 

with a1:
    st.markdown(f"### Indicador Registro ({protocolos} Protocolos Feitos)")

df_filtrado = df

with a2:
    filtro1 = st.selectbox("Selecionar Ano/Mês:", sorted(df['mes_ano'].unique(),reverse=True), index=None, placeholder="2024-12")

    if filtro1 is None:
        filtro1 = '2024-12'
        df_filtrado1 = df_filtrado[df_filtrado['mes_ano'] == filtro1]
    else:
        df_filtrado1 = df_filtrado[df_filtrado['mes_ano'] == filtro1]

df_filt = df[df['mes_ano'] != datetime.now().strftime('%Y-%m')]
df_grouped = df_filt.groupby(['mes_ano']).agg(
                                    Qtd_Protocolo=('dias_uteis', 'count'),
                                    Media_Dias=('dias_uteis', 'mean'),
                                    Total_Atrasados=('status', lambda x: (x == 'atrasado').sum())                                        
                                    ).reset_index()
df_grouped['Percentual_Atrasados'] = ((df_grouped['Total_Atrasados'] / df_grouped['Qtd_Protocolo']) * 100).round(2)
df_grouped['Media_Dias'] = (df_grouped['Media_Dias']).round(2)
df_sorted = df_grouped.sort_values(by='mes_ano', ascending=False)

def add_icon(val, col):
    rank = df_sorted[col].rank(method='min', ascending=(col == 'Media_Dias' or col == 'Percentual_Atrasados')).loc[df_sorted[df_sorted[col] == val].index[0]]
    if rank == 1:
        return '🏆'  # Troféu para o 1º lugar
    elif rank == 2:
        return '🥈'  # Medalha de prata para o 2º lugar
    elif rank == 3:
        return '🥉'  # Medalha de bronze para o 3º lugar
    else:
        return ''

# Selecionar apenas as colunas desejadas
df_filtered = df_sorted[['mes_ano', 'Qtd_Protocolo', 'Total_Atrasados', 'Percentual_Atrasados', 'Media_Dias']]

# Renomear as colunas
df_filtered = df_filtered.rename(columns={
    'mes_ano': 'Ano/Mês',
    'Qtd_Protocolo': 'Protocolos Feitos',
    'Total_Atrasados': 'Prot. Atrasados',
    'Percentual_Atrasados': 'Perc. Atraso (%)',
    'Media_Dias': 'Dias para Registro'
})

styled_df = df_filtered.style \
    .background_gradient(subset=['Protocolos Feitos'], cmap='RdYlGn') \
    .background_gradient(subset=['Prot. Atrasados', 'Dias para Registro', 'Perc. Atraso (%)'], cmap='RdYlGn_r') \
    .format({
        'Protocolos Feitos': lambda x: f"{add_icon(x, 'Qtd_Protocolo')} {x}",
        'Dias para Registro': lambda x: f"{add_icon(x, 'Media_Dias')} {x:.2f}",
        'Perc. Atraso (%)': lambda x: f"{add_icon(x, 'Percentual_Atrasados')} {x:.2f}"
    })

col11, col12, col13, col14, col15 = st.columns([2,1,1,1,1], vertical_alignment='center', border=True)
with col11:
    st.title(f'{filtro1} Métricas')
with col12:
    st.metric("**Protocolos Feitos**", df_filtrado1.shape[0])
with col13:
    st.metric("**Protocolos Atrasados**", df_filtrado1[df_filtrado1['status'] == 'atrasado'].shape[0])
with col14:
    num_atrasos = df_filtrado1[df_filtrado1['status'] == 'atrasado'].shape[0]
    total_registros = df_filtrado1.shape[0]
    perc_atraso = (num_atrasos / total_registros) * 100
    st.metric("**Percentual Atraso**", f"{perc_atraso:.2f}%")
with col15:
    tempo_medio_espera = df_filtrado1['dias_uteis'].mean()
    st.metric("**Dias para Registro**", f"{tempo_medio_espera:.2f}")

col1, col2 = st.columns(2, border=True)
with col1:
    st.title('Histórico Mensal')
    st.dataframe(styled_df, hide_index=True, height=300)
with col2:
    total_servicos = df_filtrado1.groupby('tipo_servico').size().reset_index(name='Total')
    df_atrasado = df_filtrado1[df_filtrado1['status'] == 'atrasado']
    atrasados_servicos = df_atrasado.groupby('tipo_servico').size().reset_index(name='Atrasados')
    resultado_agrupado = pd.merge(total_servicos, atrasados_servicos, on='tipo_servico', how='left')
    resultado_agrupado['Atrasados'] = resultado_agrupado['Atrasados'].fillna(0).astype(int)
    resultado_agrupado = resultado_agrupado.sort_values(by='Atrasados', ascending=False)
    df_ra = resultado_agrupado[['tipo_servico', 'Atrasados', 'Total']]
    df_ra = df_ra.copy()
    df_ra.loc[:, 'Percentual'] = ((df_ra['Atrasados']/df_ra['Total'])*100).round(2)
    st.title(f'{filtro1} Naturezas Atrasadas')
    st.dataframe(df_ra, hide_index=True, height=300)

with st.container(border=True):
    st.title('Histórico Gráfico No Prazo x Vencido')
    df_filtered['no_prazo'] = df_filtered['Protocolos Feitos'] - df_filtered['Prot. Atrasados']

    unique_ano_mes = sorted(df_filtered['Ano/Mês'].dropna().unique(), reverse=True)

    df_long = df_filtered.melt(id_vars=['Ano/Mês'], value_vars=['Prot. Atrasados', 'no_prazo'], var_name='tipo', value_name='contagem')

    # Criando o gráfico de barras agrupadas
    fig_filtrado = px.bar(
        df_long,
        x='Ano/Mês',
        y='contagem',
        color='tipo',
        barmode='group',
        text='contagem'
    )

    fig_filtrado.update_layout(xaxis=dict(tickmode='array', tickvals=df_long['Ano/Mês'], ticktext=[str(val) for val in df_long['Ano/Mês']]))

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig_filtrado)