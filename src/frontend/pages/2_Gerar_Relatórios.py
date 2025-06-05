import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nova Análise Estatística - IPEA", page_icon="📊", layout="wide")

st.title("Nova Análise Estatística")
st.markdown("Elabore novos estudos, relatórios e boletins estatísticos.")

document_models = {
    "Boletim Econômico Mensal": "boletim_economico",
    "Análise de Indicadores Sociais Regionais": "analise_social_regional",
    "Relatório de Projeções Demográficas": "projecoes_demograficas",
    "Sumário Executivo de Pesquisa de Campo": "sumario_pesquisa"
}

model_structures = {
    "boletim_economico": {
        "Título do Boletim": {"type": "text_input", "value": "Boletim Econômico - Mês/Ano", "ai_placeholder": "Assistente pode sugerir formatação de título."},
        "Introdução e Contexto": {"type": "text_area", "value": "", "height": 100, "ai_placeholder": "Assistente pode auxiliar na redação da introdução."},
        "Análise de Indicadores Chave": {"type": "text_area", "value": "", "height": 200, "ai_placeholder": "Assistente pode ajudar a estruturar a análise dos indicadores."},
        "Considerações Finais": {"type": "text_area", "value": "", "height": 150, "ai_placeholder": "Assistente pode auxiliar na redação das considerações."}
    },
    "analise_social_regional": {
        "Título da Análise": {"type": "text_input", "value": "Análise de Indicadores Sociais - Região X", "ai_placeholder": "Assistente pode sugerir formatação de título."},
        "Objetivo da Análise": {"type": "text_area", "value": "", "height": 100, "ai_placeholder": "Assistente pode auxiliar na definição do objetivo."},
        "Metodologia Aplicada": {"type": "text_area", "value": "", "height": 150, "ai_placeholder": "Assistente pode ajudar a descrever a metodologia."},
        "Resultados e Discussão": {"type": "text_area", "value": "", "height": 250, "ai_placeholder": "Assistente pode ajudar a estruturar resultados."},
        "Conclusões e Recomendações": {"type": "text_area", "value": "", "height": 150, "ai_placeholder": "Assistente pode auxiliar nas conclusões."}
    },
}

if 'current_analysis_data' not in st.session_state:
    st.session_state.current_analysis_data = {}
if 'selected_model_key' not in st.session_state:
    st.session_state.selected_model_key = None

st.subheader("1. Selecione o Modelo do Documento")
selected_model_name = st.selectbox(
    "Tipo de Documento Estatístico:",
    options=list(document_models.keys()),
    key="model_selector_nova_analise",
    index=list(document_models.keys()).index(st.session_state.get('selected_model_name_display', list(document_models.keys())[0]))
)

if selected_model_name:
    st.session_state.selected_model_name_display = selected_model_name
    new_model_key = document_models[selected_model_name]

    if st.session_state.selected_model_key != new_model_key:
        st.session_state.selected_model_key = new_model_key
        st.session_state.current_analysis_data = {}
        if new_model_key in model_structures:
            for section, details in model_structures[new_model_key].items():
                section_key_form = f"{new_model_key}_{section.replace(' ', '_').lower()}"
                st.session_state.current_analysis_data[section_key_form] = details.get("value", "")

current_model_key = st.session_state.selected_model_key

if not current_model_key or current_model_key not in model_structures:
    st.warning("Por favor, selecione um modelo de documento para prosseguir.")
    st.stop()

current_model_structure = model_structures[current_model_key]
st.subheader(f"2. Elabore as Seções: {selected_model_name}")

def get_ai_assistance_placeholder(placeholder_text):
    st.info(f"Assistente de Redação (Placeholder): {placeholder_text}")
    return f"Texto de exemplo: {placeholder_text} O assistente de IA pode ajudar a refinar ou expandir este conteúdo."

# Loop para criar os campos de entrada e botões de assistência de IA (fora do formulário principal)
for section, details in current_model_structure.items():
    section_key_form = f"{current_model_key}_{section.replace(' ', '_').lower()}"
    st.markdown(f"#### {section}")
    
    current_value_for_field = st.session_state.current_analysis_data.get(section_key_form, details.get("value", ""))

    if details["type"] == "text_area":
        new_value_from_field = st.text_area(
            label=f"Conteúdo para {section}:", # Label visível
            value=current_value_for_field,
            height=details.get("height", 150),
            key=f"field_{section_key_form}" # Chave única para o widget
        )
    elif details["type"] == "text_input":
        new_value_from_field = st.text_input(
            label=f"Conteúdo para {section}:", # Label visível
            value=current_value_for_field,
            key=f"field_{section_key_form}" # Chave única
        )
    else:
        new_value_from_field = current_value_for_field

    # Atualiza o session_state com o valor do campo em cada execução do script
    st.session_state.current_analysis_data[section_key_form] = new_value_from_field
    
    if details.get("ai_placeholder"):
        # Este botão está agora FORA de qualquer st.form
        if st.button(f"Assistência de Redação para {section}", key=f"ai_btn_{section_key_form}"):
            with st.spinner("Consultando assistente..."):
                current_text_for_ai = st.session_state.current_analysis_data.get(section_key_form, "")
                suggestion = get_ai_assistance_placeholder(details["ai_placeholder"])
                st.session_state.current_analysis_data[section_key_form] = (current_text_for_ai + "\n" + suggestion) if current_text_for_ai else suggestion
                st.rerun() # Rerun para atualizar o campo de texto com a sugestão
    st.markdown("---") # Separador visual entre seções

# Formulário apenas para o botão de submissão final
with st.form("analysis_form_final_submission"):
    st.subheader("3. Registrar Análise")
    st.markdown("Revise os campos preenchidos acima. Clique abaixo para gerar a prévia e registrar.")
    submitted = st.form_submit_button("Gerar Prévia e Registrar Análise")

if submitted:
    st.subheader("Prévia da Análise/Relatório")
    st.markdown("---")
    
    analysis_content_preview = ""
    # Reconstrói a prévia a partir do session_state no momento da submissão
    for section, details in current_model_structure.items(): # Itera sobre a estrutura original
        section_key_form = f"{current_model_key}_{section.replace(' ', '_').lower()}"
        value_from_state = st.session_state.current_analysis_data.get(section_key_form, "")
        analysis_content_preview += f"## {section}\n{value_from_state}\n\n"
        
    st.markdown(analysis_content_preview)
    st.markdown("---")

    if 'published_documents' not in st.session_state:
        st.session_state.published_documents = []
    
    title_key_form = f"{current_model_key}_título_do_boletim" 
    if f"{current_model_key}_título_da_análise" in st.session_state.current_analysis_data: # Ajuste para outros nomes de campo de título
         title_key_form = f"{current_model_key}_título_da_análise"
    # Adicione mais verificações se os nomes dos campos de título variarem mais
    
    document_title = st.session_state.current_analysis_data.get(title_key_form, f"{selected_model_name} - {pd.Timestamp.now().strftime('%Y-%m-%d')}")

    st.session_state.published_documents.append(
        {
            "title": document_title,
            "model_key": current_model_key,
            "model_name": selected_model_name,
            "content_markdown": analysis_content_preview,
            "data_fields": st.session_state.current_analysis_data.copy(),
            "publication_date": pd.Timestamp.now()
        }
    )
    st.success(f"Análise '{document_title}' registrada com sucesso e disponível para consulta.")