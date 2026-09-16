from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")

#requisitos cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        #espaços vazios
        if nome.strip() == '':
            return render_template("cadastro.html", mensagem = "Nome não informado. Preencha o nome.")
        
        if email.strip() == "":
            return render_template("cadastro.html", mensagem = "E-mail não informado. Preencha o email")
        
        if senha.strip() == "":
            return render_template("cadastro.html", mensagem = "Senha não informada. Preencha a senha")
        
#validação de email
        if "@" not in email or "." not in email:
            return render_template("cadastro.html", mensagem = "E-mail inválido. Preencha com E-mail válido.")
        conexao = sqlite3.connect("pyoneiro.db")
        cursor = conexao.cursor()
#sistema de erro para cadastro de email duplicado
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
            )

            conexao.commit()
            mensagem = "Conta criada com sucesso!"

        except sqlite3.IntegrityError:
            mensagem = "Erro: E-mail já cadastrado."
        
        conexao.close()

        return render_template("cadastro.html", mensagem=mensagem)

    return render_template("cadastro.html")

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        if email.strip() == "":
            return render_template("login.html", mensagem = "E-mail não informado. Preencha o email")
        if senha.strip() == "":
            return render_template("login.html", mensagem = "Senha não informada. Preencha a senha")
        conexao = sqlite3.connect("pyoneiro.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )

        usuario = cursor.fetchone()

        conexao.close()
        if usuario:
            return render_template("index.html")
        else:
            mensagem = "E-mail ou senha incorretos"
        return render_template("login.html", mensagem = mensagem)
    
if __name__ == "__main__":
    app.run(debug=True)