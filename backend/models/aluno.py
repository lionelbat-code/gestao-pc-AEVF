"""
Modelo de Aluno
"""

from models.database import Database
from datetime import datetime

class Aluno:
    """
    Classe para gerenciar alunos
    """
    
    @staticmethod
    def create(numero, nome, nif, morada, ee_nome, ee_nif, ee_contacto, ee_numero_cidadao=None):
        """
        Criar novo aluno
        
        Args:
            numero (str): Número de aluno (único)
            nome (str): Nome completo
            nif (str): NIF do aluno (único)
            morada (str): Morada
            ee_nome (str): Nome do encarregado de educação
            ee_nif (str): NIF do encarregado de educação
            ee_contacto (str): Contacto do encarregado de educação
            ee_numero_cidadao (str): Número de cidadão do encarregado
        
        Returns:
            dict: Dados do aluno criado ou erro
        """
        try:
            # Validar campos obrigatórios
            required_fields = [numero, nome, nif, morada, ee_nome, ee_nif, ee_contacto]
            if not all(required_fields):
                return {'error': 'Todos os campos obrigatórios devem ser preenchidos'}
            
            # Verificar se número ou NIF já existem
            existing_numero = Database.execute_one(
                "SELECT aluno_id FROM alunos WHERE numero = %s",
                (numero,)
            )
            if existing_numero:
                return {'error': 'Este número de aluno já existe'}
            
            existing_nif = Database.execute_one(
                "SELECT aluno_id FROM alunos WHERE nif = %s",
                (nif,)
            )
            if existing_nif:
                return {'error': 'Este NIF já está registado'}
            
            # Inserir aluno
            query = """
                INSERT INTO alunos 
                (numero, nome, nif, morada, ee_nome, ee_nif, ee_contacto, ee_numero_cidadao, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            """
            aluno_id = Database.execute_update(
                query,
                (numero, nome, nif, morada, ee_nome, ee_nif, ee_contacto, ee_numero_cidadao)
            )
            
            return {
                'aluno_id': aluno_id,
                'numero': numero,
                'nome': nome,
                'nif': nif,
                'morada': morada,
                'ee_nome': ee_nome,
                'ee_nif': ee_nif,
                'ee_contacto': ee_contacto,
                'ee_numero_cidadao': ee_numero_cidadao,
                'ativo': True
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def find_by_id(aluno_id):
        """
        Procurar aluno pelo ID
        
        Args:
            aluno_id (int): ID do aluno
        
        Returns:
            dict: Dados do aluno ou None
        """
        try:
            query = """
                SELECT aluno_id, numero, nome, nif, morada, ee_nome, ee_nif, 
                       ee_contacto, ee_numero_cidadao, ativo, data_criacao, data_atualizacao
                FROM alunos
                WHERE aluno_id = %s
            """
            return Database.execute_one(query, (aluno_id,))
        except Exception as err:
            return None
    
    @staticmethod
    def find_by_numero(numero):
        """
        Procurar aluno pelo número
        
        Args:
            numero (str): Número do aluno
        
        Returns:
            dict: Dados do aluno ou None
        """
        try:
            query = """
                SELECT aluno_id, numero, nome, nif, morada, ee_nome, ee_nif, 
                       ee_contacto, ee_numero_cidadao, ativo, data_criacao, data_atualizacao
                FROM alunos
                WHERE numero = %s
            """
            return Database.execute_one(query, (numero,))
        except Exception as err:
            return None
    
    @staticmethod
    def find_by_nif(nif):
        """
        Procurar aluno pelo NIF
        
        Args:
            nif (str): NIF do aluno
        
        Returns:
            dict: Dados do aluno ou None
        """
        try:
            query = """
                SELECT aluno_id, numero, nome, nif, morada, ee_nome, ee_nif, 
                       ee_contacto, ee_numero_cidadao, ativo, data_criacao, data_atualizacao
                FROM alunos
                WHERE nif = %s
            """
            return Database.execute_one(query, (nif,))
        except Exception as err:
            return None
    
    @staticmethod
    def update(aluno_id, **kwargs):
        """
        Actualizar dados do aluno
        
        Args:
            aluno_id (int): ID do aluno
            **kwargs: Campos a actualizar
        
        Returns:
            dict: Dados actualizados ou erro
        """
        try:
            allowed_fields = [
                'numero', 'nome', 'nif', 'morada', 'ee_nome', 'ee_nif', 
                'ee_contacto', 'ee_numero_cidadao', 'ativo'
            ]
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return {'error': 'Nenhum campo para actualizar'}
            
            # Validar unicidade se número ou NIF estão sendo actualizados
            if 'numero' in updates:
                existing = Database.execute_one(
                    "SELECT aluno_id FROM alunos WHERE numero = %s AND aluno_id != %s",
                    (updates['numero'], aluno_id)
                )
                if existing:
                    return {'error': 'Este número de aluno já existe'}
            
            if 'nif' in updates:
                existing = Database.execute_one(
                    "SELECT aluno_id FROM alunos WHERE nif = %s AND aluno_id != %s",
                    (updates['nif'], aluno_id)
                )
                if existing:
                    return {'error': 'Este NIF já está registado'}
            
            # Construir query dinamicamente
            set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE alunos SET {set_clause}, data_atualizacao = NOW() WHERE aluno_id = %s"
            
            values = list(updates.values()) + [aluno_id]
            Database.execute_update(query, values)
            
            return Aluno.find_by_id(aluno_id)
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def delete(aluno_id):
        """
        Deletar aluno (soft delete - marcar como inativo)
        
        Args:
            aluno_id (int): ID do aluno
        
        Returns:
            dict: Mensagem de sucesso ou erro
        """
        try:
            query = "UPDATE alunos SET ativo = FALSE, data_atualizacao = NOW() WHERE aluno_id = %s"
            Database.execute_update(query, (aluno_id,))
            
            return {'message': 'Aluno deletado com sucesso'}
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def list_all(page=1, limit=20, ativo=True, search=None):
        """
        Listar todos os alunos
        
        Args:
            page (int): Página (começa em 1)
            limit (int): Itens por página
            ativo (bool): Filtrar apenas activos ou todos
            search (str): Procurar por nome ou número
        
        Returns:
            dict: Lista de alunos e total
        """
        try:
            offset = (page - 1) * limit
            
            # Construir query com filtros
            where_clause = ""
            params = []
            
            if ativo is not None:
                where_clause += "ativo = %s"
                params.append(ativo)
            
            if search:
                if where_clause:
                    where_clause += " AND "
                where_clause += "(nome LIKE %s OR numero LIKE %s)"
                search_param = f"%{search}%"
                params.extend([search_param, search_param])
            
            # Contar total
            count_query = f"SELECT COUNT(*) as total FROM alunos {f'WHERE {where_clause}' if where_clause else ''}"
            count_result = Database.execute_one(count_query, params if where_clause else None)
            total = count_result['total'] if count_result else 0
            
            # Listar
            query = f"""
                SELECT aluno_id, numero, nome, nif, morada, ee_nome, ee_nif, 
                       ee_contacto, ee_numero_cidadao, ativo, data_criacao, data_atualizacao
                FROM alunos
                {f'WHERE {where_clause}' if where_clause else ''}
                ORDER BY data_criacao DESC
                LIMIT %s OFFSET %s
            """
            
            list_params = params + [limit, offset]
            alunos = Database.execute_query(query, list_params if where_clause or search else [limit, offset])
            
            return {
                'total': total,
                'pagina': page,
                'limite': limit,
                'dados': alunos
            }
        except Exception as err:
            return {'error': str(err)}
    
    @staticmethod
    def get_statistics():
        """
        Obter estatísticas dos alunos
        
        Returns:
            dict: Estatísticas
        """
        try:
            total_query = "SELECT COUNT(*) as total FROM alunos WHERE ativo = TRUE"
            total = Database.execute_one(total_query)
            
            return {
                'total_alunos': total['total'] if total else 0
            }
        except Exception as err:
            return {'error': str(err)}
