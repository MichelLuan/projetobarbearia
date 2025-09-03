# -*- coding: utf-8 -*-
"""
Modelos do banco de dados para o sistema de agendamentos
Este arquivo define todas as tabelas e relacionamentos do sistema
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# Cria uma instância temporária para definir os modelos
_temp_db = SQLAlchemy()

class User(UserMixin, _temp_db.Model):
    """
    Modelo para usuários do sistema (clientes que possuem barbearias)
    """
    __tablename__ = 'users'
    
    id = _temp_db.Column(_temp_db.Integer, primary_key=True)
    nome = _temp_db.Column(_temp_db.String(100), nullable=False)
    email = _temp_db.Column(_temp_db.String(120), unique=True, nullable=False)
    password = _temp_db.Column(_temp_db.String(255), nullable=False)  # Mudou de senha_hash para password
    telefone = _temp_db.Column(_temp_db.String(20))
    tipo = _temp_db.Column(_temp_db.String(20), default='cliente')  # 'admin' ou 'cliente'
    ativo = _temp_db.Column(_temp_db.Boolean, default=True)
    created_at = _temp_db.Column(_temp_db.DateTime, default=datetime.utcnow)
    updated_at = _temp_db.Column(_temp_db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com barbearias (um usuário pode ter várias barbearias)
    barbearias = _temp_db.relationship('Barbearia', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Cria hash da senha para armazenar no banco"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.nome}>'

class Barbearia(_temp_db.Model):
    """
    Modelo para barbearias cadastradas no sistema
    """
    __tablename__ = 'barbearias'
    
    id = _temp_db.Column(_temp_db.Integer, primary_key=True)
    nome = _temp_db.Column(_temp_db.String(100), nullable=False)
    endereco = _temp_db.Column(_temp_db.Text)
    telefone = _temp_db.Column(_temp_db.String(20))
    email = _temp_db.Column(_temp_db.String(120))
    horario_abertura = _temp_db.Column(_temp_db.Time, default=datetime.strptime('08:00', '%H:%M').time())
    horario_fechamento = _temp_db.Column(_temp_db.Time, default=datetime.strptime('18:00', '%H:%M').time())
    dias_funcionamento = _temp_db.Column(_temp_db.String(50), default='1,2,3,4,5,6')  # 1=Segunda, 7=Domingo
    ativo = _temp_db.Column(_temp_db.Boolean, default=True)
    created_at = _temp_db.Column(_temp_db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para o usuário proprietário
    user_id = _temp_db.Column(_temp_db.Integer, _temp_db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamentos
    profissionais = _temp_db.relationship('Profissional', backref='barbearia', lazy=True, cascade='all, delete-orphan')
    servicos = _temp_db.relationship('Servico', backref='barbearia', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Barbearia {self.nome}>'

class Profissional(_temp_db.Model):
    """
    Modelo para profissionais que trabalham nas barbearias
    """
    __tablename__ = 'profissionais'
    
    id = _temp_db.Column(_temp_db.Integer, primary_key=True)
    nome = _temp_db.Column(_temp_db.String(100), nullable=False)
    especialidade = _temp_db.Column(_temp_db.String(100))
    telefone = _temp_db.Column(_temp_db.String(20))
    email = _temp_db.Column(_temp_db.String(120))
    ativo = _temp_db.Column(_temp_db.Boolean, default=True)
    created_at = _temp_db.Column(_temp_db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para a barbearia
    barbearia_id = _temp_db.Column(_temp_db.Integer, _temp_db.ForeignKey('barbearias.id'), nullable=False)
    
    # Relacionamentos
    agendamentos = _temp_db.relationship('Agendamento', backref='profissional', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profissional {self.nome}>'

class Servico(_temp_db.Model):
    """
    Modelo para serviços oferecidos pelas barbearias
    """
    __tablename__ = 'servicos'
    
    id = _temp_db.Column(_temp_db.Integer, primary_key=True)
    nome = _temp_db.Column(_temp_db.String(100), nullable=False)
    descricao = _temp_db.Column(_temp_db.Text)
    preco = _temp_db.Column(_temp_db.Numeric(10, 2), nullable=False)
    duracao = _temp_db.Column(_temp_db.Integer, nullable=False)  # Duração em minutos
    ativo = _temp_db.Column(_temp_db.Boolean, default=True)
    created_at = _temp_db.Column(_temp_db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para a barbearia
    barbearia_id = _temp_db.Column(_temp_db.Integer, _temp_db.ForeignKey('barbearias.id'), nullable=False)
    
    # Relacionamentos
    agendamentos = _temp_db.relationship('Agendamento', backref='servico', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Servico {self.nome}>'

class Agendamento(_temp_db.Model):
    """
    Modelo para agendamentos de serviços
    """
    __tablename__ = 'agendamentos'
    
    id = _temp_db.Column(_temp_db.Integer, primary_key=True)
    data_hora = _temp_db.Column(_temp_db.DateTime, nullable=False)
    status = _temp_db.Column(_temp_db.String(20), default='confirmado')  # confirmado, cancelado, realizado
    observacoes = _temp_db.Column(_temp_db.Text)
    created_at = _temp_db.Column(_temp_db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    cliente_id = _temp_db.Column(_temp_db.Integer, _temp_db.ForeignKey('users.id'), nullable=False)
    profissional_id = _temp_db.Column(_temp_db.Integer, _temp_db.ForeignKey('profissionais.id'), nullable=False)
    servico_id = _temp_db.Column(_temp_db.Integer, _temp_db.ForeignKey('servicos.id'), nullable=False)
    
    # Relacionamento com cliente
    cliente = _temp_db.relationship('User', backref='agendamentos')
    
    def __repr__(self):
        return f'<Agendamento {self.id} - {self.data_hora}>'
    
    def verificar_conflito(self):
        """
        Verifica se há conflito de horário com outros agendamentos
        Retorna True se houver conflito, False caso contrário
        """
        # Busca agendamentos do mesmo profissional no mesmo dia
        inicio = self.data_hora
        fim = inicio + timedelta(minutes=self.servico.duracao)
        
        # Busca agendamentos conflitantes
        conflitos = Agendamento.query.filter(
            Agendamento.profissional_id == self.profissional_id,
            Agendamento.id != self.id,  # Exclui o próprio agendamento
            Agendamento.status != 'cancelado',
            _temp_db.or_(
                # Verifica se o início está dentro de outro agendamento
                _temp_db.and_(
                    self.data_hora >= Agendamento.data_hora,
                    self.data_hora < _temp_db.func.datetime(Agendamento.data_hora, f'+{Agendamento.servico.duracao} minutes')
                ),
                # Verifica se o fim está dentro de outro agendamento
                _temp_db.and_(
                    fim > Agendamento.data_hora,
                    fim <= _temp_db.func.datetime(Agendamento.data_hora, f'+{Agendamento.servico.duracao} minutes')
                ),
                # Verifica se engloba outro agendamento
                _temp_db.and_(
                    self.data_hora <= Agendamento.data_hora,
                    fim >= _temp_db.func.datetime(Agendamento.data_hora, f'+{Agendamento.servico.duracao} minutes')
                )
            )
        ).first()
        
        return conflitos is not None

def init_models(database):
    """Inicializa os modelos com a instância do banco de dados"""
    # Atualiza todas as referências de _temp_db para o db real
    for model in [User, Barbearia, Profissional, Servico, Agendamento]:
        model.__table__.metadata = database.metadata
        model.__table__.metadata.bind = database.engine
