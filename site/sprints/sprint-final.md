# Sprint Final – Entrega do Trabalho

**Período:** 01/07/2025 a 08/07/2025

## Descrição

> Esta sprint teve como foco a finalização do projeto, incluindo a containerização da aplicação com Docker e a realização do deploy para o ambiente de produção. O time concentrou esforços em revisar os requisitos implementados, garantir a estabilidade do sistema e documentar a entrega final.

## Objetivos

* [x] Realizar a dockerização do projeto
* [x] Configurar pipeline de CI/CD (se aplicável)
* [x] Fazer o deploy para ambiente de produção
* [x] Testar funcionalidades em produção
* [x] Validar os requisitos implementados
* [x] Documentar a entrega final

## Reuniões

### Reunião 1

**Data:** 02/07/2025
**Local:** Google Meet

**Decisões tomadas:**

* Definir imagem base e estrutura do Dockerfile
* Usar Docker Compose para orquestração local
* Escolher serviço de hospedagem para o deploy (ex: Render, Railway ou VPS)

---

### Reunião 2

**Data:** 05/07/2025
**Local:** Discord

**Decisões tomadas:**

* Validar deploy com ambiente de staging
* Realizar ajustes finos em variáveis de ambiente e configuração da base de dados em produção

#### Requisitos

**Funcionais:**

* [x] Aplicação disponível em ambiente de produção
* [x] Funcionalidades acessíveis e testadas em produção
* [x] Integração entre frontend e backend concluída

**Não Funcionais:**

* [x] Dockerização da aplicação
* [x] Deploy estável e funcional
* [x] Documentação de instalação e execução via Docker

---

## Finalização

> Sprint concluída com sucesso. A aplicação foi publicada em produção e está operando conforme esperado. Todos os requisitos previstos foram validados em ambiente real.

### Entregas

* [x] Dockerfile e Docker Compose configurados
* [x] Deploy em ambiente de produção
* [x] Testes de funcionalidades em produção
* [x] Documentação atualizada (README.md com instruções de execução)

### Pendências

* [ ] Implementar monitoramento contínuo (futuro)
* [ ] Realizar testes automatizados de regressão

## Observações

> O time enfrentou desafios na configuração de variáveis de ambiente e persistência de dados no banco em produção, que foram resolvidos com ajustes no `docker-compose.yml` e nas configurações do provedor de hospedagem.
> Como melhoria futura, é recomendada a implementação de testes automatizados e monitoramento de uptime.

---

### 📋 **Sprint Review – Entrega Final**

Durante a **Sprint Review**, o time apresentou a aplicação rodando em produção, demonstrando as principais funcionalidades e a integração completa entre as partes do sistema.

**Principais destaques:**

* Interface intuitiva e responsiva entregue com sucesso
* Backend funcional e integrado, com persistência de dados
* Projeto 100% dockerizado, permitindo fácil replicação e escalabilidade
* Deploy em ambiente de produção testado e acessível por link público

**Feedbacks coletados (se houver):**

* A aplicação estável, com boa performance.
* Sugestão para futura escalabilidade com uso de serviços de monitoramento e logs centralizados.