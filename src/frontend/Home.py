import streamlit as st

st.set_page_config(
    page_title="Instituto de Pesquisa e Estatística Aplicada",
    page_icon="🏛️",
    layout="wide"
)

st.title("Instituto de Pesquisa e Estatística Aplicada")
st.subheader("Dados e Análises para o Desenvolvimento Nacional")

st.markdown(
    """
    Bem-vindo à plataforma digital do Instituto de Pesquisa e Estatística Aplicada (IPEA).
    Nossa missão é fornecer dados, análises e estudos estatísticos de alta qualidade
    para subsidiar a formulação de políticas públicas e promover o debate informado
    na sociedade.

    **Nossos Serviços:**
    - **Geração de Análises e Relatórios:** Utilize nossa ferramenta para elaborar documentos estatísticos baseados em modelos padronizados.
    - **Consulta a Publicações:** Acesse nosso acervo de estudos, boletins e relatórios já publicados.
    - **Bases de Dados:** (Funcionalidade futura) Explore e baixe microdados de nossas pesquisas.

    **Como Utilizar a Plataforma:**
    - Para criar um novo estudo ou relatório, navegue até **Nova Análise Estatística**.
    - Para acessar documentos existentes, visite **Consultar Publicações**.

    Utilize o menu na barra lateral para navegar pelas seções disponíveis.
    """
)

st.sidebar.info("Selecione uma seção para começar.")

# Adicionar um rodapé institucional simples
st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")

if __name__ == '__main__':
    pass
