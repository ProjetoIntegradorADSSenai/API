import json
import mysql.connector
import os
from datetime import datetime

def get_db_connection():
    try:
        # Recupera as variáveis de ambiente do Lambda para conexão com o banco
        return mysql.connector.connect(
            user=os.environ['user'],
            password=os.environ['password'],
            host=os.environ['host'],
            database=os.environ['database']
        )
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return None

def lambda_handler(event, context):
    try:
        # Se conecta ao DB
        cnx = get_db_connection()
        if not cnx:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Database connection failed'})
            }

        cursor = cnx.cursor()

        # Timezone do Brasil
        cursor.execute("SET time_zone = 'America/Sao_Paulo';")

        # Cria o DB (primeira vez)
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.environ['database']}")
        cnx.commit()

        # Cria a tabela de peças (primeira vez)
        cursor.execute('SHOW TABLES LIKE "peca"')
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE peca (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    tipo VARCHAR(255)
                )
            """)
            cnx.commit()

        # Cria a tabela de separação - união com tabela de peças (primeira vez)
        cursor.execute('SHOW TABLES LIKE "separacao"')
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE separacao (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_peca INT,
                    FOREIGN KEY (id_peca) REFERENCES peca(id),
                    horario TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cnx.commit()

        # Cria a view de agregação dos dados por 5 em 5 min (primeira vez)
        cursor.execute(f"""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = '{os.environ['database']}' 
            AND table_name = 'agregacao';
        """)   
        if not cursor.fetchone():
            create_view_query = """
                CREATE OR REPLACE VIEW agregacao AS
                SELECT 
                    p.tipo AS peca_tipo,
                    DATE_FORMAT(
                        CONVERT_TZ(
                            FROM_UNIXTIME(
                                FLOOR(UNIX_TIMESTAMP(s.horario)/(5*60))*(5*60)
                            ),
                            'UTC', 'America/Sao_Paulo'
                        ), 
                        '%Y-%m-%d %H:%i:00'
                    ) AS time_interval,
                    COUNT(*) AS total_separacoes
                FROM 
                    separacao s
                INNER JOIN 
                    peca p ON s.id_peca = p.id
                GROUP BY 
                    p.tipo,
                    time_interval
                ORDER BY 
                    time_interval, p.tipo;
                """
            cursor.execute(create_view_query)
            cnx.commit()

            cursor.execute("""
                UPDATE separacao 
                SET horario = CONVERT_TZ(horario, 'UTC', 'America/Sao_Paulo')
            """)
            cnx.commit()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Database setup completed successfully'})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()