"""
Modelo de Computador de Sala
"""

from models.database import Database
from datetime import datetime

class ComputadorSala:
    """
    Classe para gerenciar computadores instalados em salas
    """
    
    @staticmethod
    def create(sala_id, numero_serie, marca, modelo, data_aquisicao, observacoes=None):
        """
        Criar novo computador de sala
        
        Args:
            sala_id (int): ID da sala
            numero_serie (str): Número de série (único)
            marca (str): Marca do computador
            modelo (str): Modelo
            data_aquisicao (str): Data de aquisição (YYYY-MM-DD)
            observacoes (str): Observações
        
        Returns:
            dict: Dados do computador criado ou erro
        """
        try:
            # Validar campos obrigatorios
            required_fields = [sala_id, numero_serie, marca, modelo]
            if not all(required_fields):
                return {'error': 'Campos obrigatorios: sala_id, numero_serie, marca, modelo'}
            
            # Verificar se sala existe
            sala = Database.execute_one(
                "SELECT sala_id FROM salas WHERE sala_id = %s",
                (sala_id,)
            )
            if not sala:
                return {'error': 'Sala não encontrada'}
            
            # Verificar se número de série já existe
            existing = Database.execute_one(
                "SELECT pc_sala_id FROM computadores_sala WHERE numero_serie = %s",
                (numero_serie,)
            )
            if existing:
                return {'error': 'Este número de série já existe'}
            
            # Inserir computador
            query = """
                INSERT INTO computadores_sala 
                (sala_id, numero_serie, marca, modelo, data_aquisicao, observacoes, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 'funcionando')
            """
            pc_sala_id = Database.execute_update(
                query,
                (sala_id, numero_serie, marca, modelo, data_aquisicao, observacoes)
            )
            
            return {
                'pc_sala_id': pc_sala_id,
                'sala_id': sala_id,
                'numero_serie': numero_serie,
                'marca': marca,
                'modelo': modelo,
                'data_aquisicao': data_aquisicao,
                'estado': 'funcionando',
                'observacoes': observacoes
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def find_by_id(pc_sala_id):
        """
        Procurar computador de sala pelo ID
        
        Args:
            pc_sala_id (int): ID do computador
        
        Returns:
            dict: Dados do computador ou None
        """
        try:
            query = """
                SELECT * FROM computadores_sala WHERE pc_sala_id = %s
            """
            return Database.execute_one(query, (pc_sala_id,))
        except Exception as err:
            return None
    
    @staticmethod
    def find_by_numero_serie(numero_serie):
        """
        Procurar computador de sala pelo número de série
        
        Args:
            numero_serie (str): Número de série
        
        Returns:
            dict: Dados do computador ou None
        """
        try:
            query = """
                SELECT * FROM computadores_sala WHERE numero_serie = %s
            """
            return Database.execute_one(query, (numero_serie,))
        except Exception as err:
            return None
    
    @staticmethod
    def update(pc_sala_id, **kwargs):
        """
        Actualizar dados do computador de sala
        
        Args:
            pc_sala_id (int): ID do computador
            **kwargs: Campos a actualizar
        
        Returns:
            dict: Dados actualizados ou erro
        """
        try:
            allowed_fields = [
                'marca', 'modelo', 'data_aquisicao', 'estado', 
                'descricao_avaria', 'data_ultima_manutencao', 'observacoes'
            ]
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return {'error': 'Nenhum campo para actualizar'}
            
            # Construir query dinamicamente
            set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE computadores_sala SET {set_clause}, data_atualizacao = NOW() WHERE pc_sala_id = %s"
            
            values = list(updates.values()) + [pc_sala_id]
            Database.execute_update(query, values)
            
            return ComputadorSala.find_by_id(pc_sala_id)
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def delete(pc_sala_id):
        """
        Deletar computador de sala
        
        Args:
            pc_sala_id (int): ID do computador
        
        Returns:
            dict: Mensagem de sucesso ou erro
        """
        try:
            query = "DELETE FROM computadores_sala WHERE pc_sala_id = %s"
            Database.execute_update(query, (pc_sala_id,))
            
            return {'message': 'Computador de sala deletado com sucesso'}
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def list_by_sala(sala_id, estado=None):
        """
        Listar computadores de uma sala
        
        Args:
            sala_id (int): ID da sala
            estado (str): Filtrar por estado (opcional)
        
        Returns:
            dict: Lista de computadores ou erro
        """
        try:
            where_clause = "sala_id = %s"
            params = [sala_id]
            
            if estado:
                where_clause += " AND estado = %s"
                params.append(estado)
            
            query = f"""
                SELECT * FROM computadores_sala
                WHERE {where_clause}
                ORDER BY numero_serie
            """
            
            computadores = Database.execute_query(query, params)
            
            return {
                'sala_id': sala_id,
                'total': len(computadores),
                'computadores': computadores
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def list_all(page=1, limit=20, estado=None):
        """
        Listar todos os computadores de sala
        
        Args:
            page (int): Página
            limit (int): Itens por página
            estado (str): Filtrar por estado
        
        Returns:
            dict: Lista paginada
        """
        try:
            offset = (page - 1) * limit
            
            where_clause = ""
            params = []
            
            if estado:
                where_clause = "WHERE estado = %s"
                params.append(estado)
            
            # Contar total
            count_query = f"SELECT COUNT(*) as total FROM computadores_sala {where_clause}"
            count_result = Database.execute_one(count_query, params if params else None)
            total = count_result['total'] if count_result else 0
            
            # Listar
            query = f"""
                SELECT * FROM computadores_sala
                {where_clause}
                ORDER BY data_criacao DESC
                LIMIT %s OFFSET %s
            """
            
            list_params = params + [limit, offset]
            computadores = Database.execute_query(query, list_params if params else [limit, offset])
            
            return {
                'total': total,
                'pagina': page,
                'limite': limit,
                'dados': computadores
            }
        except Exception as err:
            return {'error': str(err)}
