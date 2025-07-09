# RelatAI IPEA

RelatAI IPEA é uma plataforma que automatiza a geração de relatórios financeiros a partir de dados do IPEA (Instituto de Pesquisa Econômica Aplicada). A solução integra backend, frontend, análise de dados e NLP para oferecer insights claros e atualizados.

---

## Integrantes

- Ana Luiza Borba de Abrantes
- Arthur Henrique Vieira
- João Vitor Sales Ibiapina
- Kauã Vale Leão
- Pedro Rocha Ferreira Lima
- Saied Muhamad Yacoub Falaneh

---

## Objetivo

Fornecer relatórios automatizados com visualização interativa e resumos gerados por NLP, facilitando a interpretação de séries históricas e indicadores financeiros do IPEA.

---

## Funcionalidades

- Conexão com APIs do IPEA para coleta de séries históricas.
- Pipeline ETL para limpeza e transformação de dados.
- Cálculo de indicadores (variação percentual, médias móveis, etc.).
- Geração de relatórios em PDF, HTML e Markdown.
- Dashboard interativo com filtros e gráficos.
- Resumos automáticos por NLP.
- Exportação de dados para CSV e Excel.

---

## Tecnologias

- **Backend**: Python (FastAPI), Pandas  
- **Frontend**: Streamlit, JavaScript, HTML5, CSS3  
- **NLP**: spaCy, NLTK  
- **CI/CD**: GitHub Actions  
- **Deploy**: Streamlit Cloud  
- **Testes**: PyTest  

---

## Instalação

```bash
# Clone o repositório e acesse a pasta
git clone https://github.com/unb-mds/2025-1-RelatAI.git
cd 2025-1-RelatAI

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate    # venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o backend com autoreload
uvicorn main:app --reload

# Inicie o frontend
streamlit run src/app.py
```

## Planejamento

1. **Reunião Inicial**  
   - Levantamento de requisitos e definição de escopo.  
   - Distribuição de funções entre os integrantes.

2. **Sprints Semanais**  
   - Atualização de progresso e dificuldades.  
   - Entrega de partes funcionais (backend, frontend, IA, etc.).

3. **Sprint Review & Retrospectiva**  
   - Coleta de feedback e ajustes no planejamento.  
   - Avaliação das entregas de código e performance do sistema.

---


## Sobre

Para mais detalhes, visite a [página do projeto](https://unb-mds.github.io/2025-1-RelatAI/).

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

