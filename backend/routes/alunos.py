"""
Rotas de Alunos (CRUD)
"""

from flask import Blueprint, request, jsonify
from models.aluno import Aluno
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

# Criar blueprint
alunos_bp = Blueprint('alunos', __name__, url_prefix='/api/alunos')

# ============================================================
# Middleware de autorização
# ============================================================

def admin_required(fn):
    """
    Decorador para rotas que requerem conta admin
    """
    @wraps(fn)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if claims.get('tipo_conta') != 'admin':
            return jsonify({'error': 'Permissão negada. É necessária conta admin'}), 403
        return fn(*args, **kwargs)
    return decorated_function

# ============================================================
# ENDPOINTS
# ============================================================

@alunos_bp.route('', methods=['GET'])
@jwt_required()
def list_alunos():
    """
    Listar alunos
    
    Query Parameters:
        - page: Página (padrão: 1)
        - limit: Itens por página (padrão: 20, máximo: 100)
        - search: Procurar por nome ou número
        - ativo: true/false (padrão: true)
    
    Response:
        {
            "total": 150,
            "pagina": 1,
            "limite": 20,
            "dados": [...]
        }
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        search = request.args.get('search', None, type=str)
        ativo_param = request.args.get('ativo', 'true', type=str).lower()
        ativo = ativo_param == 'true'
        
        # Validar parâmetros
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({'error': 'Parâmetros inválidos'}), 400
        
        result = Aluno.list_all(page, limit, ativo, search)
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@alunos_bp.route('/<int:aluno_id>', methods=['GET'])
@jwt_required()
def get_aluno(aluno_id):
    """
    Obter aluno por ID
    
    Response:
        {
            "aluno": {...}
        }
    """
    try:
        aluno = Aluno.find_by_id(aluno_id)
        
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        return jsonify({'aluno': aluno}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@alunos_bp.route('/numero/<numero>', methods=['GET'])
@jwt_required()
def get_aluno_by_numero(numero):
    """
    Obter aluno por número
    
    Response:
        {
            "aluno": {...}
        }
    """
    try:
        aluno = Aluno.find_by_numero(numero)
        
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        return jsonify({'aluno': aluno}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@alunos_bp.route('', methods=['POST'])
@admin_required
def create_aluno():
    """
    Criar novo aluno (apenas admin)
    
    Request Body:
        {
            "numero": "20230001",
            "nome": "João Silva",
            "nif": "123456789",
            "morada": "Rua Principal, 123",
            "ee_nome": "Maria Silva",
            "ee_nif": "987654321",
            "ee_contacto": "912345678",
            "ee_numero_cidadao": "12345678"
        }
    
    Response:
        {
            "message": "Aluno criado com sucesso",
            "aluno": {...}
        }
    """
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['numero', 'nome', 'nif', 'morada', 'ee_nome', 'ee_nif', 'ee_contacto']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Campos obrigatórios: {required_fields}'}), 400
        
        result = Aluno.create(
            numero=data['numero'],
            nome=data['nome'],
            nif=data['nif'],
            morada=data['morada'],
            ee_nome=data['ee_nome'],
            ee_nif=data['ee_nif'],
            ee_contacto=data['ee_contacto'],
            ee_numero_cidadao=data.get('ee_numero_cidadao')
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Aluno criado com sucesso',
            'aluno': result
        }), 201
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@alunos_bp.route('/<int:aluno_id>', methods=['PUT'])
@admin_required
def update_aluno(aluno_id):
    """
    Actualizar aluno (apenas admin)
    
    Request Body:
        {
            "nome": "João Silva Updated",
            "morada": "Rua Nova, 456",
            ...
        }
    
    Response:
        {
            "message": "Aluno actualizado com sucesso",
            "aluno": {...}
        }
    """
    try:
        data = request.get_json()
        
        result = Aluno.update(aluno_id, **data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Aluno actualizado com sucesso',
            'aluno': result
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@alunos_bp.route('/<int:aluno_id>', methods=['DELETE'])
@admin_required
def delete_aluno(aluno_id):
    """
    Deletar aluno (apenas admin)
    
    Response:
        {
            "message": "Aluno deletado com sucesso"
        }
    """
    try:
        aluno = Aluno.find_by_id(aluno_id)
        
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        result = Aluno.delete(aluno_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@alunos_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """
    Obter estatísticas dos alunos
    
    Response:
        {
            "total_alunos": 150
        }
    """
    try:
        result = Aluno.get_statistics()
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500
