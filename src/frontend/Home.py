import streamlit as st
import requests
import json

# --- Inicializar estado da sessão para notificações ---
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {"id": 1, "message": "Sistema RelatAI inicializado com sucesso.", "read": False, "type": "success"},
        {"id": 2, "message": "Dados econômicos atualizados para análise.", "read": False, "type": "info"},
        {"id": 3, "message": "Bem-vindo ao sistema de relatórios inteligentes do IPEA.", "read": True, "type": "info"},
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

# --- Configuração Principal da Página ---
st.set_page_config(
    page_title="RelatAI | IPEA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Cabeçalho Personalizado ---
col_app_title, col_notifications_btn_spacer, col_notifications_btn_actual = st.columns([0.75, 0.1, 0.15])

with col_app_title:
    app_title_html = "<h1 style='color: #004080; margin-bottom:0px; font-weight:bold;'>RelatAI <span style='font-weight:normal; color: #0059b3'>| IPEA</span></h1>"
    st.markdown(app_title_html, unsafe_allow_html=True)

with col_notifications_btn_actual:
    unread_count = count_unread_notifications()
    notif_icon_char = "🔔"
    
    button_label = f"{notif_icon_char} Alertas"
    if unread_count > 0:
        button_label = f"{notif_icon_char} Alertas ({unread_count})"

    with st.popover(button_label, use_container_width=True, help="Clique para ver os alertas"):
        st.subheader("Notificações")
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

st.markdown("---")

# --- Conteúdo Principal ---
st.title("🏛️ Instituto de Pesquisa Econômica Aplicada")
st.subheader("Sistema Inteligente de Relatórios Econômicos")

# Introdução e Missão
st.markdown("""
### 🎯 Nossa Missão

O **RelatAI** é uma plataforma inteligente desenvolvida para democratizar o acesso aos dados econômicos do IPEA, 
transformando informações complexas em relatórios claros e insights acionáveis para tomada de decisão.

**Objetivos principais:**
- **Facilitar o acesso** aos indicadores econômicos brasileiros
- **Automatizar a geração** de relatórios analíticos
- **Fornecer insights** baseados em dados históricos e tendências
- **Democratizar informações** econômicas para diferentes públicos
""")

# Público-alvo
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👥 Público-Alvo
    
    **Gestores Públicos:**
    - Subsídio para formulação de políticas
    - Análises de impacto econômico
    - Monitoramento de indicadores
    
    **Pesquisadores e Acadêmicos:**
    - Dados para estudos econômicos
    - Análises históricas e tendências
    - Base para publicações científicas
    
    **Setor Privado:**
    - Inteligência de mercado
    - Planejamento estratégico
    - Análise de cenários econômicos
    """)

with col2:
    st.markdown("""
    ### 📊 Dados Disponíveis
    
    **Indicadores Macroeconômicos:**
    - IPCA (Inflação)
    - Taxa SELIC (Juros)
    - Câmbio (USD/BRL)
    - PIB (Produto Interno Bruto)
    - Dívida Pública
    - Taxa de Desemprego
    
    **Período de Cobertura:**
    - Dados históricos desde 2016
    - Atualizações regulares
    - Análises contextualizadas
    """)

st.markdown("---")

# Funcionalidades Disponíveis
st.markdown("### 🚀 Funcionalidades Disponíveis")

# Cards das funcionalidades
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
        <h4 style="color: #1f77b4; margin-bottom: 10px;">📊 Geração de Relatórios</h4>
        <p style="color: #333; margin-bottom: 15px;">Crie relatórios analíticos personalizados com contexto histórico, análise de tendências e insights de mercado.</p>
        <p style="color: #666; font-size: 14px;"><strong>Recursos:</strong><br>
        • Análise contextual<br>
        • Gráficos interativos<br>
        • Export em PDF/JSON</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #f0f8f0; padding: 20px; border-radius: 10px; border-left: 5px solid #2ca02c;">
        <h4 style="color: #2ca02c; margin-bottom: 10px;">📈 Indicadores Econômicos</h4>
        <p style="color: #333; margin-bottom: 15px;">Visualize dados em tempo real com análises automáticas e projeções baseadas em machine learning.</p>
        <p style="color: #666; font-size: 14px;"><strong>Recursos:</strong><br>
        • Dados em tempo real<br>
        • Projeções futuras<br>
        • Análises automáticas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #fff8e1; padding: 20px; border-radius: 10px; border-left: 5px solid #ff7f0e;">
        <h4 style="color: #ff7f0e; margin-bottom: 10px;">🔍 Sistema de Alertas</h4>
        <p style="color: #333; margin-bottom: 15px;">Receba notificações automáticas sobre mudanças significativas nos indicadores econômicos.</p>
        <p style="color: #666; font-size: 14px;"><strong>Recursos:</strong><br>
        • Alertas automáticos<br>
        • Monitoramento contínuo<br>
        • Notificações em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Como usar
st.markdown("### 🗺️ Como Usar a Plataforma")

st.markdown("""
**1. 📊 Gerar Relatórios:**
   - Acesse a página "Gerar Relatórios"
   - Selecione o indicador econômico desejado
   - Defina o período de análise
   - Escolha os tipos de análise (contexto histórico, tendências, impacto econômico)
   - Gere e baixe seu relatório personalizado

**2. 📈 Consultar Indicadores:**
   - Vá para "Indicadores Econômicos"
   - Visualize dados em tempo real
   - Analise projeções e tendências
   - Compare diferentes períodos
   - Gere previsões futuras com base em machine learning

**3. 🔔 Monitorar Alertas:**
   - Use o botão de alertas no canto superior direito
   - Acompanhe mudanças significativas nos dados
   - Marque notificações como lidas
""")

st.markdown("---")

# Sobre os dados
st.markdown("### 📋 Sobre os Dados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Fonte dos Dados:**
    - Instituto de Pesquisa Econômica Aplicada (IPEA)
    - Banco Central do Brasil (BCB)
    - Instituto Brasileiro de Geografia e Estatística (IBGE)
    
    **Qualidade e Confiabilidade:**
    - Dados oficiais do governo brasileiro
    - Atualizações regulares e automáticas
    - Validação e tratamento de inconsistências
    """)

with col2:
    st.markdown("""
    **Metodologia:**
    - Análises baseadas em séries históricas
    - Contexto de eventos econômicos relevantes
    - Machine learning para projeções
    
    **Transparência:**
    - Código aberto e metodologia documentada
    - Processo de coleta e tratamento transparente
    - Rastreabilidade completa dos dados
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px;">
    <p style="text-align: center; color: #666; margin-bottom: 10px;">
        <strong>RelatAI - Sistema Inteligente de Relatórios Econômicos</strong>
    </p>
    <p style="text-align: center; color: #666; font-size: 14px;">
        Desenvolvido para democratizar o acesso aos dados econômicos brasileiros<br>
        Utilize o menu lateral para navegar pelas funcionalidades disponíveis
    </p>
</div>
""", unsafe_allow_html=True)

