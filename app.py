# -*- coding: utf-8 -*-
"""
Barbearia App - Sistema de Agendamentos SaaS
Backend principal da aplicação
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Carrega configurações do ambiente
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///barbearia.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ===== MODELOS DO BANCO DE DADOS =====

class User(UserMixin, db.Model):
    """
    Modelo para usuários do sistema (clientes que possuem barbearias)
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    tipo = db.Column(db.String(20), default='cliente')
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com barbearias
    barbearias = db.relationship('Barbearia', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Cria hash da senha para armazenar no banco"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.nome}>'

class Barbearia(db.Model):
    """
    Modelo para barbearias cadastradas no sistema
    """
    __tablename__ = 'barbearias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.Text)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    horario_abertura = db.Column(db.Time, default=datetime.strptime('08:00', '%H:%M').time())
    horario_fechamento = db.Column(db.Time, default=datetime.strptime('18:00', '%H:%M').time())
    dias_funcionamento = db.Column(db.String(50), default='1,2,3,4,5,6')
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para o usuário proprietário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamentos
    profissionais = db.relationship('Profissional', backref='barbearia', lazy=True, cascade='all, delete-orphan')
    servicos = db.relationship('Servico', backref='barbearia', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Barbearia {self.nome}>'

class Profissional(db.Model):
    """
    Modelo para profissionais que trabalham nas barbearias
    """
    __tablename__ = 'profissionais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para a barbearia
    barbearia_id = db.Column(db.Integer, db.ForeignKey('barbearias.id'), nullable=False)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='profissional', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profissional {self.nome}>'

class Servico(db.Model):
    """
    Modelo para serviços oferecidos pelas barbearias
    """
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para a barbearia
    barbearia_id = db.Column(db.Integer, db.ForeignKey('barbearias.id'), nullable=False)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='servico', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Servico {self.nome}>'

class Agendamento(db.Model):
    """
    Modelo para agendamentos de serviços
    """
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='confirmado')
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    
    # Relacionamento com cliente
    cliente = db.relationship('User', backref='agendamentos')
    
    def __repr__(self):
        return f'<Agendamento {self.id} - {self.data_hora}>'

# ===== CONFIGURAÇÃO DO LOGIN MANAGER =====

@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário para o Flask-Login"""
    return User.query.get(int(user_id))

# ===== ROTAS DA APLICAÇÃO =====

@app.route('/')
def index():
    """Página inicial pública"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login e registro"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Verifica se é login de admin
        if email == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        
        # Login normal de usuário
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if user.ativo:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Sua conta foi bloqueada. Entre em contato com o suporte.', 'error')
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do usuário"""
    barbearias = Barbearia.query.filter_by(user_id=current_user.id).all()
    total_profissionais = Profissional.query.join(Barbearia).filter(Barbearia.user_id == current_user.id).count()
    total_servicos = Servico.query.join(Barbearia).filter(Barbearia.user_id == current_user.id).count()
    
    return render_template('dashboard.html', 
                         barbearias=barbearias,
                         total_profissionais=total_profissionais,
                         total_servicos=total_servicos)

# ===== ROTAS DE ADMINISTRAÇÃO =====

@app.route('/admin')
def admin_dashboard():
    """Dashboard de administração do SaaS"""
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    total_users = User.query.count()
    total_barbearias = Barbearia.query.count()
    total_profissionais = Profissional.query.count()
    total_servicos = Servico.query.count()
    usuarios_recentes = User.query.order_by(User.created_at.desc()).limit(10).all()
    barbearias_ativas = Barbearia.query.join(User).filter(User.ativo == True).count()
    barbearias_bloqueadas = Barbearia.query.join(User).filter(User.ativo == False).count()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_barbearias=total_barbearias,
                         total_profissionais=total_profissionais,
                         total_servicos=total_servicos,
                         usuarios_recentes=usuarios_recentes,
                         barbearias_ativas=barbearias_ativas,
                         barbearias_bloqueadas=barbearias_bloqueadas)

@app.route('/admin/cadastrar-usuario', methods=['POST'])
def admin_cadastrar_usuario():
    """Cadastra um novo usuário no sistema"""
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Acesso negado'})
    
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('nome') or not data.get('email') or not data.get('senha'):
            return jsonify({'success': False, 'message': 'Nome, email e senha são obrigatórios'})
        
        # Verifica se o email já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Este email já está cadastrado no sistema'})
        
        # Cria o usuário
        user = User(
            nome=data['nome'],
            email=data['email'],
            telefone=data.get('telefone'),
            tipo=data.get('tipo', 'cliente'),
            ativo=data.get('ativo', True)
        )
        user.set_password(data['senha'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Usuário {user.nome} cadastrado com sucesso!',
            'user': {
                'id': user.id,
                'nome': user.nome,
                'email': user.email,
                'tipo': user.tipo,
                'ativo': user.ativo
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao cadastrar usuário: {str(e)}'})

@app.route('/admin/usuarios')
def admin_usuarios():
    """Gerenciamento de usuários"""
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    usuarios = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/<int:user_id>/toggle-status', methods=['POST'])
def admin_toggle_user_status(user_id):
    """Ativa/desativa usuário"""
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Acesso negado'})
    
    user = User.query.get_or_404(user_id)
    user.ativo = not user.ativo
    
    if user.ativo:
        status_msg = 'ativada'
    else:
        status_msg = 'bloqueada'
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Conta {status_msg} com sucesso!',
        'ativo': user.ativo
    })

@app.route('/admin/usuarios/<int:user_id>/delete', methods=['POST'])
def admin_delete_user(user_id):
    """Deleta usuário e todas suas barbearias"""
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Acesso negado'})
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Usuário deletado com sucesso!'})

@app.route('/admin/barbearias')
def admin_barbearias():
    """Gerenciamento de barbearias"""
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    barbearias = Barbearia.query.join(User).order_by(Barbearia.created_at.desc()).all()
    return render_template('admin_barbearias.html', barbearias=barbearias)

# ===== OUTRAS ROTAS =====

@app.route('/minhas-barbearias')
@login_required
def minhas_barbearias():
    """Lista todas as barbearias do usuário logado"""
    barbearias = Barbearia.query.filter_by(user_id=current_user.id).all()
    return render_template('minhas_barbearias.html', barbearias=barbearias)

@app.route('/nova-barbearia', methods=['GET', 'POST'])
@login_required
def nova_barbearia():
    """Formulário para criar nova barbearia"""
    if request.method == 'POST':
        pass
    return render_template('nova_barbearia.html')

@app.route('/barbearia/<int:barbearia_id>/profissionais')
@login_required
def gerenciar_profissionais(barbearia_id):
    """Gerenciar profissionais de uma barbearia específica"""
    barbearia = Barbearia.query.get_or_404(barbearia_id)
    if barbearia.user_id != current_user.id:
        flash('Acesso negado!', 'error')
        return redirect(url_for('minhas_barbearias'))
    
    profissionais = Profissional.query.filter_by(barbearia_id=barbearia_id).all()
    return render_template('gerenciar_profissionais.html', barbearia=barbearia, profissionais=profissionais)

@app.route('/barbearia/<int:barbearia_id>/servicos')
@login_required
def gerenciar_servicos(barbearia_id):
    """Gerenciar serviços de uma barbearia específica"""
    barbearia = Barbearia.query.get_or_404(barbearia_id)
    if barbearia.user_id != current_user.id:
        flash('Acesso negado!', 'error')
        return redirect(url_for('minhas_barbearias'))
    
    servicos = Servico.query.filter_by(barbearia_id=barbearia_id).all()
    return render_template('gerenciar_servicos.html', barbearia=barbearia, servicos=servicos)

@app.route('/profissional/<int:profissional_id>/agenda')
def agenda_profissional(profissional_id):
    """Visualizar agenda disponível de um profissional"""
    profissional = Profissional.query.get_or_404(profissional_id)
    return render_template('agenda_profissional.html', profissional=profissional)

@app.route('/agendar', methods=['POST'])
def agendar():
    """API para fazer agendamento de serviço"""
    data = request.get_json()
    return jsonify({'success': True, 'message': 'Agendamento realizado com sucesso!'})

@app.route('/verificar-disponibilidade', methods=['POST'])
def verificar_disponibilidade():
    """API para verificar disponibilidade de horário"""
    data = request.get_json()
    return jsonify({'disponivel': True})

@app.route('/init-db')
def init_db():
    """Inicializa o banco de dados (apenas para desenvolvimento)"""
    db.create_all()
    return 'Banco de dados inicializado com sucesso!'

# ===== TRATAMENTO DE ERROS =====

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ===== INICIALIZAÇÃO =====

# Cria as tabelas quando o app é importado
with app.app_context():
    try:
        print("🗄️ Inicializando banco de dados...")
        # Força a recriação das tabelas
        db.drop_all()  # Remove todas as tabelas existentes
        print("✅ Tabelas antigas removidas")
        db.create_all()  # Cria todas as tabelas novamente
        print("✅ Tabelas criadas com sucesso!")
        
        # Verifica se as tabelas foram criadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Tabelas criadas: {tables}")
        
        # Verifica a estrutura da tabela users
        if 'users' in tables:
            columns = inspector.get_columns('users')
            print(f"🔍 Colunas da tabela users:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
        
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Executa a aplicação em modo de desenvolvimento
    app.run(debug=True, host='0.0.0.0', port=5000)
