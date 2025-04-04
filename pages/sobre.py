import streamlit as st

with st.container(border=True):
    st.subheader("🧑‍💼 Sobre Mim", divider="rainbow")

    a1, a2 = st.columns([0.23,1])

    with a1:
        st.image("imagem/eu.jpeg", use_container_width=True)

    with a2:
        st.markdown("""
        Sou Engenheiro Eletricista formado pela UNESP, com 9 anos de experiência profissional e atuação como **gestor de qualidade em um cartório de registro de imóveis e tabelionato**.

        Desenvolvi uma solução de **dashboards cartorários automatizados**, com leitura direta do banco de dados e geração de **relatórios em tempo real**, facilitando a gestão de indicadores, processos e metas de qualidade.

        Meu foco é transformar dados em decisões estratégicas, trazendo **eficiência, controle e padronização** para o ambiente cartorário.  
                    
        Além disso, conheço profundamente os requisitos da **ISO 9001**, aplicando ferramentas como **GUT, FOFA e 5W2H** na melhoria contínua dos processos.

        Se você busca organização, agilidade e relatórios profissionais para o seu cartório, essa solução é para você.
        """)

with st.container(border=True):

    st.subheader("🎯 Resultados Obtidos", divider="rainbow")

    a1, a2 = st.columns(2)

    with a1:
        with st.popover('**Melhora na satisfação do cliente**', use_container_width=True):
            st.image("imagem/google.jpg", use_container_width=True)

    a1, a2 = st.columns(2)

    with a1:
        with st.popover('Diminuição do tempo de espera', use_container_width=True):
            st.image("imagem/tempo_espera.jpg", use_container_width=True)

        with st.popover('Diminuição de desistência no telefone', use_container_width=True):
            st.image("imagem/telefone.jpg", use_container_width=True)

    with a2:
        with st.popover('Diminuição no tempo para realizar registro', use_container_width=True):
            st.image("imagem/registro.jpg", use_container_width=True)

        with st.popover('Diminuição no tempo para emitir certidão', use_container_width=True):
            st.image("imagem/certidao.jpg", use_container_width=True)