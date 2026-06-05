"""
Rotas de Computadores de Sala
"""

from flask import Blueprint, request, jsonify
from models.computador_sala import ComputadorSala
from models.sala import Sala
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

# Criar blueprint
computadores_sala_bp = Blueprint('computadores_sala', __name__, url_prefix='/api/computadores/sala')

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

@computadores_sala_bp.route('', methods=['GET'])
@jwt_required()
def list_computadores():
    """
    Listar computadores de sala
    
    Query Parameters:
        - page: Página (padrão: 1)
        - limit: Itens por página (padrão: 20)
        - estado: Filtrar por estado (funcionando, avariado, necessita_substituicao)
    
    Response:
        {
            "total": 50,
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
        
        result = ComputadorSala.list_all(page, limit, estado)
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_sala_bp.route('/<int:pc_sala_id>', methods=['GET'])
@jwt_required()
def get_computador(pc_sala_id):
    """
    Obter computador de sala por ID
    
    Response:
        {
            "computador": {...}
        }
    """
    try:
        computador = ComputadorSala.find_by_id(pc_sala_id)
        
        if not computador:
            return jsonify({'error': 'Computador não encontrado'}), 404
        
        return jsonify({'computador': computador}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_sala_bp.route('/numero/<numero_serie>', methods=['GET'])
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
        computador = ComputadorSala.find_by_numero_serie(numero_serie)
        
        if not computador:
            return jsonify({'error': 'Computador não encontrado'}), 404
        
        return jsonify({'computador': computador}), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_sala_bp.route('', methods=['POST'])
@admin_required
def create_computador():
    """
    Criar novo computador de sala (apenas admin)
    
    Request Body:
        {
            "sala_id": 1,
            "numero_serie": "SN12345",
            "marca": "Dell",
            "modelo": "Inspiron 15",
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
        required_fields = ['sala_id', 'numero_serie', 'marca', 'modelo']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Campos obrigatórios: {required_fields}'}), 400
        
        result = ComputadorSala.create(
            sala_id=data['sala_id'],
            numero_serie=data['numero_serie'],
            marca=data['marca'],
            modelo=data['modelo'],
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

@computadores_sala_bp.route('/<int:pc_sala_id>', methods=['PUT'])
@admin_required
def update_computador(pc_sala_id):
    """
    Actualizar computador de sala (apenas admin)
    
    Request Body:
        {
            "marca": "Dell",
            "modelo": "Inspiron 15",
            "estado": "avariado",
            "descricao_avaria": "Teclado danificado",
            "data_ultima_manutencao": "2024-01-20",
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
        
        result = ComputadorSala.update(pc_sala_id, **data)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'message': 'Computador actualizado com sucesso',
            'computador': result
        }), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_sala_bp.route('/<int:pc_sala_id>', methods=['DELETE'])
@admin_required
def delete_computador(pc_sala_id):
    """
    Deletar computador de sala (apenas admin)
    
    Response:
        {
            "message": "Computador de sala deletado com sucesso"
        }
    """
    try:
        computador = ComputadorSala.find_by_id(pc_sala_id)
        
        if not computador:
            return jsonify({'error': 'Computador não encontrado'}), 404
        
        result = ComputadorSala.delete(pc_sala_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500

@computadores_sala_bp.route('/by-sala/<int:sala_id>', methods=['GET'])
@jwt_required()
def get_by_sala(sala_id):
    """
    Obter computadores de uma sala específica
    
    Query Parameters:
        - estado: Filtrar por estado (opcional)
    
    Response:
        {
            "sala_id": 1,
            "total": 10,
            "computadores": [...]
        }
    """
    try:
        estado = request.args.get('estado', None, type=str)
        
        # Verificar se sala existe
        sala = Sala.find_by_id(sala_id)
        if not sala:
            return jsonify({'error': 'Sala não encontrada'}), 404
        
        result = ComputadorSala.list_by_sala(sala_id, estado)
        return jsonify(result), 200
    
    except Exception as err:
        return jsonify({'error': str(err)}), 500
