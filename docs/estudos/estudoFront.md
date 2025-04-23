### 📄 Aplicacao de HTML e CSS Customizado no Projeto

#### 📌 Objetivo
O objetivo desta parte do projeto é construir a interface do usuário (frontend) utilizando **HTML** para a estrutura do conteúdo e **CSS customizado** para o estilo visual, de forma responsiva, acessível e condizente com a identidade visual proposta pelo grupo.

#### 🧱 Estrutura do HTML

O **HTML** será utilizado para:

- Definir a estrutura básica das páginas do sistema
- Organizar o conteúdo em seções semânticas (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- Inserir formulários, botões e áreas de exibição de dados
- Garantir acessibilidade com uso correto de `alt`, `label`, `aria-*` e tags apropriadas

Exemplo de estrutura inicial:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nome do Projeto</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header>
    <h1>Bem-vindo ao Sistema</h1>
  </header>
  <main>
    <section>
      <h2>Login</h2>
      <form>
        <!-- campos aqui -->
      </form>
    </section>
  </main>
  <footer>
    <p>&copy; 2025 - Equipe de Desenvolvimento</p>
  </footer>
</body>
</html>
```

#### 🎨 Estilização com CSS Customizado

O **CSS (Cascading Style Sheets)** será utilizado para:

- Criar um layout visualmente agradável e funcional
- Aplicar paleta de cores personalizada conforme a identidade visual do projeto
- Responsividade com `@media queries`
- Animações e interações visuais com `:hover`, `:focus`, transições e outros recursos modernos

Exemplo de customização:

```css
body {
  font-family: 'Segoe UI', sans-serif;
  background-color: #f8f9fa;
  color: #333;
  margin: 0;
  padding: 0;
}

header {
  background-color: #1e90ff;
  color: white;
  padding: 1rem;
  text-align: center;
  border-bottom: 4px solid #005f99;
}

form input, form button {
  padding: 0.5rem;
  margin: 0.25rem 0;
  width: 100%;
  border-radius: 5px;
  border: 1px solid #ccc;
}
```

#### 🛠️ Ferramentas e Boas Práticas

- **Editor**: VS Code com extensões para HTML/CSS e Live Server
- **Organização**: Separar HTML (`index.html`) e CSS (`style.css`)
- **Semântica e acessibilidade** como princípios base
- **Validação** do código com W3C Validator

#### 📈 Contribuição para o Projeto

A implementação do HTML e CSS:

- Facilita a validação das funcionalidades previstas na interface
- Ajuda no alinhamento visual do sistema com os requisitos de usabilidade
- Permite testes mais fáceis e feedback rápido do cliente/professor
