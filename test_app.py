# -*- coding: utf-8 -*-
"""
Arquivo de teste para verificar se a aplicação está funcionando
Execute este arquivo para testar as funcionalidades básicas
"""

import requests
import json
from datetime import datetime, timedelta

def test_app():
    """Testa as funcionalidades básicas da aplicação"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testando Barbearia App...")
    print("=" * 50)
    
    # Teste 1: Verificar se a aplicação está rodando
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Aplicação está rodando em", base_url)
        else:
            print("❌ Aplicação retornou status:", response.status_code)
            return
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao conectar com a aplicação:", e)
        print("💡 Certifique-se de que a aplicação está rodando com: python app.py")
        return
    
    # Teste 2: Verificar rotas principais
    rotas = [
        "/login",
        "/dashboard",
        "/minhas-barbearias"
    ]
    
    print("\n🔍 Testando rotas principais...")
    for rota in rotas:
        try:
            response = requests.get(base_url + rota, timeout=5)
            if response.status_code in [200, 302]:  # 302 é redirecionamento para login
                print(f"✅ {rota} - OK")
            else:
                print(f"❌ {rota} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {rota} - Erro: {e}")
    
    # Teste 3: Verificar API de verificação de disponibilidade
    print("\n🔍 Testando API de disponibilidade...")
    try:
        dados_teste = {
            "profissional_id": 1,
            "servico_id": 1,
            "data_hora": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        response = requests.post(
            base_url + "/verificar-disponibilidade",
            json=dados_teste,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ API de verificação de disponibilidade - OK")
            try:
                data = response.json()
                print(f"   Resposta: {data}")
            except:
                print("   Resposta não é JSON válido")
        else:
            print(f"❌ API de verificação - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ API de verificação - Erro: {e}")
    
    # Teste 4: Verificar banco de dados
    print("\n🔍 Testando inicialização do banco...")
    try:
        response = requests.get(base_url + "/init-db", timeout=5)
        if response.status_code == 200:
            print("✅ Banco de dados inicializado com sucesso")
        else:
            print(f"❌ Erro ao inicializar banco - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testes concluídos!")
    print("\n💡 Para usar o sistema:")
    print("1. Acesse:", base_url)
    print("2. Clique em 'Criar Conta' para começar")
    print("3. Faça login e crie sua primeira barbearia")
    print("4. Configure profissionais e serviços")
    print("5. Comece a receber agendamentos!")

if __name__ == "__main__":
    test_app()










