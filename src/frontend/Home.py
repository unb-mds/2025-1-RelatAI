import streamlit as st
import requests
import json

# --- Inicializar estado da sessão para notificações ---
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "message": "Alerta: Nova análise de 'Projeções Demográficas' disponível para revisão.", "read": False, "type": "info"},
        {"id": 2, "message": "Sucesso: 'Boletim Econômico Mensal' foi publicado.", "read": False, "type": "success"},
        {"id": 3, "message": "Aviso: Manutenção programada do sistema para 25/05 às 02:00.", "read": True, "type": "warning"},
    ]
if 'last_notification_id' not in st.session_state:
    max_id = 0
    if st.session_state.notifications:
        max_id = max(n['id'] for n in st.session_state.notifications)
    st.session_state.last_notification_id = max_id


def count_unread_notifications():
    return sum(1 for n in st.session_state.notifications if not n['read'])

def get_next_notification_id():
    st.session_state.last_notification_id += 1
    return st.session_state.last_notification_id

# --- Funções para buscar dados da API ---
API_BASE_URL = "http://127.0.0.1:8000"

def fetch_api_data(endpoint: str):
    """Busca dados de um endpoint da API e retorna o JSON, ou None em caso de erro."""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint.lstrip('/')}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar dados de '{endpoint}': {e}")
        return None
    except json.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON da resposta de '{endpoint}'.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao buscar dados de '{endpoint}': {e}")
        return None

def fetch_and_add_predictions_to_notifications():
    """Busca previsões da API e as adiciona como notificações."""
    predictions_data = fetch_api_data("previsao")
    if predictions_data:
        new_notifications_count = 0
        for key, data in predictions_data.items():
            if isinstance(data, dict) and "descricao" in data:
                message = f"Previsão {key.upper()}: {data.get('descricao', 'Dados de previsão recebidos.')}"
                notif_type = "info"
                if "tendencia" in data:
                    if "baixa" in data["tendencia"].lower():
                        notif_type = "warning"
                
                if not any(n['message'] == message for n in st.session_state.notifications):
                    st.session_state.notifications.insert(0, {
                        "id": get_next_notification_id(),
                        "message": message,
                        "read": False,
                        "type": notif_type
                    })
                    new_notifications_count +=1
        if new_notifications_count > 0:
            st.success(f"{new_notifications_count} novas previsões adicionadas como alertas!")
            st.rerun()
        else:
            st.info("Nenhuma nova previsão para adicionar ou já existem nos alertas.")
    else:
        st.warning("Não foi possível buscar novas previsões no momento.")


def fetch_and_add_general_alerts_to_notifications():
    """Busca alertas gerais da API e os adiciona como notificações."""
    alerts_api_data = fetch_api_data("alertas")
    if alerts_api_data and "alertas" in alerts_api_data and isinstance(alerts_api_data["alertas"], list):
        new_notifications_count = 0
        for alert_message in alerts_api_data["alertas"]:
            if not any(n['message'] == str(alert_message) for n in st.session_state.notifications):
                st.session_state.notifications.insert(0, {
                    "id": get_next_notification_id(),
                    "message": str(alert_message),
                    "read": False,
                    "type": "warning" 
                })
                new_notifications_count += 1
        if new_notifications_count > 0:
            st.success(f"{new_notifications_count} novos alertas gerais adicionados!")
            st.rerun()
        else:
            st.info("Nenhum novo alerta geral para adicionar ou já existem nos alertas.")
    elif alerts_api_data:
         st.info("Nenhum novo alerta geral encontrado no momento (formato de resposta inesperado).")
    else:
        st.warning("Não foi possível buscar novos alertas gerais no momento.")


# --- Configuração Principal da Página ---
st.set_page_config(
    page_title="RelatAI | IPEA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Cabeçalho Personalizado: Título da App e Botão de Notificações ---
col_app_title, col_notifications_btn_spacer, col_notifications_btn_actual = st.columns([0.75, 0.1, 0.15]) # Ajuste as proporções conforme necessário

with col_app_title:
    app_title_html = "<h1 style='color: #004080; margin-bottom:0px; font-weight:bold;'>RelatAI <span style='font-weight:normal; color: #0059b3'>| IPEA</span></h1>"
    st.markdown(app_title_html, unsafe_allow_html=True)

with col_notifications_btn_actual: # Renomeado de col_notifications_btn para evitar conflito se a var antiga ainda existir
    unread_count = count_unread_notifications()
    notif_icon_char = "🔔"
    
    button_label = f"{notif_icon_char} Alertas"
    if unread_count > 0:
        button_label = f"{notif_icon_char} Alertas ({unread_count})"

    with st.popover(button_label, use_container_width=True, help="Clique para ver os alertas"): # use_container_width=True para preencher a coluna
        st.subheader("Notificações")
        # Removido o botão "Atualizar Alertas e Previsões" daqui
        st.divider()

        if not st.session_state.notifications:
            st.info("Nenhum alerta no momento.")
        else:
            unread_notifications = [n for n in st.session_state.notifications if not n['read']]
            read_notifications = [n for n in st.session_state.notifications if n['read']]
            
            if unread_notifications:
                for notif in unread_notifications:
                    original_index = -1
                    for i, item in enumerate(st.session_state.notifications): 
                        if item['id'] == notif['id']:
                            original_index = i
                            break
                    
                    icon_map = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌"}
                    msg_icon = icon_map.get(notif.get("type", "info"), "ℹ️")
                    
                    notif_container = st.container(border=True)
                    with notif_container:
                        col_msg, col_action = st.columns([0.85, 0.15])
                        with col_msg:
                            st.markdown(f"**{msg_icon} {notif['message']}**")
                        with col_action:
                            if original_index != -1 and st.button("Lida", key=f"read_{notif['id']}", type="primary", use_container_width=True, help="Marcar como lida"):
                                st.session_state.notifications[original_index]['read'] = True
                                st.rerun()
            
            if read_notifications:
                for notif in read_notifications:
                    icon_map = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌"}
                    msg_icon = icon_map.get(notif.get("type", "info"), "ℹ️")
                    
                    notif_container = st.container(border=True) 
                    with notif_container:
                        st.markdown(f"<span style='color:grey;'>{msg_icon} {notif['message']}</span>", unsafe_allow_html=True)
            
            st.divider()
            if any(n['read'] for n in st.session_state.notifications):
                if st.button("Limpar alertas lidos", use_container_width=True, key="clear_read_notifications_home_main_btn"):
                    st.session_state.notifications = [n for n in st.session_state.notifications if not n['read']]
                    st.rerun()

# Linha divisória após o cabeçalho personalizado
st.markdown("---")


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
    - Para criar um novo estudo ou relatório, navegue até a página Nova Análise Estatística.
    - Para acessar documentos existentes, visite a página Consultar Publicações.

    Utilize o menu na barra lateral para navegar pelas seções disponíveis.
    """
)

st.sidebar.info("Selecione uma página na barra lateral.")

st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")

# Conteúdo principal da página inicial
# Adiciona as três seções principais: Macroeconômico, Regional e Social
st.markdown("---")  # Linha divisória
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #e7f0f7; padding: 20px; border-radius: 10px; height: 100%;">
        <h3 style="color: #004080; font-weight: bold;">Macroeconômico</h3>
        <p style="color: #004080;">Dados econômicos e financeiros do Brasil em séries anuais, mensais e diárias na mesma unidade monetária.</p>
    </div>
    """, unsafe_allow_html=True)
    # Adicionar links ou botões para navegação futura, se necessário
    # st.page_link("pages/macro_data.py", label="Acessar Dados Macroeconômicos")

with col2:
    st.markdown("""
    <div style="background-color: #e7f7e7; padding: 20px; border-radius: 10px; height: 100%;">
        <h3 style="color: #006400; font-weight: bold;">Regional</h3>
        <p style="color: #006400;">Dados econômicos, demográficos e geográficos para estados, municípios (e suas áreas mínimas comparáveis), regiões administrativas e bacias hidrográficas brasileiras.</p>
    </div>
    """, unsafe_allow_html=True)
    # st.page_link("pages/regional_data.py", label="Acessar Dados Regionais")

with col3:
    st.markdown("""
    <div style="background-color: #f7e7e7; padding: 20px; border-radius: 10px; height: 100%;">
        <h3 style="color: #c00000; font-weight: bold;">Social</h3>
        <p style="color: #c00000;">Dados e indicadores sobre distribuição de renda, pobreza, educação, saúde, assistência social. Desagregações de gênero, cor e outras, acesse os links no comentário.</p>
    </div>
    """, unsafe_allow_html=True)
    # st.page_link("pages/social_data.py", label="Acessar Dados Sociais")

st.markdown("---") # Linha divisória
st.markdown("""
Os dados disponibilizados no Ipeadata são de uso público. É permitida sua reprodução e utilização em tabelas, gráficos, mapas e textos, desde que o Ipeadata seja citado.

Para consulta aos dados do Ipeadata, use a **API Ipeadata**, as bibliotecas em **R (ipeadatar)**, **Python (ipeadatapy)** ou **Excel (versão 1.15.5)**.
""")
st.markdown("### Séries mais acessadas")
# Placeholder para as séries mais acessadas - pode ser preenchido dinamicamente no futuro
col1_series, col2_series, col3_series = st.columns(3)
with col1_series:
    st.markdown("**Ipeadata Macro:**")
    st.markdown("- Taxa de juros - CDI/Over")
    st.markdown("- IPCA")
    st.markdown("- IGP-M")
    st.markdown("- INPC - geral - índice")
    st.markdown("- Taxa de câmbio - R$/US&#36;") # Using HTML entity for dollar sign
with col2_series:
    st.markdown("**Ipeadata Regional:**")
    st.markdown("- População")
    st.markdown("- PIB Estadual")
    st.markdown("- Empregados - admissões")
    st.markdown("- Empregados - demissões")
    st.markdown("- Exportações (FOB)")
with col3_series:
    st.markdown("**Ipeadata Social:**")
    st.markdown("- Índice de Gini")
    st.markdown("- IDHM")
    st.markdown("- Taxa de desemprego (desocupação)")
    st.markdown("- Taxa de pobreza nacional")
    st.markdown("- Bolsa Família - valores mensais")

if __name__ == '__main__':
    pass
