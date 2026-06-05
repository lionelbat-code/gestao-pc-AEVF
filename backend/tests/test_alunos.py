"""
Testes de Alunos
"""

import pytest
import sys
import os

# Adicionar pasta backend ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.aluno import Aluno

class TestAlunos:
    """
    Testes de CRUD de alunos
    """
    
    @pytest.fixture
    def client(self):
        """
        Criar cliente de teste
        """
        app = create_app('testing')
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def admin_token(self, client):
        """
        Obter token admin para testes
        """
        response = client.post('/api/auth/login', json={
            'email': 'admin@aevf.edu',
            'password': 'Admin@123'
        })
        return response.get_json()['token']
    
    @pytest.fixture
    def consulta_token(self, client):
        """
        Obter token de consulta para testes
        """
        response = client.post('/api/auth/login', json={
            'email': 'consulta@aevf.edu',
            'password': 'Consulta@123'
        })
        return response.get_json()['token']
    
    def test_create_aluno_success(self, client, admin_token):
        """
        Testar criar aluno com sucesso
        """
        response = client.post(
            '/api/alunos',
            json={
                'numero': '20240001',
                'nome': 'João Silva',
                'nif': '123456789',
                'morada': 'Rua Principal, 123',
                'ee_nome': 'Maria Silva',
                'ee_nif': '987654321',
                'ee_contacto': '912345678',
                'ee_numero_cidadao': '12345678'
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'aluno' in data
        assert data['aluno']['numero'] == '20240001'
        assert data['aluno']['nome'] == 'João Silva'
    
    def test_create_aluno_duplicate_numero(self, client, admin_token):
        """
        Testar criar aluno com número duplicado
        """
        # Criar primeiro aluno
        client.post(
            '/api/alunos',
            json={
                'numero': '20240002',
                'nome': 'João Silva',
                'nif': '123456790',
                'morada': 'Rua Principal, 123',
                'ee_nome': 'Maria Silva',
                'ee_nif': '987654322',
                'ee_contacto': '912345679',
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        # Tentar criar outro com mesmo número
        response = client.post(
            '/api/alunos',
            json={
                'numero': '20240002',
                'nome': 'Outro Aluno',
                'nif': '123456791',
                'morada': 'Rua Nova, 456',
                'ee_nome': 'Outro Encarregado',
                'ee_nif': '987654323',
                'ee_contacto': '912345680',
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_aluno_missing_fields(self, client, admin_token):
        """
        Testar criar aluno sem campos obrigatórios
        """
        response = client.post(
            '/api/alunos',
            json={
                'numero': '20240003',
                'nome': 'João Silva'
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_aluno_not_admin(self, client, consulta_token):
        """
        Testar criar aluno sem permissão admin
        """
        response = client.post(
            '/api/alunos',
            json={
                'numero': '20240004',
                'nome': 'João Silva',
                'nif': '123456792',
                'morada': 'Rua Principal, 123',
                'ee_nome': 'Maria Silva',
                'ee_nif': '987654324',
                'ee_contacto': '912345681',
            },
            headers={'Authorization': f'Bearer {consulta_token}'}
        )
        
        assert response.status_code == 403
    
    def test_list_alunos(self, client, admin_token):
        """
        Testar listar alunos
        """
        response = client.get(
            '/api/alunos',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total' in data
        assert 'dados' in data
        assert 'pagina' in data
    
    def test_get_aluno_by_id(self, client, admin_token):
        """
        Testar obter aluno por ID
        """
        # Criar aluno
        create_response = client.post(
            '/api/alunos',
            json={
                'numero': '20240005',
                'nome': 'João Silva',
                'nif': '123456793',
                'morada': 'Rua Principal, 123',
                'ee_nome': 'Maria Silva',
                'ee_nif': '987654325',
                'ee_contacto': '912345682',
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        aluno_id = create_response.get_json()['aluno']['aluno_id']
        
        # Obter aluno
        response = client.get(
            f'/api/alunos/{aluno_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'aluno' in data
        assert data['aluno']['aluno_id'] == aluno_id
    
    def test_update_aluno(self, client, admin_token):
        """
        Testar actualizar aluno
        """
        # Criar aluno
        create_response = client.post(
            '/api/alunos',
            json={
                'numero': '20240006',
                'nome': 'João Silva',
                'nif': '123456794',
                'morada': 'Rua Principal, 123',
                'ee_nome': 'Maria Silva',
                'ee_nif': '987654326',
                'ee_contacto': '912345683',
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        aluno_id = create_response.get_json()['aluno']['aluno_id']
        
        # Actualizar aluno
        response = client.put(
            f'/api/alunos/{aluno_id}',
            json={
                'nome': 'João Silva Updated',
                'morada': 'Rua Nova, 456'
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['aluno']['nome'] == 'João Silva Updated'
        assert data['aluno']['morada'] == 'Rua Nova, 456'
    
    def test_delete_aluno(self, client, admin_token):
        """
        Testar deletar aluno
        """
        # Criar aluno
        create_response = client.post(
            '/api/alunos',
            json={
                'numero': '20240007',
                'nome': 'João Silva',
                'nif': '123456795',
                'morada': 'Rua Principal, 123',
                'ee_nome': 'Maria Silva',
                'ee_nif': '987654327',
                'ee_contacto': '912345684',
            },
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        aluno_id = create_response.get_json()['aluno']['aluno_id']
        
        # Deletar aluno
        response = client.delete(
            f'/api/alunos/{aluno_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
