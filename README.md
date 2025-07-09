

# 🧠 RelatAI – Relatórios Financeiros Automatizados

RelatAI é um sistema que integra **coleta, análise e geração de relatórios financeiros** com linguagem natural, utilizando **FastAPI** para o backend e **Streamlit** para a interface frontend.

> 🚀 Transformamos dados públicos do IPEA e BACEN em **relatórios automatizados, acessíveis e compreensíveis para todos**.

---

## 📦 Como Executar o Projeto

### 🛠️ Pré-requisitos

- Python 3.10+
- pip
- Docker (opcional)
- Git

---

### ▶️ Rodando o Backend (FastAPI)

```bash
# Clone o repositório
git clone https://github.com/unb-mds/2025-1-RelatAI.git
cd 2025-1-RelatAI/backend

# Instale as dependências
pip install -r requirements.txt

# Execute a API
uvicorn main:app --reload
```

Acesse a documentação interativa da API:  
📎 `http://localhost:8000/docs`

---

### 💻 Rodando o Frontend (Streamlit)

```bash
cd ../frontend

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
```

Acesse a interface gráfica:  
📎 `http://localhost:8000`

---

## 🏗️ Estrutura do Projeto

```plaintext
2025-1-RelatAI/
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── pages/
│   └── components/
├── data/
│   └── raw/ processed/
├── notebooks/
│   └── análise-nlp.ipynb
├── docker-compose.yml
└── README.md
```

---

## 🧩 Arquitetura do Projeto

- **Backend (FastAPI):** fornece rotas REST para buscar dados do BACEN/IPEA, aplicar modelos de NLP e entregar resumos financeiros.
- **Frontend (Streamlit):** permite visualização interativa dos indicadores e relatórios gerados.
- **NLP & Análise de Dados:** modelos baseados em `spaCy`, `scikit-learn` e `pandas` para gerar descrições automatizadas e insights.
- **Banco de Dados:** PostgreSQL (pode ser local ou em nuvem).
- **Docker:** ambiente completo para deploy e testes.

---

## 📑 Documentação da API

### 🔹 `GET /selic`
Retorna os dados da taxa Selic histórica.

### 🔹 `GET /ipca`
Retorna os dados da inflação (IPCA).

### 🔹 `GET /cambio`
Retorna os dados do dólar comercial.

### 🔹 `GET /pib`
Retorna os dados do pib comercial.

### 🔹 `GET /divida`
Retorna os dados da divida comercial.

### 🔹 `GET /alertas`
Retorna os dados de alertas comerciais.

### 🔹 `POST /predict/{predicator_name}`
Gera um resumo textual baseado nos dados econômicos recebidos.

**Exemplo de corpo da requisição:**
```json
{
  "variavel": "selic",
  "dados": [10.75, 10.75, 10.50, 10.25]
}
```

---

## ⚙️ Tecnologias Utilizadas

| Camada         | Tecnologias                            |
|----------------|----------------------------------------|
| **Backend**    | FastAPI, Uvicorn                       |
| **Frontend**   | Streamlit, Pandas                      |
| **Análise/NLP**| Scikit-learn, spaCy, matplotlib        |
| **DevOps**     | Docker, GitHub                         |


---

## 🤝 Como Contribuir

1. Fork este repositório
2. Crie uma branch com sua feature (`git checkout -b minha-feature`)
3. Commit suas alterações (`git commit -m 'feat: minha contribuição'`)
4. Faça push para a branch (`git push origin minha-feature`)
5. Abra um Pull Request 🚀

---

## 📄 Licença


Este projeto está licenciado sob a [MIT License](LICENSE).

