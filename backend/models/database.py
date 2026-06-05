"""
Conexão à base de dados MySQL
"""

import mysql.connector
from mysql.connector import Error
from config import config as app_config
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """
    Classe para gerenciar conexões com MySQL
    """
    
    @staticmethod
    def get_connection():
        """
        Cria uma conexão com a base de dados
        
        Returns:
            mysql.connector.MySQLConnection: Conexão com a BD
        """
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'gestao_pc_aevf'),
                port=int(os.getenv('DB_PORT', 3306))
            )
            return connection
        except Error as err:
            if err.errno == 2003:
                raise Exception("Erro: Não consegue conectar ao MySQL. Verifique se o servidor está a correr.")
            elif err.errno == 1045:
                raise Exception("Erro: Credenciais de acesso incorretas.")
            elif err.errno == 1049:
                raise Exception("Erro: Base de dados não existe. Execute: python database/init_db.py")
            else:
                raise Exception(f"Erro ao conectar à base de dados: {err}")
    
    @staticmethod
    def execute_query(query, params=None):
        """
        Executa uma query (SELECT)
        
        Args:
            query (str): Query SQL
            params (tuple): Parâmetros para a query (para evitar SQL injection)
        
        Returns:
            list: Lista de resultados
        """
        connection = None
        try:
            connection = Database.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as err:
            raise Exception(f"Erro ao executar query: {err}")
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @staticmethod
    def execute_update(query, params=None):
        """
        Executa uma query de modificação (INSERT, UPDATE, DELETE)
        
        Args:
            query (str): Query SQL
            params (tuple): Parâmetros para a query
        
        Returns:
            int: ID do último registro inserido (para INSERT) ou linhas afetadas
        """
        connection = None
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            
            # Retorna o ID inserido ou linhas afetadas
            result = cursor.lastrowid if cursor.lastrowid > 0 else cursor.rowcount
            cursor.close()
            return result
        except Error as err:
            if connection:
                connection.rollback()
            raise Exception(f"Erro ao executar update: {err}")
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @staticmethod
    def execute_one(query, params=None):
        """
        Executa uma query e retorna apenas um resultado
        
        Args:
            query (str): Query SQL
            params (tuple): Parâmetros para a query
        
        Returns:
            dict: Um resultado ou None
        """
        result = Database.execute_query(query, params)
        return result[0] if result else None
