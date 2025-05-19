# Documento de Arquitetura - RelatAI

## Plataforma de Análise de Dados Financeiros do IPEA  
**Grupo 9 - 2025.1**  
**Versão 1.0**

---

## Histórico de Revisões

| Data       | Versão | Descrição                                     | Autor(es)                      |
|------------|--------|-----------------------------------------------|--------------------------------|
| 23/04/2025 | 1.0    | Considerações iniciais                        | Pedro Rocha Ferreira Lima      |
| 08/05/2025 | 2.0    | Adição de tópicos, diagramas e tecnologias    | Pedro Rocha Ferreira Lima      |
| 19/05/2025 | 3.0    | Mudança de tecnologia para backend e arquitetura | Pedro Rocha Ferreira Lima  |

---

## Autores

| Matrícula   | Nome                              | Função               |
|-------------|-----------------------------------|----------------------|
| 222034270   | Pedro Rocha Ferreira Lima         | Arquiteto de Software |
| 200014226   | Ana Luiza Borba de Abrantes       | Project Owner        |
| 231034064   | Arthur Henrique Vieira            | Dev                  |
| 222006857   | João Vitor Sales Ibiapina         | Dev                  |
| 232014057   | Kauã Vale Leão                    | DevOps               |
| 232014567   | Saied Muhamad Yacoub Falaneh     | Scrum Master         |

---

## Sumário

1. [Introdução](#1-introdução)  
2. [Representação Arquitetural](#2-representação-arquitetural)  
3. [Bibliografia](#3-bibliografia)

---

## 1. Introdução

### 1.1 Propósito

Este documento descreve a arquitetura da Plataforma de Análise de Dados Financeiros do IPEA, com foco na clareza para construção, manutenção e evolução do sistema.

### 1.2 Escopo

O sistema possibilita a coleta, análise e visualização de dados financeiros públicos. As funcionalidades incluem:
- Dashboards interativos em tempo real;
- Geração automática de textos com base em análise de dados;
- Resumos e alertas de tendências financeiras.

---

## 2. Representação Arquitetural

### 2.1 Definições

A arquitetura segue o padrão **MVC (Model-View-Controller)**:
- **Model**: lógica e estrutura de dados.
- **View**: interface visual com Streamlit.
- **Controller**: lógica de requisições com FastAPI.

### 2.2 Justificativa

- **Separação de responsabilidades**  
- **Reutilização de componentes com Python e Pandas**  
- **Facilidade de testes por camada**  
- **Desenvolvimento paralelo** (Frontend vs Backend)  
- **Escalabilidade com Docker e AWS**  
- **Alinhamento às necessidades funcionais do IPEA**

---

### 2.3 Detalhamento

#### Model
- Interage com o SQLite.
- Entidades:
  - Conjunto de Dados (CSV)
  - Análises (parâmetros/resultados)
  - Usuários (preferências)
  - Logs de acesso

#### View
- Exibição de dashboards, gráficos e mensagens.
- Planejada com Figma e implementada em Streamlit + HTML.

#### Controller
- Utiliza FastAPI para:
  - Gerenciar requisições;
  - Validar dados;
  - Processar CSVs com Pandas;
  - Enviar dados à View.

---

### 2.4 Metas e Restrições Arquiteturais

**Metas:**
- Escalabilidade
- Desempenho
- Manutenibilidade
- Segurança

**Restrições:**
- Compatibilidade com múltiplas plataformas

---

### 2.5 Visão de Casos de Uso

O sistema inclui:
- Menu de navegação;
- Dashboards em tempo real;
- Geração automática de relatórios;
- Previsões com Machine Learning;
- Upload de datasets;
- Aplicação de filtros de análise.

---

### 2.6 Visão Lógica

#### Componentes

- **Model**
  - `ConjuntoDeDados`: arquivos CSV
  - `AnaliseFinanceira`: análise com Pandas
  - `Usuario`: controle de acesso
  - `LogAcesso`: rastreamento de ações

- **View**
  - Criada com Streamlit, HTML e CSS
  - Exibe dados analisados

- **Controller**
  - Processa requisições e interage com o Model

#### Fluxo

1. Usuário interage com interface
2. Requisição é roteada no FastAPI
3. Controller executa lógica de negócio
4. Controller envia dados para View
5. View apresenta resultado ao usuário

---

### 2.7 Visão de Implementação

**Tecnologias e Bibliotecas:**
- FastAPI (backend)
- Scikit-learn (ML)
- Pandas (análise)
- Streamlit (UI)
- HTML/CSS (layout)

Organização modular do código para facilitar testes e manutenção.

---

### 2.8 Visão de Implantação

- Interface com **Streamlit + HTML/CSS**  
- Backend com **FastAPI**  
- Banco de dados: **SQLite**  
- **Implantação com Docker**, preparada para futura hospedagem em **AWS**

---

### 2.9 Restrições Adicionais

- **Acesso público** à página inicial
- **Recursos restritos a usuários logados**
- Qualidade:
  - Usabilidade
  - Portabilidade
  - Segurança
  - Manutenibilidade
  - Escalabilidade

---

## 3. Bibliografia

> **Arquitetura MVC: entendendo o modelo-visão-controlador.** DIO.me, 2024.  
> Disponível em: [https://www.dio.me/articles/arquitetura-mvc-entendendo-o-modelo-visao-controlador](https://www.dio.me/articles/arquitetura-mvc-entendendo-o-modelo-visao-controlador)  
> Acesso em: 23 abril de 2025.

---

> **RelatAI – Plataforma de análise financeira com geração automática de relatórios.**
