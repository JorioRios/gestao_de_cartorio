import streamlit as st

st.set_page_config(layout="wide")

pg = st.navigation([
    st.Page("pages/sobre.py", title="Detalhes", icon="👨‍💼"),
    st.Page("pages/projetos.py", title="Projetos", icon="📊")
])
pg.run()

telefone = "5562999336111"  # Coloque o número com código do país (ex: 55 para Brasil)
mensagem = "Olá! Tenho interesse em saber mais."

# Codifica a mensagem para a URL
mensagem_codificada = mensagem.replace(" ", "%20")
url_whatsapp = f"https://wa.me/{telefone}?text={mensagem_codificada}"

# Botão estilizado com HTML que não é bloqueado
st.sidebar.markdown(
    f"""
    <a href="{url_whatsapp}" target="_blank">
        <button style="
            background-color:#25D366;
            color:white;
            padding:10px 20px;
            border:none;
            border-radius:8px;
            font-size:16px;
            width:100%;
            cursor:pointer;
        ">
            💬 Falar no WhatsApp
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

# Sidebar - Botão Email
st.sidebar.markdown(
    """
    <div style='text-align: center; font-weight: bold;'>
        (62) 99933-6111
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div style='text-align: center; font-weight: bold;'>
        jorio.melo@gmail.com
    </div>
    """,
    unsafe_allow_html=True
)
