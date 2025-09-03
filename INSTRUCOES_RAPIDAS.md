# 🚀 Instruções Rápidas - Barbearia App

## ⚡ Começar em 5 minutos!

### 1. Instalar Python (se não tiver)
- Baixe Python 3.8+ em: https://python.org
- Marque "Add Python to PATH" na instalação

### 2. Abrir terminal/prompt na pasta do projeto
```bash
cd "c:\Users\Usuario\Desktop\Projeto App barbeiro"
```

### 3. Criar ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação
```bash
python run.py
```

### 6. Acessar no navegador
🌐 **http://localhost:5000**

---

## 📱 Como usar o sistema

### Primeiro acesso:
1. Clique em "Criar Conta"
2. Preencha seus dados
3. Faça login

### Criar barbearia:
1. No dashboard, clique "Nova Barbearia"
2. Preencha nome, endereço, telefone
3. Configure horários de funcionamento

### Adicionar profissionais:
1. Acesse "Minhas Barbearias"
2. Clique na barbearia
3. "Gerenciar Profissionais"
4. Adicione nome, especialidade, contato

### Configurar serviços:
1. Na mesma barbearia
2. "Gerenciar Serviços"
3. Adicione nome, preço, duração

### Receber agendamentos:
- Os clientes acessam a agenda dos profissionais
- Sistema verifica disponibilidade automaticamente
- Evita conflitos de horário

---

## 🔧 Comandos úteis

### Parar a aplicação:
```
Ctrl + C (no terminal)
```

### Reativar ambiente virtual:
```bash
venv\Scripts\activate
```

### Ver dependências instaladas:
```bash
pip list
```

### Atualizar dependências:
```bash
pip install -r requirements.txt --upgrade
```

---

## 🐛 Problemas comuns

### Erro "porta já em uso":
- Feche outros programas que usem porta 5000
- Ou mude a porta no arquivo `run.py`

### Erro de dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de banco:
- Acesse: http://localhost:5000/init-db
- Ou delete o arquivo `barbearia.db` e reinicie

---

## 📚 Arquivos importantes

- `app.py` - Aplicação principal
- `models.py` - Estrutura do banco
- `templates/` - Páginas HTML
- `static/` - CSS, JavaScript, imagens
- `run.py` - Execução para desenvolvimento

---

## 🎯 Próximos passos

1. **Teste o sistema** - Crie uma conta e explore
2. **Personalize** - Altere cores, logos, textos
3. **Adicione funcionalidades** - Modifique o código
4. **Deploy** - Coloque em produção quando estiver pronto

---

## 💡 Dicas

- **Sempre ative o ambiente virtual** antes de executar
- **Use `python run.py`** para desenvolvimento
- **O banco é criado automaticamente** na primeira execução
- **PWA funciona offline** após primeira visita
- **Todas as alterações** são comentadas no código

---

**🎉 Pronto! Seu sistema de barbearia está funcionando!**










