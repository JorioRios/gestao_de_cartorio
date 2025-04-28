import streamlit as st
import pandas as pd
import random

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"] == True:
    a1, a2, a3, a4, a5 = st.columns(5)
    with a1:
        if st.button("Gerar Dados Aleatórios", use_container_width=True):
            st.rerun() 
else:
    st.switch_page("main.py")

def grafico(valor):

    if valor >= 97:
        cor = 'darkgreen'
    elif 93 <= valor < 97:
        cor = 'green'
    elif 80 <= valor < 93:
        cor = "darkgoldenrod"
    elif 70 <= valor < 80:
        cor = 'red'
    else:
        cor = 'darkred'

    st.markdown(f"""
        <div style="background-color:black;padding:10px;border-radius:10px">
            <div style="width:{valor}%;background-color:{cor};padding:5px 0;border-radius:5px;text-align:center;color:white;font-weight:bold">
                {valor:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    return

a1, a2, a3, a4, a5 = st.columns(5, border=True)

prot_feitos = int(random.uniform(800,1000))
prot_atrasados = int(random.uniform(0,100))

with a1:
    st.subheader('Indicador Registro', divider="gray")
    grafico(round(((1-prot_atrasados/prot_feitos)*100), 2))
    st.write("")
    with st.popover('Ver Detalhes', use_container_width=True):
        st.metric('Dias para Registro', value=round(random.uniform(2,10), 2), border=True)
        st.metric('Protocolos Feitos', value=prot_feitos, border=True)
        st.metric('Protocolos Atrasados', value=prot_atrasados, border=True)

    if st.button("Ver Indicador de Registro", type='primary', use_container_width=True):
        st.switch_page("pages/02_seg.py")   
    if st.button("Previsão de Protocolos", type='primary', use_container_width=True):
        st.switch_page("pages/03_tres.py")  
    if st.button("Fluxograma de Protocolos", type='primary', use_container_width=True):
        st.switch_page("pages/11_fluxo.py")
    if st.button("Rendimento de Protocolos", type='primary', use_container_width=True):
        st.switch_page("pages/12_rend.py") 

cert_feitos = int(random.uniform(1600,2000))
cert_atrasados = int(random.uniform(0,200))

with a2:
    st.subheader('Indicador Certidão', divider="gray")
    grafico(round(((1-cert_atrasados/cert_feitos)*100), 2))
    st.write("")
    st.metric('Horas para Emissão', value=round(random.uniform(1,10), 2), border=True)
    b1, b2 = st.columns(2)
    with b1:
        st.metric('Cert. Feitas', value=cert_feitos, border=True)
    with b2:
        st.metric('Cert. Atrasadas', value=cert_atrasados, border=True)
    if st.button("Ver Indicador de Certidão", use_container_width=True, disabled=True):
        pass  
    if st.button("Previsão de Certidões", type='primary', use_container_width=True):
        st.switch_page("pages/13_cert.py")  
    if st.button("Fluxograma de Certidões", use_container_width=True, disabled=True):
        pass 
    if st.button("Rendimento de Certidões", use_container_width=True, disabled=True):
        pass 

of_feitos = int(random.uniform(300,500))
of_atrasados = int(random.uniform(0,5))

with a3:
    st.subheader('Indicador Ofício', divider="gray")
    grafico(round(((1-of_atrasados/of_feitos)*100), 2))
    st.write("")
    with st.container(border=True):
        st.write(f'**Dias para Responder:** {round(random.uniform(2,5), 2)}')
        st.write(f'**Ofícios Feitos:** {of_feitos}')
        st.write(f'**Ofícios Atrasados:** {of_atrasados}')
    if st.button("Ver Indicador de Ofício", use_container_width=True, disabled=True):
        pass  
    if st.button("Previsão de Ofício", use_container_width=True, disabled=True):
        pass 
    if st.button("Fluxograma de Ofício", use_container_width=True, disabled=True):
        pass 
    if st.button("Rendimento de Ofício", use_container_width=True, disabled=True):
        pass 

at_feitos = int(random.uniform(3000,3500))
at_atrasados = int(random.uniform(0,500))

with a4:
    st.subheader('Indicador Senhas', divider="gray")
    grafico(round(((1-at_atrasados/at_feitos)*100), 2))
    st.write("")
    # Criar DataFrame com uma única linha
    df = pd.DataFrame({
        'Espera (min)': round(random.uniform(2, 5), 2),
        'Atendidos': [at_feitos],
        'Atrasados': [at_atrasados]
    })

    # Exibir o DataFrame no Streamlit
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.button("Ver Indicador de Senhas", type='primary', use_container_width=True):
        st.switch_page("pages/14_atend.py")  
    if st.button("Rendimento de Atendimento", use_container_width=True, disabled=True):
        pass 

tel_feitos = int(random.uniform(6000,7000))
tel_atrasados = int(tel_feitos*random.uniform(0,1))

with a5:
    st.subheader('Indicador Telefone', divider="gray")
    grafico(round(((1-tel_atrasados/tel_feitos)*100), 2))
    st.write("")
    # Criar DataFrame transposto
    df = pd.DataFrame({
        'Valor': [round(random.uniform(2, 5), 2), tel_feitos, tel_atrasados]
    }, index=['Tempo para Atender (minutos)', 'Ligação Recebida', 'Ligação não Atendida'])
    df = df.reset_index()
    df.columns = ['Descrição', 'Valor']
    # Exibir o DataFrame no Streamlit
    st.dataframe(df, use_container_width=True, hide_index=True)    
    if st.button("Ver Indicador de Telefone", use_container_width=True, disabled=True):
        pass