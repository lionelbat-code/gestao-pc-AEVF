"""
Utilitários para JWT (JSON Web Tokens)
"""

from flask_jwt_extended import create_access_token
from datetime import timedelta
from config import config
import os

def generate_token(identity, tipo_conta='consulta'):
    """
    Gera um token JWT
    
    Args:
        identity (int): ID do utilizador
        tipo_conta (str): Tipo de conta (admin ou consulta)
    
    Returns:
        str: Token JWT
    """
    additional_claims = {'tipo_conta': tipo_conta}
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims
    )
    return access_token
