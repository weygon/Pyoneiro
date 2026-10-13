# Pyoneiro

Site para aprender Python de forma simples e interativa, feito com Flask. O usuário cria uma conta, faz login e estuda em módulos com explicação e uma pergunta para responder.

## Funcionalidades

- **Cadastro** com validação dos campos (nome, e-mail e senha obrigatórios, e-mail com formato válido e e-mail único).
- **Login** conferindo e-mail e senha no banco de dados.
- **Módulos de estudo**: lista de módulos, página de cada módulo com explicação e pergunta.
- **Resposta com feedback**: o site compara a resposta digitada com a resposta certa e mostra se acertou ou errou (ignora maiúsculas e espaços nas pontas).
- **Biblioteca em destaque**: seção na página de módulos com dados reais vindos de uma API externa (PyPI).

## Tecnologias utilizadas

| Tecnologia | Para que é usada |
|---|---|
| Python | Linguagem do projeto |
| Flask | Framework web: rotas, formulários e páginas |
| Jinja2 | Motor de templates do Flask (`{% for %}`, `{% if %}`, `{{ variável }}`) |
| SQLite (`sqlite3`) | Banco de dados dos usuários (arquivo `pyoneiro.db`) |
| HTML e CSS | Estrutura e estilo das páginas |
| `requests` | Biblioteca para fazer a chamada à API externa |
| Ambiente virtual (`.venv`) | Isola as dependências do projeto |
| VS Code | Editor de código |

## API utilizada

**PyPI JSON API** (Python Package Index), o repositório oficial de bibliotecas Python.

- Endereço usado: `https://pypi.org/pypi/flask/json`
- Não precisa de chave de API nem de cadastro.
- O código lê a parte `info` da resposta e mostra o **nome**, a **versão** e o **resumo** da biblioteca na página `/modulos`.
- Se a API estiver fora do ar ou demorar mais de 5 segundos, a seção simplesmente não aparece e o resto do site continua funcionando (tratamento com `try/except` e `timeout`).
- Fonte dos dados: [pypi.org](https://pypi.org).

## Estrutura do projeto

```
Pyoneiro/
├── app.py              # rotas e lógica do Flask
├── database.py         # cria o banco e a tabela usuarios (rodar uma vez)
├── pyoneiro.db         # banco de dados SQLite (tabela usuarios)
├── API.py              # teste da chamada à API do PyPI
├── requirements.txt    # dependências do projeto
├── templates/
│   ├── index.html      # página inicial
│   ├── cadastro.html   # cadastro de usuário
│   ├── login.html      # login
│   ├── menu.html       # menu depois do login
│   ├── modulos.html    # lista de módulos + biblioteca em destaque
│   └── modulo.html     # um módulo: explicação, pergunta e resposta
└── static/
    └── style.css       # estilos
```

## Rotas

| Rota | O que faz |
|---|---|
| `/` | Página inicial |
| `/cadastro` | Formulário de cadastro (GET e POST) |
| `/login` | Formulário de login (GET e POST) |
| `/modulos` | Lista dos módulos e biblioteca em destaque |
| `/modulo/<id>` | Página de um módulo, com pergunta e resposta (GET e POST) |

## Como executar

1. Crie e ative o ambiente virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Instale as dependências:
   ```
   python -m pip install -r requirements.txt
   ```
3. Crie o banco de dados (só na primeira vez). O script cria o arquivo `pyoneiro.db` com a tabela `usuarios` (`id`, `nome`, `email` único e `senha`):
   ```
   python database.py
   ```
4. Rode o projeto:
   ```
   python app.py
   ```
5. Abra no navegador: `http://127.0.0.1:5000`

## Limitações conhecidas e próximos passos

Este é um projeto de estudo, e estes pontos ficaram de fora e estão planejados:

- As senhas ainda são salvas em texto puro no banco. O próximo passo é guardá-las com **hash**.
- A página `/modulos` ainda pode ser aberta sem login. O próximo passo é controlar o acesso com **sessão** (`session` do Flask).
- O servidor roda em modo de desenvolvimento (`debug=True`), que não deve ser usado em um site publicado.
- Mais módulos e perguntas podem ser adicionados na lista `MODULOS`, sem criar rotas novas.

## Autor

Weygon