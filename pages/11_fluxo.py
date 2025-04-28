import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"] == False:
    st.switch_page("main.py")

if st.button("Clique Aqui Para Voltar", type='primary'):
    if st.session_state["logged_in"] == False:
        st.switch_page("main.py")
    else:
        st.switch_page("pages/10_apresent.py")

# Função para aplicar a escala de cores por coluna
def color_scale(val, min_val, max_val):
    cmap = sns.color_palette("RdYlGn_r", as_cmap=True)  # Inverte a paleta de cores
    norm = plt.Normalize(min_val, max_val)
    color = cmap(norm(val))
    r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
    brightness = (r*299 + g*587 + b*114) / 1000  # Calcular a luminosidade percebida
    text_color = 'white' if brightness < 128 else 'black'
    return f'background-color: rgb({r}, {g}, {b}); color: {text_color}'

# Função para adicionar ícones de posição
def add_icons(column):
    sorted_col = column.astype(float).sort_values(ascending=True)
    icons = {sorted_col.index[0]: '🥇', sorted_col.index[1]: '🥈', sorted_col.index[2]: '🥉'}
    return [f'{icons.get(idx, "")} {val}' for idx, val in column.items()]

# Aplica a estilização por coluna
def apply_columnwise_color_scale(df):
    styled_df = df.copy()
    for column in df.columns:
        min_val = df[column].min()
        max_val = df[column].max()
        styled_df[column] = df[column].apply(lambda val: color_scale(val, min_val, max_val))
    return styled_df

df = pd.read_excel('dados/previsao.xlsx', sheet_name='fluxo', index_col='ano_mes')

st.title('Fluxograma Protocolos de Registro')
image_prot = 'imagens/fluxograma_protocolo.jpg'
st.image(image_prot)

df_protocolo_styled = apply_columnwise_color_scale(df)
df_protocolo_formatted = df.map(lambda x: f"{x:.2f}")
df_protocolo_icons = df_protocolo_formatted.apply(add_icons, axis=0)
df_protocolo_styled = df_protocolo_icons.style.apply(lambda x: apply_columnwise_color_scale(df), axis=None)
st.dataframe(df_protocolo_styled, width=2000, height=470)