# 📝 Padeas — Bloco de Notas Web Minimalista

Um bloco de notas online instantâneo e sem necessidade de login (inspirado no Dontpad), construído com **Python (Flask)**, **Vercel Serverless Functions** e **MongoDB Atlas**.

Acesse qualquer URL (ex: `seu-site.vercel.app/minha-nota`) para criar, editar, compartilhar ou proteger suas anotações automaticamente.

---

## ✨ Funcionalidades

- **Roteamento Dinâmico:** Qualquer caminho na URL cria ou carrega automaticamente uma página exclusiva.
- **Auto-save Inteligente:** Salvamento automático em nuvem após 500ms de inatividade na digitação.
- **Menu Lateral de Atalhos:** Lista todas as páginas criadas no banco de dados com navegação rápida e opção de recolher (`☰`).
- **Proteção por Senha Opcional:** Permite travar páginas sensíveis com senha (armazenada com hash criptográfico no banco).
- **Cópia Rápida e Exclusão:** Botão discreto para copiar todo o conteúdo (`Copiar`) e opção para excluir páginas não utilizadas (`×`).
- **Custo Zero:** Projetado para rodar 100% nos planos gratuitos (*Free Tier*) da Vercel e do MongoDB Atlas.

---

## 🛠️ Tecnologias Utilizadas

- **Front-end:** HTML5, CSS3 e JavaScript puro (Vanilla JS)
- **Back-end:** Python 3 + Flask
- **Hospedagem:** Vercel (Serverless Functions)
- **Banco de Dados:** MongoDB Atlas (NoSQL)

---

## 📁 Estrutura do Projeto

```text
padeas/
├── api/
│   └── index.py          # API Flask e integração com MongoDB Atlas
├── templates/
│   └── index.html        # Interface web, editor, sidebar e tela de senha
├── .env.example          # Modelo de variável de ambiente
├── requirements.txt      # Dependências Python (Flask, pymongo, dnspython, python-dotenv)
└── vercel.json           # Configuração de rotas Serverless na Vercel
```

---

## 🚀 Como Replicar e Hospedar o Projeto

Para colocar a sua própria versão no ar gratuitamente, siga as 3 etapas abaixo:

### Etapa 1: Configurar o Banco de Dados no MongoDB Atlas (Grátis)

1. Crie uma conta gratuita no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Crie um novo projeto e clique em **Build a Database** selecionando o plano gratuito **M0 (Shared)**.
3. Em **Security > Database Access**, crie um usuário e senha para o banco de dados (anote essas credenciais).
4. Em **Security > Network Access**, clique em **Add IP Address** e selecione **Allow Access from Anywhere** (`0.0.0.0/0`) para permitir que as Serverless Functions da Vercel acessem o banco.
5. Volte para **Database**, clique em **Connect > Drivers** (selecione Python) e copie a **Connection String (URI)**. Ela terá um formato parecido com este:
   ```text
   mongodb+srv://<usuario>:<senha>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   *(Substitua `<usuario>` e `<senha>` pelos dados criados no passo 3).*

---

### Etapa 2: Preparar o Repositório no GitHub

1. Faça um **Fork** deste repositório ou clone-o para a sua máquina e envie para um repositório próprio no seu GitHub:
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

---

### Etapa 3: Fazer o Deploy na Vercel (Grátis)

1. Crie uma conta gratuita na [Vercel](https://vercel.com/) (recomendado entrar utilizando sua conta do GitHub).
2. No painel principal, clique em **Add New... > Project**.
3. Importe o repositório do projeto que está no seu GitHub.
4. Na tela de configuração (**Configure Project**), abra a aba **Environment Variables** e adicione:
   - **Key (Nome):** `MONGO_URI`
   - **Value (Valor):** Cole a sua Connection String completa do MongoDB Atlas.
5. Clique em **Add** e depois em **Deploy**.

Em menos de 1 minuto, a Vercel finalizará a publicação e gerará a URL pública do seu bloco de notas!

---

## 💻 Rodando Localmente (Opcional)

Caso queira testar ou modificar o código no seu computador antes de enviar para a Vercel:

1. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```
2. Defina a variável de ambiente `MONGO_URI` no seu terminal:
   * **Windows (PowerShell):**
     ```powershell
     $env:MONGO_URI="sua_string_de_conexao_mongodb"
     ```
   * **Linux / macOS (Bash):**
     ```bash
     export MONGO_URI="sua_string_de_conexao_mongodb"
     ```
3. Inicie o servidor local de desenvolvimento:
   ```bash
   flask --app api/index run --debug
   ```
4. Acesse `http://127.0.0.1:5000` no navegador.