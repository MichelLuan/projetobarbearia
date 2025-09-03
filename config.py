# -*- coding: utf-8 -*-
"""
Arquivo de configuração do projeto
Aqui você pode alterar as configurações conforme necessário
"""

import os

class Config:
    """Configurações base da aplicação"""
    
    # Chave secreta para sessões (ALTERE ESTA CHAVE EM PRODUÇÃO!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura-aqui'
    
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///barbearia.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de desenvolvimento
    DEBUG = True
    TESTING = False
    
    # Configurações de sessão
    SESSION_COOKIE_SECURE = False  # Mude para True em produção com HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configurações de upload (se necessário no futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'

class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///barbearia.db'

class ProductionConfig(Config):
    """Configurações para ambiente de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Dicionário com todas as configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}





