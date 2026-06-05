"""
Aplicação Flask para Gestão de Computadores - AEVF
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from routes.auth import auth_bp
from routes.alunos import alunos_bp
from middleware.error_handler import register_error_handlers
import os

def create_app(config_name=None):
    """Factory function para criar e configurar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configurar JWT
    jwt = JWTManager(app)
    
    # Registar blueprints/rotas
    app.register_blueprint(auth_bp)
    app.register_blueprint(alunos_bp)
    
    # Registar manipuladores de erro
    register_error_handlers(app)
    
    # Rotas básicas
    @app.route('/api/health', methods=['GET'])
    def health():
        """Verificar se a API está online"""
        return {'status': 'healthy', 'message': 'API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['API_HOST'],
        port=app.config['API_PORT'],
        debug=app.config['DEBUG']
    )