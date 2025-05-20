# Sprint 5

**Período:** 15/05/2025 a 26/05/2025

## Descrição

> Esta sprint teve como foco a aplicação de modelos preditivos sobre os dados econômicos (Selic, IPCA, Câmbio), geração de alertas automáticos via linguagem natural, migração do backend de Django para FastAPI, além da entrega do primeiro protótipo funcional da aplicação. Decidiu-se adotar o FastAPI pela performance, simplicidade na criação de APIs RESTful e melhor integração com as análises de NLP.

## Objetivos

* [x] Definir os horários das reuniões
* [x] Estudar conceitos necessários (previsão com scikit-learn, análise de séries temporais, NLP)
* [x] Definir requisitos do projeto
* [x] Escolher tecnologias a serem utilizadas

## Reuniões

### Reunião 1

**Data:** 15/05/2025
**Local:** UnB

**Decisões tomadas:**

* FastAPI será utilizado como backend principal
* O protótipo deverá expor uma rota para análises econômicas preditivas com linguagem natural
* A estrutura de dados seguirá com pandas e atualizações automáticas via `dados.py`
* Utilização de scikit-learn para previsões
* Alertas deverão ser gerados a partir de mudanças relevantes nas séries (ex: variações mensais acima da média)
* Separação da API em módulos para facilitar manutenção futura

---

#### Requisitos

**Funcionais:**

* [x] Rota para previsões de Selic, IPCA e Câmbio
* [x] Geração de textos descritivos automáticos com linguagem natural
* [x] Exposição de uma rota `/alertas` para indicar mudanças atípicas
* [x] Protótipo navegável com visualização dos dados

**Não Funcionais:**

* [x] API leve e performática
* [x] Código modular e com tipagem explícita
* [ ] Testes automatizados para a API

#### Tecnologias Utilizadas

| Componente         | Tecnologia                     |
| ------------------ | ------------------------------ |
| **Design**         | Figma                          |
| **Frontend**       | Streamlit                       |
| **Backend**        | FastAPI (antes: Django)        |
| **Banco de Dados** | SQLite (temporário)            |
| **Message Queue**  | Não utilizado nesta sprint     |
| **DevOps**         | GitHub Actions (CI/CD)         |
| **Infraestrutura** | Render.com (deploy temporário) |


## Finalização

> Sprint concluída com sucesso. O protótipo foi entregue com rotas funcionais para análises preditivas e alertas automáticos. A migração de Django para FastAPI foi realizada sem grandes dificuldades. Algumas rotas ainda carecem de testes automatizados, que serão priorizados na próxima sprint.

### Entregas

* [x] Protótipo funcional entregue
* [x] Rota de previsões com linguagem natural (`/analise`)
* [x] Rota de alertas econômicos (`/alertas`)
* [x] Backend em FastAPI

### Pendências

* [ ] Cobertura de testes automatizados
* [ ] Melhorar a análise de tendências (incluir sazonalidade)

## Observações

> A aplicação de NLP mostrou-se eficaz para a geração de textos analíticos simples, mas ainda há espaço para aprimorar a naturalidade das frases. A mudança para FastAPI trouxe mais agilidade no desenvolvimento. Sugestão: avaliar o uso de um modelo de séries temporais mais robusto, como Prophet ou ARIMA, para cenários futuros.
