import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consultar Publicações - IPEA", page_icon="📚", layout="wide")

st.title("Consultar Publicações e Documentos Estatísticos")
st.markdown("Acesse o acervo de análises, relatórios e boletins do Instituto.")

if 'published_documents' not in st.session_state or not st.session_state.published_documents:
    st.info("Nenhuma publicação encontrada no momento.")
    st.markdown("Novas análises podem ser elaboradas na seção **Nova Análise Estatística**.")
    st.stop()

st.subheader(f"Total de Publicações Disponíveis: {len(st.session_state.published_documents)}")

# Opções de filtro (exemplo)
# filter_text = st.text_input("Buscar por título ou palavra-chave:")
# filter_model = st.multiselect("Filtrar por tipo de documento:", 
# options=list(set(doc['model_name'] for doc in st.session_state.published_documents)))

# Aplicar filtros aqui se implementado

sorted_documents = sorted(st.session_state.published_documents, key=lambda x: x.get('publication_date', pd.Timestamp.min), reverse=True)

for i, doc in enumerate(sorted_documents):
    title = doc.get('title', f"Documento #{i+1}")
    model_name = doc.get('model_name', 'N/A')
    pub_date = doc.get('publication_date')
    
    if isinstance(pub_date, pd.Timestamp):
        pub_date_str = pub_date.strftime('%d/%m/%Y')
    else:
        pub_date_str = "Data Indisponível"

    with st.expander(f"{title} (Tipo: {model_name} - Publicado em: {pub_date_str})"):
        st.markdown("#### Resumo/Conteúdo Principal:")
        # Idealmente, mostrar um resumo ou as primeiras linhas. Por ora, o markdown completo.
        st.markdown(doc.get('content_markdown', 'Conteúdo não disponível.'))
        
        col1, col2, col_spacer = st.columns([1, 1, 5])

        download_key_name = f"download_{doc.get('title', i)}_{str(doc.get('publication_date', ''))}".replace(" ", "_").replace(":", "_").replace("/", "_")
        col1.download_button(
            label="Baixar Documento (.md)",
            data=doc.get('content_markdown', ''),
            file_name=f"{title.replace(' ', '_').replace('/', '_').lower()}.md",
            mime='text/markdown',
            key=f"dl_btn_{download_key_name}"
        )
        
        # Funcionalidade de "remover" pode não ser apropriada para um sistema governamental público,
        # mas útil para o protótipo ou para uma área administrativa.
        delete_key_name = f"delete_{doc.get('title', i)}_{str(doc.get('publication_date', ''))}".replace(" ", "_").replace(":", "_").replace("/", "_")
        if col2.button("Remover do Acervo (Simulação)", key=f"del_btn_{delete_key_name}"):
            # Lógica para encontrar e remover o item
            original_index_to_remove = -1
            for idx, original_doc_item in enumerate(st.session_state.published_documents):
                if original_doc_item.get('title') == doc.get('title') and original_doc_item.get('publication_date') == doc.get('publication_date'):
                    original_index_to_remove = idx
                    break
            if original_index_to_remove != -1:
                st.session_state.published_documents.pop(original_index_to_remove)
                st.success(f"Documento '{title}' removido do acervo (simulação).")
                st.rerun()
            else:
                st.error("Erro ao tentar remover o documento.")
        st.markdown("---")

# Adicionar um rodapé institucional simples
st.markdown("---")
st.caption("© 2025 Instituto de Pesquisa e Estatística Aplicada. Todos os direitos reservados.")