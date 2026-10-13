from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        
        if nome.strip() == '':
            return render_template("cadastro.html", mensagem = "Nome não informado. colocar o nome.")
        
        if email.strip() == "":
            return render_template("cadastro.html", mensagem = "E-mail não informado. colocar o email")
        
        if senha.strip() == "":
            return render_template("cadastro.html", mensagem = "Senha não informada. colocar a senha")
        

        if "@" not in email or "." not in email:
            return render_template("cadastro.html", mensagem = "E-mail inválido. coloque o email correto.")
        conexao = sqlite3.connect("pyoneiro.db")
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
            )

            conexao.commit()
            mensagem = "Conta criada com sucesso!"
    
        except sqlite3.IntegrityError:
            mensagem = "E-mail já cadastrado. tente outro e-mail."

        
        conexao.close()

        return render_template("cadastro.html", mensagem = mensagem)

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        if email.strip() == "":
            return render_template("login.html", mensagem = "E-mail não informado. colocar o email")
        if senha.strip() == "":
            return render_template("login.html", mensagem = "Senha não informada. colocar a senha")
        conexao = sqlite3.connect("pyoneiro.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )

        usuario = cursor.fetchone()

        conexao.close()
        if usuario:
            return render_template("menu.html")
        else:
            mensagem = "E-mail ou senha incorretos"
        return render_template("login.html", mensagem = mensagem)
    return render_template("login.html")
    
MODULOS = [
    {
        "id": 1,
        "nome": "Introdução ao Python",
        "explicacao":  ["O Python é uma linguagem de programação de alto nível, interpretada, dinâmica e com sintaxe simples.",
                        "Criada por Guido van Rossum em 1991, tornou-se uma das linguagens mais populares do mundo."
        ],
        "pergunta": "Qual o nível de sintaxe do Python? simples, mediana ou complexa?",
        "resposta": "simples"
    },
    {
        "id": 2,
        "nome": "Sintaxe do Python",
        "explicacao": [ "A sintaxe do Python é clara e legível, e usa indentação para definir blocos de código.",
                        "As palavras-chave são as palavras reservadas pela linguagem Python, nós não podemos utilizar essas palavras para nomear nossas variáveis, funções ou qualquer outro identificador, elas são usadas para definir a sintaxe e a estrutura da linguagem Python, vale lembrar que as palavras-chave são case sensitive e devem ser escritas dessa maneira.",
        ],
        "pergunta": "Como o Python define blocos de código? (sem acento e ç)",
        "resposta": "indentacao"
    },
]


@app.route("/modulos")
def modulos():
    try:
        resposta = requests.get("https://pypi.org/pypi/flask/json", timeout=5)
        info = resposta.json()["info"]
        biblioteca = {
            "nome": info["name"],
            "versao": info["version"],
            "resumo": info["summary"],
        }
    except (requests.RequestException, KeyError, ValueError):
        biblioteca = None

    return render_template("modulos.html", modulos=MODULOS, biblioteca=biblioteca)

@app.route("/modulo/<int:id>", methods=["GET", "POST"])
def modulo(id):
    modulo_escolhido = None
    for m in MODULOS:
        if m["id"] == id:
            modulo_escolhido = m

    if modulo_escolhido is None:
        return "Módulo não encontrado"

    if request.method == "POST":
        resposta_usuario = request.form["resposta"]

        if resposta_usuario.strip().lower() == modulo_escolhido["resposta"].lower():
            mensagem = "Resposta correta"
        else:
            mensagem = "Errado,você consegue se tentar novamente."

        return render_template("modulo.html", modulo=modulo_escolhido, mensagem=mensagem)

    return render_template("modulo.html", modulo=modulo_escolhido)

if __name__ == "__main__":
    app.run(debug=True)