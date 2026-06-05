"""
Rotas de Autenticação (Login/Register)
"""

from flask import Blueprint, request, jsonify
from models.user import User
from utils.jwt_utils import generate_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps

# Criar blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ============================================================
# Middleware de autorização
# ============================================================

def admin_required(fn):
    """
    Decorador para rotas que requerem account admin
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

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login do utilizador
    
    Request:
        {
            "email": "admin@aevf.edu",
            "password": "Admin@123"
        }
    
    Response:
        {
            "token": "eyJhbGciOiJIUzI1NiIs...",
            "user": {
                "utilizador_id": 1,
                "email": "admin@aevf.edu",
                "nome_completo": "Administrador AEVF",
                "tipo_conta": "admin"
            }
        }
    """
    try:
        data = request.get_json()
        
        # Validar input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e password são obrigatórios'}), 400
        
        # Verificar credenciais
        user = User.verify_credentials(data['email'], data['password'])
        
        if not user:
            return jsonify({'error': 'Email ou password incorretos'}), 401
        
        # Gerar token
        token = generate_token(user['utilizador_id'], user['tipo_conta'])
        
        return jsonify({
            'token': token,
            'user': user
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@auth_bp.route('/register', methods=['POST'])
@admin_required
def register():
    """
    Registar novo utilizador (apenas admin)
    
    Request:
        {
            "email": "novo@aevf.edu",
            "nome_completo": "Novo Utilizador",
            "password": "Senha@123",
            "tipo_conta": "consulta"
        }
    
    Response:
        {
            "message": "Utilizador criado com sucesso",
            "user": {...}
        }
    """
    try:
        data = request.get_json()
        
        # Validar input
        required_fields = ['email', 'nome_completo', 'password', 'tipo_conta']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Campos obrigatórios: {required_fields}'}), 400
        
        # Validar tipo_conta
        if data['tipo_conta'] not in ['admin', 'consulta']:
            return jsonify({'error': 'tipo_conta deve ser "admin" ou "consulta"'}), 400
        
        # Criar utilizador
        result = User.create(
            email=data['email'],
            nome_completo=data['nome_completo'],
            password=data['password'],
            tipo_conta=data['tipo_conta']
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Utilizador criado com sucesso',
            'user': result
        }), 201
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obter dados do utilizador atual (autenticado)
    
    Response:
        {
            "user": {...}
        }
    """
    try:
        utilizador_id = get_jwt_identity()
        user = User.find_by_id(utilizador_id)
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        return jsonify({'user': user}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@auth_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """
    Listar todos os utilizadores (apenas admin)
    
    Query Parameters:
        - page: Página (padrão: 1)
        - limit: Itens por página (padrão: 20)
    
    Response:
        {
            "total": 10,
            "pagina": 1,
            "limite": 20,
            "dados": [...]
        }
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({'error': 'Parâmetros inválidos'}), 400
        
        result = User.list_all(page, limit)
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@auth_bp.route('/users/<int:utilizador_id>', methods=['PUT'])
@admin_required
def update_user(utilizador_id):
    """
    Actualizar utilizador (apenas admin)
    
    Request:
        {
            "nome_completo": "Novo Nome",
            "tipo_conta": "admin",
            "ativo": true
        }
    
    Response:
        {
            "message": "Utilizador actualizado",
            "user": {...}
        }
    """
    try:
        data = request.get_json()
        
        result = User.update(utilizador_id, **data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Utilizador actualizado com sucesso',
            'user': result
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@auth_bp.route('/check-token', methods=['GET'])
@jwt_required()
def check_token():
    """
    Verificar se o token é válido
    
    Response:
        {
            "valid": true,
            "utilizador_id": 1,
            "tipo_conta": "admin"
        }
    """
    try:
        utilizador_id = get_jwt_identity()
        claims = get_jwt()
        
        return jsonify({
            'valid': True,
            'utilizador_id': utilizador_id,
            'tipo_conta': claims.get('tipo_conta')
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 401
