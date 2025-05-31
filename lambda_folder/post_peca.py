import json
import os
import mysql.connector

def get_db_connection():
    try:
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
        body = event['body']
        tipo = body['tipo']

        conn = get_db_connection()
        if not conn:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Database connection failed'})
            }

        cursor = conn.cursor()
        cursor.execute("SET time_zone = 'America/Sao_Paulo';")
        cursor.execute("INSERT INTO peca (tipo) VALUES (%s)", (tipo,))
        
        # Retorna o ID da peça para adicioná-la na tabela 'separacao' posteriormente
        cursor.execute("SELECT LAST_INSERT_ID();")
        id_peca = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Part created successfully',
                'id_peca': id_peca  # Retorna o ID
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }