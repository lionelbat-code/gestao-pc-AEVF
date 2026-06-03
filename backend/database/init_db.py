"""
Script para inicializar a base de dados
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Criar base de dados e tabelas a partir do schema.sql"""
    
    try:
        # Ler arquivo schema.sql
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r', encoding='utf-8') as file:
            schema = file.read()
        
        # Conectar ao MySQL
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Executar schema
            for statement in schema.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Error as err:
                        print(f"Erro ao executar statement: {err}")
            
            connection.commit()
            print("✅ Base de dados inicializada com sucesso!")
            
            cursor.close()
            connection.close()
    
    except Error as err:
        print(f"❌ Erro ao conectar à base de dados: {err}")
    except FileNotFoundError:
        print("❌ Arquivo schema.sql não encontrado")

if __name__ == '__main__':
    init_database()
