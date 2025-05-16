# 🧱 Documento de Arquitetura - Grupo 9 (2025.1)

## 📜 Histórico de Revisões

| Data       | Versão | Descrição                           | Autores                     |
|------------|--------|-------------------------------------|-----------------------------|
| 23/04/2025 | 1.0    | Considerações iniciais              | Pedro Rocha Ferreira Lima  |
| 08/05/2025 | 2.0    | Adição de tópicos, diagramas, tecnologias novas | Pedro Rocha Ferreira Lima  |

---

## 👥 Autores

| Matrícula  | Nome                              | Função                |
|------------|-----------------------------------|-----------------------|
| 222034270  | Pedro Rocha Ferreira Lima         | Arquiteto de Software |
| 200014226  | Ana Luiza Borba de Abrantes       | Project Owner         |
| 231034064  | Arthur Henrique Vieira            | Dev                   |
| 222006857  | João Vitor Sales Ibiapina         | Dev                   |
| 232014057  | Kauã Vale Leão                    | DevOps                |
| 232014567  | Saied Muhamad Yacoub Falaneh      | Scrum Master          |

---

## 📑 Sumário

1. [Introdução](#1-introdução)  
2. [Representação Arquitetural](#2-representação-arquitetural)  
3. [Bibliografia](#3-bibliografia)

---

## 1. 🎯 Introdução

### 1.1 Propósito

Este documento descreve a arquitetura da Plataforma de Análise de Dados Financeiros do IPEA, no contexto da disciplina de Métodos de Desenvolvimento de Software (2025.1). Seu objetivo é garantir clareza na construção, manutenção e evolução do sistema, orientando decisões técnicas e organizacionais.

### 1.2 Escopo

O sistema permitirá:
- Coleta, análise e visualização de dados financeiros públicos;
- Construção de painéis interativos em tempo real;
- Geração automática de textos e alertas baseados em dados.

---

## 2. 🧠 Representação Arquitetural

### 2.1 Definições

Adotamos o padrão **MVC** (Model-View-Controller), adaptado ao **MVT** (Model-View-Template) do Django.

### 2.2 Justificativa

- ✅ **Separação de Responsabilidade**: facilita manutenção e testes.  
- 🔁 **Reutilização de Componentes**: filtros, gráficos e módulos com Django e Pandas.  
- 🧪 **Facilidade de Testes**: apoio a testes unitários e de integração.  
- 👥 **Desenvolvimento Paralelo**: divisão entre frontend (Streamlit) e backend (Django).  
- 🚀 **Escalabilidade**: integração com Docker e AWS.  
- 🎯 **Alinhamento aos Requisitos**: pensado para analistas do IPEA e tempo do projeto.

### 2.3 Detalhamento das Camadas

#### Model
Responsável pela lógica de dados, utilizando o ORM do Django com entidades como:
- Conjunto de Dados
- Análises
- Usuários
- Logs de Acesso

#### Template (View)
Interface visual com o usuário usando **Streamlit** e **HTML/CSS**, planejada via Figma. Apresenta:
- Dashboards e gráficos
- Tabelas e mensagens

#### View (Controller)
Gerencia requisições e lógica de negócio com Django. Executa:
- Processamento de CSV com Pandas
- Interação com o banco de dados
- Renderização para o template

---

### 2.4 Metas e Restrições Arquiteturais

#### Metas
- ⚙️ **Escalabilidade**
- ⚡ **Desempenho**
- 🔧 **Manutenibilidade**
- 🔒 **Segurança**

#### Restrições
- 💻 **Compatibilidade universal**
- 🛡️ **Segurança contra acessos indevidos**

---

### 2.5 Visão de Casos de Uso

Tecnologias:
- **Backend**: Django, Pandas, Scikit-learn
- **Frontend**: HTML, CSS, Streamlit
- **Banco de Dados**: SQLite

#### Funcionalidades:
- Tela inicial com menu
- Painéis interativos em tempo real
- Geração de relatórios automáticos
- Previsões com ML
- Filtros e carregamento de datasets

---

### 2.6 Visão Lógica

#### Componentes:

- **Model**
  - `ConjuntoDeDados`
  - `AnaliseFinanceira`
  - `Usuario`
  - `LogAcesso`

- **View (Controller)**
  - Processa requisições
  - Valida, salva e envia dados para template

- **Template (Apresentação)**
  - Streamlit + HTML/CSS
  - Exibição de dashboards e alertas

#### Fluxo:

1. Usuário interage com a interface  
2. View processa a requisição  
3. Acessa ou modifica os dados no Model  
4. Retorna dados tratados ao Template

---

### 2.7 Visão de Implementação

Organização modular, dividida em camadas.

#### Bibliotecas:
- Django
- Pandas
- Scikit-learn
- Streamlit
- HTML/CSS

---

### 2.8 Visão de Implantação

- 🖥️ Execução local via navegador (desktop)
- 📦 Docker para empacotamento
- ☁️ Pronto para hospedagem futura na AWS
- 🧩 Integração: Django + Streamlit + SQLite

---

### 2.9 Restrições Adicionais

#### Funcionais:
- Acesso ao site antes do login
- Funcionalidades restritas a usuários autenticados

#### Não Funcionais:

| Requisito       | Descrição |
|-----------------|-----------|
| ✅ Usabilidade   | Interface intuitiva |
| 📱 Portabilidade | Acessível em qualquer SO ou navegador |
| 🔐 Segurança     | Proteção contra acessos indevidos |
| 🧩 Manutenibilidade | Código documentado |
| 📈 Escalabilidade | Pensado para crescimento futuro |

---

## 3. 📚 Bibliografia

> Arquitetura MVC: entendendo o modelo-visão-controlador. DIO.me, 2024.  
> Disponível em: https://www.dio.me/articles/arquitetura-mvc-entendendo-o-modelo-visao-controlador  
> Acesso em: 23 abril de 2025.

---
