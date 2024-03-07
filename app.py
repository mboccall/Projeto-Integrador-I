import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates_folder')

# Função para criar o BD
def criar_tabela():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            sobrenome TEXT,
            email TEXT,
            telefone TEXT,
            empresa TEXT,
            checkboxstatus TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Rota para exibir o formulário de cadastro

@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    nome = request.form["nome"]
    sobrenome = request.form["sobrenome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    empresa = request.form["empresa"]
    checkboxstatus = request.form["checkboxstatus"]
    
    # Inserir os dados na tabela do banco de dados
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nome, sobrenome, email, telefone, empresa, checkboxstatus)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, sobrenome, email, telefone, empresa, checkboxstatus))
    conn.commit()
    conn.close()

    return "Cliente cadastrado com sucesso!"


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    criar_tabela() # Chama a função para criar a tabela antes de iniciar a aplicação
    app.run(debug=True)
    
    
