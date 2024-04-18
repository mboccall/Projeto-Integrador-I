from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='templates_folder')
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'clientes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    sobrenome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(15))
    empresa = db.Column(db.String(100))
    checkboxstatus = db.Column(db.String(10))

# Definindo a função para criar as tabelas dentro do contexto da aplicação Flask
def criar_tabela():
    with app.app_context():
        db.create_all()

@app.route("/", methods=["GET"])
def landingpage():
    return render_template('landingpage.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template('login.html')

@app.route("/register", methods=["POST", "GET"])
def register():
    return render_template('register.html')

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
    novo_cliente = Clientes(nome=nome, sobrenome=sobrenome, email=email, telefone=telefone, empresa=empresa, checkboxstatus=checkboxstatus)
    db.session.add(novo_cliente)
    db.session.commit()

    return redirect(url_for('concluido'))

@app.route('/consultar_clientes')
def consultar_clientes():
    clientes = Clientes.query.all()
    clientes_info = []
    for cliente in clientes:
        cliente_info = [ cliente.id, cliente.nome, cliente.sobrenome, cliente.email, cliente.telefone, cliente.empresa, cliente.checkboxstatus]
        clientes_info.append(cliente_info)
    return render_template('resultados.html', clientes=clientes_info)


@app.route('/editar_cliente/<int:id>', methods=['POST'])
def editar_cliente(id):
    cliente = Clientes.query.get_or_404(id)
    cliente.nome = request.json["nome"]
    cliente.sobrenome = request.json["sobrenome"]
    cliente.email = request.json["email"]
    cliente.telefone = request.json["telefone"]
    cliente.empresa = request.json["empresa"]
    cliente.checkboxstatus = request.json["checkboxstatus"]
    db.session.commit()

    return jsonify({'nome': cliente.nome, 'sobrenome': cliente.sobrenome, 'email': cliente.email, 'telefone': cliente.telefone, 'empresa': cliente.empresa, 'checkboxstatus': cliente.checkboxstatus})

@app.route('/excluir_cliente/<int:id>', methods=['GET'])
def excluir_cliente(id):
    cliente = Clientes.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return "Cliente excluído com sucesso!"

@app.route('/cadastro')
def index():
    return render_template('index.html')

@app.route('/concluido')
def concluido():
    return render_template('concluido.html')

if __name__ == '__main__':
    criar_tabela() # Chama a função para criar a tabela antes de iniciar a aplicação
    app.run(debug=True)
