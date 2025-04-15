import streamlit as st

st.set_page_config(layout="wide")


a1, a2, a3 = st.columns([1,2,1])

with a2:
    with st.container(border=True):

        st.markdown("""
                    <h2>🔍 Como funciona a metodologia de gestão cartorária baseada em indicadores</h2>

                    Ao longo dos últimos anos, implementamos no cartório um sistema estruturado de <strong>gestão por indicadores de desempenho</strong>, com foco em <strong>prazo, qualidade e satisfação do cliente</strong>. Essa abordagem se baseia em cinco pilares principais, que representam os pontos críticos da experiência do cliente:
          
                    """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("""
                    <h4>📁 1. Protocolo</h4>
                    Monitoramento do <em>percentual de protocolos com atraso</em>, calculado como:<br>
                    <b>(Protocolos com atraso / Total de protocolos emitidos) × 100</b><br><br>
                    """, unsafe_allow_html=True)    
                
            if st.button("Ver o Relatório de Atrasos", type='primary'):
                st.switch_page("pages/02_seg.py")


        st.markdown("""
                <h4>📄 2. Certidões</h4>
                Seguindo a mesma lógica do protocolo:<br>
                <b>(Certidões com atraso / Total de certidões emitidas)</b><br><br>

                <h4>📨 3. Ofícios</h4>
                Indicador semelhante para documentos enviados aos órgãos públicos:<br>
                <b>(Ofícios com atraso / Total de ofícios emitidos)</b><br><br>

                <h4>👥 4. Atendimento presencial</h4>
                Aqui, focamos no tempo de espera:<br>
                <b>(Senhas com espera superior a 30 minutos / Total de senhas atendidas)</b><br><br>

                <h4>📞 5. Atendimento telefônico</h4>
                Indicador voltado à evasão:<br>
                <b>(Chamadas desistidas / Total de chamadas recebidas)</b><br><br>

                <hr>

                <h3>📈 Monitoramento contínuo e ações preventivas</h3>

                Esses indicadores são avaliados mensalmente em reuniões de <strong>análise crítica</strong>, nas quais avaliamos a performance do mês anterior e definimos <strong>planos de ação</strong> sempre que os resultados não atingem os padrões esperados.

                O objetivo é manter todos os indicadores com <strong>índices de erro abaixo de 1%</strong>, o que representa um cartório operando com excelência.

                Para ir além da análise pós-falha, desenvolvemos <strong>relatórios visuais em tempo real</strong>, permitindo que as equipes tomem decisões antes que a falha aconteça.
                """, unsafe_allow_html=True)

        if st.button("Ver o Relatório em Tempo ReaL", type='primary'):
            st.switch_page("pages/03_tres.py")

        st.markdown("""
                <hr>
                        
                <h3>🔧 Evolução e foco na qualidade</h3>

                No início, o foco nos prazos gerou um efeito colateral: <em>queda na qualidade</em>, com aumento de retrabalhos. Para resolver isso, criamos <strong>relatórios de retrabalho</strong>, onde cada colaborador visualiza seus próprios erros — promovendo aprendizado e melhoria contínua.

                <hr>

                <h3>🏆 Resultado prático</h3>

                ✅ Monitoramento constante<br>
                ✅ Ações corretivas ágeis<br>
                ✅ Evolução mês a mês documentada<br>
                ✅ Equipe engajada em resultados<br>
                ✅ Clientes cada vez mais satisfeitos

                <hr>

                <h3>📲 Quer aplicar no seu cartório?</h3>

                Nesta página, você verá uma amostra dos <strong>relatórios desenvolvidos</strong>.<br>
                Se quiser implementar essa metodologia no seu cartório, <strong>entre em contato comigo</strong> clicando no botão abaixo:

                <br><br>
                <a href="https://wa.me/5562999336111" target="_blank" style="background-color:#25D366; color:white; padding:10px 20px; border-radius:5px; text-decoration:none; font-weight:bold;">
                💬 Falar no WhatsApp
                </a>
                """, unsafe_allow_html=True)