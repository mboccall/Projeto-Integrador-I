from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import dotenv_values
import os

app = Flask(__name__, template_folder='templates_folder')
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'clientes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SECRET_KEY'] = "c450f568522f42a5312999a4c271055af7e5a12e61ba1de1312eeffa4f45183c"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class Clientes(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    sobrenome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(15))
    empresa = db.Column(db.String(100))
    checkboxstatus = db.Column(db.String(10))

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(128), nullable=False)

    def __init__(self, email, nome, sobrenome, senha):
        self.email = email
        self.nome = nome
        self.sobrenome = sobrenome
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

# Definindo a função para criar as tabelas dentro do contexto da aplicação Flask
def criar_tabela():
    with app.app_context():
        db.create_all()
        cadastrar_administrador()  # Chama a função que cadastra o administrador

# Cadastra a primeira conta no banco de dados, apartir das informações do .env
def cadastrar_administrador():
    env_variables = dotenv_values(".env")
    nome = env_variables.get("admin_name")
    sobrenome = env_variables.get("admin_surname")
    email = env_variables.get("admin_email")
    senha = env_variables.get("admin_password")
    if email and nome and sobrenome and senha:
        if not Usuario.query.filter_by(email=email).first():
            user = Usuario(email, nome, sobrenome, senha)
            db.session.add(user)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()

@app.route("/", methods=["GET"])
def landingpage():
    return render_template('landingpage.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('consultar_clientes'))
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = Usuario.query.filter_by(email=email).first()

        if not user:
            erro = '<p class="text-danger">Usário não encontrado!</p>'
            return render_template('login.html', erro=erro)

        if not user.verificar_senha(senha):
            erro = '<p class="text-danger">Senha incorreta!</p>'
            return render_template('login.html', erro=erro)

        login_user(user)
        return redirect(url_for('consultar_clientes'))

    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=["POST", "GET"])
@login_required
def register():
    if request.method == 'POST':
        print(request)
        email = request.form["email"]
        nome = request.form["name"]
        sobrenome = request.form["lastname"]
        senha = request.form["senha"]

        if email and nome and sobrenome and senha:
            if not Usuario.query.filter_by(email=email).first():
                user = Usuario(email, nome, sobrenome, senha)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                erro = '<p class="text-danger">Este email já está cadastrado!</p>'
                return render_template('register.html', erro=erro)
        else:
            return redirect(url_for('register'))
    else:
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
@login_required
def consultar_clientes():
    clientes = Clientes.query.all()
    clientes_info = []
    for cliente in clientes:
        cliente_info = [ cliente.id, cliente.nome, cliente.sobrenome, cliente.email, cliente.telefone, cliente.empresa, cliente.checkboxstatus]
        clientes_info.append(cliente_info)
    return render_template('resultados.html', clientes=clientes_info)


@app.route('/editar_cliente/<int:id>', methods=['POST'])
@login_required
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
@login_required
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
