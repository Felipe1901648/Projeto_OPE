from datetime import *
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:UM@tres4@localhost:5432/OPE"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '1234'
tempo = datetime.now()
hora = tempo.strftime('%H:%M')
dia = tempo.strftime('%d/%m/%Y')


class Produtos(db.Model):
    __tablename__ = 'Produtos_001'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100))
    unidades = db.Column(db.Integer())
    valor = db.Column(db.Float(precision='32'))


    def __init__(self, descricao, unidades, valor):
        self.descricao = descricao
        self.unidades = unidades
        self.valor = valor


class Cadastro(db.Model):
    __tablename__ = 'Cadastro_002'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    telefone = db.Column(db.String(13))
    login = db.Column(db.String(20))
    senha = db.Column(db.String(20))
    endereco =  db.Column(db.String(60))
    numero_casa =  db.Column(db.Integer())

    def __init__(self, nome, telefone, login, senha, endereco, numero_casa):
        self.nome = nome
        self.telefone = telefone
        self.login = login
        self.senha = senha
        self.endereco = endereco
        self.numero_casa = numero_casa

class Movimentacao(db.Model):
    __tablename__ = 'Movimentacao_004'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(30))
    descricao = db.Column(db.String(100))
    quantidade =  db.Column(db.Integer())
    data = db.Column(db.String(10))
    hora = db.Column(db.String(5))
    valor = db.Column(db.String(30))

    def __init__(self, usuario, descricao, quantidade, data, hora, valor):
        self.usuario = usuario
        self.descricao = descricao
        self.quantidade = quantidade
        self.data = data
        self.hora = hora
        self.valor = valor

class Fornecedores(db.Model):
    __tablename__ = 'Fornecedores_001'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    email =  db.Column(db.String(50))
    telefone = db.Column(db.String(13))
    prazo_entrega = db.Column(db.String(40))

    def __init__(self, empresa, endereco, email, telefone, prazo_entrega):
        self.empresa = empresa
        self.endereco = endereco
        self.email = email
        self.telefone = telefone
        self.prazo_entrega = prazo_entrega

class LoginForm(FlaskForm):
    login = StringField('nome', validators=[DataRequired()])
    senha = PasswordField('senha')
    botao = SubmitField('botao')
    


@app.route("/", methods=['GET', 'POST'])
def login():
    cadastro = Cadastro.query.all()
    form = LoginForm()
    if form.validate_on_submit():
        for info in cadastro:
            if info.login == form.login.data:
                if info.login and info.senha == form.senha.data:
                    session['username'] = info.nome
                    navegador = make_response(redirect("indexprinc"))
                    navegador.set_cookie('login', info.nome, samesite = "Strict")
                    return navegador
    session['username'] = False
    return render_template("login.html", form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        if request.form['submit_button'] == 'Sim':
            session.pop('username', None)
            return redirect(url_for('login'))
    return render_template('logouti.html')

@app.route("/indexprinc")
def indexprinc():
    if session['username'] == False:
        return render_template('autenticado.html')
    return render_template("indexprinc.html")

@app.route("/produtos")
def index():
    if session['username'] == False:
        return render_template('autenticado.html')
    clientes = Produtos.query.all()
    return render_template("index.html", clientes=clientes)

@app.route("/fornecedores")
def fornecimento():
    if session['username'] == False:
        return render_template('autenticado.html')
    fornecedores = Fornecedores.query.all()
    return render_template("fornecedores.html", fornecedores=fornecedores)

@app.route("/relatorio")
def movimentacao():
    if session['username'] == False:
        return render_template('autenticado.html')
    movimentos = Movimentacao.query.all()
    return render_template("movimentacao.html", movimentos=movimentos)    

@app.route("/usuarios")
def usuarios():
    if session['username'] == False:
        return render_template('autenticado.html')
    usuarios = Cadastro.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/add_fornecedores", methods=['GET','POST']) 
def add_fornecedores():
    if request.method == 'POST':
        cadastro = Fornecedores(request.form['empresa'], request.form['endereco'], request.form['email'], request.form['contato'], request.form['entrega'])
        db.session.add(cadastro)
        db.session.commit()
        return redirect(url_for('fornecimento'))  
    return render_template('add_fornecedores.html')

@app.route("/add_cadastro", methods=['GET','POST']) 
def add_cadastro():
    if request.method == 'POST':
        cadastro = Cadastro(request.form['nome'], request.form['telefone'], request.form['login'], request.form['senha'], request.form['endereco'], request.form['numero_casa'])
        db.session.add(cadastro)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('add_cadastro.html')

@app.route("/add", methods=['GET','POST']) 
def add():
    user = session['username']
    if session['username'] == False:
        return render_template('autenticado.html')
    if request.method == 'POST':
        tempo = datetime.now()
        hora = tempo.strftime('%H:%M')
        dia = tempo.strftime('%d/%m/%Y')
        cliente = Produtos(request.form['descricao'], request.form['unidades'], request.form['valor'])
        movimentos = Movimentacao(f'{user} adicionou', request.form['descricao'], request.form['unidades'], dia, hora, request.form['valor'])
        db.session.add(cliente)
        db.session.add(movimentos)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/edit_usuarios/<int:id>", methods=['GET', 'POST'])
def edit_usuarios(id):
    if session['username'] == False:
        return render_template('autenticado.html')
    usuarios = Cadastro.query.get(id)
    if request.method == 'POST':
        usuarios.nome = request.form['nome']
        usuarios.login = request.form['login']
        usuarios.endereco = request.form['endereco']
        usuarios.telefone = request.form['telefone']
        db.session.commit()
        return redirect(url_for('usuarios'))
    return render_template("edit_cadastro.html", usuarios=usuarios)

@app.route("/edit_fornecedores/<int:id>", methods=['GET', 'POST'])
def edit_fornecedores(id):
    if session['username'] == False:
        return render_template('autenticado.html')
    usuarios = Fornecedores.query.get(id)
    if request.method == 'POST':
        usuarios.empresa = request.form['empresa']
        usuarios.endereco = request.form['endereco']
        usuarios.email = request.form['email']
        usuarios.telefone = request.form['contato']
        usuarios.prazo_entrega = request.form['entrega']
        db.session.commit()
        return redirect(url_for('fornecimento'))
    return render_template("edit_fornecedores.html", usuarios=usuarios)

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    user = session['username']
    if session['username'] == False:
        return render_template('autenticado.html')
    cliente = Produtos.query.get(id)
    if request.method == 'POST':
        tempo = datetime.now()
        hora = tempo.strftime('%H:%M')
        dia = tempo.strftime('%d/%m/%Y')
        movimentos = Movimentacao(f'{user} alterou', '{0} para {1}' .format(cliente.descricao, request.form['descricao']), request.form['unidades'], dia, hora, '{0} para {1}' .format(cliente.valor, request.form['valor']))
        db.session.add(movimentos)
        cliente.descricao = request.form['descricao']
        cliente.unidades = request.form['unidades']
        cliente.valor = request.form['valor']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', cliente=cliente)

@app.route("/deletar_fornecedor/<int:id>")
def deletar_fornecedor(id):
    if session['username'] == False:
        return render_template('autenticado.html')
    usuario = Fornecedores.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('fornecimento'))

@app.route("/deletar_cadastro/<int:id>")
def deletar_cadastro(id):
    if session['username'] == False:
        return render_template('autenticado.html')
    usuario = Cadastro.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios'))

@app.route("/delete/<int:id>")
def delete(id):
    user = session['username']
    tempo = datetime.now()
    hora = tempo.strftime('%H:%M')
    dia = tempo.strftime('%d/%m/%Y')
    if session['username'] == False:
        return render_template('autenticado.html')
    cliente = Produtos.query.get(id)
    movimentos = Movimentacao(f'{user} removeu', cliente.descricao, cliente.unidades, dia, hora, cliente.valor)
    db.session.delete(cliente)
    db.session.add(movimentos)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug= True)
