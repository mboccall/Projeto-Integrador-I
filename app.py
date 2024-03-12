import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

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

# Rota para exibir o formulário de cadastro...
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

@app.route('/consultar_clientes')
def consultar_clientes():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return render_template('resultados.html', clientes=clientes)

@app.route('/editar_cliente/<int:id>', methods=['POST'])
def editar_cliente(id):
    nome = request.json["nome"]
    sobrenome = request.json["sobrenome"]
    email = request.json["email"]
    telefone = request.json["telefone"]
    empresa = request.json["empresa"]
    checkboxstatus = request.json["checkboxstatus"]
    
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes SET nome=?, sobrenome=?, email=?, telefone=?, empresa=?, checkboxstatus=? WHERE id=?
    ''', (nome, sobrenome, email, telefone, empresa, checkboxstatus, id))
    conn.commit()
    conn.close()
    
    # Retornar os dados atualizados para atualizar a tabela via AJAX
    return jsonify({'nome': nome, 'sobrenome': sobrenome, 'email': email, 'telefone': telefone, 'empresa': empresa, 'checkboxstatus': checkboxstatus})

@app.route('/excluir_cliente/<int:id>', methods=['GET'])
def excluir_cliente(id):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return "Cliente excluído com sucesso!"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    criar_tabela() # Chama a função para criar a tabela antes de iniciar a aplicação
    app.run(debug=True)