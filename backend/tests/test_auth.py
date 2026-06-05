"""
Testes de Autenticação
"""

import pytest
import sys
import os

# Adicionar pasta backend ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.user import User

class TestAuth:
    """
    Testes de autenticação e utilizadores
    """
    
    @pytest.fixture
    def client(self):
        """
        Criar cliente de teste
        """
        app = create_app('testing')
        with app.test_client() as client:
            yield client
    
    def test_login_success(self, client):
        """
        Testar login com credenciais correctas
        """
        response = client.post('/api/auth/login', json={
            'email': 'admin@aevf.edu',
            'password': 'Admin@123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'admin@aevf.edu'
    
    def test_login_invalid_credentials(self, client):
        """
        Testar login com credenciais incorrectas
        """
        response = client.post('/api/auth/login', json={
            'email': 'admin@aevf.edu',
            'password': 'SenhaErrada'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_login_missing_fields(self, client):
        """
        Testar login sem campos obrigatórios
        """
        response = client.post('/api/auth/login', json={
            'email': 'admin@aevf.edu'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_check_token_valid(self, client):
        """
        Testar verificação de token válido
        """
        # Primeiro fazer login
        login_response = client.post('/api/auth/login', json={
            'email': 'admin@aevf.edu',
            'password': 'Admin@123'
        })
        token = login_response.get_json()['token']
        
        # Verificar token
        response = client.get('/api/auth/check-token', headers={
            'Authorization': f'Bearer {token}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] == True
    
    def test_check_token_invalid(self, client):
        """
        Testar verificação de token inválido
        """
        response = client.get('/api/auth/check-token', headers={
            'Authorization': 'Bearer tokeninvalido'
        })
        
        assert response.status_code == 401
