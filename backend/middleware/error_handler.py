"""
Manipulador de erros global
"""

from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException

def register_error_handlers(app):
    """
    Registar manipuladores de erro
    
    Args:
        app: Aplicação Flask
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Requisição inválida'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Não autorizado'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Permissão negada'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso não encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    @app.errorhandler(JWTExtendedException)
    def jwt_error(error):
        return jsonify({'error': 'Token inválido ou expirado'}), 401
