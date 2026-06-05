"""
Modelo de Computador de Aluno (Emprestável)
"""

from models.database import Database
from datetime import datetime

class ComputadorAluno:
    """
    Classe para gerenciar computadores emprestáveis aos alunos
    """
    
    @staticmethod
    def create(numero_serie, marca, modelo, hotspot=None, sim_card=None, data_aquisicao=None, observacoes=None):
        """
        Criar novo computador de aluno
        
        Args:
            numero_serie (str): Número de série (único)
            marca (str): Marca do computador
            modelo (str): Modelo
            hotspot (str): Info do hotspot (opcional)
            sim_card (str): Info do SIM card (opcional)
            data_aquisicao (str): Data de aquisição (YYYY-MM-DD)
            observacoes (str): Observações
        
        Returns:
            dict: Dados do computador criado ou erro
        """
        try:
            # Validar campos obrigatorios
            required_fields = [numero_serie, marca, modelo]
            if not all(required_fields):
                return {'error': 'Campos obrigatorios: numero_serie, marca, modelo'}
            
            # Verificar se número de série já existe
            existing = Database.execute_one(
                "SELECT pc_id FROM computadores_aluno WHERE numero_serie = %s",
                (numero_serie,)
            )
            if existing:
                return {'error': 'Este número de série já existe'}
            
            # Inserir computador
            query = """
                INSERT INTO computadores_aluno 
                (numero_serie, marca, modelo, hotspot, sim_card, data_aquisicao, observacoes, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'disponivel')
            """
            pc_id = Database.execute_update(
                query,
                (numero_serie, marca, modelo, hotspot, sim_card, data_aquisicao, observacoes)
            )
            
            return {
                'pc_id': pc_id,
                'numero_serie': numero_serie,
                'marca': marca,
                'modelo': modelo,
                'hotspot': hotspot,
                'sim_card': sim_card,
                'data_aquisicao': data_aquisicao,
                'estado': 'disponivel',
                'observacoes': observacoes
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def find_by_id(pc_id):
        """
        Procurar computador de aluno pelo ID
        
        Args:
            pc_id (int): ID do computador
        
        Returns:
            dict: Dados do computador ou None
        """
        try:
            query = """
                SELECT * FROM computadores_aluno WHERE pc_id = %s
            """
            return Database.execute_one(query, (pc_id,))
        except Exception as err:
            return None
    
    @staticmethod
    def find_by_numero_serie(numero_serie):
        """
        Procurar computador de aluno pelo número de série
        
        Args:
            numero_serie (str): Número de série
        
        Returns:
            dict: Dados do computador ou None
        """
        try:
            query = """
                SELECT * FROM computadores_aluno WHERE numero_serie = %s
            """
            return Database.execute_one(query, (numero_serie,))
        except Exception as err:
            return None
    
    @staticmethod
    def update(pc_id, **kwargs):
        """
        Actualizar dados do computador de aluno
        
        Args:
            pc_id (int): ID do computador
            **kwargs: Campos a actualizar
        
        Returns:
            dict: Dados actualizados ou erro
        """
        try:
            allowed_fields = [
                'marca', 'modelo', 'hotspot', 'sim_card', 'data_aquisicao', 
                'estado', 'observacoes'
            ]
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return {'error': 'Nenhum campo para actualizar'}
            
            # Construir query dinamicamente
            set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE computadores_aluno SET {set_clause}, data_atualizacao = NOW() WHERE pc_id = %s"
            
            values = list(updates.values()) + [pc_id]
            Database.execute_update(query, values)
            
            return ComputadorAluno.find_by_id(pc_id)
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def delete(pc_id):
        """
        Deletar computador de aluno
        
        Args:
            pc_id (int): ID do computador
        
        Returns:
            dict: Mensagem de sucesso ou erro
        """
        try:
            query = "DELETE FROM computadores_aluno WHERE pc_id = %s"
            Database.execute_update(query, (pc_id,))
            
            return {'message': 'Computador de aluno deletado com sucesso'}
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def list_all(page=1, limit=20, estado=None):
        """
        Listar todos os computadores de aluno
        
        Args:
            page (int): Página
            limit (int): Itens por página
            estado (str): Filtrar por estado (disponivel, em_emprestimo, em_reparacao, inutilizado)
        
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
            count_query = f"SELECT COUNT(*) as total FROM computadores_aluno {where_clause}"
            count_result = Database.execute_one(count_query, params if params else None)
            total = count_result['total'] if count_result else 0
            
            # Listar
            query = f"""
                SELECT * FROM computadores_aluno
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
    
    @staticmethod
    def get_statistics():
        """
        Obter estatísticas dos computadores de aluno
        
        Returns:
            dict: Estatísticas
        """
        try:
            total_query = "SELECT COUNT(*) as total FROM computadores_aluno"
            total = Database.execute_one(total_query)
            
            disponivel_query = "SELECT COUNT(*) as total FROM computadores_aluno WHERE estado = 'disponivel'"
            disponivel = Database.execute_one(disponivel_query)
            
            em_emprestimo_query = "SELECT COUNT(*) as total FROM computadores_aluno WHERE estado = 'em_emprestimo'"
            em_emprestimo = Database.execute_one(em_emprestimo_query)
            
            em_reparacao_query = "SELECT COUNT(*) as total FROM computadores_aluno WHERE estado = 'em_reparacao'"
            em_reparacao = Database.execute_one(em_reparacao_query)
            
            return {
                'total_computadores': total['total'] if total else 0,
                'disponivel': disponivel['total'] if disponivel else 0,
                'em_emprestimo': em_emprestimo['total'] if em_emprestimo else 0,
                'em_reparacao': em_reparacao['total'] if em_reparacao else 0
            }
        except Exception as err:
            return {'error': str(err)}
