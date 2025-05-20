import streamlit as st
# from streamlit_option_menu import option_menu # Removido

# --- Inicializar estado da sessão para notificações (exemplo) ---
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "message": "Alerta: Nova análise de 'Projeções Demográficas' disponível para revisão.", "read": False, "type": "info"},
        {"id": 2, "message": "Sucesso: 'Boletim Econômico Mensal' foi publicado.", "read": False, "type": "success"},
        {"id": 3, "message": "Aviso: Manutenção programada do sistema para 25/05 às 02:00.", "read": True, "type": "warning"},
    ]

def count_unread_notifications():
    return sum(1 for n in st.session_state.notifications if not n['read'])

# --- Configuração Principal da Página ---
st.set_page_config(
    page_title="Instituto de Pesquisa e Estatística Aplicada",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto" # Ou "expanded" se preferir a barra lateral visível por padrão
)

# --- Cabeçalho Personalizado: Apenas Botão de Notificações ---
# Usaremos colunas para alinhar o botão à direita
col_title_spacer, col_notifications_btn = st.columns([0.85, 0.15]) # Ajuste as proporções conforme necessário

with col_notifications_btn:
    unread_count = count_unread_notifications()
    notif_icon_char = "🔔"
    
    button_label = f"{notif_icon_char} Alertas"
    if unread_count > 0:
        button_label = f"{notif_icon_char} Alertas ({unread_count})"

    with st.popover("Alertas do Sistema", use_container_width=False, help="Clique para ver os alertas"):
        st.subheader("Notificações")
        if not st.session_state.notifications:
            st.info("Nenhum alerta no momento.")
        else:
            # Exibe notificações não lidas primeiro, depois as lidas
            unread_notifications = [n for n in st.session_state.notifications if not n['read']]
            read_notifications = [n for n in st.session_state.notifications if n['read']]
            
            # Para manter a ordem original ao marcar como lida, iteramos sobre a lista original
            # e aplicamos estilo. A ordenação para exibição é feita visualmente.
            
            # Exibir não lidas
            if unread_notifications:
                # st.markdown("##### Não Lidas") # Opcional: título para não lidas
                for notif in unread_notifications:
                    original_index = st.session_state.notifications.index(notif)
                    icon_map = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌"}
                    msg_icon = icon_map.get(notif.get("type", "info"), "ℹ️")
                    
                    notif_container = st.container(border=True)
                    with notif_container:
                        col_msg, col_action = st.columns([0.85, 0.15])
                        with col_msg:
                            st.markdown(f"**{msg_icon} {notif['message']}**")
                        with col_action:
                            if st.button("Lida", key=f"read_{notif['id']}", type="primary", use_container_width=True, help="Marcar como lida"):
                                st.session_state.notifications[original_index]['read'] = True
                                st.rerun()
            
            # Exibir lidas
            if read_notifications:
                # st.markdown("##### Lidas") # Opcional: título para lidas
                for notif in read_notifications:
                    icon_map = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌"}
                    msg_icon = icon_map.get(notif.get("type", "info"), "ℹ️")
                    
                    notif_container = st.container(border=True) # Pode remover a borda para lidas se preferir
                    with notif_container:
                        st.markdown(f"<span style='color:grey;'>{msg_icon} {notif['message']}</span>", unsafe_allow_html=True)
            
            st.divider()
            if any(n['read'] for n in st.session_state.notifications):
                if st.button("Limpar alertas lidos", use_container_width=True):
                    st.session_state.notifications = [n for n in st.session_state.notifications if not n['read']]
                    st.rerun()

# --- Conteúdo Original da Página Home (abaixo do cabeçalho) ---
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

st.sidebar.info("Selecione uma página na barra lateral.") # Mensagem para a barra lateral padrão

# Adicionar um rodapé institucional simples
st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")

if __name__ == '__main__':
    pass
