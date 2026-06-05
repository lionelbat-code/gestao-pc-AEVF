"""
Rotas de Computadores de Aluno
"""

from flask import Blueprint, request, jsonify
from models.computador_aluno import ComputadorAluno
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

# Criar blueprint
computadores_aluno_bp = Blueprint('computadores_aluno', __name__, url_prefix='/api/computadores/aluno')

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

@computadores_aluno_bp.route('', methods=['GET'])
@jwt_required()
def list_computadores():
    """
    Listar computadores de aluno (emprestáveis)
    
    Query Parameters:
        - page: Página (padrão: 1)
        - limit: Itens por página (padrão: 20)
        - estado: Filtrar por estado (disponivel, em_emprestimo, em_reparacao, inutilizado)
    
    Response:
        {
            "total": 120,
            "pagina": 1,
            "limite": 20,
            "dados": [...]
        }
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        estado = request.args.get('estado', None, type=str)
        
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({'error': 'Parâmetros inválidos'}), 400
        
        result = ComputadorAluno.list_all(page, limit, estado)
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_aluno_bp.route('/<int:pc_id>', methods=['GET'])
@jwt_required()
def get_computador(pc_id):
    """
    Obter computador de aluno por ID
    
    Response:
        {
            "computador": {...}
        }
    """
    try:
        computador = ComputadorAluno.find_by_id(pc_id)
        
        if not computador:
            return jsonify({'error': 'Computador não encontrado'}), 404
        
        return jsonify({'computador': computador}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_aluno_bp.route('/numero/<numero_serie>', methods=['GET'])
@jwt_required()
def get_by_numero_serie(numero_serie):
    """
    Obter computador pelo número de série
    
    Response:
        {
            "computador": {...}
        }
    """
    try:
        computador = ComputadorAluno.find_by_numero_serie(numero_serie)
        
        if not computador:
            return jsonify({'error': 'Computador não encontrado'}), 404
        
        return jsonify({'computador': computador}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_aluno_bp.route('', methods=['POST'])
@admin_required
def create_computador():
    """
    Criar novo computador de aluno (apenas admin)
    
    Request Body:
        {
            "numero_serie": "SN12345",
            "marca": "Dell",
            "modelo": "Inspiron 15",
            "hotspot": "SIM",
            "sim_card": "SIM12345",
            "data_aquisicao": "2023-01-15",
            "observacoes": "Computador novo"
        }
    
    Response (201):
        {
            "message": "Computador criado com sucesso",
            "computador": {...}
        }
    """
    try:
        data = request.get_json()
        
        # Validar campos obrigatorios
        required_fields = ['numero_serie', 'marca', 'modelo']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Campos obrigatórios: {required_fields}'}), 400
        
        result = ComputadorAluno.create(
            numero_serie=data['numero_serie'],
            marca=data['marca'],
            modelo=data['modelo'],
            hotspot=data.get('hotspot'),
            sim_card=data.get('sim_card'),
            data_aquisicao=data.get('data_aquisicao'),
            observacoes=data.get('observacoes')
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Computador criado com sucesso',
            'computador': result
        }), 201
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_aluno_bp.route('/<int:pc_id>', methods=['PUT'])
@admin_required
def update_computador(pc_id):
    """
    Actualizar computador de aluno (apenas admin)
    
    Request Body:
        {
            "marca": "Dell",
            "modelo": "Inspiron 15",
            "estado": "em_reparacao",
            "observacoes": "Aguarda reparação"
        }
    
    Response:
        {
            "message": "Computador actualizado com sucesso",
            "computador": {...}
        }
    """
    try:
        data = request.get_json()
        
        result = ComputadorAluno.update(pc_id, **data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Computador actualizado com sucesso',
            'computador': result
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_aluno_bp.route('/<int:pc_id>', methods=['DELETE'])
@admin_required
def delete_computador(pc_id):
    """
    Deletar computador de aluno (apenas admin)
    
    Response:
        {
            "message": "Computador de aluno deletado com sucesso"
        }
    """
    try:
        computador = ComputadorAluno.find_by_id(pc_id)
        
        if not computador:
            return jsonify({'error': 'Computador não encontrado'}), 404
        
        result = ComputadorAluno.delete(pc_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_aluno_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """
    Obter estatísticas dos computadores de aluno
    
    Response:
        {
            "total_computadores": 120,
            "disponivel": 80,
            "em_emprestimo": 35,
            "em_reparacao": 5
        }
    """
    try:
        result = ComputadorAluno.get_statistics()
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500
