"""
Rotas de Salas
"""

from flask import Blueprint, request, jsonify
from models.sala import Sala
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

# Criar blueprint
salas_bp = Blueprint('salas', __name__, url_prefix='/api/salas')

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

@salas_bp.route('', methods=['GET'])
@jwt_required()
def list_salas():
    """
    Listar salas
    
    Query Parameters:
        - page: Página (padrão: 1)
        - limit: Itens por página (padrão: 20)
        - ativo: true/false
    
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
        ativo_param = request.args.get('ativo', 'true', type=str).lower()
        ativo = ativo_param == 'true'
        
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({'error': 'Parâmetros inválidos'}), 400
        
        result = Sala.list_all(page, limit, ativo)
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@salas_bp.route('/<int:sala_id>', methods=['GET'])
@jwt_required()
def get_sala(sala_id):
    """
    Obter sala por ID
    
    Response:
        {
            "sala": {...}
        }
    """
    try:
        sala = Sala.find_by_id(sala_id)
        
        if not sala:
            return jsonify({'error': 'Sala não encontrada'}), 404
        
        return jsonify({'sala': sala}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@salas_bp.route('', methods=['POST'])
@admin_required
def create_sala():
    """
    Criar nova sala (apenas admin)
    
    Request Body:
        {
            "numero_sala": "A101",
            "localizacao": "Piso 1, Ala A",
            "capacidade_alunos": 30,
            "observacoes": "Sala com quadro inteligente"
        }
    
    Response (201):
        {
            "message": "Sala criada com sucesso",
            "sala": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('numero_sala'):
            return jsonify({'error': 'Número da sala é obrigatório'}), 400
        
        result = Sala.create(
            numero_sala=data['numero_sala'],
            localizacao=data.get('localizacao'),
            capacidade_alunos=data.get('capacidade_alunos'),
            observacoes=data.get('observacoes')
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Sala criada com sucesso',
            'sala': result
        }), 201
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@salas_bp.route('/<int:sala_id>', methods=['PUT'])
@admin_required
def update_sala(sala_id):
    """
    Actualizar sala (apenas admin)
    
    Request Body:
        {
            "numero_sala": "A101",
            "localizacao": "Piso 1, Ala A",
            "capacidade_alunos": 30,
            "observacoes": "Sala com quadro inteligente",
            "ativo": true
        }
    
    Response:
        {
            "message": "Sala actualizada com sucesso",
            "sala": {...}
        }
    """
    try:
        data = request.get_json()
        
        result = Sala.update(sala_id, **data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Sala actualizada com sucesso',
            'sala': result
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@salas_bp.route('/<int:sala_id>', methods=['DELETE'])
@admin_required
def delete_sala(sala_id):
    """
    Deletar sala (apenas admin)
    
    Response:
        {
            "message": "Sala deletada com sucesso"
        }
    """
    try:
        sala = Sala.find_by_id(sala_id)
        
        if not sala:
            return jsonify({'error': 'Sala não encontrada'}), 404
        
        result = Sala.delete(sala_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500
