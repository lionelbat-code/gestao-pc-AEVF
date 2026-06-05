"""
Modelo de Utilizador
"""

from models.database import Database
from utils.password import hash_password, verify_password
from datetime import datetime

class User:
    """
    Classe para gerenciar utilizadores
    """
    
    @staticmethod
    def create(email, nome_completo, password, tipo_conta='consulta'):
        """
        Criar novo utilizador
        
        Args:
            email (str): Email do utilizador
            nome_completo (str): Nome completo
            password (str): Password em texto plano
            tipo_conta (str): 'admin' ou 'consulta'
        
        Returns:
            dict: Dados do utilizador criado ou erro
        """
        try:
            # Verificar se email já existe
            existing = User.find_by_email(email)
            if existing:
                return {'error': 'Este email já está registado'}
            
            # Hash da password
            password_hash = hash_password(password)
            
            # Inserir na BD
            query = """
                INSERT INTO utilizadores (email, nome_completo, password_hash, tipo_conta, ativo)
                VALUES (%s, %s, %s, %s, TRUE)
            """
            utilizador_id = Database.execute_update(query, (email, nome_completo, password_hash, tipo_conta))
            
            return {
                'utilizador_id': utilizador_id,
                'email': email,
                'nome_completo': nome_completo,
                'tipo_conta': tipo_conta
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def find_by_email(email):
        """
        Procurar utilizador pelo email
        
        Args:
            email (str): Email a procurar
        
        Returns:
            dict: Dados do utilizador ou None
        """
        try:
            query = "SELECT * FROM utilizadores WHERE email = %s"
            return Database.execute_one(query, (email,))
        except Exception as err:
            return None
    
    @staticmethod
    def find_by_id(utilizador_id):
        """
        Procurar utilizador pelo ID
        
        Args:
            utilizador_id (int): ID do utilizador
        
        Returns:
            dict: Dados do utilizador ou None
        """
        try:
            query = "SELECT utilizador_id, email, nome_completo, tipo_conta, ativo FROM utilizadores WHERE utilizador_id = %s"
            return Database.execute_one(query, (utilizador_id,))
        except Exception as err:
            return None
    
    @staticmethod
    def verify_credentials(email, password):
        """
        Verificar credenciais de login
        
        Args:
            email (str): Email do utilizador
            password (str): Password em texto plano
        
        Returns:
            dict: Dados do utilizador se correcto, None se incorreto
        """
        try:
            user = User.find_by_email(email)
            
            if not user:
                return None
            
            if not user.get('ativo'):
                return None
            
            # Verificar password
            if verify_password(password, user['password_hash']):
                # Actualizar data do último login
                query = "UPDATE utilizadores SET data_ultimo_login = NOW() WHERE utilizador_id = %s"
                Database.execute_update(query, (user['utilizador_id'],))
                
                # Retornar sem a password hash
                return {
                    'utilizador_id': user['utilizador_id'],
                    'email': user['email'],
                    'nome_completo': user['nome_completo'],
                    'tipo_conta': user['tipo_conta']
                }
            
            return None
        except Exception as err:
            return None
    
    @staticmethod
    def update(utilizador_id, **kwargs):
        """
        Actualizar dados do utilizador
        
        Args:
            utilizador_id (int): ID do utilizador
            **kwargs: Campos a actualizar (nome_completo, tipo_conta, ativo)
        
        Returns:
            dict: Dados actualizados ou erro
        """
        try:
            allowed_fields = ['nome_completo', 'tipo_conta', 'ativo']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return {'error': 'Nenhum campo para actualizar'}
            
            # Construir query dinamicamente
            set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE utilizadores SET {set_clause}, data_atualizacao = NOW() WHERE utilizador_id = %s"
            
            values = list(updates.values()) + [utilizador_id]
            Database.execute_update(query, values)
            
            return User.find_by_id(utilizador_id)
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def list_all(page=1, limit=20):
        """
        Listar todos os utilizadores (admin only)
        
        Args:
            page (int): Página (começa em 1)
            limit (int): Itens por página
        
        Returns:
            dict: Lista de utilizadores e total
        """
        try:
            offset = (page - 1) * limit
            
            # Contar total
            count_query = "SELECT COUNT(*) as total FROM utilizadores"
            count_result = Database.execute_one(count_query)
            total = count_result['total'] if count_result else 0
            
            # Listar
            query = """
                SELECT utilizador_id, email, nome_completo, tipo_conta, ativo, data_criacao, data_ultimo_login
                FROM utilizadores
                ORDER BY data_criacao DESC
                LIMIT %s OFFSET %s
            """
            users = Database.execute_query(query, (limit, offset))
            
            return {
                'total': total,
                'pagina': page,
                'limite': limit,
                'dados': users
            }
        except Exception as err:
            return {'error': str(err)}
