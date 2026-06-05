"""
Utilitários para hash e validação de passwords
"""

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Gera hash seguro da password usando Werkzeug
    
    Args:
        password (str): Password em texto plano
    
    Returns:
        str: Hash seguro da password
    """
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password, password_hash):
    """
    Verifica se a password corresponde ao hash
    
    Args:
        password (str): Password em texto plano
        password_hash (str): Hash da password
    
    Returns:
        bool: True se corresponde, False caso contrário
    """
    return check_password_hash(password_hash, password)
