from bertopic import BERTopic
from utils.dados import carregar_dados

# Gera um resumo automático dos principais tópicos utilizando BERTopic
def gerar_resumo_nlp():
    df = carregar_dados()
    if "descricao" not in df.columns:
        return "Sem coluna 'descricao' para gerar resumo."
    df_textos = df["descricao"].dropna().astype(str)
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(df_textos.tolist())
    resumo = topic_model.get_topic_info().head(3).to_string()  # Retorna os 3 principais tópicos
    return resumo