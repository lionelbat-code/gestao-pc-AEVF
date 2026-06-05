"""
Modelo de Sala
"""

from models.database import Database
from datetime import datetime

class Sala:
    """
    Classe para gerenciar salas de aula
    """
    
    @staticmethod
    def create(numero_sala, localizacao=None, capacidade_alunos=None, observacoes=None):
        """
        Criar nova sala
        
        Args:
            numero_sala (str): Número da sala (único)
            localizacao (str): Localização
            capacidade_alunos (int): Capacidade de alunos
            observacoes (str): Observações
        
        Returns:
            dict: Dados da sala criada ou erro
        """
        try:
            if not numero_sala:
                return {'error': 'Número da sala é obrigatorório'}
            
            # Verificar se número já existe
            existing = Database.execute_one(
                "SELECT sala_id FROM salas WHERE numero_sala = %s",
                (numero_sala,)
            )
            if existing:
                return {'error': 'Esta sala já existe'}
            
            # Inserir sala
            query = """
                INSERT INTO salas 
                (numero_sala, localizacao, capacidade_alunos, observacoes, ativo)
                VALUES (%s, %s, %s, %s, TRUE)
            """
            sala_id = Database.execute_update(
                query,
                (numero_sala, localizacao, capacidade_alunos, observacoes)
            )
            
            return {
                'sala_id': sala_id,
                'numero_sala': numero_sala,
                'localizacao': localizacao,
                'capacidade_alunos': capacidade_alunos,
                'observacoes': observacoes,
                'ativo': True
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def find_by_id(sala_id):
        """
        Procurar sala pelo ID
        
        Args:
            sala_id (int): ID da sala
        
        Returns:
            dict: Dados da sala ou None
        """
        try:
            query = """
                SELECT * FROM salas WHERE sala_id = %s
            """
            return Database.execute_one(query, (sala_id,))
        except Exception as err:
            return None
    
    @staticmethod
    def find_by_numero(numero_sala):
        """
        Procurar sala pelo número
        
        Args:
            numero_sala (str): Número da sala
        
        Returns:
            dict: Dados da sala ou None
        """
        try:
            query = """
                SELECT * FROM salas WHERE numero_sala = %s
            """
            return Database.execute_one(query, (numero_sala,))
        except Exception as err:
            return None
    
    @staticmethod
    def update(sala_id, **kwargs):
        """
        Actualizar dados da sala
        
        Args:
            sala_id (int): ID da sala
            **kwargs: Campos a actualizar
        
        Returns:
            dict: Dados actualizados ou erro
        """
        try:
            allowed_fields = ['numero_sala', 'localizacao', 'capacidade_alunos', 'observacoes', 'ativo']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return {'error': 'Nenhum campo para actualizar'}
            
            # Construir query dinamicamente
            set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE salas SET {set_clause}, data_atualizacao = NOW() WHERE sala_id = %s"
            
            values = list(updates.values()) + [sala_id]
            Database.execute_update(query, values)
            
            return Sala.find_by_id(sala_id)
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def delete(sala_id):
        """
        Deletar sala (soft delete)
        
        Args:
            sala_id (int): ID da sala
        
        Returns:
            dict: Mensagem de sucesso ou erro
        """
        try:
            query = "UPDATE salas SET ativo = FALSE, data_atualizacao = NOW() WHERE sala_id = %s"
            Database.execute_update(query, (sala_id,))
            
            return {'message': 'Sala deletada com sucesso'}
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def list_all(page=1, limit=20, ativo=True):
        """
        Listar todas as salas
        
        Args:
            page (int): Página
            limit (int): Itens por página
            ativo (bool): Filtrar apenas activas
        
        Returns:
            dict: Lista paginada
        """
        try:
            offset = (page - 1) * limit
            
            where_clause = ""
            params = []
            
            if ativo is not None:
                where_clause = "WHERE ativo = %s"
                params.append(ativo)
            
            # Contar total
            count_query = f"SELECT COUNT(*) as total FROM salas {where_clause}"
            count_result = Database.execute_one(count_query, params if params else None)
            total = count_result['total'] if count_result else 0
            
            # Listar
            query = f"""
                SELECT * FROM salas
                {where_clause}
                ORDER BY numero_sala
                LIMIT %s OFFSET %s
            """
            
            list_params = params + [limit, offset]
            salas = Database.execute_query(query, list_params if params else [limit, offset])
            
            return {
                'total': total,
                'pagina': page,
                'limite': limit,
                'dados': salas
            }
        except Exception as err:
            return {'error': str(err)}
